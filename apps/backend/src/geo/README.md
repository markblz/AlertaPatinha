# geo — Local

**Milestone:** M1 · **Owns schema:** `geo` · **May depend on:** nothing (callers pass the viewer in)

## Responsibility
Pure location policy: privacy classification, stable display geometry (H3), viewer-tier masking, private zones, `location_access_log`.

## Public surface (planned — `public.py`)
- `classify_privacy(...) -> PrivacyClass`
- `display_for(point, privacy_class, kind) -> Display`
- `view_for(observation, viewer, context) -> LocationView  # the ONLY output path for coordinates`
- `log_exact_access(viewer, observation_id, purpose)`

## Invariant
No response lets a viewer locate a point more precisely than their access allows — alone or combined. Spec: docs/domain/location-privacy.md.

## Layout when code arrives
`public.py` → `service/` → `repository/` (ORM models, queries) → `domain/` (pure logic).
Add this module's schema to `alembic/env.py` OWNED_SCHEMAS (already listed) and a
layers contract in `.importlinter` with its first layer.
