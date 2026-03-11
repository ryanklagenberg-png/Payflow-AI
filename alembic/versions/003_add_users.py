"""Add users table with seed data

Revision ID: 003
Revises: 002
Create Date: 2026-03-10
"""
from typing import Sequence, Union

import bcrypt
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

revision: str = "003"
down_revision: Union[str, None] = "002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _hash(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("email", sa.String(255), unique=True, nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("role", sa.String(20), nullable=False, server_default="user"),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    # Seed default users
    users_table = sa.table(
        "users",
        sa.column("email", sa.String),
        sa.column("name", sa.String),
        sa.column("password_hash", sa.String),
        sa.column("role", sa.String),
    )
    op.bulk_insert(users_table, [
        {
            "email": "admin@payflow.ai",
            "name": "Admin",
            "password_hash": _hash("PayFlow2026!"),
            "role": "admin",
        },
        {
            "email": "ryan.klagenberg@payflow.ai",
            "name": "Ryan Klagenberg",
            "password_hash": _hash("PayFlow2026!"),
            "role": "admin",
        },
    ])


def downgrade() -> None:
    op.drop_table("users")
