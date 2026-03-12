import csv
import io
import logging
import uuid
from datetime import date

from typing import List

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy import and_, func as sa_func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config import settings
from app.database import get_db
from app.models.invoice import AuditLog, Invoice, InvoiceLineItem
from app.schemas.invoice import InvoiceDetail, InvoiceListItem, InvoiceListResponse, InvoiceUpdate, InvoiceUploadResponse
from app.models.user import User
from app.services import storage
from app.services.auth import get_current_user
from app.services.coding import predict_coding, update_vendor_history
from app.services.extraction import extract_invoice

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/invoices", tags=["invoices"])


async def log_audit(
    db: AsyncSession,
    invoice_id: uuid.UUID,
    action: str,
    details: str | None = None,
    previous_value: dict | None = None,
    new_value: dict | None = None,
    user: User | None = None,
):
    entry = AuditLog(
        invoice_id=invoice_id,
        action=action,
        details=details,
        previous_value=previous_value,
        new_value=new_value,
        user_id=user.id if user else None,
        user_email=user.email if user else None,
    )
    db.add(entry)

ALLOWED_TYPES = {"application/pdf", "image/png", "image/jpeg", "image/webp", "image/tiff"}


@router.post("/upload", response_model=InvoiceUploadResponse)
async def upload_invoice(file: UploadFile, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail=f"File type {file.content_type} not supported.")

    if file.size and file.size > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail=f"File exceeds {settings.MAX_FILE_SIZE_MB}MB limit.")

    file_path = await storage.save_file(file)

    invoice = Invoice(
        file_name=file.filename or "unknown",
        file_path=file_path,
        file_content_type=file.content_type or "application/octet-stream",
        status="uploaded",
    )
    db.add(invoice)
    await db.flush()

    try:
        invoice.status = "processing"
        await db.flush()

        result = await extract_invoice(file_path)

        invoice.vendor_name = result.vendor_name
        invoice.vendor_address = result.vendor_address
        invoice.invoice_number = result.invoice_number
        invoice.invoice_date = date.fromisoformat(result.invoice_date) if result.invoice_date else None
        invoice.due_date = date.fromisoformat(result.due_date) if result.due_date else None
        invoice.po_number = result.po_number
        invoice.job_number = result.job_number
        invoice.cost_code = result.cost_code
        invoice.subtotal = result.subtotal
        invoice.tax_amount = result.tax_amount
        invoice.total_amount = result.total_amount
        invoice.currency = result.currency
        invoice.payment_terms = result.payment_terms
        invoice.confidence_score = result.confidence_score
        invoice.raw_extraction = result.model_dump()
        invoice.status = "extracted"

        for item in result.line_items:
            line = InvoiceLineItem(
                invoice_id=invoice.id,
                line_number=item.line_number,
                description=item.description,
                quantity=item.quantity,
                unit_price=item.unit_price,
                amount=item.amount,
            )
            db.add(line)

        await log_audit(db, invoice.id, "extracted", f"Confidence: {result.confidence_score}", user=user)

        # Run coding agent
        try:
            coding_result = await predict_coding(invoice.id, db)
            await log_audit(
                db, invoice.id, "coded",
                f"AI coding: {coding_result.method} (confidence: {coding_result.confidence:.2f})",
                user=user,
            )
        except Exception as coding_err:
            logger.warning("Coding prediction failed for %s: %s", file.filename, coding_err)

        await db.commit()
        message = f"Invoice extracted successfully. Confidence: {result.confidence_score}"

    except Exception as e:
        logger.error("Extraction failed for %s: %s", file.filename, e)
        invoice.status = "failed"
        await log_audit(db, invoice.id, "extraction_failed", str(e), user=user)
        await db.commit()
        message = f"Invoice uploaded but extraction failed: {e}"

    return InvoiceUploadResponse(
        id=invoice.id,
        status=invoice.status,
        file_name=invoice.file_name,
        message=message,
    )


