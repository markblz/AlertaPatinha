# Data model — relatos, casos, elos, blocos

Evidence: [spatiotemporal notes §2–4, §7](<../research/research_notes/Stray pet platform research/spatiotemporal_chains.md>)
(Wildbook model, Fellegi–Sunter scoring, bitemporal design, parameter table).
Vocabulary: [glossary](glossary.md). Privacy columns: [location-privacy](location-privacy.md).

## Key invariant

> A relato is an immutable fact about (time interval, place, appearance) with
> transaction-time provenance. A caso is a revisable hypothesis built only from
> append-only elo and bloco rows. Nothing is ever "moved into" a caso.

**Main failure mode:** storing relatos *inside* casos (FK `observation.chain_id`
updated in place). Merges and splits then destroy history, and a wrong merge
cannot be undone. A close second: transitive over-merge (A≈B, B≈C ⇒ A=C, false
at colonies of look-alike cats).

## Tables (sketch — the first migrations are yours to write)

```sql
-- schema observations
observation(
  id uuid pk, client_id uuid unique,                -- idempotency key from the client outbox
  reporter_id uuid, source text,                    -- 'web' | 'whatsapp' | 'import'
  kind text,                                        -- sighting | emergency | lost | found
  species text, animal_count int default 1,
  valid_time tstzrange not null,                    -- WHEN SEEN (interval)
  time_precision text not null,                     -- exact | minutes | hour | part_of_day | day | approx
  time_text text, edtf text,                        -- original words + EDTF (e.g. '2026-10-20T15:00~')
  recorded_at timestamptz not null default now(),   -- WHEN RECORDED (server clock only)
  true_geom geography(Point,4326) not null,         -- restricted: never in public schemas
  loc_accuracy_m int, loc_source text,              -- gps | pin | geocode | text
  privacy_class text not null, display_mode text not null,
  display_cell h3index, display_geom geography,     -- derived once at write time (stable)
  h3_r9 h3index not null, h3_r7 h3index not null,   -- blocking + aggregation
  attributes jsonb not null default '{}',           -- coat, size, sex, collar, injury flags, urgency answers
  hidden_at timestamptz                             -- set only via moderation event
)
observation_photo(observation_id, photo_id, position)   -- photos owned by media
sighting_group(id) + sighting_group_member(group_id, observation_id)  -- one photo, several animals

-- schema chains
chain(
  id uuid pk, species text, status text,            -- emergency | lost_pet | community | colony_feral | unknown
  created_at timestamptz, created_by uuid
)                                                   -- state is DERIVED from events (or a cached projection)
chain_link(                                         -- append-only: the latest row per (chain, observation) wins
  id bigserial pk, chain_id uuid, observation_id uuid,
  link_state text,                                  -- suggested | asserted | confirmed | rejected | retracted
  score_bits real, method text,                     -- reporter | model | crowd_vote | moderator
  actor_id uuid, evidence jsonb, recorded_at timestamptz default now()
)
chain_event(                                        -- the bloco log, append-only
  id bigserial pk, chain_id uuid, type text, payload jsonb,
  actor_id uuid, valid_time tstzrange, recorded_at timestamptz default now(),
  client_id uuid unique                             -- idempotent client-originated events
)
chain_state(chain_id pk, state, last_seen_valid_time, last_seen_cell, home_estimate geography,
            home_sigma_m, merged_into uuid, updated_at)   -- PROJECTION, rebuildable from events

-- schema geo
private_zone(id, owner_id, kind, geom geography(Polygon), created_at)
location_access_log(id bigserial, viewer_id, tier, observation_id, purpose, at)
```

Projections (`chain_state`) are caches. Rebuilding them from `chain_link` +
`chain_event` must produce the same result — that is the test of the model.

## Time

- `valid_time` is an interval, never a point. A GPS-stamped live photo gives
  a narrow interval; "ontem à tarde" gives a wide one. Overlap queries (`&&`)
  handle fuzzy-vs-window filtering for the map's time slider.
- PT-BR part-of-day parse table (v0, validate with users): madrugada 00–06 ·
  manhã 06–12 · tarde 12–18 · noite 18–24 · "hoje cedo" 05–09 · "agora há
  pouco" now−1h…now. Keep `time_text` always.
- "Último avistamento" = max upper bound of `valid_time` among **confirmed**
  links only; shown with its precision ("visto ontem à tarde", never "às 15:00").
- Late reports insert into the past without rewriting history; corrections are
  `observation_corrected` events with their own `recorded_at`.
- Freshness of a location: `2^(−Δt/h)`, Δt from the interval midpoint, h by caso type.

## Caso lifecycle

```
open ──(2nd confirmed relato or helper action)──▶ active
active ──(no confirmed update for T_stale)──▶ stale ──(T_dormant)──▶ dormant
stale/dormant ──(new confirmed relato)──▶ active
any ──resolve(encerramento)──▶ resolved        any ──archive(policy)──▶ archived
any ──merge(into X, human)──▶ merged            merged ──unmerge(human)──▶ previous state
```

