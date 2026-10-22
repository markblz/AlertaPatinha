# Roadmap

Each milestone ships something a real person can use in the pilot city. Exit
criteria are observable. 🧠 = core logic the owner implements first (learning
protocol); Claude reviews. Everything else is boilerplate/glue.

Pilot: one city (ideally 2–3 bairros) with 1–2 committed ONGs/protetores, so
the map is never empty where people look. Cold start is local, not national.

## M0 — Fundação ✅ (2026-10-21)

- Research base (`docs/research/`), vision, glossary, architecture, ADRs, compliance, behavioral design, domain specs.
- Dockerized stack: Postgres 18 + PostGIS 3.6 + h3 4.2 + pgvector 0.8, Valkey, Centrifugo 6, SeaweedFS, FastAPI, Next.js PWA with map + precision legend.
- Quality gates: ruff, mypy --strict, import-linter (3 contracts, probed), pytest, tsc.

## M1 — Relatar e ver no mapa

Goal: anyone reports in < 30 s without an account; the map shows it honestly.

**Status:** slice 1 built on `feat/m1-relatar-mapa` (report without photo, map, share page, offline outbox, native-ready frontend — [plan](plans/m1-slice-1.md)). Waiting on 🧠 `geo` policy + `parse_seen`.

- `identity`: anonymous session (device-bound, rate-limited).
- `media`: presigned upload → quarantine → job: decode, EXIF read+strip, face/plate blur (EgoBlur, Apache-2.0 — required before public launch, compliance §6), variants, ThumbHash, PDQ. Add `procrastinate` + `worker` service + `pyvips` here.
- 🧠 `geo`: `classify_privacy`, `display_for`, `view_for` (location-privacy.md) + contract tests.
- 🧠 `observations`: `parse_seen` (fuzzy PT-BR time), create relato (idempotent on `client_id`), map read model (bbox + zoom → aggregates / clustered features).
- Web: 3-step relato flow (foto → local → enviar), map with clustering and time filter, relato page with share link, IndexedDB outbox.
- Ops: `docker-compose.prod.yml`, Caddy, `Dockerfile.prod` (standalone), pgBackRest nightly, Sentry. Protomaps Brazil PMTiles on object storage/CDN.
- **Exit:** median time-to-submit < 30 s on a low-end Android over 3G in a usability test (n ≥ 5); zero exact-coordinate leaks in contract tests; pilot deploy live.

## M2 — Casos e linha do tempo

- 🧠 `chains`: elos + blocos (append-only), `derive_state`, `freshness`, `score_pair`, link suggestion job, merge/unmerge.
- "É o mesmo animal?" review cards; "Visto de novo" flow that adds to an existing caso instead of duplicating.
- Encerramento + **close-the-loop** notification with outcome photo to every contributor.
- **Exit:** ≥ 30% of new relatos in the pilot join an existing caso; every resolved caso notifies its contributors; rebuild-projection test green.

## M3 — Conversa e ajuda por perto

- `conversations`: per-caso chat (persist → publish after commit).
- 🧠 `alerts`: watch areas, waves (start small, widen ×2 to the cap until N accept), "Estou indo" with TTL/check-in and max concurrent claimers, notification budget.
- PWA: Serwist service worker, Web Push (VAPID), install prompt (iOS push needs home-screen install).
- **Exit:** median time from emergência to first "Estou indo" measured and reported; no user receives more than the notification budget.

## M4 — Confiança e moderação

- `identity`: phone verification via WhatsApp OTP (authentication template), T2 promotion (private, outcome-based), T3 vouching + staff review, T4 org verification.
- `geo`: exact-location access by tier/claim + `location_access_log`.
- `moderation`: flags, notice-and-takedown tickets (STF art. 19 regime), explained removals, community rules shown to newcomers, private denúncia → export for authorities.
- Masked contact relay + "sinais secretos" for lost-pet verification; protetor caseload caps.
- **Exit:** takedown SLA met in drills; access log covers 100% of exact reads; scam-report rate tracked.

## M5 — WhatsApp (intake)

- New module `intake`: Cloud API webhooks, STT for voice notes, LLM extraction → draft relato → slot-filling → confirmation → `observations.public.create`. Utility templates for "Ainda está aí?" and outcomes.
- Spec: `docs/integrations/whatsapp-intake.md`. Legal gate: §4.7 data-use review.
- **Exit:** golden-set field accuracy target met; median ≤ 2 follow-up questions per relato; cost per 1,000 relatos within budget.

## M6 — Re-identificação por foto

- New module `matching`: detection/crop, embeddings (permissive license only), pgvector; search = SQL filter (species, space, time) → rank → top 10–20 to a human. Never auto-merge.
- Build a Brazilian SRD evaluation set from confirmed elos before trusting any model.
- Spec: `docs/domain/photo-pipeline.md`.
- **Exit:** measured top-k recall on the local eval set; suggestion precision tracked in production.

## Always-on

- Re-fit v0 parameters (radii, half-lives, link weights) from pilot data every quarter.
- Experiments backlog: `docs/product/behavioral-design.md` §6.
- Lawyer questions: `docs/compliance.md` §7 — answer before M4 (identity) and M5 (WhatsApp).
- Brand: register `alertapatinha` + plural on .com.br/.org.br/.app.br/.com; file INPI (classes 09, 42, likely 45).
