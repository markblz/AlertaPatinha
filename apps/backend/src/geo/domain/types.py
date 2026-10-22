from dataclasses import dataclass
from datetime import timedelta
from enum import IntEnum, StrEnum
from uuid import UUID


@dataclass(frozen=True, slots=True)
class Point:
    lat: float
    lng: float


# Polygon exterior ring as (lat, lng) points, open (first point not repeated) —
# the shape h3.cell_to_boundary returns.
Ring = tuple[Point, ...]


class RelatoKind(StrEnum):
    SIGHTING = "sighting"
    EMERGENCY = "emergency"
    LOST = "lost"
    FOUND = "found"


class AnimalFlag(StrEnum):
    COMMUNITY = "community"  # cão/gato comunitário
    COLONY = "colony"  # colônia / feral
    SENSITIVE = "sensitive"  # valuable breed: theft target


class PrivacyClass(StrEnum):
    PUBLIC_PLACE = "public_place"
    NEAR_REPORTER_HOME = "near_reporter_home"
    PRIVATE_ZONE = "private_zone"
    COLONY = "colony"
    COMMUNITY = "community"
    SENSITIVE_ANIMAL = "sensitive_animal"


class DisplayMode(StrEnum):
    EXACT = "exact"
    APPROXIMATE = "approximate"
    HIDDEN = "hidden"


class Tier(IntEnum):
    T0 = 0  # anonymous
    T1 = 1  # phone-verified
    T2 = 2  # trusted (private, outcome-based)
    T3 = 3  # verified protetor/mantenedor with a territory
    T4 = 4  # verified org (ONG, CCZ) with a service area


@dataclass(frozen=True, slots=True)
class PrivateZone:
    id: UUID
    owner_id: UUID
    ring: Ring


@dataclass(frozen=True, slots=True)
class Display:
    """Public geometry, decided once at write time and stored."""

    mode: DisplayMode
    cell: str | None  # H3 cell (hex string); None when hidden
    publish_delay: timedelta = timedelta(0)


@dataclass(frozen=True, slots=True)
class Viewer:
    id: UUID | None  # None = nobody (public map, realtime payloads)
    tier: Tier
    is_staff: bool = False
    territories: tuple[Ring, ...] = ()  # T3 territory / T4 service area

    @classmethod
    def public(cls) -> "Viewer":
        return cls(id=None, tier=Tier.T0)


@dataclass(frozen=True, slots=True)
class AccessContext:
    alerted: bool = False  # viewer was alerted for this caso
    active_claim: bool = False  # viewer holds an unexpired "Estou indo"
    mantenedor_approved: bool = False  # colony exact access granted by its mantenedor
    staff_purpose: str | None = None  # staff must record why


@dataclass(frozen=True, slots=True)
class ObservationGeoFacts:
    observation_id: UUID
    reporter_id: UUID | None
    point: Point
    accuracy_m: int | None
    privacy_class: PrivacyClass
    display: Display
    zone_owner_ids: frozenset[UUID] = frozenset()  # owners of private zones covering point


@dataclass(frozen=True, slots=True)
class LocationView:
    """The only shape in which a location leaves geo."""

    mode: DisplayMode
    point: Point | None = None  # set only when mode is EXACT
    accuracy_m: int | None = None
    cell: str | None = None  # set only when mode is APPROXIMATE
    boundary: Ring | None = None
