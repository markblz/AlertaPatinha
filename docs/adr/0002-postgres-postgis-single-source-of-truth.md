# ADR-0002 — Postgres 18 + PostGIS + h3 + pgvector as the single source of truth

**Status:** accepted · 2026-10-21

## Context
The domain is spatio-temporal (points, intervals, radius queries, grid cells),
later vector similarity (re-ID), with strong consistency needs (immutable
facts, append-only links, idempotent writes).

## Decision
- PostgreSQL **18.6**, PostGIS **3.6.4**, h3-pg **4.2.3** (PGDG), pgvector **0.8.7** — custom image `infra/postgres/Dockerfile` on `postgis/postgis:18-3.6`.
- Extensions created by the Alembic baseline (`CREATE EXTENSION … CASCADE`; `h3_postgis` needs `postgis_raster`). `/api/v1/health/ready` fails if any is missing.
- One schema per module; Alembic autogenerate filtered to `OWNED_SCHEMAS` (the postgis image also creates `tiger`/`topology`, which we never touch).
- Everything else (Valkey, Centrifugo history, S3 variants, tiles) is derived.
- Exact radius queries: `ST_DWithin` on `geography`. H3 for blocking, display cells, aggregation and fan-out keys — never alone for exact distance.

## Consequences
- One backup/restore story (pgBackRest). Jobs live here too (ADR-0005).
- `postgis/postgis` images are **amd64-only**: an ARM host (Graviton, OCI Ampere) needs another base image or a source build.
- h3-pg from PGDG lags upstream (4.2.3 vs 4.5.0) and prints deprecation notices for `h3_lat_lng_to_cell` → use `h3_latlng_to_cell`.
- PG18 volume path is `/var/lib/postgresql` (not `/data`).

## Alternatives rejected
- PG19 / PostGIS 3.7 at launch: not GA / RC only. Revisit PG19 ≥ 19.2 for the LISTEN/NOTIFY commit-lock fix.
- Separate vector DB: extra infra for a feature that is M6 and filters by geo/time first anyway.
