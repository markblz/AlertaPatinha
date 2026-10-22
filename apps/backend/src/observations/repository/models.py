import uuid
from datetime import datetime
from typing import Any

from geoalchemy2 import Geography
from sqlalchemy import CheckConstraint, DateTime, Index, SmallInteger, Text, func
from sqlalchemy.dialects.postgresql import JSONB, TSTZRANGE, Range
from sqlalchemy.dialects.postgresql.base import ischema_names
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import UserDefinedType

from src.shared.db import Base

SCHEMA = "observations"


class H3Index(UserDefinedType[str]):
    """h3-pg's h3index; asyncpg round-trips it as text ('89a8100c003ffff')."""

    cache_ok = True

    def get_col_spec(self, **kw: Any) -> str:
        return "h3index"


ischema_names["h3index"] = H3Index  # lets autogenerate reflect the column type


class ObservationRow(Base):
    """A relato. Insert-only: corrections are chain events, hiding is moderation."""

    __tablename__ = "observation"
    __table_args__ = (
        CheckConstraint("kind IN ('sighting', 'emergency', 'lost', 'found')", name="kind"),
        CheckConstraint("species IN ('dog', 'cat', 'other')", name="species"),
        CheckConstraint("animal_count BETWEEN 1 AND 50", name="animal_count"),
        CheckConstraint("display_mode IN ('exact', 'approximate', 'hidden')", name="display_mode"),
        CheckConstraint("(display_mode = 'hidden') = (display_cell IS NULL)", name="display_cell"),
        CheckConstraint("NOT isempty(valid_time)", name="valid_time"),
        Index("ix_observation_valid_time", "valid_time", postgresql_using="gist"),
        {"schema": SCHEMA},
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, server_default=func.gen_random_uuid())
    client_id: Mapped[uuid.UUID] = mapped_column(unique=True)
    reporter_id: Mapped[uuid.UUID | None] = mapped_column(index=True)
    source: Mapped[str] = mapped_column(Text)
    kind: Mapped[str] = mapped_column(Text)
    species: Mapped[str] = mapped_column(Text)
    animal_count: Mapped[int] = mapped_column(SmallInteger, server_default="1")

    valid_time: Mapped[Range[datetime]] = mapped_column(TSTZRANGE)
    time_precision: Mapped[str] = mapped_column(Text)
    time_text: Mapped[str | None] = mapped_column(Text)
    edtf: Mapped[str | None] = mapped_column(Text)
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    publish_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)

    true_geom: Mapped[object] = mapped_column(
        Geography(geometry_type="POINT", srid=4326, spatial_index=False)
    )
    loc_accuracy_m: Mapped[int | None]
    loc_source: Mapped[str] = mapped_column(Text)

    privacy_class: Mapped[str] = mapped_column(Text)
    display_mode: Mapped[str] = mapped_column(Text)
    display_cell: Mapped[str | None] = mapped_column(H3Index)
    display_geom: Mapped[object | None] = mapped_column(
        Geography(geometry_type="POLYGON", srid=4326, spatial_index=True)
    )
    h3_r9: Mapped[str] = mapped_column(H3Index, index=True)
    h3_r7: Mapped[str] = mapped_column(H3Index, index=True)

    attributes: Mapped[dict[str, Any]] = mapped_column(JSONB, server_default="{}")
    hidden_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
