# observations — Relatos

**Milestone:** M1 · **Owns schema:** `observations` · **May depend on:** geo, media, identity

## Responsibility
Create and read immutable relatos (avistamento, emergência, perdido, achado), fuzzy PT-BR time → interval, attributes, idempotency, map read model.

## Public surface (planned — `public.py`)
- `create_observation(cmd, viewer) -> ObservationId  # idempotent on client_id`
- `get_observation(id, viewer) -> ObservationView`
- `map_features(bbox, zoom, window, viewer) -> FeatureCollection`

## Invariant
A relato is never updated after insert; corrections are events. Spec: docs/domain/data-model.md.

## Layout when code arrives
`public.py` → `service/` → `repository/` (ORM models, queries) → `domain/` (pure logic).
Add this module's schema to `alembic/env.py` OWNED_SCHEMAS (already listed) and a
layers contract in `.importlinter` with its first layer.
