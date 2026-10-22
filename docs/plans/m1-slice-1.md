# M1 · Slice 1 — relatar sem foto, ver no mapa (branch `feat/m1-relatar-mapa`)

## Built (verified 2026-10-22)

| Piece | Where | Proof |
|---|---|---|
| Actor + device session, cookie **or** Bearer | `identity`, `api/identity` | 6 tests + 2 mutation checks |
| Private zones, append-only access log, render paths that fail closed | `geo` (minus 🧠) | contract tests, DB trigger tests |
| Insert-only relato: bitemporal, masked at write, idempotent `client_id` | `observations` (minus 🧠), migrations 0002–0004 | integration tests, DB trigger tests |
| Map read (public precision, display-geom bbox, whole-hour windows) | `api/observations` | privacy contract tests (3 leak mutations caught) |
| One error envelope; OpenAPI → typed TS client; drift test | `api/errors.py`, `core/api/` | `test_openapi_contract` |
| PWA: map + legend + sheet, 3-step relato flow, offline outbox, share page with WhatsApp preview, icons/manifest | `apps/frontend` | tsc, `check:arch`, prod build, Playwright run on a 412 px phone viewport |

## 🧠 Yours (tests are written and red; nothing else blocks them)

```bash
make test-yours            # 61 unit tests, no database
make test                  # +12 integration tests that go green with your policy
```

1. `src/geo/domain/policy.py` — `classify_privacy`, `display_for`, `can_see_exact`, `view_for`. Spec: `docs/domain/location-privacy.md`. Helpers: `src/geo/domain/cells.py`. Decisions the tests leave to you: the "near home" radius, single-zone display (res-7 or hidden), alert/claim rules beyond the examples.
2. `src/observations/domain/seen.py` — `parse_seen`, `coarsen_for_public`. Spec: `docs/domain/data-model.md § Time`. The web chips send exactly these phrases: `agora há pouco`, `hoje|ontem` + `de madrugada|de manhã|à tarde|à noite`, plus free text ("Outro horário"). Decide: unknown text → `SeenParseError` (the UI asks again) or a wide `approx` interval.

Constraint: pure functions — no I/O, clock or randomness. The suite was checked
to be satisfiable (a throwaway reference passed all 90 tests); it is not in the repo.

Until both exist, `POST /api/v1/relatos` returns 500 and the web outbox keeps
relatos queued on the phone — they send themselves once the policy lands.

## Next slices (proposed order)

2. **Fotos**: presign → quarantine → procrastinate worker (pyvips, EXIF strip, EgoBlur, variants, ThumbHash) → photo step first in the flow; OG image uses the blurred variant.
3. **Abuse controls**: Valkey rate limits (session creation per IP, relatos per session), bbox/scrape limits.
4. **Low zoom**: 🧠 res-6 aggregates with k-suppression (k = 3) instead of `zoom_in`.
5. **Realtime**: outbox job → Centrifugo `map:<res-5 cell>` publish after commit.
6. **Ops**: `docker-compose.prod.yml`, Caddy, `Dockerfile.prod`, pgBackRest, Sentry, PMTiles basemap → pilot deploy.
