# conversations — Conversa

**Milestone:** M3 · **Owns schema:** `conversations` · **May depend on:** chains, identity

## Responsibility
Per-caso chat: persist messages, publish to Centrifugo `caso:<id>` after commit, moderation hooks.

## Public surface (planned — `public.py`)
- `post_message(chain_id, viewer, text, client_id) -> MessageId`
- `list_messages(chain_id, viewer, cursor)`

## Invariant
Clients never publish to Centrifugo; the backend publishes committed messages only.

## Layout when code arrives
`public.py` → `service/` → `repository/` (ORM models, queries) → `domain/` (pure logic).
Add this module's schema to `alembic/env.py` OWNED_SCHEMAS (already listed) and a
layers contract in `.importlinter` with its first layer.
