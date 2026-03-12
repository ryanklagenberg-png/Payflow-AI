"""Add coding prediction columns and vendor_coding_history table

Revision ID: 006
Revises: 005
Create Date: 2026-03-11
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB, UUID

revision: str = "006"
down_revision: Union[str, None] = "005"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add coding prediction columns to invoices
    op.add_column("invoices", sa.Column("coding_predictions", JSONB, nullable=True))
    op.add_column("invoices", sa.Column("coding_status", sa.String(20), nullable=True))
    op.add_column("invoices", sa.Column("coding_confidence", sa.Float, nullable=True))
    op.add_column("invoices", sa.Column("coding_method", sa.String(30), nullable=True))

    # Create vendor_coding_history table
    op.create_table(
        "vendor_coding_history",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", UUID(as_uuid=True), nullable=False),
        sa.Column("vendor_name", sa.String(255), nullable=False),
        sa.Column("job_number", sa.String(50), nullable=False),
        sa.Column("cost_code", sa.String(20), nullable=False),
        sa.Column("invoice_count", sa.Integer, default=1, nullable=False),
        sa.Column("last_used_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index(
        "ix_vendor_coding_history_tenant_vendor",
        "vendor_coding_history",
        ["tenant_id", "vendor_name"],
    )

    # Backfill vendor_coding_history from existing approved/extracted invoices
    op.execute("""
        INSERT INTO vendor_coding_history (id, tenant_id, vendor_name, job_number, cost_code, invoice_count, last_used_at, created_at)
        SELECT gen_random_uuid(), tenant_id, lower(trim(vendor_name)), job_number, cost_code,
               count(*)::int, max(updated_at), now()
        FROM invoices
        WHERE vendor_name IS NOT NULL AND job_number IS NOT NULL AND cost_code IS NOT NULL
          AND status IN ('approved', 'extracted')
        GROUP BY tenant_id, lower(trim(vendor_name)), job_number, cost_code
    """)


def downgrade() -> None:
    op.drop_table("vendor_coding_history")
    op.drop_column("invoices", "coding_method")
    op.drop_column("invoices", "coding_confidence")
    op.drop_column("invoices", "coding_status")
    op.drop_column("invoices", "coding_predictions")
