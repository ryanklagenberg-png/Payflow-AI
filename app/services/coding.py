import json
import logging
import re
import uuid

import anthropic
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.invoice import Invoice, VendorCodingHistory
from app.prompts.gl_coding import GL_CODING_PROMPT
from app.schemas.coding import CodingAlternative, CodingPrediction

logger = logging.getLogger(__name__)

client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

# Mark III job number pattern: {company}-{division}-{job#}
JOB_NUMBER_PATTERN = re.compile(r"^\d-\d{2}-\d{4,5}$")
COST_CODE_PATTERN = re.compile(r"^\d{2}-\d{3}$")

AUTO_APPLY_THRESHOLD = 0.90


def _normalize_vendor(name: str) -> str:
    """Normalize vendor name for matching."""
    name = name.lower().strip()
    # Strip common suffixes
    for suffix in [" inc", " inc.", " llc", " ltd", " corp", " corporation", " co.", " company"]:
        if name.endswith(suffix):
            name = name[: -len(suffix)].strip()
    return name


async def _get_vendor_history(
    db: AsyncSession, vendor_name: str, tenant_id: uuid.UUID
) -> list[dict]:
    """Get this vendor's coding history, ordered by most-used."""
    normalized = _normalize_vendor(vendor_name)
    query = (
        select(VendorCodingHistory)
        .where(
            and_(
                VendorCodingHistory.tenant_id == tenant_id,
                VendorCodingHistory.vendor_name == normalized,
            )
        )
        .order_by(VendorCodingHistory.invoice_count.desc())
        .limit(10)
    )
    result = await db.execute(query)
    rows = result.scalars().all()
    return [
        {
            "job_number": r.job_number,
            "cost_code": r.cost_code,
            "invoice_count": r.invoice_count,
            "last_used": str(r.last_used_at),
        }
        for r in rows
    ]


async def _check_po_match(
    db: AsyncSession, po_number: str, tenant_id: uuid.UUID
) -> dict | None:
    """Check if any approved invoice with this PO has known job/cost coding."""
    query = (
        select(Invoice)
        .where(
            and_(
                Invoice.tenant_id == tenant_id,
                Invoice.po_number == po_number,
                Invoice.job_number.isnot(None),
                Invoice.cost_code.isnot(None),
                Invoice.status.in_(["approved", "extracted"]),
            )
        )
        .order_by(Invoice.updated_at.desc())
        .limit(1)
    )
    result = await db.execute(query)
    match = result.scalar_one_or_none()
    if match:
        return {"job_number": match.job_number, "cost_code": match.cost_code}
    return None


async def predict_coding(invoice_id: uuid.UUID, db: AsyncSession) -> CodingPrediction:
    """Run the GL & Job Coding Agent on an invoice."""
    query = select(Invoice).where(Invoice.id == invoice_id)
    result = await db.execute(query)
    invoice = result.scalar_one_or_none()
    if not invoice:
        raise ValueError(f"Invoice {invoice_id} not found")

    # Signal 1: PO match (highest confidence, no Claude call needed)
    if invoice.po_number:
        po_match = await _check_po_match(db, invoice.po_number, invoice.tenant_id)
        if po_match:
            prediction = CodingPrediction(
                predicted_job_number=po_match["job_number"],
                predicted_cost_code=po_match["cost_code"],
                confidence=0.95,
                method="po_match",
                reasoning=f"Matched PO {invoice.po_number} to existing invoice with job {po_match['job_number']} / {po_match['cost_code']}",
            )
            await _store_prediction(db, invoice, prediction)
            return prediction

    # Signal 2: Job reference already on invoice (validate format)
    if invoice.job_number and JOB_NUMBER_PATTERN.match(invoice.job_number):
        # Job was on the invoice — still might need cost code from Claude or history
        if invoice.cost_code and COST_CODE_PATTERN.match(invoice.cost_code):
            # Both already extracted and valid
            prediction = CodingPrediction(
                predicted_job_number=invoice.job_number,
                predicted_cost_code=invoice.cost_code,
                confidence=0.95,
                method="job_reference",
                reasoning="Job number and cost code were extracted directly from the invoice document",
            )
            await _store_prediction(db, invoice, prediction)
            return prediction

    # Gather context for Claude
    vendor_history = []
    if invoice.vendor_name:
        vendor_history = await _get_vendor_history(db, invoice.vendor_name, invoice.tenant_id)

    # Signal 3: Strong vendor history match (skip Claude if single dominant coding)
    if vendor_history and not invoice.job_number:
        top = vendor_history[0]
        if top["invoice_count"] >= 3 and (
            len(vendor_history) == 1
            or top["invoice_count"] >= vendor_history[1]["invoice_count"] * 3
        ):
            alternatives = [
                CodingAlternative(
                    job_number=h["job_number"],
                    cost_code=h["cost_code"],
                    confidence=0.7,
                    reasoning=f"Used {h['invoice_count']} times previously",
                )
                for h in vendor_history[1:3]
            ]
            prediction = CodingPrediction(
                predicted_job_number=top["job_number"],
                predicted_cost_code=top["cost_code"],
                confidence=0.90,
                method="vendor_history",
                reasoning=f"Vendor has been coded to this job/cost {top['invoice_count']} times — dominant pattern",
                alternatives=alternatives,
            )
            await _store_prediction(db, invoice, prediction)
            return prediction

    # Signal 4: Call Claude for material analysis + any partial signals
    prediction = await _call_claude_coding(invoice, vendor_history)
    await _store_prediction(db, invoice, prediction)
    return prediction


