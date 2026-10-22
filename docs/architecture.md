# Architecture

Modular monolith, dockerized, mirroring Kubera's layout (ADR-0001). One
FastAPI process, one Next.js PWA, one Postgres. Everything else is derived.

## System

```
 Browser / PWA (low-end Android, prepaid data)
   │  HTTPS same-origin                      │ WebSocket (subscribe only)
   ▼                                         ▼
 ┌──────────────┐  /api/* proxy  ┌─────────────────┐  publish (HTTP API)  ┌─────────────┐
 │ web (Next.js)│ ─────────────▶ │ backend FastAPI │ ───────────────────▶ │ centrifugo  │
 │  MapLibre    │                │  api/ + src/    │                      │  (valkey)   │
 └──────────────┘                └───────┬─────────┘                      └─────────────┘
        │ basemap tiles (PMTiles/CDN)    │ SQL (asyncpg)      ▲ jobs (procrastinate, same DB)
        ▼                                ▼                    │
   tiles CDN                     ┌──────────────────────────────┐      presigned PUT/GET
                                 │ Postgres 18                  │   ┌──────────────────────┐
                                 │ PostGIS · h3 · pgvector      │   │ S3: quarantine (priv) │
                                 │ ONE schema per module        │   │     public variants   │
                                 └──────────────────────────────┘   └──────────────────────┘
 Later: WhatsApp Cloud API webhooks → backend `intake` module (M5); `matching` re-ID worker (M6)
```

## Modules (`apps/backend/src/`)

| Module | PT-BR | Owns (schema) | Responsibility | Milestone |
|---|---|---|---|---|
| `identity` | Pessoas | `identity` | Anonymous sessions, phone verification (WhatsApp OTP), users, trust tiers, orgs (ONG/CCZ), roles, bans | M1 (anon) → M4 |
| `geo` | Local | `geo` | **Pure location policy**: privacy classification, stable display geometry (H3), private zones, viewer-tier masking, `location_access_log`, fuzzy place helpers | M1 |
| `media` | Fotos | `media` | Presigned uploads, quarantine, processing pipeline, variants, perceptual hashes | M1 |
| `observations` | Relatos | `observations` | Create/read immutable relatos, fuzzy time → interval, attributes, idempotency, map read model | M1 |
| `chains` | Casos | `chains` | Casos, elos, blocos, state machine, decay, link suggestion + review, merges/splits, resolution | M2 |
| `conversations` | Conversa | `conversations` | Per-caso chat persistence + realtime publish | M3 |
| `alerts` | Alertas | `alerts` | Watch areas, alert waves, "Estou indo" claims with expiry, Web Push | M3 |
| `moderation` | Moderação | `moderation` | Flags, takedown tickets, decisions, denúncias routing, hiding via events | M4 |

Not yet created (YAGNI until their milestone): `intake` (WhatsApp, M5),
`matching` (photo re-ID, M6).

## Dependency direction between modules

```
moderation
   │
alerts   conversations          (siblings: independent)
   │         │
   └──── chains
           │
      observations
           │
  geo    media    identity       (siblings: independent, depend on nothing)
```

A module may import only modules *below* it, and only via their `public.py`.
Enforced by two import-linter contracts (`apps/backend/.importlinter`):
independence-except-public + a layers contract for this direction.

`geo` stays dependency-free on purpose: masking is a pure function of
(true location, privacy class, viewer capabilities). Callers pass the viewer
in; `geo` never asks `identity`. That keeps the most safety-critical code
trivially unit-testable.

## Key flows

**1. Relatar (M1)**
```
client: compress photo → POST /api/v1/media/uploads → PUT presigned (quarantine)
client: POST /api/v1/relatos {client_id, kind, species, photo_ids, location{lat,lng,accuracy_m,source}, seen{text|interval}, attrs}
backend (one transaction):
  geo.public.classify_and_mask(point, reporter, private_zones) → privacy_class, display_mode, display_cell/geom
  observations: insert relato (idempotent on client_id)
  enqueue jobs (same tx): media.process(photo_ids), chains.suggest_links(relato), alerts.dispatch(if emergency), realtime.publish(map cell)
→ 201 {relato_id, share_url, suggested_casos[]}
```
**2. Map read (M1)** — `GET /api/v1/map?bbox&zoom&since`: zoomed out → H3
aggregate counts (res 6/7); city zoom → masked features (server clustering);
street zoom → individual features. Every feature carries `display_mode`.
Live updates: subscribe `map:<h3 res-5 cell>` for visible cells.

**3. Linking (M2)** — job: block (species, open states, H3 k-ring, valid-time
overlap) → exact `ST_DWithin` → score → write `suggested` elos → "É o mesmo
animal?" cards → human confirm/reject → `chain_event`. Never auto-confirm.

**4. Help nearby (M3)** — emergency → watch areas intersecting → wave 1
(radius r, target k accepts) → wait → widen ×2 until k accepts or cap →
claims expire and re-open. Notification budget per user.

**5. Conversa (M3)** — POST message → persist → enqueue publish `caso:<id>`
→ Centrifugo → subscribers. Clients never publish directly.

## Cross-cutting decisions

| Concern | Decision | ADR |
|---|---|---|
| Source of truth | Postgres only; realtime/tiles/variants derived | 0002 |
| Identity of animals | Observation-first, chains as hypotheses, append-only, bitemporal | 0003 |
| Location privacy | Server-side, write-time, stable H3 masking, tiered access, audit log | 0004 |
| Realtime | Centrifugo + Valkey; publish after commit via job (transactional outbox) | 0005 |
| Jobs | procrastinate (Postgres-backed, enqueue in the same transaction) | 0005 |
| Maps | MapLibre + self-hosted Protomaps PMTiles; OpenFreeMap dev only | 0006 |
| Storage | S3 API; SeaweedFS dev; no MinIO; originals never served | 0007 |
| Identity of people | Anonymous-first, WhatsApp OTP, trust tiers, in-house | 0008 |
| Client | PWA first; native only if iOS push becomes the bottleneck | 0009 |
| Matching | System suggests, humans confirm — heuristics and ML alike | 0010 |

## API style

Command-oriented endpoints for consequential operations, plain reads for
the rest (applied from the owner's usual default):
`POST /casos/{id}/elos/{elo_id}:confirm`, `POST /casos/{id}:resolve`,
`POST /alertas/{id}/claims` — never a generic `PATCH /chain_links/{id}`.
Every write accepts `client_id` (UUID) for idempotency.

## Scaling path (from research, thresholds are judgment calls)

- **MVP (≤50k MAU):** single VM in São Paulo, this compose stack + Caddy, PMTiles on CDN, nightly pgBackRest.
- **~50k–300k MAU:** DB on its own VM/managed PG in BR + replica; 2× backend/web; Martin vector tiles; H3 `watch_cells` fan-out; self-hosted Photon/Nominatim.
- **~1M MAU:** Centrifugo cluster on dedicated Valkey; read replicas for map; media/tiles fully on CDN; consider PG19 for NOTIFY fix; Expo app only if iOS push opt-in is the bottleneck.
- Kubernetes: not before ~1M MAU and >1 ops engineer.
