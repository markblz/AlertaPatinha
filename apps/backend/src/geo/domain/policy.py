"""🧠 Location policy — owner implements first; Claude reviews.

Spec: docs/domain/location-privacy.md. Tests: tests/geo/test_policy.py.

Rules for this file: pure functions only — no I/O, no clock, no randomness.
`src/geo/domain/cells.py` has the H3 helpers you need.
"""

from collections.abc import Sequence

from src.geo.domain.types import (
    AccessContext,
    AnimalFlag,
    Display,
    LocationView,
    ObservationGeoFacts,
    Point,
    PrivacyClass,
    PrivateZone,
    RelatoKind,
    Viewer,
)

_YOURS = "🧠 yours to implement — docs/domain/location-privacy.md"


def classify_privacy(
    point: Point,
    reporter_home: Point | None,
    private_zones: Sequence[PrivateZone],
    relato_kind: RelatoKind,
    animal_flags: frozenset[AnimalFlag],
) -> PrivacyClass:
    """Most restrictive class wins. `private_zones` are candidates near the point
    (the repository pre-filters by distance); deciding containment is yours."""
    raise NotImplementedError(_YOURS)


def display_for(point: Point, privacy_class: PrivacyClass, relato_kind: RelatoKind) -> Display:
    """Stable: the same inputs always give the same Display."""
    raise NotImplementedError(_YOURS)


def can_see_exact(viewer: Viewer, observation: ObservationGeoFacts, context: AccessContext) -> bool:
    raise NotImplementedError(_YOURS)


def view_for(
    observation: ObservationGeoFacts, viewer: Viewer, context: AccessContext
) -> LocationView:
    """The ONLY function that turns stored facts into an outgoing location."""
    raise NotImplementedError(_YOURS)
