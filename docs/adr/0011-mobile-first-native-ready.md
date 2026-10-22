# ADR-0011 — Mobile-first web, ready for store apps without a fork

**Status:** accepted · 2026-10-22 · amends [ADR-0009](0009-pwa-first.md)

## Context
The owner wants the platform excellent on phones, present on the open web
(shareable, indexable), and quick to ship as Android/iOS apps later.
Evidence: [mobile_native_path](<../research/research_notes/Mobile and native path/mobile_native_path.md>)
(verified 2026-10-22). Key facts: a Trusted Web Activity (TWA) puts the PWA on
Google Play with no code fork; Apple guideline 4.2 rejects "repackaged
websites", so iOS needs a bundled app (Capacitor 8 with a static export of the
app screens), not `server.url`; MapLibre GL JS is ~292 KB + 147 KB worker
gzipped, about a low-end phone's whole JS budget.

## Decision
**Order:** PWA now → Play via TWA (Bubblewrap) → iOS via Capacitor (bundled
static export) when iOS numbers justify it → Expo only for native-grade needs
(background location, offline map packs).

**Rules the codebase follows now** (each enforced where marked ✅):
1. **Two zones** in `apps/frontend/app/`: `(public)/` = server-rendered share pages with Open Graph tags (WhatsApp previews); `(app)/` = screens that must survive `output: "export"`. App zone, `features/`, `platform/`, `core/` use no Server Actions, `next/headers`, route handlers, dynamic segments or `@/server`. ✅ `pnpm check:arch`
2. **All writes go through FastAPI `/api/v1`.** No Server Actions. ✅ (rule 1)
3. **One typed client generated from OpenAPI** (`core/api/`), base URL injected: `""` on the web (Next proxies `/api`), the site URL in a native shell. ✅ `make api-contract` + backend drift test
4. **Bearer or cookie, same token.** Web: HttpOnly cookie. Native: `POST /sessions/anonymous {"delivery":"token"}` → secure storage → `Authorization: Bearer`. WebViews block third-party cookies. ✅ tested
5. **Platform capabilities behind `platform/web/*`** (geolocation, share, outbox storage, ids). A shell swaps the implementation; features don't change.
6. **`core/` is pure TypeScript** — no DOM, React or Next — so it moves to a shared package unchanged. ✅ `pnpm check:arch`
7. **One error envelope** `{detail: {code, message, errors?}}`; clients map `code` to their own copy. ✅ tested
8. **GeoJSON out**: positions are `number[]` (not tuples) so GL JS and MapLibre Native consume API geometry as-is.
9. **Offline outbox** (IndexedDB now; SQLite/MMKV in a shell) with idempotent `client_id`. Background Sync is only an enhancement.
10. **Map off the critical path:** lazy-loaded, prefetched on idle, and the report flow completes with a good GPS fix even if the map never loads.
11. **Client photo re-encode is JPEG** (Safari iOS cannot encode WebP from canvas); the server makes the WebP variants.

**Deferred, with a trigger:** `push_endpoint(kind ∈ webpush|fcm|apns|expo)` lands with M3 alerts; CORS for `capacitor://localhost`/`https://localhost` and `/.well-known/assetlinks.json` + `apple-app-site-association` (served by Caddy as JSON, no redirect) land with the first store build.

## Consequences
- One product, three distribution channels, no rewrite. The main risk is app-zone code quietly using a server-only Next feature; the zone check makes that a build failure instead of a surprise on iOS day.
- The relato detail lives at `/r/[id]` (public zone, SSR). A static-exported shell will need a client route (`/relato?id=`) rendering the same `features/relato/RelatoDetail`.
- **Owner decision pending:** the Android `applicationId` / iOS bundle id must be frozen before the first store upload and should derive from a domain you own (e.g. `br.org.alertapatinha.app`) — register the domain first.
