"""identity: actor + device session

Revision ID: 0002
Revises: 0001
Create Date: 2026-10-22
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0002"
down_revision: str | None = "0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA identity")
    op.create_table(
        "actor",
        sa.Column("id", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("tier", sa.SmallInteger(), server_default="0", nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.CheckConstraint("tier BETWEEN 0 AND 4", name="ck_actor_tier"),
        sa.PrimaryKeyConstraint("id", name="pk_actor"),
        schema="identity",
    )
    op.create_table(
        "session",
        sa.Column("id", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("actor_id", sa.Uuid(), nullable=False),
        sa.Column("token_hash", sa.LargeBinary(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["actor_id"], ["identity.actor.id"], name="fk_session_actor_id_actor"
        ),
        sa.PrimaryKeyConstraint("id", name="pk_session"),
        sa.UniqueConstraint("token_hash", name="uq_session_token_hash"),
        schema="identity",
    )
    op.create_index("ix_identity_session_actor_id", "session", ["actor_id"], schema="identity")


def downgrade() -> None:
    op.execute("DROP SCHEMA identity CASCADE")
