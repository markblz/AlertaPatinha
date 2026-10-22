# identity — Pessoas

**Milestone:** M1 (anonymous) → M4 · **Owns schema:** `identity` · **May depend on:** nothing

## Responsibility
Anonymous device sessions, phone verification (WhatsApp OTP), users, trust tiers T0–T4, organizations (ONG, CCZ) with service areas, protetor territories, roles (staff), bans.

## Public surface (`public.py`)
- `start_anonymous_session(session) -> IssuedSession` — one actor + one device token (only its SHA-256 is stored)
- `resolve_token(session, token) -> Principal | None` — same token as HttpOnly cookie (web) or Bearer (native)
- Planned: `verify_phone(...)` (M4, raises the tier on the SAME actor)

## Invariant
Reputation (T2) is private and outcome-scored; it is never exposed as a public number.

## Layout
`public.py` → `service.py` → `repository/` (ORM models, queries) → `domain/` (pure logic). Enforced by the `modules-are-layered` import contract.
