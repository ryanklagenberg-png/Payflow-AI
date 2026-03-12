import uuid
from datetime import date, datetime

from sqlalchemy import (
    Date,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Invoice(Base):
    __tablename__ = "invoices"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), default=uuid.UUID("00000000-0000-0000-0000-000000000000"), index=True
    )
    status: Mapped[str] = mapped_column(String(20), default="uploaded")
    file_name: Mapped[str] = mapped_column(String(255))
    file_path: Mapped[str] = mapped_column(String(500))
    file_content_type: Mapped[str] = mapped_column(String(100))

    # Extracted fields
    vendor_name: Mapped[str | None] = mapped_column(String(255))
    vendor_address: Mapped[str | None] = mapped_column(Text)
    invoice_number: Mapped[str | None] = mapped_column(String(100))
    invoice_date: Mapped[date | None] = mapped_column(Date)
    due_date: Mapped[date | None] = mapped_column(Date)
    po_number: Mapped[str | None] = mapped_column(String(100))
    subtotal: Mapped[float | None] = mapped_column(Numeric(12, 2))
    tax_amount: Mapped[float | None] = mapped_column(Numeric(12, 2))
    total_amount: Mapped[float | None] = mapped_column(Numeric(12, 2))
    currency: Mapped[str] = mapped_column(String(10), default="USD")
    payment_terms: Mapped[str | None] = mapped_column(String(100))

    # Construction-specific fields
    job_number: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    cost_code: Mapped[str | None] = mapped_column(String(20), nullable=True)

    # AI metadata
    raw_extraction: Mapped[dict | None] = mapped_column(JSONB)
    confidence_score: Mapped[float | None] = mapped_column(Float)

    # Coding predictions
    coding_predictions: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    coding_status: Mapped[str | None] = mapped_column(String(20), nullable=True)
    coding_confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    coding_method: Mapped[str | None] = mapped_column(String(30), nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    line_items: Mapped[list["InvoiceLineItem"]] = relationship(back_populates="invoice", cascade="all, delete-orphan")

    __table_args__ = (Index("ix_invoices_tenant_status", "tenant_id", "status"),)


class InvoiceLineItem(Base):
    __tablename__ = "invoice_line_items"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    invoice_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("invoices.id", ondelete="CASCADE"))
    line_number: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)
    quantity: Mapped[float | None] = mapped_column(Numeric(12, 4))
    unit_price: Mapped[float | None] = mapped_column(Numeric(12, 4))
    amount: Mapped[float | None] = mapped_column(Numeric(12, 2))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    invoice: Mapped["Invoice"] = relationship(back_populates="line_items")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    invoice_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("invoices.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    user_email: Mapped[str | None] = mapped_column(String(255))
    action: Mapped[str] = mapped_column(String(50))  # uploaded, extracted, approved, rejected, edited, re-extracted, deleted
    details: Mapped[str | None] = mapped_column(Text)
    previous_value: Mapped[dict | None] = mapped_column(JSONB)
    new_value: Mapped[dict | None] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    invoice: Mapped["Invoice"] = relationship()


class VendorCodingHistory(Base):
    __tablename__ = "vendor_coding_history"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), default=uuid.UUID("00000000-0000-0000-0000-000000000000")
    )
    vendor_name: Mapped[str] = mapped_column(String(255))
    job_number: Mapped[str] = mapped_column(String(50))
    cost_code: Mapped[str] = mapped_column(String(20))
    invoice_count: Mapped[int] = mapped_column(Integer, default=1)
    last_used_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (Index("ix_vendor_coding_history_tenant_vendor", "tenant_id", "vendor_name"),)
