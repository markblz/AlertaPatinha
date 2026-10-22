import dataclasses
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from src.geo.domain import policy
from src.geo.domain.types import (
    AccessContext,
    AnimalFlag,
    Display,
    DisplayMode,
    LocationView,
    ObservationGeoFacts,
    Point,
    PrivacyClass,
    RelatoKind,
    Viewer,
)
from src.geo.repository import queries


class PrivacyViolation(RuntimeError):
    """A public render produced an exact point. A policy bug: fail closed."""


async def mask_for_write(
    session: AsyncSession,
    point: Point,
    reporter_id: uuid.UUID | None,
    kind: RelatoKind,
    flags: frozenset[AnimalFlag],
) -> tuple[PrivacyClass, Display]:
    zones = await queries.candidate_zones(session, point)
    home = await queries.reporter_home(session, reporter_id) if reporter_id else None
    privacy_class = policy.classify_privacy(point, home, zones, kind, flags)
    return privacy_class, policy.display_for(point, privacy_class, kind)


def render_public(facts: ObservationGeoFacts) -> LocationView:
    """For the map and realtime payloads: no session, no log, never exact."""
    view = policy.view_for(facts, Viewer.public(), AccessContext())
    if view.mode is DisplayMode.EXACT or view.point is not None:
        raise PrivacyViolation(f"public view of {facts.observation_id} is exact")
    return view


async def render_for(
    session: AsyncSession,
    facts: ObservationGeoFacts,
    viewer: Viewer,
    context: AccessContext,
    purpose: str,
) -> LocationView:
    """For one authenticated viewer. Writes the access log iff the view is exact."""
    if viewer.id is not None:
        owners = await queries.zone_owners_covering(session, facts.point)
        facts = dataclasses.replace(facts, zone_owner_ids=owners)
    view = policy.view_for(facts, viewer, context)
    if view.mode is DisplayMode.EXACT:
        await queries.log_exact_access(session, viewer, facts.observation_id, purpose)
    return view
