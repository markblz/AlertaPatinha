# Alerta Patinha — Claude Code instructions

Brazilian civic platform for stray, lost and at-risk animals: people report
(relato) what they see, the platform links reports into cases (caso) over time,
shows them on a live map with explicit location precision, and connects nearby
people who can help. Modular monolith: ONE FastAPI backend, ONE Next.js PWA,
ONE Postgres. Read `docs/architecture.md` and `docs/domain/glossary.md` first.

## Non-negotiable rules

1. **Modular monolith.** One backend process, one frontend app. Module
   boundaries are enforced by `import-linter` (`make imports`) and the
   `public.py` convention, never by network calls.

2. **Postgres is the only source of truth.** Valkey, Centrifugo history, image
   variants in S3, map tiles and caches are derived and must be rebuildable
   from Postgres + quarantined originals.

3. **Schema ownership.** Each module owns exactly one Postgres schema, created
   in that module's first migration and listed in `alembic/env.py`
   `OWNED_SCHEMAS`. Other modules read/write it only through the owner's
   `public.py`. No cross-schema SQL.

4. **Relatos are immutable facts; casos are revisable hypotheses.** A relato
   never lives *inside* a caso. Membership is expressed only by `chain_link`
   rows, and caso history only by `chain_event` rows — both append-only.
   Corrections, retractions, merges and splits are NEW rows. No UPDATE/DELETE
   on those tables (moderation hides via events, it does not erase history).

5. **Location privacy is decided on the server, at write time.**
   - Public geometry (`display_*`) is derived once when the relato is written
     and is stable. Never add fresh random noise per request — averaging
     repeated reads recovers the true point.
   - Exact geometry is never serialized to a viewer whose trust tier may not
     see it. The API layer receives already-masked views from `geo.public`.
   - Every read of exact coordinates writes `geo.location_access_log`.

6. **The system suggests identity; humans confirm.** No code path — heuristic
   or ML — merges casos or confirms a link on its own. Every link stores its
   method, actor and evidence.

7. **Uploaded bytes are never served.** Originals stay in the private
   quarantine bucket. Only re-encoded, metadata-stripped variants are public.
   EXIF GPS/time are kept as private evidence fields, never published.

8. **Bitemporal time.** `valid_time` = when the animal was seen (an interval
   + precision, e.g. "ontem à tarde"); `recorded_at` = server clock at insert.
   Never conflate them; never trust a client clock for `recorded_at`.

9. **Every client write is idempotent.** Client-generated UUID per write
   (the offline outbox retries). Same UUID twice = same result.

10. **Product safety invariants.** No money flows through the platform. No
    public naming, photo or location of an alleged abuser. Contact between
    users goes through a masked relay. WhatsApp only via the official Cloud
    API (never Baileys/Evolution/WPPConnect).

11. **Frontend deps are installed IN the container.** `make web-add PKG=...`,
    never a host `pnpm add` (host glibc vs container musl; the dev server
    never sees host `node_modules`).

12. **Native-ready frontend (ADR-0011).** `core/` is pure TS (no DOM/React/
    Next). `app/(app)/`, `features/`, `platform/` stay static-exportable: no
    Server Actions, `next/headers`, route handlers or dynamic segments.
    Server-rendered share pages live in `app/(public)/`. Enforced by
    `pnpm check:arch` (`make web-typecheck`).

13. **The API contract is generated.** After any endpoint/schema change run
    `make api-contract`; the backend test `test_openapi_contract` fails on a
    stale `apps/frontend/core/api/openapi.json`. Errors use one envelope
    `{detail: {code, message}}`; clients branch on `code`.

## Dependency flow (per module)

```
api/<module>/router  →  src/<module>/public  →  src/<module>/service
                                              →  src/<module>/repository
                                              →  src/<module>/domain
```

Never the reverse. `src/` never imports `api/`. Domain models are not API
schemas: `src/<module>/domain/` and `api/<module>/schemas.py` stay separate.
Module-to-module dependency direction is in `docs/architecture.md`.

## Repository layout

```
AlertaPatinha/
├── apps/
│   ├── backend/            # FastAPI modular monolith (uv, alembic, import-linter)
│   │   ├── api/            # HTTP layer: routers, schemas, deps
│   │   └── src/<module>/   # identity, observations, geo, chains, media,
│   │                       # conversations, alerts, moderation (+ README.md each)
│   └── frontend/           # Next.js PWA: app/(app) · app/(public) · core/ · platform/ · features/
├── infra/                  # postgres image, centrifugo, seaweedfs configs
├── docs/
│   ├── vision.md  architecture.md  roadmap.md  compliance.md
│   ├── domain/             # glossary, data model, location privacy, photo pipeline
│   ├── product/            # behavioral design (participation, trust, abuse)
│   ├── integrations/       # whatsapp intake
│   ├── adr/                # decision records
│   ├── research/           # evidence base (notes + synthesized report)
│   └── llm_explanations/   # post-task explanation files
├── docker-compose.yml  Makefile  .env.example
└── CLAUDE.md
```

## Mentor / engineering preferences

- Decomposition check before any non-trivial change: ask the user's approach
  first (see the user's global CLAUDE.md).
- Core domain logic (link scoring, location masking, fuzzy-time parsing,
  decay, alert waves) is specified in `docs/domain/` and implemented by the
  user first; Claude reviews. Boilerplate is written directly.
- KISS first. DRY with taste. Name the key invariant and the main failure mode.
- Rule of three before extracting shared code. Comments only for non-obvious WHY.

## LLM explanation files

After every completed logical task, write ONE file under
`docs/llm_explanations/` (this overrides the global default of a repo-root
`llm_explanations/`). Naming and template: `docs/llm_explanations/README.md`.

## Things NOT to do

- Don't create modules, packages or services before their milestone
  (`docs/roadmap.md`). `intake` (WhatsApp) and `matching` (re-ID) do not exist yet.
- Don't add a Python dependency "for later" — add it with the code that uses it.
- Don't use MinIO, Redis ≥8, Google Maps, tile.openstreetmap.org in prod,
  arq, fastapi-users or encode/broadcaster (reasons: `docs/adr/`).
- Don't publish client-side to Centrifugo. Clients subscribe; the backend
  publishes after the Postgres commit.
- Don't use Postgres LISTEN/NOTIFY as a fan-out bus (PG18 commit lock).
