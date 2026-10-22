# chains — Casos

**Milestone:** M2 · **Owns schema:** `chains` · **May depend on:** observations, geo, identity

## Responsibility
Casos, elos (relato↔caso, suggested→confirmed), blocos (timeline events), state derivation, freshness/decay, link suggestion + review, merge/split, encerramento + close-the-loop.

## Public surface (planned — `public.py`)
- `suggest_links(observation_id)  (job)`
- `confirm_link / reject_link / retract_link (commands)`
- `append_event(chain_id, type, payload, actor)`
- `get_chain(id, viewer) -> ChainView`
- `resolve(chain_id, encerramento, actor)`

## Invariant
chain_link and chain_event are append-only; chain_state is a rebuildable projection; nothing auto-confirms.

## Layout when code arrives
`public.py` → `service/` → `repository/` (ORM models, queries) → `domain/` (pure logic).
Add this module's schema to `alembic/env.py` OWNED_SCHEMAS (already listed) and a
layers contract in `.importlinter` with its first layer.
