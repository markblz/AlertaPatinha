"""observations: relato (immutable, bitemporal, masked at write time)

Revision ID: 0004
Revises: 0003
Create Date: 2026-10-22
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from geoalchemy2 import Geography
from sqlalchemy.dialects.postgresql import JSONB, TSTZRANGE

revision: str = "0004"
down_revision: str | None = "0003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA observations")
    op.create_table(
        "observation",
        sa.Column("id", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("client_id", sa.Uuid(), nullable=False),
        sa.Column("reporter_id", sa.Uuid(), nullable=True),
        sa.Column("source", sa.Text(), nullable=False),
        sa.Column("kind", sa.Text(), nullable=False),
        sa.Column("species", sa.Text(), nullable=False),
        sa.Column("animal_count", sa.SmallInteger(), server_default="1", nullable=False),
        sa.Column("valid_time", TSTZRANGE(), nullable=False),
        sa.Column("time_precision", sa.Text(), nullable=False),
        sa.Column("time_text", sa.Text(), nullable=True),
        sa.Column("edtf", sa.Text(), nullable=True),
        sa.Column(
            "recorded_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column("publish_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "true_geom",
            Geography(geometry_type="POINT", srid=4326, spatial_index=False),
            nullable=False,
        ),
        sa.Column("loc_accuracy_m", sa.Integer(), nullable=True),
        sa.Column("loc_source", sa.Text(), nullable=False),
        sa.Column("privacy_class", sa.Text(), nullable=False),
        sa.Column("display_mode", sa.Text(), nullable=False),
        sa.Column(
            "display_geom",
            Geography(geometry_type="POLYGON", srid=4326, spatial_index=False),
            nullable=True,
        ),
        sa.Column("attributes", JSONB(), server_default="{}", nullable=False),
        sa.Column("hidden_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(
            "kind IN ('sighting', 'emergency', 'lost', 'found')", name="ck_observation_kind"
        ),
        sa.CheckConstraint("species IN ('dog', 'cat', 'other')", name="ck_observation_species"),
        sa.CheckConstraint("animal_count BETWEEN 1 AND 50", name="ck_observation_animal_count"),
        sa.CheckConstraint(
            "display_mode IN ('exact', 'approximate', 'hidden')", name="ck_observation_display_mode"
        ),
        sa.CheckConstraint("NOT isempty(valid_time)", name="ck_observation_valid_time"),
        sa.PrimaryKeyConstraint("id", name="pk_observation"),
        sa.UniqueConstraint("client_id", name="uq_observation_client_id"),
        schema="observations",
    )
    # h3index comes from the h3 extension; SQLAlchemy has no type for it.
    op.execute(
        "ALTER TABLE observations.observation "
        "ADD COLUMN display_cell h3index, "
        "ADD COLUMN h3_r9 h3index NOT NULL, "
        "ADD COLUMN h3_r7 h3index NOT NULL, "
        "ADD CONSTRAINT ck_observation_display_cell "
        "  CHECK ((display_mode = 'hidden') = (display_cell IS NULL))"
    )
    for name, cols, using in (
        ("ix_observations_observation_reporter_id", ["reporter_id"], None),
        ("ix_observations_observation_publish_at", ["publish_at"], None),
        ("ix_observations_observation_h3_r9", ["h3_r9"], None),
        ("ix_observations_observation_h3_r7", ["h3_r7"], None),
        ("ix_observation_valid_time", ["valid_time"], "gist"),
        ("idx_observation_display_geom", ["display_geom"], "gist"),
    ):
        op.create_index(name, "observation", cols, schema="observations", postgresql_using=using)
    # Relatos are facts (CLAUDE.md rule 4). Moderation hiding is the one
    # sanctioned UPDATE, and only of hidden_at.
    op.execute(
        """
        CREATE FUNCTION observations.guard_immutable() RETURNS trigger LANGUAGE plpgsql AS $$
        BEGIN
          IF TG_OP = 'DELETE' THEN
            RAISE EXCEPTION 'observations.observation is insert-only';
          END IF;
          IF (to_jsonb(NEW) - 'hidden_at') IS DISTINCT FROM (to_jsonb(OLD) - 'hidden_at') THEN
            RAISE EXCEPTION 'observations.observation is immutable (only hidden_at may change)';
          END IF;
          RETURN NEW;
        END $$
        """
    )
    op.execute(
        "CREATE TRIGGER observation_immutable "
        "BEFORE UPDATE OR DELETE ON observations.observation "
        "FOR EACH ROW EXECUTE FUNCTION observations.guard_immutable()"
    )


def downgrade() -> None:
    op.execute("DROP SCHEMA observations CASCADE")
