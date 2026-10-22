import uuid
from datetime import datetime

from geoalchemy2 import Geography
from sqlalchemy import BigInteger, CheckConstraint, DateTime, SmallInteger, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from src.shared.db import Base

SCHEMA = "geo"


class PrivateZoneRow(Base):
    __tablename__ = "private_zone"
    __table_args__ = (
        CheckConstraint("kind IN ('home', 'private')", name="kind"),
        {"schema": SCHEMA},
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, server_default=func.gen_random_uuid())
    owner_id: Mapped[uuid.UUID] = mapped_column(index=True)
    kind: Mapped[str] = mapped_column(Text)
    geom: Mapped[object] = mapped_column(
        Geography(geometry_type="POLYGON", srid=4326, spatial_index=True)
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class LocationAccessLogRow(Base):
    """Append-only (UPDATE/DELETE blocked by trigger): one row per exact point served."""

    __tablename__ = "location_access_log"
    __table_args__ = {"schema": SCHEMA}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    viewer_id: Mapped[uuid.UUID | None]
    tier: Mapped[int] = mapped_column(SmallInteger)
    observation_id: Mapped[uuid.UUID] = mapped_column(index=True)
    purpose: Mapped[str] = mapped_column(Text)
    at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
