"""geo: private zones + append-only exact-location access log

Revision ID: 0003
Revises: 0002
Create Date: 2026-10-22
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from geoalchemy2 import Geography

revision: str = "0003"
down_revision: str | None = "0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA geo")
    op.create_table(
        "private_zone",
        sa.Column("id", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("owner_id", sa.Uuid(), nullable=False),
        sa.Column("kind", sa.Text(), nullable=False),
        sa.Column(
            "geom",
            Geography(geometry_type="POLYGON", srid=4326, spatial_index=False),
            nullable=False,
        ),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.CheckConstraint("kind IN ('home', 'private')", name="ck_private_zone_kind"),
        sa.PrimaryKeyConstraint("id", name="pk_private_zone"),
        schema="geo",
    )
    op.create_index("ix_geo_private_zone_owner_id", "private_zone", ["owner_id"], schema="geo")
    op.create_index(
        "idx_private_zone_geom", "private_zone", ["geom"], schema="geo", postgresql_using="gist"
    )

    op.create_table(
        "location_access_log",
        sa.Column("id", sa.BigInteger(), sa.Identity(), nullable=False),
        sa.Column("viewer_id", sa.Uuid(), nullable=True),
        sa.Column("tier", sa.SmallInteger(), nullable=False),
        sa.Column("observation_id", sa.Uuid(), nullable=False),
        sa.Column("purpose", sa.Text(), nullable=False),
        sa.Column("at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_location_access_log"),
        schema="geo",
    )
    op.create_index(
        "ix_geo_location_access_log_observation_id",
        "location_access_log",
        ["observation_id"],
        schema="geo",
    )
    # Audit rows are evidence: the database itself refuses to change them.
    op.execute(
        """
        CREATE FUNCTION geo.forbid_mutation() RETURNS trigger LANGUAGE plpgsql AS $$
        BEGIN
          RAISE EXCEPTION '%.% is append-only', TG_TABLE_SCHEMA, TG_TABLE_NAME;
        END $$
        """
    )
    op.execute(
        "CREATE TRIGGER location_access_log_append_only "
        "BEFORE UPDATE OR DELETE ON geo.location_access_log "
        "FOR EACH ROW EXECUTE FUNCTION geo.forbid_mutation()"
    )


def downgrade() -> None:
    op.execute("DROP SCHEMA geo CASCADE")
