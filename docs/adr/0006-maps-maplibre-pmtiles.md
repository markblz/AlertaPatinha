# ADR-0006 — Maps: MapLibre GL JS + self-hosted Protomaps PMTiles

**Status:** accepted · 2026-10-21

## Context
The map is the main view, national scale, many views per user, low-end
Android. Google Maps JS would cost ~US$16k/month at 10M loads. OSM's public
tile servers forbid heavy use; Stadia/MapTiler free tiers are non-commercial.

## Decision
- **MapLibre GL JS 6.x** (ESM-only, requires WebGL2) via `features/map/MapView.tsx`.
- Basemap: **Protomaps PMTiles Brazil extract** on object storage/CDN in prod (M1). Dev uses **OpenFreeMap** (`NEXT_PUBLIC_MAP_STYLE_URL`), no SLA.
- Own data: GeoJSON API with server-side clustering / H3 aggregates first; **Martin** vector tiles when density makes GeoJSON heavy (Phase 1).
- Geocoding: Photon/Nominatim self-hosted later; no per-call commercial API.
- OSM/ODbL attribution visible on every map view.

## Consequences
- No per-view fees; tiles cached at the edge.
- Risk: WebGL2 absence on very old devices → needs a list-view fallback (M1).
- Brazil extract size not yet measured (`pmtiles extract --dry-run`).

## Alternatives rejected
Leaflet (raster-first), Google Maps (cost), tile.openstreetmap.org (policy),
pg_tileserv (no release since Feb 2024).
