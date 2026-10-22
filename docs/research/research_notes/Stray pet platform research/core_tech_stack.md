# Core Technology Stack: Brazilian Stray/Lost-Pet Civic Platform (verified 2026-10-21)

Method: version numbers and repo status were pulled live on 2026-10-21 from the GitHub releases/tags API, PyPI JSON and the npm registry. AWS prices come from AWS's own on-demand price data files. Policies and pricing come from official pages fetched the same day. Anything not verified is under "Gaps". The baseline under evaluation is the team's existing stack: FastAPI + SQLAlchemy 2 async + Alembic + Postgres 18 + Next.js 16 (React 19) + pnpm + uv + Docker Compose + Caddy, with module boundaries enforced by import-linter.

---

## Q1. Backend framework: keep FastAPI, or move to Django (GeoDjango + DRF/Ninja + Channels), NestJS or Go?

### Takeaway
Keep FastAPI + SQLAlchemy async + GeoAlchemy2. I found no evidence that justifies a framework switch. Django's real advantages are the built-in admin and GeoDjango. Its weak spots for this app are the ones that matter here: the async ORM, a tasks framework that ships with no production worker, and Channels' slow release cadence. Build moderation as a Next.js back-office, or bolt on sqladmin for internal CRUD. Don't use the admin as the reason to switch frameworks.

