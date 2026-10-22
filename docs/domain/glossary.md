# Glossary — ubiquitous language

UI speaks PT-BR; code speaks English. One concept = one word in each, always.
If a new concept appears, add it here before naming a table or a screen.

| PT-BR (UI) | Code | Definition |
|---|---|---|
| **Relato** | `observation` | One person's immutable record of seeing an animal at a time and place, usually with a photo. Never edited after creation; corrections are new events. |
| ↳ Avistamento | `kind=sighting` | "I saw this animal here." No action implied. |
| ↳ Emergência | `kind=emergency` | Animal at risk now (injured, trapped, in traffic, being harmed). Carries urgency answers and triggers alerts. |
| ↳ Perdido | `kind=lost` | A guardian reports their own missing pet (last seen place/time). |
| ↳ Achado | `kind=found` | Someone is holding / has sheltered an animal and looks for its guardian. |
| **Caso** | `chain` | Revisable hypothesis that several relatos concern the same animal (or the same situation). Has a status, a state and a timeline. Users call it "caso"; the code calls it chain. |
| ↳ Tipo do caso | `chain.status` | `emergency`, `lost_pet`, `community` (cão/gato comunitário), `colony_feral`, `unknown`. Drives radii, decay and privacy defaults. |
| ↳ Situação | `chain.state` | `open → active → stale → dormant → resolved / archived`, or `merged`. See data-model.md. |
| **Bloco** | `chain_event` | One entry in a caso's timeline: relato linked, "visto de novo", status change, vet visit, "Estou indo", resolution, correction, merge/split. Append-only. |
| **Elo** | `chain_link` | Association relato ↔ caso with a state: `suggested`, `asserted`, `confirmed`, `rejected`, `retracted`. Each row records method (`reporter`, `model`, `crowd_vote`, `moderator`), actor and evidence. |
| "É o mesmo animal?" | link review | Human-in-the-loop card asking reporters / caso members to confirm or reject a suggested elo. |
| **Linha do tempo** | caso timeline | Ordered blocos of a caso, by valid time, with transaction time shown on demand. |
| **Conversa** | `conversation` | Chat attached to one caso. Messages persist in Postgres; delivery via Centrifugo. |
| **Alerta** | `alert` | Geo-targeted, time-boxed ask sent in waves to nearby helpers for a specific caso. |
| **Estou indo** | `claim` | A helper's commitment to act on a caso. Expires; expiry re-opens the ask. |
| **Área de interesse** | `watch_area` | Where a user wants to hear about cases (home, route, protetor's territory). |
| **Zona privada** | `private_zone` | User-declared sensitive place (own home, feeding point, colony). Relatos inside it are never shown precisely. |
| **Precisão** | `display_mode` | `exact` (pin), `approximate` (H3 cell, no centre dot), `hidden`. Always shown on the map. |
| **Nível de confiança** | `trust_tier` | T0 anônimo · T1 telefone verificado · T2 colaborador com histórico (private, outcome-scored) · T3 protetor/mantenedor verificado (individual, has a territory) · T4 organização verificada — ONG (CNPJ) or CCZ (service area). Gates exact location and some actions. Moderação/staff is a **role**, not a tier. |
| **Protetor(a)** | `role=protector` | Independent animal rescuer/caretaker. T3 after vouching + staff review. |
| **ONG** | `org(kind=ngo)` | Verified animal-welfare organization (CNPJ). Members act as T4 inside its service area. |
| **CCZ / Zoonoses** | `org(kind=public_agency)` | Municipal zoonoses / animal-welfare agency. Members act as T4 inside its service area. |
| **Encerramento** | `resolution` | How a caso ended: `reunited`, `adopted`, `in_care`, `treated_released`, `deceased`, `not_found`, `duplicate`. Triggers the close-the-loop notification to every contributor. |
| **Denúncia** | `abuse_report` | Private report of maus-tratos routed to authorities. Never public, never on the map. |
| Validade / quando viu | `valid_time` | Interval when the animal was seen + `time_precision`. Distinct from `recorded_at`. |
| Registrado em | `recorded_at` | Server time the row was written (transaction time). |
| Frescor | freshness | 2^(−Δt/h) relevance of a location, h = half-life by caso type. |
