import uuid
from datetime import date, datetime

from pydantic import BaseModel


class LineItemSchema(BaseModel):
    line_number: int
    description: str
    quantity: float | None = None
    unit_price: float | None = None
    amount: float | None = None


class ExtractionResult(BaseModel):
    vendor_name: str | None = None
    vendor_address: str | None = None
    invoice_number: str | None = None
    invoice_date: str | None = None
    due_date: str | None = None
    po_number: str | None = None
    job_number: str | None = None
    cost_code: str | None = None
    subtotal: float | None = None
    tax_amount: float | None = None
    total_amount: float | None = None
    currency: str = "USD"
    payment_terms: str | None = None
    line_items: list[LineItemSchema] = []
    confidence_score: float | None = None


class InvoiceUploadResponse(BaseModel):
    id: uuid.UUID
    status: str
    file_name: str
    message: str

    model_config = {"from_attributes": True}


class InvoiceLineItemOut(BaseModel):
    id: uuid.UUID
    line_number: int
    description: str
    quantity: float | None = None
    unit_price: float | None = None
    amount: float | None = None

    model_config = {"from_attributes": True}


class InvoiceDetail(BaseModel):
    id: uuid.UUID
    status: str
    file_name: str
    vendor_name: str | None = None
    vendor_address: str | None = None
    invoice_number: str | None = None
    invoice_date: date | None = None
    due_date: date | None = None
    po_number: str | None = None
    job_number: str | None = None
    cost_code: str | None = None
    subtotal: float | None = None
    tax_amount: float | None = None
    total_amount: float | None = None
    currency: str
    payment_terms: str | None = None
    confidence_score: float | None = None
    coding_predictions: dict | None = None
    coding_status: str | None = None
    coding_confidence: float | None = None
    coding_method: str | None = None
    line_items: list[InvoiceLineItemOut] = []
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class InvoiceUpdate(BaseModel):
    vendor_name: str | None = None
    vendor_address: str | None = None
    invoice_number: str | None = None
    invoice_date: date | None = None
    due_date: date | None = None
    po_number: str | None = None
    job_number: str | None = None
    cost_code: str | None = None
    subtotal: float | None = None
    tax_amount: float | None = None
    total_amount: float | None = None
    currency: str | None = None
    payment_terms: str | None = None


class InvoiceListItem(BaseModel):
    id: uuid.UUID
    status: str
    file_name: str
    vendor_name: str | None = None
    invoice_number: str | None = None
    total_amount: float | None = None
    invoice_date: date | None = None
    job_number: str | None = None
    cost_code: str | None = None
    po_number: str | None = None
    coding_status: str | None = None
    coding_confidence: float | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class InvoiceListResponse(BaseModel):
    items: list[InvoiceListItem]
    total: int
