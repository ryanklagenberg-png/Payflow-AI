"""Initial schema - invoices and line items

Revision ID: 001
Revises:
Create Date: 2026-03-09
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB, UUID

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "invoices",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("tenant_id", UUID(as_uuid=True), nullable=False, server_default=sa.text("'00000000-0000-0000-0000-000000000000'::uuid")),
        sa.Column("status", sa.String(20), nullable=False, server_default="uploaded"),
        sa.Column("file_name", sa.String(255), nullable=False),
        sa.Column("file_path", sa.String(500), nullable=False),
        sa.Column("file_content_type", sa.String(100), nullable=False),
        sa.Column("vendor_name", sa.String(255)),
        sa.Column("vendor_address", sa.Text),
        sa.Column("invoice_number", sa.String(100)),
        sa.Column("invoice_date", sa.Date),
        sa.Column("due_date", sa.Date),
        sa.Column("po_number", sa.String(100)),
        sa.Column("subtotal", sa.Numeric(12, 2)),
        sa.Column("tax_amount", sa.Numeric(12, 2)),
        sa.Column("total_amount", sa.Numeric(12, 2)),
        sa.Column("currency", sa.String(10), nullable=False, server_default="USD"),
        sa.Column("payment_terms", sa.String(100)),
        sa.Column("raw_extraction", JSONB),
        sa.Column("confidence_score", sa.Float),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_invoices_tenant_id", "invoices", ["tenant_id"])
    op.create_index("ix_invoices_tenant_status", "invoices", ["tenant_id", "status"])
    op.create_index("ix_invoices_created_at", "invoices", ["created_at"])

    op.create_table(
        "invoice_line_items",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("invoice_id", UUID(as_uuid=True), sa.ForeignKey("invoices.id", ondelete="CASCADE"), nullable=False),
        sa.Column("line_number", sa.Integer, nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("quantity", sa.Numeric(12, 4)),
        sa.Column("unit_price", sa.Numeric(12, 4)),
        sa.Column("amount", sa.Numeric(12, 2)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_line_items_invoice_id", "invoice_line_items", ["invoice_id"])


def downgrade() -> None:
    op.drop_table("invoice_line_items")
    op.drop_table("invoices")
