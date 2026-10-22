# ADR-0004 — Server-side, write-time, stable location masking with tiered access

**Status:** accepted · 2026-10-21

## Context
The map must say whether a location is exact or approximate. Location data
can hurt animals (theft, colony poisoning) and people (reporter's home,
live position). Documented leaks come from combination: averaging fresh noise,
reporter trails, exact timestamps (iNaturalist), EXIF.

## Decision
- `display_mode` (exact/approximate/hidden) + `display_cell` (H3) + `display_geom` computed **once at write time** by `geo` and stored. No per-request noise.
- Public default by type: res-9 (emergência, perdido, avistamento), res-8 (comunitário), res-7 or hidden (colônia, zonas privadas, sensitive animals). **No public exact pins, emergencies included.**
- Exact access only for: reporter (own), alerted/claiming helpers while active, T3 in territory, T4 in service area, staff with purpose. Each exact read → `geo.location_access_log`.
- `geo.public.view_for()` is the only output path for coordinates; contract tests cover REST, GeoJSON and realtime payloads.

## Consequences
- Rescue speed for emergencies relies on alerting (helpers get exact), not on a public pin.
- Masking code is pure and dependency-free → easy to test exhaustively.
- Parameters (cells, delays) are v0 and must be re-fit with pilot data.

## Alternatives rejected
Per-request noise (averaging leak), geo-indistinguishability (~289 m mean
shift kills utility), donut masking (density varies), public exact emergency
pins (reporter's live location). Details: `docs/domain/location-privacy.md`.
