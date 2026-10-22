# moderation — Moderação

**Milestone:** M4 · **Owns schema:** `moderation` · **May depend on:** alerts, conversations, chains, observations, geo, media, identity

## Responsibility
Flags, notice-and-takedown tickets (STF art. 19 regime), decisions with explanations, private denúncias routed to authorities, hiding content via owners' events.

## Public surface (planned — `public.py`)
- `flag(target, reason, viewer)`
- `decide(ticket_id, decision, staff)`
- `file_denuncia(...)  # never public, never on the map`

## Invariant
Moderation hides via events; it never deletes history. Alleged abusers are never named or located publicly.

## Layout when code arrives
`public.py` → `service/` → `repository/` (ORM models, queries) → `domain/` (pure logic).
Add this module's schema to `alembic/env.py` OWNED_SCHEMAS (already listed) and a
layers contract in `.importlinter` with its first layer.
