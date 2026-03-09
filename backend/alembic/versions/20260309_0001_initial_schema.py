"""initial schema

Revision ID: 20260309_0001
Revises:
Create Date: 2026-03-09 13:10:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "20260309_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "plans",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("slug", sa.String(length=20), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("price_monthly", sa.Integer(), nullable=False),
        sa.Column("max_files_per_month", sa.Integer(), nullable=False),
        sa.Column("max_file_size_mb", sa.Integer(), nullable=False),
        sa.Column("max_chat_messages_per_day", sa.Integer(), nullable=False),
        sa.Column("max_analyses_per_month", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug"),
    )
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("plan_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["plan_id"], ["plans.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_table(
        "uploaded_files",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("original_name", sa.String(length=500), nullable=False),
        sa.Column("s3_key", sa.String(length=500), nullable=False),
        sa.Column("parquet_s3_key", sa.String(length=500), nullable=True),
        sa.Column("mime_type", sa.String(length=100), nullable=False),
        sa.Column("size_bytes", sa.BigInteger(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("row_count", sa.Integer(), nullable=True),
        sa.Column("column_count", sa.Integer(), nullable=True),
        sa.Column("profile", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("domain", sa.String(length=20), nullable=True),
        sa.Column("preview", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "analyses",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("title", sa.String(length=500), nullable=True),
        sa.Column("insights", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("chart_specs", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("llm_tokens_used", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "usage_records",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("period", sa.Date(), nullable=False),
        sa.Column("files_uploaded", sa.Integer(), nullable=False),
        sa.Column("analyses_run", sa.Integer(), nullable=False),
        sa.Column("chat_messages_sent", sa.Integer(), nullable=False),
        sa.Column("tokens_consumed", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "analysis_files",
        sa.Column("analysis_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("file_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(["analysis_id"], ["analyses.id"]),
        sa.ForeignKeyConstraint(["file_id"], ["uploaded_files.id"]),
        sa.PrimaryKeyConstraint("analysis_id", "file_id"),
    )
    op.create_table(
        "chat_messages",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("analysis_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("role", sa.String(length=20), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("chart_spec", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("tokens_used", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["analysis_id"], ["analyses.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    plans_table = sa.table(
        "plans",
        sa.column("id", postgresql.UUID(as_uuid=False)),
        sa.column("slug", sa.String(length=20)),
        sa.column("name", sa.String(length=50)),
        sa.column("price_monthly", sa.Integer()),
        sa.column("max_files_per_month", sa.Integer()),
        sa.column("max_file_size_mb", sa.Integer()),
        sa.column("max_chat_messages_per_day", sa.Integer()),
        sa.column("max_analyses_per_month", sa.Integer()),
    )
    op.bulk_insert(
        plans_table,
        [
            {
                "id": "11111111-1111-1111-1111-111111111111",
                "slug": "free",
                "name": "Free",
                "price_monthly": 0,
                "max_files_per_month": 5,
                "max_file_size_mb": 5,
                "max_chat_messages_per_day": 10,
                "max_analyses_per_month": 3,
            },
            {
                "id": "22222222-2222-2222-2222-222222222222",
                "slug": "starter",
                "name": "Starter",
                "price_monthly": 990,
                "max_files_per_month": 30,
                "max_file_size_mb": 20,
                "max_chat_messages_per_day": 50,
                "max_analyses_per_month": 15,
            },
            {
                "id": "33333333-3333-3333-3333-333333333333",
                "slug": "business",
                "name": "Business",
                "price_monthly": 3990,
                "max_files_per_month": 1000000,
                "max_file_size_mb": 50,
                "max_chat_messages_per_day": 1000000,
                "max_analyses_per_month": 1000000,
            },
            {
                "id": "44444444-4444-4444-4444-444444444444",
                "slug": "pro",
                "name": "Pro",
                "price_monthly": 9990,
                "max_files_per_month": 1000000,
                "max_file_size_mb": 100,
                "max_chat_messages_per_day": 1000000,
                "max_analyses_per_month": 1000000,
            },
        ],
    )


def downgrade() -> None:
    op.drop_table("chat_messages")
    op.drop_table("analysis_files")
    op.drop_table("usage_records")
    op.drop_table("analyses")
    op.drop_table("uploaded_files")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
    op.drop_table("plans")
