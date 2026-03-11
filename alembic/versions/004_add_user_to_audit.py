"""Add user_id and user_email to audit_logs

Revision ID: 004
Revises: 003
Create Date: 2026-03-10
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

revision: str = "004"
down_revision: Union[str, None] = "003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("audit_logs", sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True))
    op.add_column("audit_logs", sa.Column("user_email", sa.String(255), nullable=True))


def downgrade() -> None:
    op.drop_column("audit_logs", "user_email")
    op.drop_column("audit_logs", "user_id")
