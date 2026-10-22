# alerts — Alertas

**Milestone:** M3 · **Owns schema:** `alerts` · **May depend on:** chains, geo, identity

## Responsibility
Watch areas, alert waves (small ring → widen until N accept), "Estou indo" claims with TTL/check-in, notification budget, Web Push.

## Public surface (planned — `public.py`)
- `dispatch(chain_id)  (job)`
- `claim(chain_id, viewer) -> Claim`
- `set_watch_area(viewer, geom)`

## Invariant
A user never exceeds the notification budget; an expired claim always re-opens the ask.

## Layout when code arrives
`public.py` → `service/` → `repository/` (ORM models, queries) → `domain/` (pure logic).
Add this module's schema to `alembic/env.py` OWNED_SCHEMAS (already listed) and a
layers contract in `.importlinter` with its first layer.
