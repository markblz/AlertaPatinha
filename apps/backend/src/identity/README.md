# identity — Pessoas

**Milestone:** M1 (anonymous) → M4 · **Owns schema:** `identity` · **May depend on:** nothing

## Responsibility
Anonymous device sessions, phone verification (WhatsApp OTP), users, trust tiers T0–T4, organizations (ONG, CCZ) with service areas, protetor territories, roles (staff), bans.

## Public surface (planned — `public.py`)
- `get_viewer(session) -> Viewer  # id, tier, roles, territories/service areas`
- `start_anonymous_session(device) -> Session`
- `verify_phone(...)  (M4)`

## Invariant
Reputation (T2) is private and outcome-scored; it is never exposed as a public number.

## Layout when code arrives
`public.py` → `service/` → `repository/` (ORM models, queries) → `domain/` (pure logic).
Add this module's schema to `alembic/env.py` OWNED_SCHEMAS (already listed) and a
layers contract in `.importlinter` with its first layer.
