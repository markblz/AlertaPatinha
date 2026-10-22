"""🧠 When was the animal seen — owner implements first; Claude reviews.

Spec: docs/domain/data-model.md § Time. Tests: tests/observations/test_seen.py.
Pure functions: `now` and `tz` are parameters, never read from the clock here.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from zoneinfo import ZoneInfo

from src.geo.public import RelatoKind


class TimePrecision(StrEnum):
    EXACT = "exact"
    MINUTES = "minutes"
    HOUR = "hour"
    PART_OF_DAY = "part_of_day"
    DAY = "day"
    APPROX = "approx"


@dataclass(frozen=True, slots=True)
class SeenInterval:
    """valid_time: when the animal was seen. Half-open [start, end), tz-aware."""

    start: datetime
    end: datetime
    precision: TimePrecision
    text: str | None  # the reporter's own words, always kept
    edtf: str | None = None  # e.g. '2026-10-20T15:00~'


@dataclass(frozen=True, slots=True)
class PublicSeen:
    """What a viewer may know about valid_time: coarsened, never finer than policy."""

    start: datetime
    end: datetime
    precision: TimePrecision


class SeenParseError(ValueError):
    """The text could not be understood. The API turns this into a 422 that asks again."""


_YOURS = "🧠 yours to implement — docs/domain/data-model.md § Time"


def parse_seen(text: str | None, now: datetime, tz: ZoneInfo) -> SeenInterval:
    raise NotImplementedError(_YOURS)


def coarsen_for_public(seen: SeenInterval, kind: RelatoKind, tz: ZoneInfo) -> PublicSeen:
    """Emergência → whole hours; everything else → part of day (location-privacy.md
    § Time is location too). Never narrower than `seen`."""
    raise NotImplementedError(_YOURS)
