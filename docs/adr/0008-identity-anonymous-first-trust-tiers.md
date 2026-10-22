# ADR-0008 — Anonymous-first identity, WhatsApp OTP, trust tiers (in-house)

**Status:** accepted · 2026-10-21

## Context
Any login before the first relato kills participation. But accountability is
needed for exact locations, contact, claims, and Sybil resistance (only a
central identity authority stops Sybils — Douceur). Phone verification is the
practical Brazilian anchor; WhatsApp authentication messages cost ~US$0.0068
vs ~US$0.06/segment for SMS.

## Decision
- T0: device-bound anonymous session; may file relatos (rate-limited, lower-trust queue, IP/timestamp logged for Marco Civil requests).
- T1: phone verified via **WhatsApp OTP** (authentication template), SMS fallback.
- T2: private, outcome-scored reputation (never a public score).
- T3: protetor/mantenedor — 2 T3 vouches + staff review; has a territory.
- T4: organization — ONG (CNPJ) or CCZ (gov e-mail domain); has a service area.
- Staff/moderação is a role, not a tier.
- In-house implementation (opaque sessions), no external IdP for now.

## Consequences
- Progressive identity: ask for a phone only when the action needs it (claim, contact, exact location).
- Phone-only T1 keeps people without documents included.

## Alternatives rejected
fastapi-users (maintenance mode), Keycloak/authentik (heavy for MVP),
Zitadel (AGPL since 2025), Better Auth (TS-only, backend is Python).
