import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from sqlalchemy import func, select, text
from sqlalchemy.dialects.postgresql import Range, insert
from sqlalchemy.engine import Row
from sqlalchemy.ext.asyncio import AsyncSession

from src.geo.public import (
    Display,
    DisplayMode,
    ObservationGeoFacts,
    Point,
    PrivacyClass,
    RelatoKind,
)
from src.observations.domain.seen import SeenInterval, TimePrecision
from src.observations.domain.types import Species, StoredRelato
from src.observations.repository.models import ObservationRow


@dataclass(frozen=True, slots=True)
class InsertValues:
    client_id: uuid.UUID
    reporter_id: uuid.UUID | None
    source: str
    kind: str
    species: str
    animal_count: int
    seen: SeenInterval
    point: Point
    accuracy_m: int | None
    loc_source: str
    privacy_class: str
    display: Display
    display_ring_wkt: str | None
    h3_r9: str
    h3_r7: str
    attributes: dict[str, Any]


def _point_wkt(point: Point) -> str:
    return f"SRID=4326;POINT({point.lng} {point.lat})"


async def insert_if_new(session: AsyncSession, v: InsertValues) -> uuid.UUID | None:
    """Returns the new id, or None if `client_id` already exists (idempotent replay)."""
    stmt = (
        insert(ObservationRow)
        .values(
            client_id=v.client_id,
            reporter_id=v.reporter_id,
            source=v.source,
            kind=v.kind,
            species=v.species,
            animal_count=v.animal_count,
            valid_time=Range(v.seen.start, v.seen.end, bounds="[)"),
            time_precision=v.seen.precision.value,
            time_text=v.seen.text,
            edtf=v.seen.edtf,
            publish_at=func.now() + v.display.publish_delay,
            true_geom=func.ST_GeogFromText(_point_wkt(v.point)),
            loc_accuracy_m=v.accuracy_m,
            loc_source=v.loc_source,
            privacy_class=v.privacy_class,
            display_mode=v.display.mode.value,
            display_cell=v.display.cell,
            display_geom=(func.ST_GeogFromText(v.display_ring_wkt) if v.display_ring_wkt else None),
            h3_r9=v.h3_r9,
            h3_r7=v.h3_r7,
            attributes=v.attributes,
        )
        .on_conflict_do_nothing(index_elements=[ObservationRow.client_id])
        .returning(ObservationRow.id)
    )
    return (await session.execute(stmt)).scalar_one_or_none()


async def find_by_client_id(
    session: AsyncSession, client_id: uuid.UUID
) -> tuple[uuid.UUID, uuid.UUID | None] | None:
    row = (
        await session.execute(
            select(ObservationRow.id, ObservationRow.reporter_id).where(
                ObservationRow.client_id == client_id
            )
        )
    ).first()
    return (row.id, row.reporter_id) if row else None


# Private columns are selected only to build ObservationGeoFacts / SeenInterval,
# which leave the module solely through geo.render_* and coarsen_for_public.
_STORED_COLUMNS = """
    id, reporter_id, kind, species, animal_count,
    ST_Y(true_geom::geometry) AS lat, ST_X(true_geom::geometry) AS lng, loc_accuracy_m,
    privacy_class, display_mode, display_cell::text AS display_cell,
    lower(valid_time) AS seen_start, upper(valid_time) AS seen_end,
    time_precision, time_text, edtf, attributes, publish_at
"""


def _stored(row: Row[Any]) -> StoredRelato:
    m = row._mapping
    return StoredRelato(
        id=m["id"],
        kind=RelatoKind(m["kind"]),
        species=Species(m["species"]),
        animal_count=m["animal_count"],
        geo=ObservationGeoFacts(
            observation_id=m["id"],
            reporter_id=m["reporter_id"],
            point=Point(lat=m["lat"], lng=m["lng"]),
            accuracy_m=m["loc_accuracy_m"],
            privacy_class=PrivacyClass(m["privacy_class"]),
            # publish_delay is already applied (publish_at); not needed on read.
            display=Display(mode=DisplayMode(m["display_mode"]), cell=m["display_cell"]),
        ),
        seen=SeenInterval(
            start=m["seen_start"],
            end=m["seen_end"],
            precision=TimePrecision(m["time_precision"]),
            text=m["time_text"],
            edtf=m["edtf"],
        ),
        attributes=m["attributes"],
        publish_at=m["publish_at"],
    )


async def get(session: AsyncSession, relato_id: uuid.UUID) -> StoredRelato | None:
    row = (
        await session.execute(
            text(
                f"SELECT {_STORED_COLUMNS} FROM observations.observation "
                "WHERE id = :id AND hidden_at IS NULL"
            ),
            {"id": relato_id},
        )
    ).first()
    return _stored(row) if row else None


async def in_bbox(
    session: AsyncSession,
    *,
    west: float,
    south: float,
    east: float,
    north: float,
    since: datetime,
    until: datetime,
    limit: int,
) -> list[StoredRelato]:
    # Filter on display_geom, NEVER true_geom: shrinking a bbox around a
    # point until it disappears would otherwise binary-search the exact spot.
    rows = await session.execute(
        text(
            f"SELECT {_STORED_COLUMNS} FROM observations.observation "
            "WHERE hidden_at IS NULL AND publish_at <= now() AND display_mode <> 'hidden' "
            "  AND display_geom && ST_MakeEnvelope(:w, :s, :e, :n, 4326)::geography "
            "  AND valid_time && tstzrange(:since, :until, '[)') "
            # Hour bucket, then random UUID: ordering by exact valid_time would
            # leak the true sequence of relatos published as the same hour.
            "ORDER BY date_trunc('hour', upper(valid_time)) DESC, id LIMIT :limit"
        ),
        {
            "w": west,
            "s": south,
            "e": east,
            "n": north,
            "since": since,
            "until": until,
            "limit": limit,
        },
    )
    return [_stored(r) for r in rows]
