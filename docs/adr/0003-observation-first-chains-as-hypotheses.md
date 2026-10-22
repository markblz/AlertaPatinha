# ADR-0003 — Observation-first model: relatos are facts, casos are hypotheses

**Status:** accepted · 2026-10-21

## Context
Users want to "generate chains and complement them with temporal data
blocks". Identity of street animals is uncertain; wrong merges are the most
damaging error (a guardian told their dog was found). Wildbook (wildlife
re-ID) solved this shape: a sighting is a first-class record, an individual
is a revisable hypothesis, and matching "assists but never decides".

## Decision
- `observation` (relato) is immutable. Corrections are events.
- `chain` (caso) state is derived from append-only `chain_link` (elo) and `chain_event` (bloco) rows; `chain_state` is a rebuildable projection.
- Bitemporal: `valid_time tstzrange` + `time_precision` + `time_text` (when seen) vs `recorded_at` (server clock).
- Every client-originated write carries `client_id` (UUID) for idempotency.

## Consequences
- Merges/splits are reversible; history and moderation audit are free.
- Slightly more complex reads (projection) — mitigated by `chain_state`.
- Test of the model: replaying links/events rebuilds identical projections.

## Alternatives rejected
- `observation.chain_id` updated in place: destructive merges, no provenance.
- Point timestamps: lie about precision ("ontem à tarde" ≠ 15:00) and break time-window filtering.

Spec: `docs/domain/data-model.md`.
