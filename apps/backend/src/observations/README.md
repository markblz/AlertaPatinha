# observations — Relatos

**Milestone:** M1 · **Owns schema:** `observations` · **May depend on:** geo, media, identity

## Responsibility
Create and read immutable relatos (avistamento, emergência, perdido, achado), fuzzy PT-BR time → interval, attributes, idempotency, map read model.

## Public surface (`public.py`)
- `create_relato(session, NewRelato, reporter_id, now, tz) -> CreateResult` — idempotent on `client_id`; replays return the original
- `get_relato(session, id, viewer, now, tz) -> RelatoView` — location via `geo.render_*` only
- `map_page(session, bbox, since, until, tz) -> MapPage` — public precision for everyone, whole-hour windows, capped
- 🧠 `domain/seen.py` (`parse_seen`, `coarsen_for_public`) — owner implements; tests `tests/observations/test_seen.py`

## Invariant
A relato is never updated after insert; corrections are events. Spec: docs/domain/data-model.md.

## Layout
`public.py` → `service.py` → `repository/` (ORM models, queries) → `domain/` (pure logic). Enforced by the `modules-are-layered` import contract.
