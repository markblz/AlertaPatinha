import uuid
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from sqlalchemy.ext.asyncio import AsyncSession

from src.geo import public as geo
from src.observations.domain import seen as seen_policy
from src.observations.domain.seen import PublicSeen
from src.observations.domain.types import (
    CreateResult,
    MapFeature,
    MapPage,
    NewRelato,
    RelatoView,
    StoredRelato,
)
from src.observations.repository import queries

MAP_FEATURE_CAP = 500
_HOUR = timedelta(hours=1)


class ClientIdConflict(Exception):
    """The client_id belongs to another reporter's relato."""


class RelatoNotFound(Exception):
    pass


def _polygon_wkt(ring: geo.Ring) -> str:
    coords = [*ring, ring[0]]
    return "SRID=4326;POLYGON((" + ", ".join(f"{p.lng} {p.lat}" for p in coords) + "))"


async def _replay(
    session: AsyncSession, client_id: uuid.UUID, reporter_id: uuid.UUID | None
) -> CreateResult | None:
    existing = await queries.find_by_client_id(session, client_id)
    if existing is None:
        return None
    relato_id, owner = existing
    if owner != reporter_id:
        raise ClientIdConflict(str(client_id))
    return CreateResult(id=relato_id, created=False)


async def create_relato(
    session: AsyncSession,
    cmd: NewRelato,
    reporter_id: uuid.UUID | None,
    now: datetime,
    tz: ZoneInfo,
) -> CreateResult:
    # Replays return the original even if the retry arrives hours later with a
    # different "now": the first write is the fact.
    if (replay := await _replay(session, cmd.client_id, reporter_id)) is not None:
        return replay

    seen = seen_policy.parse_seen(cmd.seen_text, now, tz)
    privacy_class, display = await geo.mask_for_write(
        session, cmd.point, reporter_id, cmd.kind, cmd.animal_flags
    )
    new_id = await queries.insert_if_new(
        session,
        queries.InsertValues(
            client_id=cmd.client_id,
            reporter_id=reporter_id,
            source=cmd.source,
            kind=cmd.kind.value,
            species=cmd.species.value,
            animal_count=cmd.animal_count,
            seen=seen,
            point=cmd.point,
            accuracy_m=cmd.accuracy_m,
            loc_source=cmd.loc_source.value,
            privacy_class=privacy_class.value,
            display=display,
            display_ring_wkt=_polygon_wkt(geo.ring_of(display.cell)) if display.cell else None,
            h3_r9=geo.cell_of(cmd.point, 9),
            h3_r7=geo.cell_of(cmd.point, 7),
            attributes=dict(cmd.attributes),
        ),
    )
    if new_id is None:  # a concurrent retry won the insert
        replay = await _replay(session, cmd.client_id, reporter_id)
        assert replay is not None
        return replay
    return CreateResult(id=new_id, created=True)


def _own_seen(stored: StoredRelato) -> PublicSeen:
    s = stored.seen
    return PublicSeen(start=s.start, end=s.end, precision=s.precision)


async def get_relato(
    session: AsyncSession, relato_id: uuid.UUID, viewer: geo.Viewer, now: datetime, tz: ZoneInfo
) -> RelatoView:
    stored = await queries.get(session, relato_id)
    if stored is None:
        raise RelatoNotFound(str(relato_id))
    is_mine = viewer.id is not None and viewer.id == stored.geo.reporter_id
    if stored.publish_at > now and not is_mine:
        raise RelatoNotFound(str(relato_id))

    if viewer.id is None:
        location = geo.render_public(stored.geo)
    else:
        location = await geo.render_for(
            session, stored.geo, viewer, geo.AccessContext(), purpose="relato_detail"
        )
    return RelatoView(
        id=stored.id,
        kind=stored.kind,
        species=stored.species,
        animal_count=stored.animal_count,
        location=location,
        seen=_own_seen(stored)
        if is_mine
        else seen_policy.coarsen_for_public(stored.seen, stored.kind, tz),
        attributes=stored.attributes,
        is_mine=is_mine,
    )


def _floor_hour(t: datetime) -> datetime:
    return t.replace(minute=0, second=0, microsecond=0)


async def map_page(
    session: AsyncSession,
    *,
    west: float,
    south: float,
    east: float,
    north: float,
    since: datetime,
    until: datetime,
    tz: ZoneInfo,
) -> MapPage:
    # Whole-hour windows: sliding `since` minute by minute would otherwise
    # reveal valid_time more precisely than the coarsened value we publish.
    since = _floor_hour(since)
    until = _floor_hour(until) + (_HOUR if until != _floor_hour(until) else timedelta(0))
    rows = await queries.in_bbox(
        session,
        west=west,
        south=south,
        east=east,
        north=north,
        since=since,
        until=until,
        limit=MAP_FEATURE_CAP + 1,
    )
    return MapPage(
        features=[
            MapFeature(
                id=r.id,
                kind=r.kind,
                species=r.species,
                animal_count=r.animal_count,
                location=geo.render_public(r.geo),
                seen=seen_policy.coarsen_for_public(r.seen, r.kind, tz),
            )
            for r in rows[:MAP_FEATURE_CAP]
        ],
        truncated=len(rows) > MAP_FEATURE_CAP,
    )
