"""🧠 Acceptance tests for src/observations/domain/seen.py (docs/domain/data-model.md § Time).

Red until you implement. Part-of-day table v0: madrugada 00–06 · manhã 06–12 ·
tarde 12–18 · noite 18–24 · "hoje cedo" 05–09 · "agora há pouco" now−1h…now.
"""

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pytest

from src.geo.domain.types import RelatoKind
from src.observations.domain.seen import (
    PublicSeen,
    SeenInterval,
    TimePrecision,
    coarsen_for_public,
    parse_seen,
)

SP = ZoneInfo("America/Sao_Paulo")  # no DST since 2019: -03 all year
NOW = datetime(2026, 10, 21, 10, 0, tzinfo=SP)


def at(day: int, hour: int, minute: int = 0) -> datetime:
    return datetime(2026, 10, day, hour, minute, tzinfo=SP)


# ── parse_seen ───────────────────────────────────────────────────────────────


def test_example_1_ontem_a_tarde() -> None:
    got = parse_seen("ontem à tarde", NOW, SP)

    assert (got.start, got.end) == (at(20, 12), at(20, 18))
    assert got.precision is TimePrecision.PART_OF_DAY


def test_example_2_agora_ha_pouco() -> None:
    got = parse_seen("agora há pouco", NOW, SP)

    assert (got.start, got.end) == (NOW - timedelta(hours=1), NOW)
    assert got.precision is TimePrecision.APPROX


@pytest.mark.parametrize(
    ("text", "start", "end"),
    [
        ("ontem de madrugada", at(20, 0), at(20, 6)),
        ("ontem de manhã", at(20, 6), at(20, 12)),
        ("ontem à noite", at(20, 18), at(21, 0)),
        ("hoje de madrugada", at(21, 0), at(21, 6)),
        ("hoje cedo", at(21, 5), at(21, 9)),
    ],
)
def test_part_of_day_table(text: str, start: datetime, end: datetime) -> None:
    got = parse_seen(text, NOW, SP)

    assert (got.start, got.end) == (start, end)


@pytest.mark.parametrize("text", ["ONTEM A TARDE", "ontem a tarde", "  Ontem  à  tarde "])
def test_caps_missing_accents_and_spacing_parse_the_same(text: str) -> None:
    got = parse_seen(text, NOW, SP)

    assert (got.start, got.end, got.precision) == (
        at(20, 12),
        at(20, 18),
        TimePrecision.PART_OF_DAY,
    )


def test_keeps_the_reporters_own_words() -> None:
    assert parse_seen("ontem à tarde", NOW, SP).text == "ontem à tarde"


def test_never_ends_after_now() -> None:
    now = at(21, 15)

    got = parse_seen("hoje à tarde", now, SP)

    assert (got.start, got.end) == (at(21, 12), now)


def test_no_text_means_right_now() -> None:
    got = parse_seen(None, NOW, SP)

    assert got.end == NOW
    assert NOW - got.start <= timedelta(minutes=15)


def test_results_are_timezone_aware() -> None:
    got = parse_seen("ontem à tarde", NOW, SP)

    assert got.start.utcoffset() is not None and got.end.utcoffset() is not None


# ── coarsen_for_public ───────────────────────────────────────────────────────


def narrow(start: datetime, end: datetime) -> SeenInterval:
    return SeenInterval(start=start, end=end, precision=TimePrecision.MINUTES, text=None)


def test_emergency_is_published_to_the_hour() -> None:
    got = coarsen_for_public(narrow(at(21, 15, 7), at(21, 15, 9)), RelatoKind.EMERGENCY, SP)

    assert got == PublicSeen(start=at(21, 15), end=at(21, 16), precision=TimePrecision.HOUR)


def test_sighting_is_published_to_the_part_of_day() -> None:
    got = coarsen_for_public(narrow(at(21, 15, 7), at(21, 15, 9)), RelatoKind.SIGHTING, SP)

    assert got == PublicSeen(start=at(21, 12), end=at(21, 18), precision=TimePrecision.PART_OF_DAY)


def test_an_interval_across_parts_of_day_covers_both() -> None:
    got = coarsen_for_public(narrow(at(21, 11, 30), at(21, 13)), RelatoKind.LOST, SP)

    assert (got.start, got.end) == (at(21, 6), at(21, 18))


@pytest.mark.parametrize("kind", list(RelatoKind))
@pytest.mark.parametrize(
    "seen",
    [
        narrow(at(21, 0, 1), at(21, 0, 2)),
        narrow(at(20, 23, 50), at(21, 0, 10)),
        SeenInterval(at(20, 12), at(20, 18), TimePrecision.PART_OF_DAY, "ontem à tarde"),
        SeenInterval(at(19, 0), at(21, 0), TimePrecision.DAY, "anteontem ou ontem"),
    ],
)
def test_public_time_is_never_narrower_than_the_fact(kind: RelatoKind, seen: SeenInterval) -> None:
    got = coarsen_for_public(seen, kind, SP)

    assert got.start <= seen.start and got.end >= seen.end
