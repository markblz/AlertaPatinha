"""Contract helpers (location-privacy.md § Serialization contract, point 4)."""

import json
from collections.abc import Iterator

from src.geo.domain import cells
from src.geo.domain.types import Point

# Keys that must never reach a viewer who is not entitled to them.
PRIVATE_KEYS = {"reporter_id", "recorded_at", "time_text", "true_geom", "lat", "lng", "edtf"}


def coordinate_pairs(payload: object) -> Iterator[tuple[float, float]]:
    if isinstance(payload, dict):
        for value in payload.values():
            yield from coordinate_pairs(value)
    elif isinstance(payload, list):
        if len(payload) == 2 and all(isinstance(v, float) for v in payload):
            yield (payload[0], payload[1])
        else:
            for value in payload:
                yield from coordinate_pairs(value)


def keys(payload: object) -> Iterator[str]:
    if isinstance(payload, dict):
        for k, v in payload.items():
            yield k
            yield from keys(v)
    elif isinstance(payload, list):
        for v in payload:
            yield from keys(v)


def values_of(payload: object, key: str) -> Iterator[object]:
    if isinstance(payload, dict):
        for k, v in payload.items():
            if k == key:
                yield v
            yield from values_of(v, key)
    elif isinstance(payload, list):
        for v in payload:
            yield from values_of(v, key)


def assert_no_finer_than_cell(payload: object, true_point: Point, cell: str) -> None:
    """Every coordinate is a vertex of `cell`; nothing private is present."""
    # GPS accuracy describes the exact fix; next to a cell it only leaks.
    assert all(v is None for v in values_of(payload, "accuracy_m")), "accuracy_m leaked"
    allowed = {(round(p.lng, 6), round(p.lat, 6)) for p in cells.ring_of(cell)}
    pairs = list(coordinate_pairs(payload))
    assert pairs, "expected a geometry in the payload"
    for pair in pairs:
        assert pair in allowed, f"{pair} is not a vertex of {cell}"
    leaked = PRIVATE_KEYS & set(keys(payload))
    assert not leaked, f"private keys in payload: {leaked}"
    text = json.dumps(payload)
    for digits in (5, 6):
        assert f"{true_point.lat:.{digits}f}" not in text
        assert f"{true_point.lng:.{digits}f}" not in text
