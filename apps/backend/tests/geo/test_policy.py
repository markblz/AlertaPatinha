"""🧠 Acceptance tests for src/geo/domain/policy.py (docs/domain/location-privacy.md).

Red until you implement the policy. If a test encodes a decision you disagree
with, change the spec first, then the test — never just the test.
"""

import math
import uuid
from datetime import timedelta

import pytest

from src.geo.domain import cells, policy
from src.geo.domain.types import (
    AccessContext,
    AnimalFlag,
    DisplayMode,
    LocationView,
    ObservationGeoFacts,
    Point,
    PrivacyClass,
    PrivateZone,
    RelatoKind,
    Ring,
    Tier,
    Viewer,
)

SE = Point(lat=-23.5505, lng=-46.6333)  # Praça da Sé, São Paulo
NO_FLAGS: frozenset[AnimalFlag] = frozenset()


def offset(p: Point, north_m: float = 0.0, east_m: float = 0.0) -> Point:
    return Point(
        lat=p.lat + north_m / 111_320,
        lng=p.lng + east_m / (111_320 * math.cos(math.radians(p.lat))),
    )


def square(center: Point, half_m: float) -> Ring:
    return (
        offset(center, half_m, -half_m),
        offset(center, half_m, half_m),
        offset(center, -half_m, half_m),
        offset(center, -half_m, -half_m),
    )


def facts(
    point: Point = SE,
    *,
    kind: RelatoKind = RelatoKind.SIGHTING,
    privacy_class: PrivacyClass = PrivacyClass.PUBLIC_PLACE,
    reporter_id: uuid.UUID | None = None,
    zone_owner_ids: frozenset[uuid.UUID] = frozenset(),
) -> ObservationGeoFacts:
    return ObservationGeoFacts(
        observation_id=uuid.uuid4(),
        reporter_id=reporter_id,
        point=point,
        accuracy_m=15,
        privacy_class=privacy_class,
        display=policy.display_for(point, privacy_class, kind),
        zone_owner_ids=zone_owner_ids,
    )


def viewer(tier: Tier = Tier.T1, **kw: object) -> Viewer:
    return Viewer(id=uuid.uuid4(), tier=tier, **kw)  # type: ignore[arg-type]


def resolution(view: LocationView) -> int:
    assert view.cell is not None, view
    return cells.resolution_of(view.cell)


# ── classify_privacy ─────────────────────────────────────────────────────────


def test_a_street_far_from_home_and_zones_is_a_public_place() -> None:
    home = offset(SE, north_m=5_000)

    got = policy.classify_privacy(SE, home, [], RelatoKind.SIGHTING, NO_FLAGS)

    assert got is PrivacyClass.PUBLIC_PLACE


def test_example_2_point_120m_from_reporter_home_is_near_home() -> None:
    home = offset(SE, east_m=120)

    got = policy.classify_privacy(SE, home, [], RelatoKind.SIGHTING, NO_FLAGS)

    assert got is PrivacyClass.NEAR_REPORTER_HOME
    assert cells.resolution_of(policy.display_for(SE, got, RelatoKind.SIGHTING).cell or "") == 7


def test_a_point_inside_a_private_zone_is_private_zone() -> None:
    zone = PrivateZone(id=uuid.uuid4(), owner_id=uuid.uuid4(), ring=square(SE, 50))

    got = policy.classify_privacy(SE, None, [zone], RelatoKind.SIGHTING, NO_FLAGS)

    assert got is PrivacyClass.PRIVATE_ZONE


def test_a_candidate_zone_that_does_not_contain_the_point_is_ignored() -> None:
    zone = PrivateZone(id=uuid.uuid4(), owner_id=uuid.uuid4(), ring=square(offset(SE, 400), 50))

    got = policy.classify_privacy(SE, None, [zone], RelatoKind.SIGHTING, NO_FLAGS)

    assert got is PrivacyClass.PUBLIC_PLACE


