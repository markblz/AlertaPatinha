# ADR-0001 — Modular monolith, dockerized, Kubera layout

**Status:** accepted · 2026-10-21

## Context
Small team, one product, owner already operates Kubera (FastAPI + Next.js +
Postgres + Docker Compose) and wants the same shape: backend, frontend and
database as separate containers.

## Decision
- ONE FastAPI backend (`apps/backend`), ONE Next.js PWA (`apps/frontend`), ONE Postgres.
- Modules under `src/<module>/` with a `public.py` surface; boundaries enforced by import-linter: (1) `src` never imports `api`; (2) modules are independent except through `public.py`; (3) a layers contract fixes the direction between modules (architecture.md).
- Docker Compose for dev now; `docker-compose.prod.yml` + Caddy arrive in M1.
- Browser talks only to the web origin; Next proxies `/api/*` to the backend.

## Consequences
- One deploy unit, one transaction boundary, cheap refactors across modules.
- Discipline is mechanical (contracts were probed: illegal imports fail).
- Split a module into its own service only if a trigger fires: 10× scale mismatch, team split, deploy-frequency conflict, SLO divergence.

## Alternatives rejected
- Microservices: network boundaries without a team or scale reason.
- Django (GeoDjango/admin): attractive admin, but no async ORM gains in 6.0/6.1, tasks framework has no worker, and the team baseline is FastAPI ([stack Q1](<../research/research_notes/Stray pet platform research/core_tech_stack.md>)).
