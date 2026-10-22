import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum

from src.geo.public import AnimalFlag, LocationView, ObservationGeoFacts, Point, RelatoKind
from src.observations.domain.seen import PublicSeen, SeenInterval


class Species(StrEnum):
    DOG = "dog"
    CAT = "cat"
    OTHER = "other"


class LocSource(StrEnum):
    GPS = "gps"  # device geolocation
    PIN = "pin"  # dropped/adjusted on the map
    GEOCODE = "geocode"  # typed address
    TEXT = "text"  # described in words (WhatsApp, M5)


@dataclass(frozen=True, slots=True)
class NewRelato:
    client_id: uuid.UUID
    kind: RelatoKind
    species: Species
    point: Point
    accuracy_m: int | None
    loc_source: LocSource
    seen_text: str | None
    animal_count: int = 1
    animal_flags: frozenset[AnimalFlag] = frozenset()
    attributes: dict[str, object] = field(default_factory=dict)
    source: str = "web"


@dataclass(frozen=True, slots=True)
class StoredRelato:
    """A relato as read back from storage. Holds private facts (exact point,
    precise valid_time): it never leaves this module except through views."""

    id: uuid.UUID
    kind: RelatoKind
    species: Species
    animal_count: int
    geo: ObservationGeoFacts
    seen: SeenInterval
    attributes: dict[str, object]
    publish_at: datetime


@dataclass(frozen=True, slots=True)
class CreateResult:
    id: uuid.UUID
    created: bool  # False = idempotent replay of an earlier write


@dataclass(frozen=True, slots=True)
class RelatoView:
    id: uuid.UUID
    kind: RelatoKind
    species: Species
    animal_count: int
    location: LocationView
    seen: PublicSeen
    attributes: dict[str, object]
    is_mine: bool


@dataclass(frozen=True, slots=True)
class MapFeature:
    id: uuid.UUID
    kind: RelatoKind
    species: Species
    animal_count: int
    location: LocationView
    seen: PublicSeen


@dataclass(frozen=True, slots=True)
class MapPage:
    features: list[MapFeature]
    truncated: bool  # hit the feature cap: zoom in for the rest
