# Location privacy

Owner module: `geo` (pure policy, no dependencies). Evidence:
[spatiotemporal notes §5–6](<../research/research_notes/Stray pet platform research/spatiotemporal_chains.md>),
[trust & safety](<../research/research_notes/Stray pet platform research/game_theory_trust_safety.md>),
[compliance](../compliance.md).

## Key invariant

> No data the server sends to a viewer lets them locate a point more precisely
> than that viewer's access allows — not in one response, not by combining many.

**Main failure mode:** leaks by *combination* rather than by a single field —
fresh noise averaged over repeated reads, a reporter's trail across many
relatos, exact timestamps, small-count aggregates, EXIF in a photo, an exact
point inside a Centrifugo payload that the REST API correctly masks.

## Threat model

| Adversary | Wants | Main defence |
|---|---|---|
| Thief of valuable/purebred dogs | Where a specific animal sleeps | Sensitive-animal class → coarse cell + publication delay |
| Poisoner of colonies / "nuisance" neighbours | Feeding points, colonies | Colony/comunitário → res-7 or hidden; exact only with mantenedor approval |
| Stalker / harasser of a reporter | Reporter's home, routine | Zonas privadas; reporter identity not public; no per-reporter public trail |
| Scammer ("achei seu pet, manda Pix") | Contact + details of lost-pet guardians | Masked relay; hidden "sinais secretos" (see behavioral-design) |
| Scraper | Bulk export of the map | Rate limits; bbox size caps; aggregates at low zoom |

## Precision model

`display_mode ∈ {exact, approximate, hidden}` is decided **once, at write time**,
from `(caso/relato type, privacy_class)`. The result is stored
(`display_cell`, `display_geom`) and never recomputed per request.

| Relato context | Public display (T0–T2) | Notes |
|---|---|---|
| Emergência in a public place | approximate, **H3 res-9** (~0.105 km², r≈183 m) | Exact to alerted helpers, claimers, T3/T4 in area. **No public exact** — it reveals where the reporter stands, live. |
| Perdido (guardian's last-seen) | approximate res-9 | Guardian chooses; never their home address |
| Avistamento / achado of a possibly lost pet | approximate res-9 | |
| Comunitário (cão/gato comunitário) | approximate res-8 (~0.74 km²) | |
| Colônia / feral | approximate **res-7** (~5.2 km²) or hidden | Exact only with mantenedor (T3) approval, logged |
| Sensitive animal (valuable breed flag) | res-7 + publication delay | Delay length: design call for pilot (e.g., 12–24 h) |
| Inside any zona privada / near reporter's declared home | res-7 or hidden | Never finer, for anyone but the zone owner and staff |
| Aggregates (heatmap, zoomed-out counts) | res-6 counts, suppress cells with count < k | k = 3 initially (design call) |

Privacy classes (`privacy_class`): `public_place`, `near_reporter_home`,
`private_zone`, `colony`, `community`, `sensitive_animal`. Most restrictive wins.

## Who may see exact coordinates

| Viewer | Exact access |
|---|---|
| Reporter | Their own relato |
| T1/T2 helper | Only while alerted for, or holding an active claim on, that caso; ends on resolution/expiry |
| T3 protetor/mantenedor | Inside their declared territory; colonies need mantenedor approval |
| T4 org (ONG, CCZ) | Inside their service area |
| Staff (moderação) | With a recorded purpose |
| Everyone else | Never |

Every serialization of an exact point writes one `geo.location_access_log`
row: `(viewer_id, tier, observation_id, purpose, at)`. Append-only.

## Time is location too

- Public `valid_time` is coarsened: emergência → hour; others → part of day
  ("ontem à tarde"). `recorded_at` is never public at full precision —
  iNaturalist's documented leak was exact dates in the API.
- Sensitive classes get a publication delay before appearing on the map.

## Serialization contract (how the invariant is enforced)

1. `true_geom` lives in a column only `geo`/`observations` repositories read.
   ORM-to-schema mapping for public endpoints never includes it.
2. `geo.public.view_for(observation, viewer) -> LocationView` is the ONLY way
   to produce coordinates for output. API schemas accept `LocationView`, never
   a raw geometry.
3. Realtime payloads are built from the same `LocationView` with the
   *public* viewer: subscribers get public precision; exact access is an
   authenticated REST call that writes the access log.
4. **Contract tests**: for each endpoint and each realtime payload type,
   render with a T0 viewer and assert that every coordinate falls on the
   allowed geometry (cell boundary / hidden) and that no field (including
   nested `attributes`, photo URLs, EXIF) carries more precision.
5. Photos: EXIF stripped from every public variant (photo-pipeline.md).

## Map visual language

- Exact → pin. Its GPS accuracy (`loc_accuracy_m`) as a uniform, bordered
  circle (the most accurately read uncertainty encoding in McKenzie 2016).
- Approximate → hex cell outline + light fill, **no centre dot** (people read
  the centre of an uncertainty shape as the true spot).
- Hidden → not on the map; caso still reachable by link with "local protegido".
- The legend is always visible (`apps/frontend/features/map/PrecisionLegend.tsx`).

## Rejected alternatives

| Alternative | Why not |
|---|---|
| Fresh random noise per request/report | Averaging repeated reads recovers the point |
| Geo-indistinguishability (Andrés 2013) | Protection-level noise ≈ 289 m mean shift; half of lost cats are found within 50 m — destroys search value |
| Donut masking | Under-protects where population density varies (normal in Brazilian cities) |
| Public exact pin for emergencies (opt-in) | Reveals reporter's live position; helpers who need it get it anyway (logged). Revisit with pilot data. |
| iNaturalist 0.2° cells (~500 km²) | Far too coarse for animals whose relevant radius is 50 m–2 km |

## Core logic to implement (owner first, then review)

```python
# src/geo/domain/ — pure functions, no I/O
def classify_privacy(point, reporter_home, private_zones, relato_kind, animal_flags) -> PrivacyClass
def display_for(point, privacy_class, relato_kind) -> Display  # mode, h3 cell, boundary geom (stable)
def can_see_exact(viewer: Viewer, observation: ObservationGeoFacts, context: AccessContext) -> bool
def view_for(observation, viewer, context) -> LocationView      # the only output path
```

Acceptance examples (turn into tests):
1. Same point classified twice → identical `display_cell` (stability).
2. Point 120 m from the reporter's declared home → `near_reporter_home` → res-7.
3. Colony relato viewed by T3 without mantenedor approval → approximate res-7, no log row.
4. Emergency viewed by a T1 helper holding an active claim → exact + one log row; after claim expiry → res-9, no row.
5. A point inside two private zones of different owners → hidden for everyone but each zone's owner and staff.
6. 100 public reads of the same relato → 100 identical geometries.