@router.get("", response_model=InvoiceListResponse)
async def list_invoices(
    status: str | None = None,
    job_number: str | None = None,
    search: str | None = None,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
):
    base_query = select(Invoice)
    if status:
        base_query = base_query.where(Invoice.status == status)
    if job_number:
        base_query = base_query.where(Invoice.job_number == job_number)
    if search:
        search_term = f"%{search}%"
        base_query = base_query.where(
            or_(
                Invoice.vendor_name.ilike(search_term),
                Invoice.invoice_number.ilike(search_term),
                Invoice.job_number.ilike(search_term),
                Invoice.po_number.ilike(search_term),
            )
        )

    # Get total count
    count_query = select(sa_func.count()).select_from(base_query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    # Get paginated items
    items_query = base_query.order_by(Invoice.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(items_query)
    items = result.scalars().all()

    return InvoiceListResponse(items=items, total=total)


@router.get("/export/csv")
async def export_invoices_csv(
    status: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(Invoice).order_by(Invoice.created_at.desc())
    if status:
        query = query.where(Invoice.status == status)
    result = await db.execute(query)
    invoices = result.scalars().all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "ID", "Status", "File Name", "Vendor Name", "Vendor Address",
        "Invoice Number", "Invoice Date", "Due Date", "PO Number",
        "Job Number", "Cost Code",
        "Subtotal", "Tax", "Total", "Currency", "Payment Terms",
        "Confidence Score", "Created At",
    ])
    for inv in invoices:
        writer.writerow([
            str(inv.id), inv.status, inv.file_name, inv.vendor_name or "",
            inv.vendor_address or "", inv.invoice_number or "",
            str(inv.invoice_date) if inv.invoice_date else "",
            str(inv.due_date) if inv.due_date else "",
            inv.po_number or "",
            inv.job_number or "",
            inv.cost_code or "",
            inv.subtotal if inv.subtotal is not None else "",
            inv.tax_amount if inv.tax_amount is not None else "",
            inv.total_amount if inv.total_amount is not None else "",
            inv.currency, inv.payment_terms or "",
            inv.confidence_score if inv.confidence_score is not None else "",
            str(inv.created_at),
        ])

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=invoices.csv"},
    )


@router.get("/duplicates")
async def get_duplicates(db: AsyncSession = Depends(get_db)):
    """Find potential duplicate invoices based on vendor + amount + date or invoice number."""
    query = select(Invoice).where(
        Invoice.status.notin_(["failed", "uploaded", "processing"])
    ).order_by(Invoice.created_at.desc())
    result = await db.execute(query)
    invoices = list(result.scalars().all())

    groups: dict[str, list[dict]] = {}

    for inv in invoices:
        # Key 1: same invoice number + vendor (strongest signal)
        if inv.invoice_number and inv.vendor_name:
            key = f"inv:{inv.vendor_name.lower().strip()}|{inv.invoice_number.lower().strip()}"
            groups.setdefault(key, []).append(inv)

        # Key 2: same vendor + amount + date
        if inv.vendor_name and inv.total_amount and inv.invoice_date:
            key = f"vad:{inv.vendor_name.lower().strip()}|{float(inv.total_amount)}|{inv.invoice_date}"
            groups.setdefault(key, []).append(inv)

    duplicates = []
    seen_ids = set()
    for key, group in groups.items():
        if len(group) < 2:
            continue
        group_ids = tuple(sorted(str(i.id) for i in group))
        if group_ids in seen_ids:
            continue
        seen_ids.add(group_ids)
        duplicates.append({
            "match_type": "invoice_number" if key.startswith("inv:") else "vendor_amount_date",
            "invoices": [
                {
                    "id": str(inv.id),
                    "vendor_name": inv.vendor_name,
                    "invoice_number": inv.invoice_number,
                    "total_amount": float(inv.total_amount) if inv.total_amount else None,
                    "invoice_date": str(inv.invoice_date) if inv.invoice_date else None,
                    "status": inv.status,
                    "file_name": inv.file_name,
                    "created_at": str(inv.created_at),
                }
                for inv in group
            ],
        })

    return duplicates


