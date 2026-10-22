import json
import uuid

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from src.geo.domain.types import Point, PrivateZone, Viewer
from src.geo.repository.models import LocationAccessLogRow, PrivateZoneRow

# Generous pre-filter: whether "near" or "inside" applies is the policy's call.
ZONE_CANDIDATE_RADIUS_M = 1000


def _geog(point: Point) -> str:
    return f"SRID=4326;POINT({point.lng} {point.lat})"


def _ring_from_geojson(geojson: str) -> tuple[Point, ...]:
    exterior = json.loads(geojson)["coordinates"][0]
    return tuple(Point(lat=lat, lng=lng) for lng, lat in exterior[:-1])


async def candidate_zones(session: AsyncSession, point: Point) -> list[PrivateZone]:
    rows = await session.execute(
        text(
            "SELECT id, owner_id, ST_AsGeoJSON(geom) FROM geo.private_zone "
            "WHERE kind = 'private' AND ST_DWithin(geom, ST_GeogFromText(:p), :r)"
        ),
        {"p": _geog(point), "r": ZONE_CANDIDATE_RADIUS_M},
    )
    return [
        PrivateZone(id=zid, owner_id=owner, ring=_ring_from_geojson(gj)) for zid, owner, gj in rows
    ]


async def reporter_home(session: AsyncSession, reporter_id: uuid.UUID) -> Point | None:
    row = (
        await session.execute(
            text(
                "SELECT ST_Y(c), ST_X(c) FROM ("
                "  SELECT ST_Centroid(geom::geometry) AS c FROM geo.private_zone"
                "  WHERE owner_id = :owner AND kind = 'home' ORDER BY created_at DESC LIMIT 1"
                ") home"
            ),
            {"owner": reporter_id},
        )
    ).first()
    return Point(lat=row[0], lng=row[1]) if row else None


async def zone_owners_covering(session: AsyncSession, point: Point) -> frozenset[uuid.UUID]:
    owners = await session.scalars(
        select(PrivateZoneRow.owner_id)
        .where(PrivateZoneRow.kind == "private")
        .where(text("ST_Covers(geom, ST_GeogFromText(:p))").bindparams(p=_geog(point)))
    )
    return frozenset(owners)


async def log_exact_access(
    session: AsyncSession, viewer: Viewer, observation_id: uuid.UUID, purpose: str
) -> None:
    session.add(
        LocationAccessLogRow(
            viewer_id=viewer.id,
            tier=int(viewer.tier),
            observation_id=observation_id,
            purpose=purpose,
        )
    )
    await session.flush()
