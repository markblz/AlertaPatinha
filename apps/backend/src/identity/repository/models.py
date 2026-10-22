import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, LargeBinary, SmallInteger, func
from sqlalchemy.orm import Mapped, mapped_column

from src.shared.db import Base

SCHEMA = "identity"


class ActorRow(Base):
    """A person as the platform knows them. Starts anonymous (tier 0, one device);
    phone verification (M4) raises the tier on the SAME actor, so earlier
    relatos stay theirs."""

    __tablename__ = "actor"
    __table_args__ = (CheckConstraint("tier BETWEEN 0 AND 4", name="tier"), {"schema": SCHEMA})

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, server_default=func.gen_random_uuid())
    tier: Mapped[int] = mapped_column(SmallInteger, server_default="0")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class SessionRow(Base):
    """One per device. The same token works as an HttpOnly cookie (web) or a
    Bearer header (native app)."""

    __tablename__ = "session"
    __table_args__ = {"schema": SCHEMA}

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, server_default=func.gen_random_uuid())
    actor_id: Mapped[uuid.UUID] = mapped_column(ForeignKey(ActorRow.id), index=True)
    token_hash: Mapped[bytes] = mapped_column(LargeBinary, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