@router.get("/stats")
async def get_stats(db: AsyncSession = Depends(get_db)):
    """Dashboard statistics for charts."""
    query = select(Invoice).order_by(Invoice.created_at.desc())
    result = await db.execute(query)
    invoices = list(result.scalars().all())

    # Status breakdown
    status_counts: dict[str, int] = {}
    for inv in invoices:
        status_counts[inv.status] = status_counts.get(inv.status, 0) + 1

    # Spend by vendor (top 10)
    vendor_spend: dict[str, float] = {}
    for inv in invoices:
        if inv.vendor_name and inv.total_amount:
            name = inv.vendor_name.strip()
            vendor_spend[name] = vendor_spend.get(name, 0) + float(inv.total_amount)
    top_vendors = sorted(vendor_spend.items(), key=lambda x: x[1], reverse=True)[:10]

    # Weekly volume (last 12 weeks)
    from datetime import datetime, timedelta
    now = datetime.utcnow()
    weekly: dict[str, int] = {}
    for i in range(11, -1, -1):
        week_start = now - timedelta(weeks=i)
        label = week_start.strftime("%b %d")
        weekly[label] = 0
    for inv in invoices:
        created = inv.created_at.replace(tzinfo=None) if inv.created_at.tzinfo else inv.created_at
        weeks_ago = (now - created).days // 7
        if weeks_ago < 12:
            week_start = now - timedelta(weeks=weeks_ago)
            label = week_start.strftime("%b %d")
            if label in weekly:
                weekly[label] += 1

    # Division spend (based on middle segment of job_number like "1-21-12345" -> "21")
    DIVISION_NAMES = {
        "21": "Electrical",
        "32": "HVAC",
        "33": "Plumbing",
        "77": "Components",
    }
    division_totals: dict[str, float] = {}
    for inv in invoices:
        if inv.job_number and inv.total_amount:
            parts = inv.job_number.split("-")
            div_code = parts[1] if len(parts) >= 3 else None
            div_name = DIVISION_NAMES.get(div_code, "Other") if div_code else "Other"
            division_totals[div_name] = division_totals.get(div_name, 0) + float(inv.total_amount)

    # Top jobs by spend
    job_spend: dict[str, float] = {}
    for inv in invoices:
        if inv.job_number and inv.total_amount:
            job_spend[inv.job_number] = job_spend.get(inv.job_number, 0) + float(inv.total_amount)
    top_jobs = sorted(job_spend.items(), key=lambda x: x[1], reverse=True)[:10]

    return {
        "status_breakdown": [{"name": k, "value": v} for k, v in status_counts.items()],
        "vendor_spend": [{"name": v[0], "amount": v[1]} for v in top_vendors],
        "weekly_volume": [{"week": k, "count": v} for k, v in weekly.items()],
        "division_spend": [{"name": k, "amount": v} for k, v in division_totals.items()],
        "top_jobs": [{"job_number": j[0], "total_amount": j[1]} for j in top_jobs],
    }


@router.get("/{invoice_id}", response_model=InvoiceDetail)
async def get_invoice(invoice_id: str, db: AsyncSession = Depends(get_db)):
    query = select(Invoice).options(selectinload(Invoice.line_items)).where(Invoice.id == invoice_id)
    result = await db.execute(query)
    invoice = result.scalar_one_or_none()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found.")
    return invoice


