# ADR-0005 — Realtime via Centrifugo + Valkey; jobs via procrastinate

**Status:** accepted · 2026-10-21

## Context
Per-caso chat and live map updates on flaky mobile networks; multiple backend
processes later. Background work: image processing, link suggestion, alert
waves, realtime publishes, WhatsApp webhooks.

## Decision
- **Centrifugo 6.10.1** (Apache-2.0) on **Valkey 9.1** (BSD-3). Namespaces `map:` (H3 res-5 cells) and `caso:`; history + `force_recovery` for reconnects. Clients subscribe only; **the backend publishes** via HTTP API.
- **procrastinate** (Postgres-backed) for jobs: enqueue in the **same transaction** as the domain write (transactional outbox). Realtime publishes are jobs → nothing is announced that was not committed.
- Added with the first job in M1 (dependency + `worker` service), not before.

## Consequences
- No broker besides Postgres for jobs; one less moving part.
- Centrifugo handles presence, recovery, SSE fallback, scale-out (cluster on Valkey at ~1M MAU).
- If the PG-backed queue contends at scale, move notification fan-out to Taskiq/Dramatiq on Valkey.

## Alternatives rejected
- FastAPI WebSockets + `encode/broadcaster`: archived; single-process.
- Postgres LISTEN/NOTIFY as bus: global commit lock on PG18 (fix only in PG19).
- Redis ≥ 8: RSALv2/SSPL/AGPL. arq: maintenance-only. Celery: sync-first, extra broker.