@pytest.mark.parametrize(
    ("flag", "expected"),
    [
        (AnimalFlag.COMMUNITY, PrivacyClass.COMMUNITY),
        (AnimalFlag.COLONY, PrivacyClass.COLONY),
        (AnimalFlag.SENSITIVE, PrivacyClass.SENSITIVE_ANIMAL),
    ],
)
def test_animal_flags_set_the_class(flag: AnimalFlag, expected: PrivacyClass) -> None:
    got = policy.classify_privacy(SE, None, [], RelatoKind.SIGHTING, frozenset({flag}))

    assert got is expected


def test_most_restrictive_class_wins_private_zone_over_community() -> None:
    zone = PrivateZone(id=uuid.uuid4(), owner_id=uuid.uuid4(), ring=square(SE, 50))

    got = policy.classify_privacy(
        SE, None, [zone], RelatoKind.SIGHTING, frozenset({AnimalFlag.COMMUNITY})
    )

    assert got is PrivacyClass.PRIVATE_ZONE


# ── display_for ──────────────────────────────────────────────────────────────


def test_example_1_same_point_twice_gives_the_same_display() -> None:
    first = policy.display_for(SE, PrivacyClass.PUBLIC_PLACE, RelatoKind.SIGHTING)
    second = policy.display_for(SE, PrivacyClass.PUBLIC_PLACE, RelatoKind.SIGHTING)

    assert first == second


def test_public_emergency_is_never_exact_but_the_res9_cell_containing_the_point() -> None:
    display = policy.display_for(SE, PrivacyClass.PUBLIC_PLACE, RelatoKind.EMERGENCY)

    assert display.mode is DisplayMode.APPROXIMATE
    assert display.cell == cells.cell_of(SE, 9)


@pytest.mark.parametrize(
    ("privacy_class", "res"),
    [
        (PrivacyClass.PUBLIC_PLACE, 9),
        (PrivacyClass.COMMUNITY, 8),
        (PrivacyClass.NEAR_REPORTER_HOME, 7),
        (PrivacyClass.SENSITIVE_ANIMAL, 7),
    ],
)
def test_display_resolution_per_class(privacy_class: PrivacyClass, res: int) -> None:
    display = policy.display_for(SE, privacy_class, RelatoKind.SIGHTING)

    assert display.mode is DisplayMode.APPROXIMATE
    assert display.cell == cells.cell_of(SE, res)


def test_colony_is_res7_or_hidden_never_finer() -> None:
    display = policy.display_for(SE, PrivacyClass.COLONY, RelatoKind.SIGHTING)

    assert display.mode in (DisplayMode.APPROXIMATE, DisplayMode.HIDDEN)
    if display.cell is not None:
        assert cells.resolution_of(display.cell) <= 7


def test_sensitive_animal_waits_before_publication() -> None:
    display = policy.display_for(SE, PrivacyClass.SENSITIVE_ANIMAL, RelatoKind.SIGHTING)

    assert display.publish_delay >= timedelta(hours=12)


def test_public_place_publishes_immediately() -> None:
    display = policy.display_for(SE, PrivacyClass.PUBLIC_PLACE, RelatoKind.SIGHTING)

    assert display.publish_delay == timedelta(0)


# ── view_for / can_see_exact ─────────────────────────────────────────────────


def test_public_viewer_gets_the_cell_boundary_and_no_point() -> None:
    f = facts()

    view = policy.view_for(f, Viewer.public(), AccessContext())

    assert view.mode is DisplayMode.APPROXIMATE
    assert view.point is None and view.accuracy_m is None
    assert view.cell == f.display.cell
    assert view.boundary == cells.ring_of(view.cell or "")


def test_reporter_sees_their_own_relato_exact() -> None:
    reporter = viewer(Tier.T0)
    f = facts(reporter_id=reporter.id)

    view = policy.view_for(f, reporter, AccessContext())

    assert view.mode is DisplayMode.EXACT
    assert view.point == SE and view.accuracy_m == 15