@router.patch("/{invoice_id}", response_model=InvoiceDetail)
async def update_invoice(invoice_id: str, updates: InvoiceUpdate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    query = select(Invoice).options(selectinload(Invoice.line_items)).where(Invoice.id == invoice_id)
    result = await db.execute(query)
    invoice = result.scalar_one_or_none()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found.")

    changed = updates.model_dump(exclude_unset=True)
    previous = {k: getattr(invoice, k) for k in changed}
    # Serialize date/Decimal values for JSON
    for k, v in previous.items():
        if hasattr(v, "isoformat"):
            previous[k] = v.isoformat()
        elif hasattr(v, "__float__"):
            previous[k] = float(v)

    for field, value in changed.items():
        setattr(invoice, field, value)

    # If job_number or cost_code was manually edited, mark coding as manual
    if "job_number" in changed or "cost_code" in changed:
        invoice.coding_status = "manual"

    new_val = {k: v.isoformat() if hasattr(v, "isoformat") else v for k, v in changed.items()}
    await log_audit(db, invoice.id, "edited", f"Fields changed: {', '.join(changed.keys())}", previous, new_val, user=user)
    await db.commit()
    await db.refresh(invoice)
    return invoice


@router.delete("/{invoice_id}")
async def delete_invoice(invoice_id: str, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    query = select(Invoice).where(Invoice.id == invoice_id)
    result = await db.execute(query)
    invoice = result.scalar_one_or_none()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found.")

    # Delete the file from disk
    try:
        import os
        if os.path.exists(invoice.file_path):
            os.remove(invoice.file_path)
    except OSError:
        pass

    await log_audit(db, invoice.id, "deleted", f"Deleted invoice: {invoice.file_name}", user=user)
    await db.delete(invoice)
    await db.commit()
    return {"message": "Invoice deleted"}


VALID_TRANSITIONS = {
    "extracted": ["approved", "rejected"],
    "approved": ["rejected"],
    "rejected": ["approved"],
    "failed": [],
    "uploaded": [],
    "processing": [],
}


@router.post("/{invoice_id}/status")
async def update_invoice_status(invoice_id: str, body: dict, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    new_status = body.get("status")
    if not new_status:
        raise HTTPException(status_code=400, detail="Missing 'status' field.")

    query = select(Invoice).options(selectinload(Invoice.line_items)).where(Invoice.id == invoice_id)
    result = await db.execute(query)
    invoice = result.scalar_one_or_none()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found.")

    allowed = VALID_TRANSITIONS.get(invoice.status, [])
    if new_status not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot transition from '{invoice.status}' to '{new_status}'. Allowed: {allowed}",
        )

    old_status = invoice.status
    invoice.status = new_status
    await log_audit(db, invoice.id, new_status, f"Status changed from {old_status} to {new_status}",
                    {"status": old_status}, {"status": new_status}, user=user)

    # Update vendor coding history on approval
    if new_status == "approved" and invoice.vendor_name and invoice.job_number and invoice.cost_code:
        await update_vendor_history(db, invoice.vendor_name, invoice.job_number, invoice.cost_code, invoice.tenant_id)

    await db.commit()
    await db.refresh(invoice)
    return {"id": str(invoice.id), "status": invoice.status}


@router.post("/{invoice_id}/re-extract")
async def re_extract_invoice(invoice_id: str, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    """Re-run AI extraction on an existing invoice file."""
    query = select(Invoice).options(selectinload(Invoice.line_items)).where(Invoice.id == invoice_id)
    result = await db.execute(query)
    invoice = result.scalar_one_or_none()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found.")

    old_confidence = invoice.confidence_score
    old_status = invoice.status

    # Clear existing line items
    for item in list(invoice.line_items):
        await db.delete(item)

    invoice.status = "processing"
    await db.flush()

    try:
        result = await extract_invoice(invoice.file_path)

        invoice.vendor_name = result.vendor_name
        invoice.vendor_address = result.vendor_address
        invoice.invoice_number = result.invoice_number
        invoice.invoice_date = date.fromisoformat(result.invoice_date) if result.invoice_date else None
        invoice.due_date = date.fromisoformat(result.due_date) if result.due_date else None
        invoice.po_number = result.po_number
        invoice.job_number = result.job_number
        invoice.cost_code = result.cost_code
        invoice.subtotal = result.subtotal
        invoice.tax_amount = result.tax_amount
        invoice.total_amount = result.total_amount
        invoice.currency = result.currency
        invoice.payment_terms = result.payment_terms
        invoice.confidence_score = result.confidence_score
        invoice.raw_extraction = result.model_dump()
        invoice.status = "extracted"

        for item in result.line_items:
            line = InvoiceLineItem(
                invoice_id=invoice.id,
                line_number=item.line_number,
                description=item.description,
                quantity=item.quantity,
                unit_price=item.unit_price,
                amount=item.amount,
            )
            db.add(line)

        await log_audit(db, invoice.id, "re-extracted",
                        f"Re-extracted. Confidence: {old_confidence} → {result.confidence_score}",
                        {"status": old_status, "confidence": old_confidence},
                        {"status": "extracted", "confidence": result.confidence_score}, user=user)

        # Re-run coding agent
        try:
            coding_result = await predict_coding(invoice.id, db)
            await log_audit(db, invoice.id, "coded",
                            f"AI coding: {coding_result.method} (confidence: {coding_result.confidence:.2f})", user=user)
        except Exception as coding_err:
            logger.warning("Coding prediction failed on re-extract for %s: %s", invoice.file_name, coding_err)

        await db.commit()

        return {"id": str(invoice.id), "status": "extracted", "confidence_score": result.confidence_score,
                "message": f"Re-extraction successful. Confidence: {result.confidence_score}"}

    except Exception as e:
        logger.error("Re-extraction failed for %s: %s", invoice.file_name, e)
        invoice.status = "failed"
        await log_audit(db, invoice.id, "re-extraction_failed", str(e), user=user)
        await db.commit()
        raise HTTPException(status_code=500, detail=f"Re-extraction failed: {e}")


@router.get("/{invoice_id}/audit")
async def get_audit_log(invoice_id: str, db: AsyncSession = Depends(get_db)):
    """Get audit trail for an invoice."""
    # Verify invoice exists
    inv_query = select(Invoice).where(Invoice.id == invoice_id)
    inv_result = await db.execute(inv_query)
    if not inv_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Invoice not found.")

    query = select(AuditLog).where(AuditLog.invoice_id == invoice_id).order_by(AuditLog.created_at.desc())
    result = await db.execute(query)
    logs = result.scalars().all()

    return [
        {
            "id": str(log.id),
            "action": log.action,
            "details": log.details,
            "previous_value": log.previous_value,
            "new_value": log.new_value,
            "user_email": log.user_email,
            "created_at": str(log.created_at),
        }
        for log in logs
    ]


@router.post("/upload-bulk", response_model=list[InvoiceUploadResponse])
async def upload_invoices_bulk(files: List[UploadFile], db: AsyncSession = Depends(get_db)):
    results = []
    for file in files:
        if file.content_type not in ALLOWED_TYPES:
            results.append(InvoiceUploadResponse(
                id="00000000-0000-0000-0000-000000000000",
                status="failed",
                file_name=file.filename or "unknown",
                message=f"File type {file.content_type} not supported.",
            ))
            continue

        if file.size and file.size > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
            results.append(InvoiceUploadResponse(
                id="00000000-0000-0000-0000-000000000000",
                status="failed",
                file_name=file.filename or "unknown",
                message=f"File exceeds {settings.MAX_FILE_SIZE_MB}MB limit.",
            ))
            continue

        file_path = await storage.save_file(file)

        invoice = Invoice(
            file_name=file.filename or "unknown",
            file_path=file_path,
            file_content_type=file.content_type or "application/octet-stream",
            status="uploaded",
        )
        db.add(invoice)
        await db.flush()

        try:
            invoice.status = "processing"
            await db.flush()

            result = await extract_invoice(file_path)

            invoice.vendor_name = result.vendor_name
            invoice.vendor_address = result.vendor_address
            invoice.invoice_number = result.invoice_number
            invoice.invoice_date = date.fromisoformat(result.invoice_date) if result.invoice_date else None
            invoice.due_date = date.fromisoformat(result.due_date) if result.due_date else None
            invoice.po_number = result.po_number
            invoice.job_number = result.job_number
            invoice.cost_code = result.cost_code
            invoice.subtotal = result.subtotal
            invoice.tax_amount = result.tax_amount
            invoice.total_amount = result.total_amount
            invoice.currency = result.currency
            invoice.payment_terms = result.payment_terms
            invoice.confidence_score = result.confidence_score
            invoice.raw_extraction = result.model_dump()
            invoice.status = "extracted"

            for item in result.line_items:
                line = InvoiceLineItem(
                    invoice_id=invoice.id,
                    line_number=item.line_number,
                    description=item.description,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    amount=item.amount,
                )
                db.add(line)

            # Run coding agent
            try:
                coding_result = await predict_coding(invoice.id, db)
            except Exception as coding_err:
                logger.warning("Coding prediction failed for %s: %s", file.filename, coding_err)

            await db.commit()
            message = f"Invoice extracted successfully. Confidence: {result.confidence_score}"

        except Exception as e:
            logger.error("Extraction failed for %s: %s", file.filename, e)
            invoice.status = "failed"
            await db.commit()
            message = f"Invoice uploaded but extraction failed: {e}"

        results.append(InvoiceUploadResponse(
            id=invoice.id,
            status=invoice.status,
            file_name=invoice.file_name,
            message=message,
        ))

    return results


@router.post("/{invoice_id}/confirm-coding")
async def confirm_coding(invoice_id: str, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    """Accept the AI-predicted job coding for an invoice."""
    query = select(Invoice).options(selectinload(Invoice.line_items)).where(Invoice.id == invoice_id)
    result = await db.execute(query)
    invoice = result.scalar_one_or_none()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found.")

    if not invoice.coding_predictions:
        raise HTTPException(status_code=400, detail="No coding predictions available.")

    predictions = invoice.coding_predictions
    job_number = predictions.get("predicted_job_number")
    cost_code = predictions.get("predicted_cost_code")

    previous = {"job_number": invoice.job_number, "cost_code": invoice.cost_code, "coding_status": invoice.coding_status}

    if job_number:
        invoice.job_number = job_number
    if cost_code:
        invoice.cost_code = cost_code
    invoice.coding_status = "confirmed"

    await log_audit(
        db, invoice.id, "coding_confirmed",
        f"Confirmed AI coding: job={job_number}, cost_code={cost_code}",
        previous, {"job_number": job_number, "cost_code": cost_code, "coding_status": "confirmed"},
        user=user,
    )

    # Update vendor history
    if invoice.vendor_name and job_number and cost_code:
        await update_vendor_history(db, invoice.vendor_name, job_number, cost_code, invoice.tenant_id)

    await db.commit()
    await db.refresh(invoice)
    return invoice


@router.post("/{invoice_id}/select-coding")
async def select_coding_alternative(
    invoice_id: str, body: dict, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
):
    """Select an alternative coding prediction instead of the top one."""
    query = select(Invoice).options(selectinload(Invoice.line_items)).where(Invoice.id == invoice_id)
    result = await db.execute(query)
    invoice = result.scalar_one_or_none()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found.")

    job_number = body.get("job_number")
    cost_code = body.get("cost_code")
    if not job_number and not cost_code:
        raise HTTPException(status_code=400, detail="Provide job_number and/or cost_code.")

    previous = {"job_number": invoice.job_number, "cost_code": invoice.cost_code, "coding_status": invoice.coding_status}

    if job_number:
        invoice.job_number = job_number
    if cost_code:
        invoice.cost_code = cost_code
    invoice.coding_status = "confirmed"

    await log_audit(
        db, invoice.id, "coding_confirmed",
        f"Selected alternative coding: job={job_number}, cost_code={cost_code}",
        previous, {"job_number": job_number, "cost_code": cost_code, "coding_status": "confirmed"},
        user=user,
    )

    if invoice.vendor_name and job_number and cost_code:
        await update_vendor_history(db, invoice.vendor_name, job_number, cost_code, invoice.tenant_id)

    await db.commit()
    await db.refresh(invoice)
    return invoice


@router.get("/{invoice_id}/file")
async def get_invoice_file(invoice_id: str, db: AsyncSession = Depends(get_db)):
    query = select(Invoice).where(Invoice.id == invoice_id)
    result = await db.execute(query)
    invoice = result.scalar_one_or_none()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found.")
    return FileResponse(
        path=invoice.file_path,
        media_type=invoice.file_content_type,
        filename=invoice.file_name,
    )
