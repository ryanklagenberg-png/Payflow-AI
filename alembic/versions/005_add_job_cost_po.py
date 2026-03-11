"""Add job_number, cost_code, po_number columns to invoices

Revision ID: 005
Revises: 004
Create Date: 2026-03-10
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "005"
down_revision: Union[str, None] = "004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("invoices", sa.Column("job_number", sa.String(50), nullable=True))
    op.add_column("invoices", sa.Column("cost_code", sa.String(20), nullable=True))
    # po_number already exists on the table; skip adding it
    op.create_index("ix_invoices_job_number", "invoices", ["job_number"])


def downgrade() -> None:
    op.drop_index("ix_invoices_job_number", table_name="invoices")
    op.drop_column("invoices", "cost_code")
    op.drop_column("invoices", "job_number")