def test_another_t0_user_does_not_see_exact() -> None:
    f = facts(reporter_id=uuid.uuid4())

    assert policy.can_see_exact(viewer(Tier.T0), f, AccessContext()) is False


def test_example_3_colony_for_t3_without_mantenedor_approval_is_res7() -> None:
    t3 = viewer(Tier.T3, territories=(square(SE, 2_000),))
    f = facts(privacy_class=PrivacyClass.COLONY)

    view = policy.view_for(f, t3, AccessContext(mantenedor_approved=False))

    assert view.mode is not DisplayMode.EXACT
    if view.mode is DisplayMode.APPROXIMATE:
        assert resolution(view) <= 7


def test_colony_for_t3_with_mantenedor_approval_inside_territory_is_exact() -> None:
    t3 = viewer(Tier.T3, territories=(square(SE, 2_000),))
    f = facts(privacy_class=PrivacyClass.COLONY)

    assert policy.can_see_exact(t3, f, AccessContext(mantenedor_approved=True)) is True


def test_t3_outside_their_territory_does_not_see_exact() -> None:
    t3 = viewer(Tier.T3, territories=(square(offset(SE, 10_000), 2_000),))
    f = facts(kind=RelatoKind.EMERGENCY)

    assert policy.can_see_exact(t3, f, AccessContext()) is False


def test_example_4_emergency_exact_for_t1_holding_an_active_claim() -> None:
    helper = viewer(Tier.T1)
    f = facts(kind=RelatoKind.EMERGENCY)

    view = policy.view_for(f, helper, AccessContext(active_claim=True))

    assert view.mode is DisplayMode.EXACT and view.point == SE


def test_example_4_after_claim_expiry_back_to_res9() -> None:
    helper = viewer(Tier.T1)
    f = facts(kind=RelatoKind.EMERGENCY)

    view = policy.view_for(f, helper, AccessContext(active_claim=False))

    assert view.mode is DisplayMode.APPROXIMATE and resolution(view) == 9


def test_example_5_inside_two_zones_hidden_for_all_but_owners_and_staff() -> None:
    owner_a, owner_b = viewer(Tier.T0), viewer(Tier.T0)
    zones = [
        PrivateZone(id=uuid.uuid4(), owner_id=owner_a.id or uuid.uuid4(), ring=square(SE, 50)),
        PrivateZone(id=uuid.uuid4(), owner_id=owner_b.id or uuid.uuid4(), ring=square(SE, 80)),
    ]
    privacy_class = policy.classify_privacy(SE, None, zones, RelatoKind.SIGHTING, NO_FLAGS)
    f = facts(
        privacy_class=privacy_class,
        reporter_id=uuid.uuid4(),
        zone_owner_ids=frozenset(z.owner_id for z in zones),
    )
    org = viewer(Tier.T4, territories=(square(SE, 5_000),))
    staff = viewer(Tier.T0, is_staff=True)

    assert policy.view_for(f, Viewer.public(), AccessContext()).mode is DisplayMode.HIDDEN
    assert policy.view_for(f, org, AccessContext()).mode is DisplayMode.HIDDEN
    assert policy.view_for(f, owner_a, AccessContext()).mode is not DisplayMode.HIDDEN
    assert policy.view_for(f, owner_b, AccessContext()).mode is not DisplayMode.HIDDEN
    assert (
        policy.view_for(f, staff, AccessContext(staff_purpose="takedown")).mode
        is not DisplayMode.HIDDEN
    )


def test_staff_without_a_recorded_purpose_gets_no_exact_point() -> None:
    staff = viewer(Tier.T0, is_staff=True)

    assert policy.can_see_exact(staff, facts(), AccessContext()) is False


def test_example_6_hundred_public_reads_are_identical() -> None:
    f = facts(kind=RelatoKind.EMERGENCY)

    views = {policy.view_for(f, Viewer.public(), AccessContext()) for _ in range(100)}

    assert len(views) == 1
