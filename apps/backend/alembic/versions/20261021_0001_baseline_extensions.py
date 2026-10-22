"""baseline: extensions the domain depends on

Revision ID: 0001
Revises:
Create Date: 2026-10-21

PostGIS itself is created by the postgis image's init script; IF NOT EXISTS
keeps this migration valid on a managed Postgres where it is not.
Module schemas are NOT created here: each module creates its own schema in
its first migration (CLAUDE.md rule 3).
"""

from collections.abc import Sequence

from alembic import op

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

EXTENSIONS = ("postgis", "h3", "h3_postgis", "vector", "unaccent", "pg_trgm", "pg_stat_statements")


def upgrade() -> None:
    # CASCADE: h3_postgis requires postgis_raster, which nothing else creates.
    for ext in EXTENSIONS:
        op.execute(f"CREATE EXTENSION IF NOT EXISTS {ext} CASCADE")


def downgrade() -> None:
    # postgis stays: the image owns it and tiger/topology depend on it.
    for ext in reversed(EXTENSIONS[1:]):
        op.execute(f"DROP EXTENSION IF EXISTS {ext}")
