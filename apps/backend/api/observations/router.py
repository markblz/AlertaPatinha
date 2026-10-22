import uuid
from datetime import UTC, datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Query, Response

from api.deps import AppSettings, CurrentPrincipal, DbSession, OptionalPrincipal, viewer_of
from api.errors import api_error, responses
from api.observations.schemas import (
    CreateRelatoIn,
    LocationOut,
    MapFeatureOut,
    MapFeatureProps,
    MapOut,
    RelatoCreated,
    RelatoOut,
    SeenOut,
    geometry_of,
)
from src.geo.public import Point
from src.observations.public import (
    ClientIdConflict,
    NewRelato,
    RelatoNotFound,
    SeenParseError,
    create_relato,
    get_relato,
    map_page,
)

router = APIRouter(prefix="/api/v1", tags=["relatos"])

# ~55 km: a city, not a state. Wider views get aggregates (later slice), not points.
MAP_MAX_SPAN_DEG = 0.5
MAP_MAX_WINDOW = timedelta(days=90)


@router.post(
    "/relatos", response_model=RelatoCreated, status_code=201, responses=responses(401, 409, 422)
)
async def create(
    body: CreateRelatoIn,
    response: Response,
    db: DbSession,
    settings: AppSettings,
    principal: CurrentPrincipal,
) -> RelatoCreated:
    cmd = NewRelato(
        client_id=body.client_id,
        kind=body.kind,
        species=body.species,
        animal_count=body.animal_count,
        point=Point(lat=body.location.lat, lng=body.location.lng),
        accuracy_m=body.location.accuracy_m,
        loc_source=body.location.source,
        seen_text=body.seen_text,
        animal_flags=frozenset(body.flags),
        attributes=body.attributes.model_dump(exclude_defaults=True),
    )
    try:
        result = await create_relato(
            db, cmd, reporter_id=principal.actor_id, now=datetime.now(UTC), tz=settings.tz
        )
    except SeenParseError as exc:
        raise api_error(422, "seen_unparseable", str(exc)) from exc
    except ClientIdConflict as exc:
        raise api_error(409, "client_id_conflict", "client_id already used") from exc
    await db.commit()
    if not result.created:
        response.status_code = 200
    return RelatoCreated(id=result.id, share_path=f"/r/{result.id}")


@router.get("/relatos/{relato_id}", response_model=RelatoOut, responses=responses(404, 422))
async def detail(
    relato_id: uuid.UUID,
    db: DbSession,
    settings: AppSettings,
    principal: OptionalPrincipal,
) -> RelatoOut:
    try:
        view = await get_relato(
            db, relato_id, viewer_of(principal), now=datetime.now(UTC), tz=settings.tz
        )
    except RelatoNotFound as exc:
        raise api_error(404, "relato_not_found", "Relato not found") from exc
    # Commit BEFORE responding: an exact point must never be served without
    # its location_access_log row being durable.
    await db.commit()
    return RelatoOut(
        id=view.id,
        kind=view.kind,
        species=view.species,
        animal_count=view.animal_count,
        location=LocationOut.of(view.location),
        seen=SeenOut.of(view.seen),
        attributes=view.attributes,
        is_mine=view.is_mine,
    )


def _parse_bbox(raw: str) -> tuple[float, float, float, float]:
    try:
        west, south, east, north = (float(part) for part in raw.split(","))
    except ValueError as exc:
        raise api_error(422, "bbox_invalid", "bbox must be west,south,east,north") from exc
    if not (-180 <= west < east <= 180 and -90 <= south < north <= 90):
        raise api_error(422, "bbox_invalid", "bbox must be west,south,east,north")
    return west, south, east, north


@router.get("/map", response_model=MapOut, responses=responses(422))
async def map_features(
    db: DbSession,
    settings: AppSettings,
    bbox: Annotated[str, Query(description="west,south,east,north (WGS84)")],
    since: datetime | None = None,
    until: datetime | None = None,
) -> MapOut:
    west, south, east, north = _parse_bbox(bbox)
    if east - west > MAP_MAX_SPAN_DEG or north - south > MAP_MAX_SPAN_DEG:
        return MapOut(features=[], zoom_in=True)

    now = datetime.now(UTC)
    until = min(until or now, now)
    since = max(since or until - timedelta(days=7), until - MAP_MAX_WINDOW)
    page = await map_page(
        db, west=west, south=south, east=east, north=north, since=since, until=until, tz=settings.tz
    )
    features = []
    for f in page.features:
        geometry = geometry_of(f.location)
        if geometry is None:  # hidden: never on the map
            continue
        features.append(
            MapFeatureOut(
                id=f.id,
                geometry=geometry,
                properties=MapFeatureProps(
                    kind=f.kind,
                    species=f.species,
                    animal_count=f.animal_count,
                    display_mode=f.location.mode,
                    seen_start=f.seen.start,
                    seen_end=f.seen.end,
                    seen_precision=f.seen.precision,
                ),
            )
        )
    return MapOut(features=features, truncated=page.truncated)
