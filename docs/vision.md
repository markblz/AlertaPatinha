# Vision

## The moment this exists for

Someone walking to the bus sees a thin caramelo limping near the padaria. Today
they photograph it, post in two Facebook groups and a WhatsApp group, and move
on. The posts scroll away. Six hours later someone else sees the same dog two
blocks away and starts from zero. A protetora 800 m away never hears of it. A
guardian three bairros over is searching for exactly this dog.

Alerta Patinha turns that scattered moment into **one caso** with a timeline,
on a map, that the right nearby people actually see — and tells everyone who
helped how it ended.

## What makes it different

- **Relatos, not posts.** Structured (photo + place + time + a few taps), so
  they can be searched by place and time, deduplicated and linked.
- **Casos as living chains.** Sightings of the same animal accumulate as blocos
  on a timeline instead of becoming new, disconnected posts.
- **Honest maps.** Every point says whether it is exact or approximate.
  Sensitive places (homes, feeding points, colonies) are never exposed.
- **Specific, nearby, time-boxed asks** instead of broadcast — "Você está a
  400 m. Pode ir ver? (expira em 30 min)".
- **Closing the loop** is a product feature: every contributor gets the ending.

## Who it serves

| Persona | Needs | Risk to manage |
|---|---|---|
| Passer-by (most users, T0/T1) | Report in < 30 s, no login, on a cheap Android on prepaid data | Drops off at any friction; never returns if nothing happens |
| Guardian of a lost pet | Search sightings by place/time; alert nearby; avoid scams | "Found your pet, send Pix" extortion |
| Protetor(a) independente | See relevant cases in their territory; coordinate; not drown | Burnout from being the default sink for every case |
| ONG | Triage, intake capacity, credibility | Overload; fake profiles using their name |
| CCZ / zoonoses | Hotspots, poisoning clusters, official channel | Distrust from protetores; liability |
| Moderators | Fast triage, takedown, abuse handling | Exposure to graphic content |

## Goals

1. Make a first relato possible in **three steps** (foto → local → enviar), no account.
2. Turn repeated sightings into **one caso** with a trustworthy timeline.
3. Show a **live map** where location precision is explicit and privacy-safe.
4. Get the **right nearby people** to act, without pile-ons or nobody-goes.
5. **Close the loop** on every caso that ends.
6. Work at **national scale** on low-end phones and thin data plans.
7. Later: accept relatos via **WhatsApp** and suggest matches from **photos**.

## Non-goals (for now)

- Adoption marketplace, pet social network, vet booking, product sales.
- Handling money (donations, rewards, vaquinhas) — see anti-goals.
- Replacing ONGs/CCZs; the platform routes and coordinates, it does not shelter.
- Native apps before the PWA proves the loop (ADR-0009).

## Anti-goals — it fails even if it "works" when…

- …it **exposes** a reporter's home, a feeding point or a colony, or helps
  thieves find valuable dogs.
- …it becomes a **vigilante board**: naming, photographing or locating alleged
  abusers. (Denúncias go privately to authorities.)
- …it enables **scams**: fake finders, fake rescues, look-alike Pix keys.
- …it **burns out protetores** by routing every case to the same few people.
- …it **auto-merges** identities and tells a guardian their dog was found
  when it wasn't.
- …it rewards **volume over truth** (points, leaderboards, streaks).

## Success metrics (north stars and guards)

| Metric | Why |
|---|---|
| % of casos with a resolution (`resolved` with an encerramento) | The loop actually closes |
| Median time from emergência relato to first "Estou indo" | Help arrives |
| % of first-time reporters who file a second relato within 90 days | Closing the loop works |
| % of relatos that join an existing caso (vs. duplicates) | Chains work |
| Protetor active caseload p90 vs. cap | Burnout guard |
| Exact-location exposures outside policy (must be 0) | Privacy guard |
| Scam reports per 1,000 casos | Abuse guard |

## Key bets (to validate early)

- Brazilians will report into a structured form if it is faster than a
  WhatsApp group post. Pilot in one city before scaling (cold start is local).
- WhatsApp intake (M5) is the real growth channel; the PWA is the source of
  truth and the map.
- Verified ONGs/CCZs anchor trust in each city.

Evidence: `docs/research/` · Behavioral mechanisms: `docs/product/behavioral-design.md`.