### Cited Findings
- FastAPI is still pre-1.0. The latest release is **0.159.0 (2026-10-21)** — [GitHub releases](https://github.com/fastapi/fastapi/releases), [PyPI](https://pypi.org/project/fastapi/)
- The SQLAlchemy **2.1** series is current: **2.1.6 released 2026-10-21** — [SQLAlchemy releases](https://github.com/sqlalchemy/sqlalchemy/releases), [PyPI](https://pypi.org/project/SQLAlchemy/). **GeoAlchemy2 0.20.0** (2026-05-12) — [GeoAlchemy2 releases](https://github.com/geoalchemy/geoalchemy2/releases). **Alembic 1.20.0** (2026-09-11) — [PyPI](https://pypi.org/project/alembic/)
- Other current Python pieces: asyncpg 0.32.0 (2026-10-06), psycopg 3.3.6 (2026-09-18), Pydantic 2.14.1 (2026-10-11), uvicorn 0.54.0 (2026-09-25), granian 2.8.5 (2026-10-20), import-linter 2.15 (2026-09-04) — [PyPI asyncpg](https://pypi.org/project/asyncpg/), [PyPI psycopg](https://pypi.org/project/psycopg/), [PyPI pydantic](https://pypi.org/project/pydantic/), [PyPI uvicorn](https://pypi.org/project/uvicorn/), [PyPI granian](https://pypi.org/project/granian/), [PyPI import-linter](https://pypi.org/project/import-linter/)
- **Django 6.0** was released on 2025-12-03. It added a built-in Tasks framework, but "Django handles task creation and queuing, but does not provide a worker mechanism to run tasks", and "the two built-in backends ... are primarily intended for development and testing". It also added native CSP support and template partials, and supports Python 3.12–3.14. The only async addition was `AsyncPaginator`/`AsyncPage` — [Django 6.0 release notes](https://docs.djangoproject.com/en/6.0/releases/6.0/)
- **Django 6.1** was released on 2026-08-05 and supports PostgreSQL 15+. Its notes list **no async ORM improvements**. GeoDjango dropped PostGIS 3.1, and new features include `QuerySet.fetch_mode()` and DB-level `on_delete`. Under DEP 20, Django moves to calendar versioning: the releases previously planned as 7.0 and 7.1 become "Django 2028/2029". 6.1 mainstream support ends April 2027 and extended support ends December 2027 — [Django 6.1 release notes](https://docs.djangoproject.com/en/6.1/releases/6.1/). The latest tags are 6.1.2 and 6.0.9 — [django/django tags](https://github.com/django/django/tags)
- Django ecosystem cadence: DRF 3.18.3 (2026-10-06), django-ninja 1.7.1 (2026-09-19), **channels 4.3.2 (last release 2025-11-20)**, **channels-redis 4.3.0 (last release 2025-07-22)**, django-unfold 0.110.0 (2026-10-13) — [PyPI djangorestframework](https://pypi.org/project/djangorestframework/), [PyPI django-ninja](https://pypi.org/project/django-ninja/), [PyPI channels](https://pypi.org/project/channels/), [PyPI channels-redis](https://pypi.org/project/channels-redis/), [PyPI django-unfold](https://pypi.org/project/django-unfold/)
- Admin options on FastAPI/Starlette: **sqladmin 0.32.0** (2026-09-20) and **starlette-admin 1.0.2** (2026-10-03) — [PyPI sqladmin](https://pypi.org/project/sqladmin/), [PyPI starlette-admin](https://pypi.org/project/starlette-admin/)
- OpenAPI→TypeScript generators: **@hey-api/openapi-ts 0.99.0** (still 0.x), **openapi-typescript 7.13.0**, **orval 8.44.0** — [npm @hey-api/openapi-ts](https://www.npmjs.com/package/@hey-api/openapi-ts), [npm openapi-typescript](https://www.npmjs.com/package/openapi-typescript), [npm orval](https://www.npmjs.com/package/orval)
- FastAPI's own WebSocket docs warn that the in-memory connection manager "will only work while the process is running, and will only work with a single process". The docs point to `encode/broadcaster` for multi-process use — [FastAPI WebSockets docs](https://fastapi.tiangolo.com/advanced/websockets/). **encode/broadcaster is archived** (archived=true, last push 2025-04-09) — [encode/broadcaster](https://github.com/encode/broadcaster)
- **fastapi-users is in maintenance mode**: "no new features will be added". The latest release is v15.0.5 (2026-03-27) — [fastapi-users README](https://github.com/fastapi-users/fastapi-users)

### Inferences
- Reusing the baseline wins on team velocity. The team already runs FastAPI, SQLAlchemy async, Alembic, uv and import-linter in production. GeoAlchemy2 gives typed PostGIS columns and functions, so GeoDjango's ORM spatial lookups are not a differentiator worth a rewrite of team habits.
- Django admin is the strongest pro-Django argument. But moderation here is map-centric and photo-centric: chain timelines, abuse reports, approximate-vs-exact location review. That needs a custom UI regardless. Build a `/moderation` area in the Next.js app against the same API. Use sqladmin only for internal CRUD on reference tables.
- Watch the FastAPI WebSocket trap. The official guidance leads to an archived library. That supports keeping realtime out of FastAPI processes and putting it in Centrifugo (see Q4).
- NestJS would unify the language (TypeScript end-to-end), and Go would give raw throughput. Neither addresses a bottleneck we've identified. The hot path that benefits from Go, the realtime fan-out, is covered by Centrifugo, which is written in Go. Switching splits the team's expertise and discards the existing modular-monolith tooling.
- Key invariant: one Python backend owns every write and every authorization decision. Realtime, tiles and workers are downstream readers or executors.
- Main failure mode: FastAPI is "assemble your own batteries", so auth, rate limiting, admin and jobs each need a deliberate choice. Module boundaries enforced by import-linter are the mitigation.
- Decide SQLAlchemy 2.0 vs 2.1 up front. 2.1 is now current. Verify GeoAlchemy2 0.20 compatibility before upgrading the template.

### Gaps
- I found no credible 2026 benchmark comparing FastAPI, Django, NestJS and Go for geo-heavy CRUD.
- I did not verify GeoAlchemy2 0.20.0 compatibility with SQLAlchemy 2.1.x (release notes not fetched).
- NestJS/Prisma/TypeORM PostGIS ergonomics were not researched in depth.

---

## Q2. Database: Postgres 18 + PostGIS 3.6 + h3-pg + pgvector; partitioning; PT-BR full-text search; Docker images

### Takeaway
Use **PostgreSQL 18 (latest minor 18.6) + PostGIS 3.6.4 + pgvector 0.8.7 + h3-pg**. Base the image on `postgis/postgis:18-3.6` and extend it with PGDG packages. Do not adopt PostgreSQL 19 (GA planned 2026-11-19) or PostGIS 3.7 (still RC) at launch. Two Docker gotchas matter: the official postgis image is **amd64-only**, and the **PG18 image changed its volume path**.

### Cited Findings
- PostgreSQL 18's latest minor tag is **REL_18_6**. PG19 is at **REL_19_RC1 (tagged 2026-10-12)** — [postgres/postgres tags](https://github.com/postgres/postgres/tags). The RC1 announcement gives the **planned PG19 GA as 2026-11-19**, with an RC2 shipping alongside the 2026-11-12 update release — [PostgreSQL 19 RC1 news](https://www.postgresql.org/about/news/postgresql-19-rc-1-released-3409/)
- **PostGIS 3.6.0** was released in September 2025. At release it required "PostgreSQL 12 - 18beta3"; 3.6.1 states "PostgreSQL 12 - 18" — [PostGIS 3.6.0](https://www.postgis.net/2025/09/PostGIS-3.6.0/), [postgis.net news](https://postgis.net/news). The latest 3.6.x tag is **3.6.4**, and **3.7 is at 3.7.0rc3** (not GA) — [postgis/postgis tags](https://github.com/postgis/postgis/tags)
- Aiven reports PostGIS 3.6.4 fully supported on PG18. It warns that a **breaking change in 3.6 requires a manual migration step for PostGIS topology columns** — [Aiven changelog](https://aiven.io/changelog/7c487a7d-a0a7-4b62-a92e-de3a4fedd88d)
- The official `postgis/postgis` image: the `18-3.6` Dockerfile is `FROM docker.io/postgres:18-trixie` with `POSTGIS_VERSION=3.6.4+dfsg-2.pgdg13+1`, and the README says "Supported architecture: `amd64` (x86-64)" — [docker-postgis repo](https://github.com/postgis/docker-postgis)
- The official `postgres:18` image changed paths: "in 18+, PGDATA has changed ... and the VOLUME has moved from /var/lib/postgresql/data to /var/lib/postgresql" (`PGDATA=/var/lib/postgresql/18/docker`) — [docker-library/postgres 18/trixie Dockerfile](https://github.com/docker-library/postgres/blob/master/18/trixie/Dockerfile)
- **pgvector v0.8.7** was tagged 2026-10-01 — [pgvector tags](https://github.com/pgvector/pgvector/tags). PG18 support arrived in 0.8.1 — [EDB pgvector release notes](https://www.enterprisedb.com/docs/pg_extensions/pgvector/rel_notes/). Indexed `vector` goes up to **2,000 dims** and `halfvec` up to **4,000 dims**. **Iterative index scans** (since 0.8.0) fix the "filtering applied after the index is scanned" problem: with the default `hnsw.ef_search=40` and a filter matching 10% of rows, only about 4 rows come back unless iterative scan is enabled — [pgvector README](https://github.com/pgvector/pgvector)
- PGDG apt carries **postgresql-18-pgvector 0.8.7** — [PGDG pool pgvector](https://apt.postgresql.org/pub/repos/apt/pool/main/p/pgvector/)
- **h3-pg has moved**: `zachasme/h3-pg` is archived (2025-12-30), and the active repo is **`postgis/h3-pg`, latest v4.5.0 (2026-06-08)**, Apache-2.0 — [postgis/h3-pg](https://github.com/postgis/h3-pg), [zachasme/h3-pg (archived)](https://github.com/zachasme/h3-pg). The **PGDG package for PG18 on Debian trixie is postgresql-18-h3 4.2.3** (`pgdg13+2`), behind upstream — [PGDG pool h3-pg](https://apt.postgresql.org/pub/repos/apt/pool/main/h/h3-pg/). Python `h3` is 4.5.0 — [PyPI h3](https://pypi.org/project/h3/)
- The LISTEN/NOTIFY scalability fix, commit `282b1cde` "Optimize LISTEN/NOTIFY via shared channel map and direct advancement" (2026-01-15), is in the PG19 line (ahead of REL_19_RC1) and **not in PG18** — [postgres commit 282b1cde](https://github.com/postgres/postgres/commit/282b1cde9dedf456ecf02eb27caf086023a7bb71)

### Inferences
- Compose image recipe (boilerplate): `FROM postgis/postgis:18-3.6`, then `apt-get install postgresql-18-pgvector postgresql-18-h3`, then `CREATE EXTENSION postgis, vector, h3, h3_postgis, unaccent, pg_trgm`. Mount the volume at `/var/lib/postgresql`, not `/data`. The new path silently breaks copy-pasted compose files from PG≤17, which then start from an empty cluster.
- **ARM pitfall**: the official postgis image is amd64-only, while AWS Graviton (about 20% cheaper per the price data in Q10) and OCI Ampere A1 (Always Free) are ARM. Either build your own multi-arch image from `postgres:18-trixie` plus the PGDG `postgresql-18-postgis-3` package, or stay on x86.
- h3-pg version skew: PGDG gives 4.2.3 and upstream is 4.5.0. Pin the PGDG version. Nothing in the use case (cell lookup, grid disk, polygon-to-cells) obviously needs 4.5-only features, but check the changelog.
- Partitioning: use native declarative RANGE partitioning on `observed_at` (monthly) for `sightings` and `chain_blocks`. Note that partitioned tables require the partition key in every PK/unique constraint, so use `(id, observed_at)` PKs or a UUIDv7 id with the time component. PG18 ships a native `uuidv7()` function; verify in the PG18 release notes. Automate with pg_partman or a scheduled job. Do this from day 1. Retrofitting partitioning onto a large hot table is painful.
- PT-BR full-text search: create a custom text search configuration (`portuguese` stemmer + `unaccent` dictionary) and a generated `tsvector` column with GIN, plus `pg_trgm` for fuzzy pet names and street names. Postgres FTS is good enough until search becomes a product feature in its own right.
- Do not take PG19 at GA. The NOTIFY fix is attractive, but wait for 19.1/19.2 and PostGIS/pgvector/h3 packages built for 19.
- Key invariant: exact coordinates live in a column only the backend can read. Approximate geometry is derived (snapped or jittered) at write time and is the only geometry any public tile, GeoJSON or API endpoint ever serializes.

### Gaps
- The current pg_partman version and PG18 compatibility were not checked.
- I did not verify which h3-pg features differ between 4.2.3 and 4.5.0.
- The PG18 `uuidv7()` built-in was not re-verified this session.

---

## Q3. Maps: client library, basemap tiles, serving our own data, geocoding

### Takeaway
Use **MapLibre GL JS** (now v6, WebGL2-only, ESM-only) with a **self-hosted Protomaps PMTiles Brazil extract on object storage behind a CDN**. Use OpenFreeMap as a zero-cost bootstrap or fallback. Never use `tile.openstreetmap.org` for production. For our own data, start with a **bbox GeoJSON API with server-side clustering** and add **Martin** (function sources → MVT) when density demands it. Geocoding: Photon (forward/autocomplete) plus Nominatim (reverse), self-hosted. Google Maps costs roughly US$9k–16k per month at 3–10M loads.

### Cited Findings
- **MapLibre GL JS 6.15.0** (2026-10-18). **v6.0.0 (2026-07-22)** is a breaking release: "Switch to an ESM-only distribution ... UMD bundles ... are no longer published". "**WebGL (v1) support has been removed; WebGL2 is now required**". The TypeScript target moves to ES2022, and `GeoJSONSource.setData` loses its `waitForCompletion` parameter — [MapLibre v6.0.0 release](https://github.com/maplibre/maplibre-gl-js/releases/tag/v6.0.0), [npm maplibre-gl](https://www.npmjs.com/package/maplibre-gl). react-map-gl 8.1.3 — [npm react-map-gl](https://www.npmjs.com/package/react-map-gl)
- **OSM tile policy**: "capacity is limited". "Commercial services, or those that seek donations, should be especially aware that access may be withdrawn at any point". "Availability is best-effort: there is no SLA". Offline/prefetch is "not permitted on tile.openstreetmap.org". Apps need a unique User-Agent, a valid Referer, and visible attribution — [OSMF Tile Usage Policy](https://operations.osmfoundation.org/policies/tiles/)
- **Protomaps**: daily builds, ODbL, zooms 0–15. "A full planet file is roughly 120 gigabytes", and "each additional zoom level roughly doubles the file size" (use `pmtiles extract --maxzoom`) — [Protomaps downloads](https://docs.protomaps.com/basemaps/downloads). The actual **2026-10-21 planet build is 139,052,567,898 bytes (~139 GB), basemap version 4.15.2** — [Protomaps build metadata](https://build-metadata.protomaps.dev/builds.json). go-pmtiles CLI v1.31.2 — [go-pmtiles releases](https://github.com/protomaps/go-pmtiles/releases). pmtiles JS 4.5.0 — [npm pmtiles](https://www.npmjs.com/package/pmtiles)
- The Geofabrik Brazil OSM extract is **2,096,862,892 bytes (~2.1 GB), last modified 2026-10-20** — [Geofabrik Brazil](https://download.geofabrik.de/south-america/brazil.html)
- **OpenFreeMap**: free with "no limits on the number of map views or requests", "no registration ... no API keys", commercial use allowed, self-hostable, donation-funded. "At the moment, I don't offer SLA guarantees" — [OpenFreeMap](https://openfreemap.org/)
- **Stadia Maps**: the Free tier gives 200,000 credits per month but "Commercial use not allowed". Starter is $20/mo (1M credits), Standard $80/mo (7.5M), Professional $250/mo (25M). One vector basemap tile costs 1 credit — [Stadia pricing](https://stadiamaps.com/pricing/)
- **MapTiler**: the Free tier gives 5k sessions and 100k API requests per month, "Suitable for testing, PoC, prototyping, personal, or non-commercial use", and service "will pause until the next month" when over quota. Flex is $30/mo for 25k sessions, with overage at $2.50 per 1k sessions — [MapTiler pricing](https://www.maptiler.com/cloud/pricing/)
- **Google Maps Platform** (post-2025 model): Dynamic Maps gives 10,000 free loads per month, then **$7.00/1k** up to 100k, $5.60 to 500k, $4.20 to 1M, $2.10 to 5M, and $0.53 above 5M. Geocoding gives 10k free, then $5.00/1k, tiering down to $0.38. Autocomplete costs $2.83/1k. 2D Map Tiles API costs $0.60/1k after 100k free — [Google Maps pricing list](https://developers.google.com/maps/billing-and-pricing/pricing), [Maps Platform pricing overview](https://mapsplatform.google.com/pricing/)
- **Martin v1.16.1** (2026-09-09). 1.0.0 shipped 2025-11-19. It serves tiles from PostGIS tables and **functions** (auto-discovered), PMTiles (local and over HTTP) and MBTiles, and `martin cp` bulk-generates MBTiles — [Martin releases](https://github.com/maplibre/martin/releases), [Martin README](https://github.com/maplibre/martin)
- **pg_tileserv**'s last release is **v1.0.11 (2024-02-02)** and its last commit was 2025-12-11 — [pg_tileserv releases](https://github.com/CrunchyData/pg_tileserv/releases)
- **supercluster v9.1.0** (2026-09-03), ISC license — [supercluster](https://github.com/mapbox/supercluster)
- **Photon 1.3.0** (2026-08-07) is based on OpenSearch and needs Java 21+. For the full planet, "At least 64GB RAM are recommended". Country extracts exist — [Photon README](https://github.com/komoot/photon), [Nominatim: Photon country extracts](https://nominatim.org/2020/10/21/photon-country-extracts.html). The legacy country-extract directory lists a Brazil dump `photon-db-br-250720.tar.bz2` of **~2 GB, dated 2025-07-21** (possibly stale or relocated for Photon 1.x) — [GraphHopper Photon BR extracts](https://download1.graphhopper.com/public/extracts/by-country-code/br/)
- **Nominatim v5.3.3** (2026-10-14) — [Nominatim releases](https://github.com/osm-search/Nominatim/releases)

### Inferences
- **Basemap plan**: run `pmtiles extract <daily build> brasil.pmtiles --bbox=<Brazil bbox> --maxzoom=15` and host the single file on object storage behind a CDN. MapLibre reads it via HTTP range requests, with no tile server. Size estimate (unverified): the Brazil OSM PBF is about 2.1 GB, about 2–3% of the planet by data volume, which suggests a z15 Brazil extract in the **low single-digit GB** range. Run `pmtiles extract --dry-run` to get the real number. Capping at z14 roughly halves it.
- Refresh the extract monthly with a CI job. Keep OpenFreeMap as the dev default and emergency fallback style URL. It has no SLA, so don't rely on it alone in production.
- **Own data, MVP**: `GET /map/points?bbox=&zoom=&since=` returns clustered GeoJSON. Cluster server-side in SQL (`ST_SnapToGrid`/`ST_ClusterDBSCAN`, or H3 cell aggregation at a zoom-mapped resolution) so low-end phones never receive raw point clouds. Client-side supercluster is fine for fewer than ~10k points in view.
- **At scale**: Martin function sources (`fn(z,x,y,query)`) can apply auth-free public filtering, recency windows and approximate geometry, and tiles become CDN-cacheable. Prefer Martin over pg_tileserv, which has had no release since Feb 2024.
- **Approximate-location invariant**: tiles, GeoJSON and Centrifugo map messages must only ever contain the approximate geometry for approximate items. A clustered count at high zoom can still leak a home location, so set a minimum cluster radius for "approximate" items.
- **WebGL2 risk**: MapLibre v6 drops WebGL1. On very old or low-end Android GPUs, or blocklisted drivers, the map fails to init. Listen for the `error` event and fall back to a list or static view, or pin MapLibre 5.x if field telemetry shows meaningful failure rates.
- Google Maps cost at scale (my arithmetic from the published tiers, assuming 10 dynamic map loads per MAU per month): 1M MAU means about 10M loads, about **US$16k/month** (630 + 2,240 + 2,100 + 8,400 + 2,650). At 3M loads it is about **US$9.2k/month**. A self-hosted PMTiles file on a CDN costs storage plus requests. This is the decisive cost argument.
- Geocoding: self-host Photon (BR extract, autocomplete) and Nominatim (reverse geocoding to bairro/município for chain labels) on one VM in phase 2. In the MVP, reverse geocoding can be deferred: store raw coords and backfill via a job.

### Gaps
- The exact size of a Protomaps Brazil extract at z14/z15 was not measured; run `pmtiles extract --dry-run`.
- WebGL2 availability on Brazil's low-end Android installed base was not quantified (caniuse webgl2 not fetched).
- I did not research ViaCEP or BrasilAPI (CEP lookup) terms, rate limits or reliability.
- Nominatim hardware for a Brazil-only import and Photon 1.x's current BR dump location were not verified.
- OpenFreeMap's tile update frequency is not stated; only weekly planet downloads are mentioned.

---

## Q4. Realtime: per-chain chat and live map updates

### Takeaway
Use **Centrifugo v6 (Apache-2.0) with a Valkey engine**. Postgres is the source of truth for messages; the backend publishes to Centrifugo after commit. Avoid hand-rolled FastAPI WebSockets (the docs point to an archived library) and Postgres LISTEN/NOTIFY as a fan-out bus (a global commit lock in PG≤18). Choose **Valkey (BSD-3)** over Redis 8 (RSALv2/SSPLv1/AGPLv3 tri-license) for license simplicity.

### Cited Findings
- **Centrifugo v6.10.1 (2026-10-20)**, Apache-2.0 — [Centrifugo releases](https://github.com/centrifugal/centrifugo/releases), [Centrifugo repo](https://github.com/centrifugal/centrifugo). The v6 major release changed the config format, so follow the v6 migration guide — [Centrifugal blog](https://centrifugal.dev/blog/tags/release)
- Centrifugo features: channel history with "automatic stream recovery on reconnect", presence, delta compression, map subscriptions and shared poll, and a "PostgreSQL integration" to publish within the same DB transaction as business logic. Server API over HTTP/GRPC, proxy events (connect/subscribe/publish/RPC) to the backend. Transports: WebSocket, SSE, HTTP-streaming, WebTransport and GRPC. Brokers: Redis, Redis Cluster and NATS. It claims "millions of concurrent channels" — [Centrifugo introduction](https://centrifugal.dev/docs/getting-started/introduction)
- Client and server SDKs: centrifuge-js 5.8.0 — [npm centrifuge](https://www.npmjs.com/package/centrifuge); Python `cent` 5.2.0 — [PyPI cent](https://pypi.org/project/cent/)
- **LISTEN/NOTIFY**: committing a transaction that issued NOTIFY takes a global lock that serializes commits. Recall.ai traced repeated outages in March 2025 to it — [Recall.ai](https://recall.ai/blog/postgres-listen-notify-does-not-scale). DBOS measured a cap of about 2.9K stream writes/s and reached 60K/s only after batching notifications — [DBOS](https://dbos.dev/blog/postgres-listen-notify-scalability). Recall.ai's update credits commit `282b1cde` with eliminating the bottleneck. That commit is in the PG19 line, not PG18 (see Q2) — [postgres commit](https://github.com/postgres/postgres/commit/282b1cde9dedf456ecf02eb27caf086023a7bb71)
- **Valkey 9.1.2 (2026-09-01), BSD-3-Clause** — [Valkey releases](https://github.com/valkey-io/valkey/releases)
- **Redis 8.10.2 (2026-09-17)**. Since Redis 8 the license is tri-licensed: "(a) RSALv2; or (b) SSPLv1; or (c) AGPLv3". Redis 7.2 and earlier remain BSD — [Redis LICENSE.txt](https://github.com/redis/redis/blob/unstable/LICENSE.txt), [Redis releases](https://github.com/redis/redis/releases). Redis 7.2 (the previous FOSS line) was scheduled for EOL at the end of February 2026 — [The Register](https://www.theregister.com/2025/08/14/redis_redux/)
- FastAPI's in-process WebSocket pattern is single-process only, and the library it recommends (`encode/broadcaster`) is archived — [FastAPI docs](https://fastapi.tiangolo.com/advanced/websockets/), [encode/broadcaster](https://github.com/encode/broadcaster)

### Inferences
- Message flow: client → `POST /chains/{id}/messages` (FastAPI validates, authorizes and INSERTs) → after commit, publish to channel `chain:{id}` via the Centrifugo HTTP API (or a transactional outbox). Every message is persisted first, so Centrifugo history is only a reconnection buffer, never the record.
- Live map: channels per coarse H3 cell (e.g. `map:{h3_res5}`). The client subscribes to the cells covering its viewport. The payload carries approximate geometry only.
- Use Centrifugo connection JWTs minted by FastAPI, with channel-permission checks via subscribe proxy or subscription tokens, so the authorization logic stays in Python.
- Built-in SSE/HTTP-streaming fallback helps on flaky mobile networks and through corporate proxies. Presence ("3 people viewing this case") comes for free.
- Valkey vs Redis: both are fine to run unmodified, since AGPL obligations apply to modifications offered over a network. Valkey avoids any licensing review and is the default in most new compose stacks. Valkey is wire-compatible with Redis 7.2.
- KISS alternative for a tiny MVP: SSE from FastAPI plus Valkey pub/sub for map updates only, no chat. Centrifugo is one container and removes reconnection, recovery and presence work, so it pays for itself immediately.

### Gaps
- The Centrifugo introduction page doesn't mention Valkey explicitly. Verify Valkey 9 is supported as a Redis-protocol engine in the v6 docs (very likely, since it is wire-compatible, but not confirmed).
- I did not check which features are Centrifugo PRO-only (e.g. some analytics or push features).
- No independent Centrifugo benchmark from 2025–2026 was found.

---

## Q5. Client: Next.js PWA vs React Native/Expo; camera, geolocation, iOS limits, offline queueing, Serwist, performance budgets

### Takeaway
Go **PWA-first on Next.js 16**. Brazil is about 78% Android, where PWAs get Web Push, install prompts and Background Sync. On iOS (about 22%), push requires home-screen install (iOS 16.4+), and Background Sync does not exist. Add Expo later only if iOS reach, background location or reliable push become proven needs. Use `<input type="file" accept="image/*" capture="environment">` for photos. Build the offline queue as an IndexedDB outbox, with Background Sync as an Android-only enhancement. Serwist now supports Turbopack.

### Cited Findings
- Brazil mobile OS share in July 2026: **Android 77.59%, iOS 22.41%** — [StatCounter Brazil mobile OS](https://gs.statcounter.com/os-market-share/mobile/brazil)
- **Next.js 16.4.2** (2026-10-15), **React 19.3.1** — [Next.js releases](https://github.com/vercel/next.js/releases), [npm react](https://www.npmjs.com/package/react)
- The Next.js PWA guide says Web Push is supported on "iOS 16.4+ for applications installed to the home screen". Next.js now has an **experimental `useOffline` hook** and `experimental.useOffline` config "for connectivity-aware UI and automatic retries of failed navigation and Server Action requests". For full service-worker offline caching it points to Serwist, "which provides Next.js integration examples for both Turbopack and webpack" — [Next.js PWA guide](https://nextjs.org/docs/app/guides/progressive-web-apps)
- **@serwist/next 9.5.13** and **@serwist/turbopack 9.5.13** (2026-10-04) — [npm @serwist/turbopack](https://www.npmjs.com/package/@serwist/turbopack), [Serwist repo](https://github.com/serwist/serwist). Open issues include "`next dev --turbo` support" (#54) and "`createSerwistRoute` crashes at runtime on Vercel" (#360) — [Serwist issues](https://github.com/serwist/serwist/issues/54), [#360](https://github.com/serwist/serwist/issues/360)
- **Declarative Web Push** shipped for Home Screen web apps in iOS/iPadOS 18.4. It needs no service worker for display, and the SW can optionally modify the notification — [WebKit: Meet Declarative Web Push](https://webkit.org/?p=16535), [WebKit Safari 18.4](https://webkit.org/blog/16574/digital-credentials-api/)
- **Background Sync API**: supported in Chrome for Android and Samsung Internet. **Not supported in Safari (macOS or iOS, through 27.x) or Firefox**. About 76.66% global usage — [caniuse background-sync](https://caniuse.com/background-sync)
- **HTML Media Capture (`capture` attr)**: supported in Chrome Android, iOS Safari, Samsung Internet and Firefox Android. Not supported on desktop browsers — [caniuse html-media-capture](https://caniuse.com/html-media-capture)
- Apple–CADE (Brazil) settlement: alternative marketplaces and payments with **iOS 26.5** (announced 2026-06-18). Marketplaces need Apple authorization, notarization is still required, and **no sideloading requirement**. The coverage does not mention browser-engine changes — [The Next Web](https://thenextweb.com/news/apple-brazil-cade-sideloading-alternative-app-stores), [Truth on the Market](https://truthonthemarket.com/2026/02/04/apple-in-brazil-ex-post-antitrust-meets-ex-ante-ambitions/)
- Performance budgets: Alex Russell's 2023 edition estimated **~150KiB HTML/CSS/fonts and ~300–350KiB gzipped JS** to serve global P75 devices and networks. A 2026 edition was published 2025-11-24 — [Infrequently Noted series](https://infrequently.org/series/performance-inequality). Web Almanac 2025 data cited there: **only 48% of origins pass Core Web Vitals on mobile** — [SpeedCurve newsletter](https://www.speedcurve.com/newsletter/56-new-performance-inequality-gap-hidden-cost-of-media-on-the-web-the-value-of-stubborn-empathy-/)
- Native path, if needed later: **Expo SDK 58 (58.0.17)**, **React Native 0.88.0** — [npm expo](https://www.npmjs.com/package/expo), [npm react-native](https://www.npmjs.com/package/react-native)
- IndexedDB helpers: idb 8.0.4, dexie 4.4.6 — [npm idb](https://www.npmjs.com/package/idb), [npm dexie](https://www.npmjs.com/package/dexie)

### Inferences
- **Camera**: `<input type="file" accept="image/*" capture="environment">` opens the native camera on every target mobile browser with no permission prompt. Use `getUserMedia` only if an in-app viewfinder is truly needed: it adds a permission prompt, more JS and more battery drain. Compress on the client with `createImageBitmap` and canvas (or OffscreenCanvas in a worker) to about 1600px long edge, WebP/JPEG quality ~0.75, which gives roughly 150–400 KB. This is the single biggest prepaid-data saving.
- **EXIF**: EXIF GPS can deanonymize reporters. Read it client-side as a location hint, but strip all EXIF before upload, and strip again server-side.
- **Geolocation UX**: request permission only after the user taps "Use my location", with a PT-BR pre-prompt explaining why. Always offer "drop a pin" as a fallback. Make the user choose "exact" vs "approximate" explicitly at submit time.
- **Offline queue**: write every report to an IndexedDB outbox (idb/dexie) with a client-generated UUIDv7 as the idempotency key. Flush on `online`, on app focus, and (Android only) via Background Sync. The server must treat the idempotency key as unique, because retries will duplicate otherwise.
- **iOS push**: users must "Add to Home Screen" first, so design an in-app install education flow for iOS. Fall back to WhatsApp or e-mail notifications for non-installed iOS users.
- **Bundle discipline**: keep the shell RSC-heavy. Lazy-load MapLibre only on map routes, since MapLibre alone is a large chunk. Make the "report emergency" flow work without the map: photo, auto-location, submit. Set CI budgets (e.g. size-limit or Lighthouse CI) of ≤170 KB gz JS for the report flow route.
- Serwist + Turbopack is now officially pointed to by Next.js docs, but two open issues remain. Pin versions and test the SW in production builds; dev-mode SW behaviour differs.
- When to add Expo: if iOS install-to-home-screen friction kills push opt-in, or if background geofencing ("notify me when I'm near a lost pet") becomes core. Neither is MVP.

### Gaps
- The 2026 Performance Inequality Gap budget numbers and reference device were not retrieved; only the 2023 numbers are cited.
- No Brazil-specific data was found on Android device tiers or RAM distribution.
- I did not verify whether the CADE settlement or iOS 26.5 changes anything about browser engines or PWA capabilities in Brazil. The coverage is silent on this.

---

## Q6. Background jobs: arq vs Celery vs Dramatiq vs procrastinate/pgqueuer vs Taskiq

### Takeaway
Use **procrastinate (Postgres-backed, MIT, async)** for MVP and phase 1: jobs are enqueued in the same transaction as the domain write, with no extra broker. Move high-volume notification fan-out to **Taskiq or Dramatiq on Valkey** only when queue throughput or LISTEN/NOTIFY contention shows up. **Avoid arq** (maintenance-only).

### Cited Findings
- **arq v0.28.0** (2026-04-16): "**In maintenance only mode**" (issue #510) — [arq README](https://github.com/python-arq/arq)
- **procrastinate 3.10.0** (2026-09-23), MIT — [procrastinate releases](https://github.com/procrastinate-org/procrastinate/releases)
- **pgqueuer v1.6.0** (2026-10-11), MIT — [pgqueuer releases](https://github.com/janbjorge/pgqueuer/releases)
- **Taskiq 0.13.0** (2026-09-26, still 0.x); taskiq-redis 1.2.4 — [Taskiq releases](https://github.com/taskiq-python/taskiq/releases), [PyPI taskiq-redis](https://pypi.org/project/taskiq-redis/)
- **Dramatiq v2.2.1** (2026-09-02), with asyncio actor fixes — [Dramatiq releases](https://github.com/Bogdanp/dramatiq/releases)
- **Celery**: the latest stable is 5.6.3 (2026-03-26); 5.7.0rc1 came out 2026-10-18 — [Celery releases](https://github.com/celery/celery/releases)
- Django 6.0's tasks framework provides no worker (relevant only if Django were chosen) — [Django 6.0 notes](https://docs.djangoproject.com/en/6.0/releases/6.0/)
- Image libs: pyvips 3.2.0, Pillow 13.0.0 — [PyPI pyvips](https://pypi.org/project/pyvips/), [PyPI pillow](https://pypi.org/project/pillow/)

### Inferences
- A Postgres-backed queue gives a **transactional enqueue**: "report saved" and "process photo / notify nearby" commit atomically. That removes the classic dual-write bug where the row exists but the job was lost, or the job runs before the row is visible.
- Job classes: (1) image pipeline (validate MIME, decode, strip EXIF, resize variants, perceptual hash, later embeddings) is CPU-bound, so run a separate worker container with concurrency equal to cores; pyvips uses much less RAM than Pillow on large photos. (2) Notification fan-out is I/O-bound and bursty, so batch it per 500 recipients. (3) WhatsApp webhooks: ack within the HTTP request, then enqueue processing.
- Pitfall: Postgres queues typically use `SKIP LOCKED` polling plus LISTEN/NOTIFY wakeups. At very high enqueue rates on PG18 the NOTIFY commit lock (Q4) can bite. Monitor commit latency, and plan the Valkey-backed queue for the fan-out path at scale.
- Celery is mature but sync-first and operationally heavier, so it's a poor fit for an async SQLAlchemy codebase. Taskiq is the most async-native option but still 0.x.

### Gaps
- I did not verify from the docs whether procrastinate and pgqueuer use LISTEN/NOTIFY by default and whether it can be disabled.
- No throughput benchmarks across these libraries from 2025–2026 were found.

---

## Q7. Object storage: MinIO status vs Garage vs SeaweedFS vs R2/S3/Brazilian providers; CDN; presigned uploads

### Takeaway
**Do not adopt MinIO.** The community repo is archived, and no binaries or images have been published since October 2025. For dev and self-hosted use, take **Garage (v2.4.1)** or **SeaweedFS (4.48, Apache-2.0)**. For production media, **Cloudflare R2** has free egress, which matters for photo- and tile-heavy traffic, but it has **no South American location or jurisdiction**. That makes it an LGPD international transfer, so contracts need the ANPD SCCs. Magalu Cloud's S3-compatible storage is the in-country alternative.

### Cited Findings
- **MinIO**: the GitHub repo is archived=true (last push 2026-04-24), and the last release is `RELEASE.2025-10-15T17-29-55Z` — [minio/minio](https://github.com/minio/minio). Timeline: maintenance mode announced 2025-12-03; README changed to "no longer maintained" and the repo archived 2026-02-12; re-archived 2026-04-25; Docker images and binaries not published since October 2025; source-only, with users steered to the commercial AIStor — [glukhov.org](https://glukhov.org/data-infrastructure/object-storage/minio-dead/), [It's FOSS](https://itsfoss.com/news/minio-moves-away-from-open-source/), [ayedo](https://ayedo.de/en/posts/minio-im-maintenance-mode/). A community fork (pgsty/minio) restored the admin console and fixed a CVE — [Vonng blog](https://blog.vonng.com/en/db/minio-resurrect/). (Most of these are commentary sources. The archived status and last release date are verified from GitHub.)
- **Garage v2.4.1** (2026-09-08), described as an "S3-compatible object store for small self-hosted geo-distributed deployments" — [Garage releases (Deuxfleurs Forgejo)](https://git.deuxfleurs.fr/Deuxfleurs/garage/releases)
- **SeaweedFS 4.48** (2026-09-28), Apache-2.0 — [SeaweedFS releases](https://github.com/seaweedfs/seaweedfs/releases)
- **Cloudflare R2**: Standard storage $0.015/GB-mo, Class A $4.50/M, Class B $0.36/M, **egress free**. The free tier is 10 GB-mo, 1M Class A and 10M Class B — [R2 pricing](https://developers.cloudflare.com/r2/pricing/). **Location hints: wnam, enam, weur, eeur, apac, oc. Jurisdictions: eu, fedramp, us. There is no South America option** — [R2 data location](https://developers.cloudflare.com/r2/reference/data-location/)
- **Magalu Cloud** offers S3-compatible object storage, VMs, managed Kubernetes and MySQL/PostgreSQL-compatible DBs, billed in BRL. It claims 30–75% lower cost than comparable offers from Brazil — [Startups.com.br](https://startups.com.br/negocios/magazine-luiza-lanca-servico-de-nuvem-proprio-para-atender-pmes/). It has five data centers (three in Greater São Paulo, two in Fortaleza) per a 2026-05-25 report — [Baguete](https://www.baguete.com.br/noticias/magalu-cloud-levanta-r-300-milhoes-com-bndes)
- LGPD international transfers via contract must use the **ANPD standard contractual clauses** (Res. CD/ANPD 19/2024), adopted verbatim. The adaptation deadline was **2025-08-23** — [Lefosse](https://lefosse.com/noticias/transferencia-internacional-de-dados-prazo-para-adocao-das-clausulas-padrao-da-anpd-se-encerra-em-23-de-agosto/), [Mattos Filho](https://www.mattosfilho.com.br/unico/regulamentacao-transferencia-internacional-dados/)

### Inferences
- **Upload pipeline**: the client asks the API for a presigned POST (content-type and max-size conditions, ~5-minute TTL) to a **private quarantine bucket**. A worker then validates (magic bytes, dimensions), re-encodes (which strips EXIF), generates variants (thumb/medium) and writes them to a **public media bucket** behind a CDN under content-hash keys (immutable, long cache TTL). Originals stay private. Key invariant: nothing a user uploaded is ever served before the worker re-encodes it.
- Dev parity: the compose stack runs Garage or SeaweedFS with the same S3 API, so code uses boto3/aioboto3 with an endpoint URL switch only.
- Cost shape: with photos at ~200 KB and many views, egress dominates. AWS sa-east-1 internet egress is ~$0.15/GB (Q10), while R2 egress is $0. That is the main reason to prefer R2, or a CDN in front of in-country storage, at 1M MAU.
- LGPD stance: lost-pet photos are mostly not personal data, but photos can contain faces, house numbers and plates, and location plus account data is personal data. Using R2 or US clouds is lawful with ANPD SCCs in the processor contract. Keep the primary DB in Brazil to simplify.

### Gaps
- Garage's license (believed AGPLv3) was not verified this session; the API returned none.
- Magalu Cloud Object Storage prices, egress pricing and CDN offering were not retrievable (the calculator renders client-side).
- I did not verify whether Cloudflare has signed or offers the ANPD SCCs.
- Brazilian CDN PoP coverage for Cloudflare and others was not verified.

---

## Q8. Auth: phone OTP via WhatsApp vs SMS, social sign-in, passkeys; anonymous-first; libraries/IdPs

### Takeaway
Go **anonymous-first** (a device session can report immediately) with **progressive identity**. The primary upgrade is phone OTP via **WhatsApp authentication templates** (~US$0.0068 per message in Brazil), with an SMS fallback (~US$0.06/segment on Twilio, about 9× more). Google sign-in is optional, and passkeys come later. Implement auth in-house in the FastAPI auth module with opaque, revocable server-side sessions. Skip Keycloak/Zitadel at MVP. Don't build on fastapi-users, which is in maintenance mode.

### Cited Findings
- WhatsApp has used **per-message pricing since 2025-07-01**: charged on delivery, by category and recipient country. User-initiated messages are free. Meta's own comparison table footnote puts its "current rate for utility and authentication messages to users in Brazil" at **~0.68¢** — [Meta WhatsApp pricing](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing.md). Third-party guides list Brazil authentication at **$0.0068** and marketing at $0.0625 — [Courier guide](https://www.courier.com/guides/whatsapp-pricing), [Authgear](https://www.authgear.com/post/whatsapp-api-pricing)
- **BRL billing**: rollout began 2026-07-01, and all eligible businesses with a Brazil Sold-To can create BRL accounts as of 2026-07-16, invoiced by Facebook Brasil. **Accounts must migrate to BRL by 2027-06-30**; from 2027-07-01 Meta stops delivering from non-BRL accounts of eligible customers — [Meta WhatsApp pricing](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing.md)
- **Service messages are charged again as of 2026-10-01**: "Meta provides every business phone number with a free tier of 1,000 service messages per month" and "charges as of the 1,001st service message". Free-entry-point windows "may remain open for up to 7 days". Utility/auth tiers apply per market with monthly volume discounts — [Meta WhatsApp pricing](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing.md)
- **Authentication templates**: fixed body "<VERIFICATION_CODE> is your verification code.", with optional security disclaimer and expiry line (1–90 min). Buttons: copy code (all platforms), one-tap autofill (Android; iOS 26+ via keyboard suggestions, not earlier iOS) and zero-tap (Android only). Meta recommends confirming the user's WhatsApp number before sending — [Meta authentication templates](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/authentication-templates/authentication-templates)
- **Twilio SMS to Brazil: $0.0599 per segment**, "additional carrier fees may apply", plus a $0.001 failed-message fee (page current as of October 2026) — [Twilio SMS pricing Brazil](https://www.twilio.com/en-us/sms/pricing/br)
- **Zitadel** moved Apache-2.0 → **AGPL-3.0 with v3 (2025-03-31)**; the latest is v4.19.5 (2026-10-15) — [Zitadel blog](https://zitadel.com/blog/apache-to-agpl), [Zitadel releases](https://github.com/zitadel/zitadel/releases)
- **Keycloak 26.8.1** (2026-10-13) — [Keycloak releases](https://github.com/keycloak/keycloak/releases). **authentik 2026.8.5** (2026-10-21) — [authentik releases](https://github.com/goauthentik/authentik/releases). **Better Auth 1.7.12** (2026-10-20, a TypeScript library) — [Better Auth](https://github.com/better-auth/better-auth)
- **fastapi-users: maintenance mode, no new features** — [fastapi-users](https://github.com/fastapi-users/fastapi-users)

### Inferences
- Cost example (my arithmetic): 100k phone verifications per month at 1.3 sends each comes to about US$884 via WhatsApp vs about US$7,790 via Twilio SMS. WhatsApp's near-universal use in Brazil also makes delivery success likely higher. Keep SMS as a fallback for non-WhatsApp numbers. Local Brazilian SMS aggregators may be cheaper than Twilio (not verified).
- **Anonymous-first design**: the first visit gets a server-issued opaque `anon_session` (httpOnly cookie, stored server-side with a device fingerprint hash and rate-limit counters). Reports from anonymous sessions are allowed but marked lower-trust (useful for moderation and trust scoring). Upgrading attaches the phone number to the existing session, so the user keeps their reports.
- **Session model**: opaque random tokens in Postgres or Valkey, revocable, rotated on privilege change. That is simpler than JWT access/refresh pairs when there is one backend. Only Centrifugo needs JWTs (short-lived, minted by FastAPI).
- An IdP (Keycloak, Zitadel or authentik) adds a JVM or Go service, its own DB and its own upgrade cadence. Phone-OTP-first with anonymous upgrade is custom logic in every IdP anyway. Zitadel's AGPL is fine for unmodified use, but add an IdP only if B2B/NGO SSO (OIDC for partner shelters) becomes a requirement.
- Better Auth is TS-only. Using it would move auth into Next.js and split the source of truth away from FastAPI, so avoid it given the backend-owns-writes invariant.
- WhatsApp intake agent cost note: since 2026-10-01, service replies beyond 1,000 per month per number are billed. A conversational intake bot will incur per-message costs at scale; budget for it.

### Gaps
- Meta's official Brazil rate card CSV was not opened. The $0.0068 value comes from Meta's footnote (~0.68¢) plus third-party tables, and post-BRL-migration BRL prices are unknown.
- Brazilian SMS aggregator pricing (Zenvia etc.) was not researched.
- Passkey support on low-end Android (Credential Manager / Google Password Manager coverage) was not researched.
- Anti-abuse options (Cloudflare Turnstile, hCaptcha, proof-of-work) were not researched.

---

## Q9. Geo-targeted notification fan-out: who should be notified about a new event?

### Takeaway
Use a **two-stage match**. An H3 cell inverted index (`watch_cells(h3_cell, user_id)`, B-tree) finds candidates by equality lookup, and an exact `ST_DWithin` on geography filters them. Fan out through the job queue in batches, deliver via Web Push (VAPID), and add FCM/APNs only if a native app arrives. I found no published benchmark comparing this against a pure GiST approach; the choice rests on query-shape reasoning.

### Cited Findings
- h3-pg (now under the PostGIS org, v4.5.0) provides H3 bindings in Postgres, including grid-disk neighbor lookups that join against indexed H3 columns — [postgis/h3-pg](https://github.com/postgis/h3-pg), [Nile h3_postgis docs](https://thenile.dev/docs/extensions/h3_postgis). The `h3_postgis` cast uses the cell centroid, so distance checks on cells are approximate — [h3-pg skill doc on PGXN](https://pgxn.org/dist/h3/docs/h3-pg-skill/SKILL.html)
- Python h3 4.5.0 — [PyPI h3](https://pypi.org/project/h3/). pywebpush 2.5.0 (2026-08-30) — [PyPI pywebpush](https://pypi.org/project/pywebpush/). firebase-admin 7.7.0 — [PyPI firebase-admin](https://pypi.org/project/firebase-admin/)
- Web Push on iOS works only for home-screen-installed apps (16.4+), and Declarative Web Push arrived in iOS 18.4 — [Next.js PWA guide](https://nextjs.org/docs/app/guides/progressive-web-apps), [WebKit](https://webkit.org/?p=16535)

### Inferences
- Why H3 first: each user's watch area is a circle with a per-user radius. A pure-PostGIS query `ST_DWithin(user.center, event.point, user.radius)` can't use a GiST index efficiently when the radius varies per row, unless you store pre-buffered polygons and use `ST_Intersects(watch_polygon, event_point)`, which also works and is GiST-indexable. H3 turns the match into `event_cell IN (precomputed cells)`, an equality join that is trivially indexable, cheap to shard or partition by cell, and identical to the Centrifugo map channel keys (Q4). Two concepts, one key.
- Recipe: on subscription save, compute `h3_polygon_to_cells(buffer(center, radius), res=7 or 8)` (res 7 is about 5 km² cells; res 8 is about 0.7 km²). Insert rows into `watch_cells`. On a new event, `SELECT user_id FROM watch_cells WHERE h3_cell = h3_lat_lng_to_cell(event, res)`, then confirm with `ST_DWithin`, dedupe, and apply quiet hours and per-user rate limits. Enqueue push jobs in batches.
- Simplest version that works (MVP): the PostGIS `ST_Intersects` on buffered watch polygons with a GiST index is fine up to hundreds of thousands of subscribers. Switch to the H3 table when fan-out query time or row counts justify it. Both live in Postgres, so the migration is cheap.
- Main failure modes: (1) notification storms in dense cities, so cap notifications per user per hour and aggregate ("5 new sightings near you"). (2) Location privacy: the subscription center is a home location, so store it coarsened or encrypted, and never expose it.
- Delivery: Web Push via VAPID with pywebpush covers Chrome/Android and installed iOS PWAs. Remove dead subscriptions on 404/410 responses. A WhatsApp utility message is a paid fallback channel for high-urgency events.

### Gaps
- No benchmark found comparing H3 inverted index vs PostGIS GiST for geofence subscription matching at 1M+ subscribers.
- Web Push delivery reliability metrics in Brazil were not found.

---

## Q10. Hosting in Brazil: latency, LGPD, provider options and rough costs

### Takeaway
Host the database and API **in Brazil** (São Paulo region) for latency and simpler LGPD posture. AWS sa-east-1 costs about **59% more** than us-east-1 for identical instances, and egress is ~$0.15/GB. OCI claims uniform global pricing and has São Paulo and Vinhedo regions. Magalu Cloud bills in BRL, but its public price list could not be retrieved. MVP on one VM costs roughly US$0–250/month. At 1M MAU, expect roughly **US$3–6k/month** on AWS São Paulo on-demand before savings plans, highly sensitive to media egress. These are inferences from the cited unit prices.

### Cited Findings
- AWS on-demand Linux prices (USD/hour), from AWS price data, 2026-10-21 — [AWS EC2 on-demand pricing](https://aws.amazon.com/ec2/pricing/on-demand/), data files [São Paulo](https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/ec2/USD/current/ec2-ondemand-without-sec-sel/South%20America%20(Sao%20Paulo)/Linux/index.json) and [N. Virginia](https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/ec2/USD/current/ec2-ondemand-without-sec-sel/US%20East%20(N.%20Virginia)/Linux/index.json):

  | Instance | vCPU/RAM | sa-east-1 | us-east-1 | ratio |
  |---|---|---|---|---|
  | t4g.medium | 2 / 4 GiB | 0.0536 | 0.0336 | 1.60 |
  | t4g.large | 2 / 8 GiB | 0.1072 | 0.0672 | 1.60 |
  | m7g.large | 2 / 8 GiB | 0.1301 | 0.0816 | 1.59 |
  | m7g.xlarge | 4 / 16 GiB | 0.2601 | 0.1632 | 1.59 |
  | m7g.2xlarge | 8 / 32 GiB | 0.5202 | 0.3264 | 1.59 |
  | r7g.2xlarge | 8 / 64 GiB | 0.6818 | 0.4284 | 1.59 |
  | m8g.xlarge | 4 / 16 GiB | 0.2861 | 0.1795 | 1.59 |
- AWS São Paulo internet egress was cut 40% in 2020 to **$0.150/GB for the first 10 TB**, stepping down to $0.114/GB above 150 TB. Inbound is free. This is a 2020 announcement and the current rate was not re-verified — [AWS News Blog](https://aws.amazon.com/blogs/aws/aws-data-transfer-out-dto-40-price-reduction-in-south-america-sao-paulo-region)
- **OCI**: Oracle states uniform pricing across all public regions, except outbound bandwidth. It cites AWS São Paulo as 59% more than US East for m5d.large (2020 data) — [Oracle blog](https://blogs.oracle.com/cloud-infrastructure/cost-advantages-to-consider-when-choosing-a-cloud-platform-part-1-pricing-consistency-with-consumption-flexibility), [Oracle "Top reasons" PDF](https://oracle.com/a/ocom/docs/gated/top-reasons-oci-cloud-native.pdf). Regions include Brazil East (São Paulo) and Brazil Southeast (Vinhedo) — [Oracle public cloud regions](https://www.oracle.com/cloud/public-cloud-regions/). **Always Free**: 3,000 OCPU-hours and 18,000 GB-hours per month of VM.Standard.A1.Flex, equal to 4 OCPU / 24 GB (ARM), in the tenancy's home region only. Idle Always Free instances can be reclaimed — [OCI Always Free resources](https://docs.oracle.com/en-us/iaas/Content/FreeTier/resourceref.htm)
- **Magalu Cloud**: BRL billing, claims 30–75% cheaper than comparable in-Brazil offers, five DCs (3 in SP, 2 in Fortaleza), and raised R$300M from BNDES — [Startups.com.br](https://startups.com.br/negocios/magazine-luiza-lanca-servico-de-nuvem-proprio-para-atender-pmes/), [Baguete](https://www.baguete.com.br/noticias/magalu-cloud-levanta-r-300-milhoes-com-bndes). Its price calculator loads dynamically and could not be read — [magalu.cloud/precos](https://magalu.cloud/precos/)
- **LGPD**: international transfers by contract require the ANPD SCCs (Res. 19/2024; deadline 2025-08-23) — [Lefosse](https://lefosse.com/noticias/transferencia-internacional-de-dados-prazo-para-adocao-das-clausulas-padrao-da-anpd-se-encerra-em-23-de-agosto/). One 2026 source reports **Res. CD/ANPD 32/2026 as a Brazil–EU mutual adequacy decision**; this is single-source and unverified — [Confidata](https://confidata.com.br/blog/transferencia-internacional-dados-atualizacao-anpd-2026)

### Inferences
- **MVP (single VM, Docker Compose)**, roughly 2–4 vCPU / 8–24 GB:
  - OCI Always Free A1 in São Paulo or Vinhedo costs US$0. It is ARM, so build an ARM PostGIS image (Q2), and accept capacity and reclamation risk. Fine for a pilot, not for a launch with press attention.
  - AWS sa-east-1 m7g.xlarge (4/16) costs about **US$190/mo** on-demand (0.2601 × 730), plus EBS and egress. t4g.large costs about US$78/mo.
  - Add R2 for media (free up to 10 GB) and a nightly pgBackRest to object storage.
- **~1M MAU (rough)**, AWS sa-east-1 on-demand, before savings plans (typically 30–40% off with 1-year commitments):
  - 3× m7g.xlarge API/Next.js ≈ $570
  - 2× m7g.xlarge Centrifugo + Valkey ≈ $380
  - 2× m7g.xlarge workers ≈ $380
  - Postgres primary + replica on r7g.2xlarge ≈ $995
  - Compute subtotal ≈ **$2.3k/mo**
  - Plus EBS (≈1–2 TB gp3, price not verified), Photon/Nominatim VM (~$190–380), monitoring, and egress. If 1M MAU pull ~20 MB/month each of images, tiles and JS from AWS directly, that is ~20 TB × ~$0.15 ≈ **$3k/mo** of egress. Serving media and tiles via R2 or a CDN cuts most of it.
  - Realistic band: **US$3–6k/month**. Map tiles via Google would add ~$9–16k/month on top (Q3), which is why self-hosted PMTiles matters.
- Latency: users in the Northeast and North are far from São Paulo, but the gap to US East is much larger. Put the CDN in front of everything static. Hetzner and OVH have no Brazil region, which matters for DB round-trips more than for static assets (not re-verified this session).
- LGPD posture: keep the primary DB, backups and logs with PII in Brazil. Use foreign processors (Cloudflare, Sentry, Meta) under ANPD SCCs, and record them in the RoPA. Publish a PT-BR privacy notice that explains exact vs approximate location handling.

### Gaps
- GCP southamerica-east1 and Azure Brazil South prices were not retrieved.
- Magalu Cloud VM, storage and egress prices could not be retrieved.
- Locaweb and Hostinger VPS offerings were not researched.
- Current (2026) AWS sa-east-1 egress and EBS gp3 prices were not re-verified.
- No ping/latency measurements were gathered (e.g. São Paulo↔Fortaleza/Manaus, São Paulo↔Ashburn).
- The ANPD Res. 32/2026 EU adequacy claim was not verified against the ANPD.

---

## Q11. Observability and ops: Sentry, OpenTelemetry, backups, CI

### Takeaway
Use the **Sentry SDK** for both backend and frontend errors, plus **OpenTelemetry** traces and metrics to a Grafana-compatible backend. Back up with **pgBackRest 2.60** (upgrade past the October 2026 encryption advisory) to object storage, and rehearse restores. CI runs the full compose stack, including the PostGIS image, for integration tests.

### Cited Findings
- **sentry-sdk 2.72.0** (2026-10-12) — [PyPI sentry-sdk](https://pypi.org/project/sentry-sdk/). **opentelemetry-sdk 1.45.1** (2026-10-06) — [PyPI opentelemetry-sdk](https://pypi.org/project/opentelemetry-sdk/)
- **pgBackRest 2.60.0** (2026-10-18). News on 2026-10-04: "**Weak Encryption Subkeys and Salts**", with 2.59.3 released the same day. In 2.60, "the restore command will now error and stop if any restored file contains an invalid page checksum" (set `checksum-page-error=n` to only warn). New: GCS Workload Identity Federation and prefetching for object-store reads — [pgBackRest README/News](https://github.com/pgbackrest/pgbackrest), [pgBackRest 2.60.0 release](https://github.com/pgbackrest/pgbackrest/releases), [pgBackRest news](https://pgbackrest.org/news.html)
- **WAL-G v3.0.9** (2026-08-20) — [WAL-G releases](https://github.com/wal-g/wal-g/releases)

### Inferences
- pgBackRest vs WAL-G: both are fine. pgBackRest has richer restore verification and is actively maintained (October 2026 releases). If using repo encryption, read the advisory and re-key per its guidance.
- RPO/RTO for a civic emergency app: target RPO ≤ 5 min (continuous WAL archiving) and RTO ≤ 1 h at MVP. Test the restore monthly in CI or a scheduled job. Untested backups are the classic failure mode.
- Observability minimums: request traces with route and module attributes (useful alongside import-linter boundaries), queue depth and job latency, Centrifugo connection counts, push success/410 rates, and photo pipeline durations. Set PII scrubbing in Sentry (`send_default_pii=False`) and never log exact coordinates.
- CI: GitHub Actions (or equivalent) with `docker compose -f compose.ci.yml up` for postgis/valkey/centrifugo/garage; Alembic upgrade/downgrade checks; import-linter; generated TS client drift check (regenerate from OpenAPI and fail on diff); Lighthouse CI budgets on the report flow.

### Gaps
- Sentry self-hosted vs SaaS cost at scale, and GlitchTip as an alternative, were not researched.
- The details of the pgBackRest encryption advisory (affected versions, required action) were not read.

---

## Q12. Synthesis: recommended stack table, "avoid" list, phased evolution

### Takeaway
Reuse the team's baseline almost entirely: FastAPI/SQLAlchemy/Alembic/PG18/Next.js 16/uv/pnpm/Compose/Caddy. The evidence-backed changes and additions are: PostGIS 3.6 + pgvector + h3-pg on a custom PG image; Centrifugo + Valkey for realtime; procrastinate for jobs; MapLibre v6 + self-hosted PMTiles + Martin later; Garage/SeaweedFS for local S3, with R2 or in-country S3 in production; Serwist (Turbopack) for the PWA; and in-house anonymous-first auth with WhatsApp OTP.

### Cited Findings
Recommended stack (versions as of 2026-10-21; sources in Q1–Q11):

| Component | Choice | Version | Why | Alternative considered (rejected because) |
|---|---|---|---|---|
| API framework | FastAPI (modular monolith, import-linter) | 0.159.0 ([GitHub](https://github.com/fastapi/fastapi/releases)) | Team baseline, async, Pydantic→OpenAPI | Django 6.1: admin/GeoDjango attractive, but no async ORM gains in 6.0/6.1, tasks lack a worker ([6.0](https://docs.djangoproject.com/en/6.0/releases/6.0/), [6.1](https://docs.djangoproject.com/en/6.1/releases/6.1/)); NestJS/Go: language switch without a bottleneck to solve |
| ORM / migrations | SQLAlchemy async + GeoAlchemy2 + Alembic | 2.1.6 / 0.20.0 / 1.20.0 ([PyPI](https://pypi.org/project/SQLAlchemy/)) | Typed PostGIS columns and functions | GeoDjango ORM (tied to Django switch) |
| ASGI server | uvicorn (or granian) | 0.54.0 / 2.8.5 ([PyPI](https://pypi.org/project/uvicorn/)) | Baseline | n/a |
| Database | PostgreSQL 18 | 18.6 ([tags](https://github.com/postgres/postgres/tags)) | Current GA; PG19 GA only planned for 2026-11-19 ([PG news](https://www.postgresql.org/about/news/postgresql-19-rc-1-released-3409/)) | PG19 at GA (too fresh for extensions) |
| Spatial | PostGIS | 3.6.4 ([tags](https://github.com/postgis/postgis/tags)) | Supports PG18 | 3.7 (RC only) |
| Grid index | h3-pg (postgis/h3-pg) | upstream 4.5.0; PGDG pkg 4.2.3 ([repo](https://github.com/postgis/h3-pg), [PGDG](https://apt.postgresql.org/pub/repos/apt/pool/main/h/h3-pg/)) | Fan-out matching, map channel keys, aggregation | Pure GiST only (fine for MVP) |
| Vectors (later) | pgvector HNSW (halfvec) | 0.8.7 ([tags](https://github.com/pgvector/pgvector/tags)) | Re-ID embeddings in the same DB; iterative scans for filtered kNN | Separate vector DB (extra infra) |
| DB image | `postgis/postgis:18-3.6` + PGDG pgvector/h3 | 3.6.4 base ([docker-postgis](https://github.com/postgis/docker-postgis)) | Official; mount `/var/lib/postgresql` | Third-party images; note: amd64-only |
| Cache / pub-sub | Valkey | 9.1.2 ([releases](https://github.com/valkey-io/valkey/releases)) | BSD-3 | Redis 8.x tri-license RSALv2/SSPL/AGPL ([LICENSE](https://github.com/redis/redis/blob/unstable/LICENSE.txt)) |
| Realtime | Centrifugo (Valkey engine) | 6.10.1 ([releases](https://github.com/centrifugal/centrifugo/releases)) | Recovery, presence, SSE fallback, Apache-2.0 | FastAPI WS (single-process; broadcaster archived), LISTEN/NOTIFY (commit lock on PG18) |
| Jobs | procrastinate (PG-backed) | 3.10.0 ([releases](https://github.com/procrastinate-org/procrastinate/releases)) | Transactional enqueue, no extra broker | arq (maintenance-only); Celery (sync-first); Taskiq/Dramatiq on Valkey later |
| Image processing | pyvips | 3.2.0 ([PyPI](https://pypi.org/project/pyvips/)) | Low memory, fast | Pillow 13.0.0 (fine, heavier) |
| Object storage (dev/self-host) | Garage or SeaweedFS | 2.4.1 / 4.48 ([Garage](https://git.deuxfleurs.fr/Deuxfleurs/garage/releases), [SeaweedFS](https://github.com/seaweedfs/seaweedfs/releases)) | Maintained, S3 API | MinIO CE (archived, no binaries since Oct 2025) |
| Object storage (prod) | Cloudflare R2 (or Magalu S3 for in-country) | n/a ([R2 pricing](https://developers.cloudflare.com/r2/pricing/)) | Free egress for photos/tiles | AWS S3 sa-east-1 (egress ~$0.15/GB) |
| Map renderer | MapLibre GL JS | 6.15.0 ([release](https://github.com/maplibre/maplibre-gl-js/releases/tag/v6.0.0)) | OSS, vector, PMTiles | Leaflet (raster-first, no vector styling); Google Maps (~$7/1k loads) |
| Basemap | Protomaps PMTiles Brazil extract on CDN; OpenFreeMap fallback | basemap v4.15.2 ([builds](https://build-metadata.protomaps.dev/builds.json)) | No per-view fees | OSM tiles (policy forbids heavy commercial use); Stadia/MapTiler free tiers (non-commercial) |
| Own-data tiles | GeoJSON + server clustering → Martin later | Martin 1.16.1 ([releases](https://github.com/maplibre/martin/releases)) | Simple first, MVT at scale | pg_tileserv (no release since Feb 2024) |
| Geocoding | Photon + Nominatim (self-hosted, phase 2) | 1.3.0 / 5.3.3 ([Photon](https://github.com/komoot/photon), [Nominatim](https://github.com/osm-search/Nominatim/releases)) | No per-call fees | Google Geocoding ($5/1k after 10k) |
| Frontend | Next.js + React (PWA) | 16.4.2 / 19.3.1 ([releases](https://github.com/vercel/next.js/releases)) | Team baseline; RSC keeps JS small | Expo 58 / RN 0.88 (later, if iOS push/background geo needed) |
| Service worker | Serwist (@serwist/turbopack) | 9.5.13 ([npm](https://www.npmjs.com/package/@serwist/turbopack)) | Named in Next.js PWA docs | next-pwa (unmaintained, not re-verified); hand-rolled SW |
| API client | @hey-api/openapi-ts or orval | 0.99.0 / 8.44.0 ([npm](https://www.npmjs.com/package/orval)) | Typed client from FastAPI OpenAPI | Hand-written fetchers |
| Auth | In-house: anon sessions + WhatsApp OTP (+ SMS fallback), opaque sessions | n/a | Fits anonymous-first; ~$0.0068/OTP in BR ([Meta](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing.md)) | Keycloak 26.8 / Zitadel 4.19 (AGPL) / authentik: heavy for MVP; fastapi-users (maintenance mode); Better Auth (TS-only) |
| Push | Web Push (VAPID, pywebpush) | 2.5.0 ([PyPI](https://pypi.org/project/pywebpush/)) | Android + installed iOS PWAs | FCM only when native app exists |
| Errors / tracing | Sentry SDK + OpenTelemetry | 2.72.0 / 1.45.1 ([PyPI](https://pypi.org/project/sentry-sdk/)) | Standard | n/a |
| Backups | pgBackRest → object storage | 2.60.0 ([releases](https://github.com/pgbackrest/pgbackrest/releases)) | Active; restore verification | WAL-G 3.0.9 (also fine) |
| Edge | Caddy (baseline) | not re-verified | Auto-TLS, WebSocket proxying | Traefik/Nginx |

Avoid list (each backed by findings above):
- **MinIO Community Edition** for new deployments: archived repo, no binaries or images since October 2025 ([GitHub](https://github.com/minio/minio)).
- **tile.openstreetmap.org** as the production basemap: the policy allows withdrawal without notice and has no SLA ([OSMF](https://operations.osmfoundation.org/policies/tiles/)).
- **Stadia/MapTiler free tiers** in production: non-commercial terms, and MapTiler pauses service when over quota ([Stadia](https://stadiamaps.com/pricing/), [MapTiler](https://www.maptiler.com/cloud/pricing/)).
- **Google Maps JS** as the map: ~$16k/month at 10M loads (Q3 arithmetic on [Google pricing](https://developers.google.com/maps/billing-and-pricing/pricing)).
- **arq** (maintenance-only) ([arq](https://github.com/python-arq/arq)); **fastapi-users** for new auth (maintenance mode) ([repo](https://github.com/fastapi-users/fastapi-users)); **encode/broadcaster** (archived) ([repo](https://github.com/encode/broadcaster)).
- **Postgres LISTEN/NOTIFY as a high-volume fan-out bus on PG18**: the commit-serializing lock ([Recall.ai](https://recall.ai/blog/postgres-listen-notify-does-not-scale)).
- **pg_tileserv** for new builds: no release since Feb 2024 ([releases](https://github.com/CrunchyData/pg_tileserv/releases)).
- **PostgreSQL 19 / PostGIS 3.7 at launch**: not GA, or GA too recently ([PG news](https://www.postgresql.org/about/news/postgresql-19-rc-1-released-3409/), [PostGIS tags](https://github.com/postgis/postgis/tags)).
- **Relying on Background Sync for iOS users**: unsupported in Safari ([caniuse](https://caniuse.com/background-sync)).
- **Copying PG≤17 compose volume paths onto the PG18 image** ([Dockerfile](https://github.com/docker-library/postgres/blob/master/18/trixie/Dockerfile)).

### Inferences
Phased evolution (assumptions: Brazil-first launch, small team, Compose-based ops):

- **Phase 0, MVP (0 to ~50k MAU), single VM in São Paulo**
  - **Compose services**: caddy, next, api (FastAPI), worker (procrastinate), centrifugo, valkey, postgres (PostGIS + pgvector + h3), garage (or R2 directly in prod).
  - **Map**: PMTiles Brazil extract on R2/CDN, with an OpenFreeMap fallback style.
  - **Own data**: bbox GeoJSON + SQL clustering.
  - **Fan-out**: PostGIS `ST_Intersects` on buffered watch polygons, jobs via procrastinate, Web Push.
  - **Auth**: anon session → WhatsApp OTP.
  - **Reverse geocoding**: deferred, or a light Nominatim instance.
  - **Backups**: pgBackRest nightly full + WAL archive to object storage.
  - **Cost**: ~US$0 (OCI Free, ARM) to ~US$200–300/month (AWS sa-east-1 m7g.xlarge + storage).
- **Phase 1 (~50k–300k MAU)**
  - Split the DB onto its own VM or managed Postgres in BR, with a streaming replica for reads and failover.
  - Run 2× API/Next behind Caddy or a load balancer.
  - Introduce Martin function sources for the map once point density makes GeoJSON heavy.
  - Move the subscription matching to the H3 `watch_cells` table.
  - Self-host Photon and Nominatim.
  - Add declarative partition automation and an image-embedding worker with pgvector (HNSW, halfvec).
- **Phase 2 (~1M MAU)**
  - Run Centrifugo as a 2–3 node cluster on a dedicated Valkey.
  - Move the notification fan-out queue to Taskiq/Dramatiq on Valkey if PG queue contention appears.
  - Add read replicas for map/tile queries.
  - Push all media and tiles through CDN/R2 to avoid sa-east-1 egress.
  - Consider PG19 once 19.2+ and extensions are packaged, mainly for the NOTIFY scalability fix.
  - Consider an Expo app if iOS push opt-in is the growth bottleneck.
  - **Cost**: ~US$3–6k/month on AWS São Paulo on-demand (before commitments), dominated by DB and egress.
- **Move to Kubernetes**: only when more than one ops engineer exists and Compose-on-VMs becomes the bottleneck. YAGNI before ~1M MAU.

Key invariants to carry through all phases:
1. Postgres is the only source of truth. Realtime, tiles and caches are derived.
2. Approximate locations are derived at write time, and only the derived geometry is ever serialized publicly.
3. Every client write is idempotent (client UUID), because offline queues retry.
4. Uploaded bytes are never served before re-encoding and EXIF stripping.

### Gaps
- I did not verify the next-pwa maintenance status or the Caddy version.
- Phase thresholds (MAU numbers) are judgment calls, not benchmarked.
- No load testing data exists for this specific workload. Recommend a k6/Locust test of report-create + fan-out + map-bbox before Phase 1.
