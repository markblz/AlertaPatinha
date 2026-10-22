# Alerta Patinha

Viu um animal precisando de ajuda? **Relate, acompanhe e ajude perto de você.**

Brazilian civic platform that centralizes emergencies and sightings of stray,
lost and community animals: a photo + a place + a time become a **relato**;
relatos of the same animal are linked into a **caso** with a timeline; a live
map shows where — always saying whether the location is exact or approximate —
and nearby people get specific, time-boxed asks for help.

- Backend: FastAPI modular monolith — `apps/backend/`
- Frontend: Next.js PWA + MapLibre — `apps/frontend/`
- Database: PostgreSQL 18 + PostGIS 3.6 + h3-pg + pgvector — `infra/postgres/`
- Realtime: Centrifugo on Valkey · Object storage: S3 API (SeaweedFS in dev)

## Quick start

```bash
cp .env.example .env      # optional in dev: compose has defaults
make up                   # postgres, valkey, centrifugo, s3, backend, web
make migrate              # alembic upgrade head (extensions + module schemas)
make health               # {"status":"ok","extensions":{...}}
```

| Service | URL |
|---|---|
| Web (map) | <http://localhost:3100> |
| API (Swagger) | <http://localhost:8100/docs> |
| Centrifugo | <http://localhost:8101> (ws: `/connection/websocket`) |
| S3 (SeaweedFS) | <http://localhost:8102> |
| Postgres | `localhost:5440` |

Ports are chosen to run beside the Kubera stack. Override in `.env`.

## Quality gates

```bash
make check     # ruff + mypy --strict + import-linter + pytest (backend, on host via uv)
docker compose exec web pnpm typecheck
```

## Where to read

1. `docs/vision.md` — why, for whom, goals / non-goals / anti-goals
2. `docs/domain/glossary.md` — the vocabulary (relato, caso, bloco, elo…)
3. `docs/architecture.md` — modules, data flows, dependency direction
4. `docs/domain/data-model.md` and `docs/domain/location-privacy.md` — the core
5. `docs/product/behavioral-design.md` — why people will (or won't) use it
6. `docs/roadmap.md` — milestones M0–M6 and exit criteria
7. `docs/adr/` — decisions · `docs/compliance.md` — LGPD, Marco Civil, STF art. 19
8. `docs/research/` — the evidence base behind all of the above