async def _call_claude_coding(
    invoice: Invoice, vendor_history: list[dict]
) -> CodingPrediction:
    """Call Claude to predict job coding based on invoice data and context."""
    # Build line items summary
    line_items_text = "None extracted"
    if invoice.raw_extraction and invoice.raw_extraction.get("line_items"):
        items = invoice.raw_extraction["line_items"]
        line_items_text = json.dumps(items, indent=2)

    vendor_history_text = json.dumps(vendor_history, indent=2) if vendor_history else "No prior history for this vendor"

    user_message = f"""Predict the job_number and cost_code for this invoice:

Vendor: {invoice.vendor_name or "Unknown"}
PO Number: {invoice.po_number or "Not provided"}
Extracted Job Number: {invoice.job_number or "Not on invoice"}
Extracted Cost Code: {invoice.cost_code or "Not on invoice"}
Invoice Amount: {invoice.total_amount or "Unknown"}

Line Items:
{line_items_text}

Vendor Coding History (most recent first):
{vendor_history_text}

Predict the job_number and cost_code for this invoice."""

    try:
        message = client.messages.create(
            model=settings.CLAUDE_MODEL,
            max_tokens=1024,
            system=GL_CODING_PROMPT,
            messages=[{"role": "user", "content": user_message}],
        )

        response_text = message.content[0].text

        # Strip markdown fences
        if response_text.startswith("```"):
            lines = response_text.split("\n")
            lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            response_text = "\n".join(lines)

        data = json.loads(response_text)
        return CodingPrediction(**data)

    except Exception as e:
        logger.error("Coding prediction Claude call failed: %s", e)
        return CodingPrediction(
            predicted_job_number=None,
            predicted_cost_code=None,
            confidence=0.0,
            method="manual_required",
            reasoning=f"AI coding prediction failed: {e}",
        )


async def _store_prediction(
    db: AsyncSession, invoice: Invoice, prediction: CodingPrediction
) -> None:
    """Store the prediction on the invoice record."""
    invoice.coding_predictions = prediction.model_dump()
    invoice.coding_status = "predicted"
    invoice.coding_confidence = prediction.confidence
    invoice.coding_method = prediction.method

    # Auto-apply if high confidence and fields aren't already set
    if prediction.confidence >= AUTO_APPLY_THRESHOLD:
        if prediction.predicted_job_number and not invoice.job_number:
            invoice.job_number = prediction.predicted_job_number
        if prediction.predicted_cost_code and not invoice.cost_code:
            invoice.cost_code = prediction.predicted_cost_code


async def update_vendor_history(
    db: AsyncSession,
    vendor_name: str,
    job_number: str,
    cost_code: str,
    tenant_id: uuid.UUID,
) -> None:
    """Upsert vendor coding history when an invoice is confirmed/approved."""
    normalized = _normalize_vendor(vendor_name)

    query = select(VendorCodingHistory).where(
        and_(
            VendorCodingHistory.tenant_id == tenant_id,
            VendorCodingHistory.vendor_name == normalized,
            VendorCodingHistory.job_number == job_number,
            VendorCodingHistory.cost_code == cost_code,
        )
    )
    result = await db.execute(query)
    existing = result.scalar_one_or_none()

    if existing:
        existing.invoice_count += 1
        from sqlalchemy import func
        existing.last_used_at = func.now()
    else:
        entry = VendorCodingHistory(
            tenant_id=tenant_id,
            vendor_name=normalized,
            job_number=job_number,
            cost_code=cost_code,
            invoice_count=1,
        )
        db.add(entry)