Default parameters v0 — **extrapolated**, re-fit after 3–6 months of data:

| Caso type | Link soft gate | Link hard gate | Location half-life | Active → dormant / archive | Alert radius (start → cap) |
|---|---|---|---|---|---|
| Emergência | 100 m / 6 h | 500 m / 24 h | 2–6 h | 72 h without update → archive | small ring → 2–5 km, widen ×2 per missed target |
| Pet perdido (cão) | 1 km + growth | 5 km at 48 h, then city | 24–48 h | 60 d | 3 km → city + shelters/CCZ |
| Gato perdido (indoor-only) | 200 m | 500 m | 7 d | 90 d | 500 m |
| Gato perdido (outdoor access) | 500 m | 2 km | 7 d | 90 d | 2 km |
| Comunitário | 300 m | 1 km | 30 d | never archive; yearly re-confirm | 1 km |
| Colônia / feral | 150 m | 400 m | 60–90 d | never archive; yearly re-confirm | 500 m, verified helpers only |

Anchors: lost cats median 50 m from escape, 75% within 500 m, alive-recovery
flat after ~61 days (Huang 2018); free-roaming dogs' 95% home range ≈ r 135–160 m
(Warembourg 2021). No peer-reviewed lost-dog distance data exists.

## Elos — who can move them

| Transition | Who |
|---|---|
| → `suggested` | System (heuristic now, model in M6) |
| → `asserted` | The reporter ("é o mesmo que este caso") |
| → `confirmed` | Guardian of a perdido caso · a T3 on the caso · ≥2 independent T2+ voters with >2/3 agreement · staff |
| → `rejected` | Same quorum as confirmed |
| → `retracted` | Whoever asserted it |

Votes stay hidden until you vote (anti-herding). Only `confirmed` elos move
"último avistamento", the home estimate and the map marker.

## Bloco (chain_event) types

`observation_linked` · `observation_unlinked` · `seen_again` ·
`status_changed` · `claim_started` / `claim_expired` / `claim_completed` ·
`vet_visit` · `in_care` · `note` · `observation_corrected` · `merged` /
`unmerged` · `split` · `resolved(encerramento)` · `reopened` · `hidden`
(moderation). New types are added here first.

## Linking pipeline (M2)

1. **Normalize** (at write): parse time → interval + precision; record accuracy; classify privacy; derive display.
2. **Block**: same species; casos in {open, active, stale, dormant}; `h3_r9` within `gridDisk(k)` covering the hard gate; `valid_time` overlap with an expanded window. Then exact `ST_DWithin(true_geom, …, hard_gate_m)`.
3. **Score** (bits, Fellegi–Sunter style): `W = Σ log2(m_i/u_i)` over space-time plausibility (home-range model, not Kalman — resident animals have no momentum), coat, size, sex, collar, "reporter says same", and the embedding bin (M6). Posterior with prior ≈ 1/n_candidates.
4. **Decide**: < 0.2 nothing · 0.2–0.8 "É o mesmo animal?" card · > 0.8 strong suggestion, still human-confirmed.
5. **Guard over-merge**: before confirming, check the new relato pairwise against the caso's representative photos, not just its nearest member.
6. **Learn**: confirmed/rejected pairs re-estimate m/u per city (EM, Splink-style). Track suggestion precision/recall.
7. **Nightly**: ST-DBSCAN over unlinked sightings → propose comunitário/colônia casos; space-time permutation scan on poisoning/abuse categories → private alert to T4.

## Core logic to implement (owner first, then review)

```python
# src/observations/domain/
def parse_seen(text: str | None, now: datetime, tz: ZoneInfo) -> SeenInterval  # interval + precision + edtf
# src/chains/domain/
def derive_state(links: list[LinkRow], events: list[EventRow], now: datetime) -> ChainState
def freshness(valid_time: Interval, now: datetime, half_life: timedelta) -> float
def score_pair(a: ObservationFacts, b: ObservationFacts, params: LinkParams) -> Score  # bits + breakdown
```

Acceptance examples:
1. `parse_seen("ontem à tarde", now=2026-10-21 10:00 -03)` → [2026-10-20 12:00, 18:00) -03, `part_of_day`.
2. `parse_seen("agora há pouco", now)` → [now−1h, now], `approx`.
3. Replaying a caso's links/events in a different insertion order of *equal* `recorded_at` → same `ChainState` (deterministic tiebreak by id).
4. A `suggested` elo never changes "último avistamento"; confirming it does.
5. merge(A→B) then unmerge → `derive_state` equals the pre-merge states of A and B.
6. Two sightings 230 m / 3 h apart, same coat/size, community dog → score in the "ask" band, not auto-confirmed.

## Open questions

- Multi-animal relatos (a litter, a pack): one caso per animal, or a group caso? (Wildbook: one annotation per animal.)
- Should `chain_state` be a materialized projection updated by jobs, or a SQL view at first? (KISS: view until it hurts.)
- Partition `observation` by `recorded_at` month from day one, or at ~10M rows?
