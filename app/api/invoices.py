import logging
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config import settings
from app.database import get_db
from app.models.invoice import Invoice, InvoiceLineItem
from app.schemas.invoice import InvoiceDetail, InvoiceListItem, InvoiceUploadResponse
from app.services import storage
from app.services.extraction import extract_invoice

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/invoices", tags=["invoices"])

ALLOWED_TYPES = {"application/pdf", "image/png", "image/jpeg", "image/webp", "image/tiff"}


@router.post("/upload", response_model=InvoiceUploadResponse)
async def upload_invoice(file: UploadFile, db: AsyncSession = Depends(get_db)):
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

        await db.commit()
        message = f"Invoice extracted successfully. Confidence: {result.confidence_score}"

    except Exception as e:
        logger.error("Extraction failed for %s: %s", file.filename, e)
        invoice.status = "failed"
        await db.commit()
        message = f"Invoice uploaded but extraction failed: {e}"

    return InvoiceUploadResponse(
        id=invoice.id,
        status=invoice.status,
        file_name=invoice.file_name,
        message=message,
    )


@router.get("", response_model=list[InvoiceListItem])
async def list_invoices(
    status: str | None = None,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
):
    query = select(Invoice).order_by(Invoice.created_at.desc()).offset(skip).limit(limit)
    if status:
        query = query.where(Invoice.status == status)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{invoice_id}", response_model=InvoiceDetail)
async def get_invoice(invoice_id: str, db: AsyncSession = Depends(get_db)):
    query = select(Invoice).options(selectinload(Invoice.line_items)).where(Invoice.id == invoice_id)
    result = await db.execute(query)
    invoice = result.scalar_one_or_none()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found.")
    return invoice
