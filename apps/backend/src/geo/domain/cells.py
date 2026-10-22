"""Typed wrapper over h3-py (it ships no type hints). The only h3 import in geo."""

import h3

from src.geo.domain.types import Point, Ring


def cell_of(point: Point, resolution: int) -> str:
    return str(h3.latlng_to_cell(point.lat, point.lng, resolution))


def resolution_of(cell: str) -> int:
    return int(h3.get_resolution(cell))


def ring_of(cell: str) -> Ring:
    return tuple(Point(lat=lat, lng=lng) for lat, lng in h3.cell_to_boundary(cell))


def center_of(cell: str) -> Point:
    lat, lng = h3.cell_to_latlng(cell)
    return Point(lat=lat, lng=lng)
