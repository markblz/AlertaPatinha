# Behavioral Design — Alerta Patinha

> Status: draft v0 · 2026-10-21 · Sources: `docs/research/research_notes/Stray pet platform research/`.
> Link labels: **PP** = participation_psychology, **GT** = game_theory_trust_safety, **PA** = prior_art_brazil_context, **ST** = spatiotemporal_chains.

## 1. Purpose and how to use this doc

- This doc turns the participation-psychology and trust-and-safety research into mechanisms a builder can ship, measure and remove. It covers behavior: who reports, who acts, who comes back, who abuses. Data model, ML and stack are covered in other docs.
- Each principle (P1–P16) is one buildable unit: **Evidence → Mechanism → Metric → Failure mode → Phase** (MVP / v2 / later). Read the failure mode before you build; it names the test case.
- Evidence grades are the notes' own: strong / moderate / weak / contested / classic / unverified. *Borrowed* marks evidence from another domain (CPR dispatch, 311, Wikipedia, citizen science, education). Nearly all of it is borrowed, because no controlled study of an animal-emergency platform exists ([PP §7][pp7]).
- "(design call)" marks our own inference. Every parameter is a hypothesis that §6 calibrates. Plan for small effects: US nudge-unit effects are about 1/6 of published academic ones ([PP §3][pp3]).

| PT-BR (UI) | Code | Meaning |
|---|---|---|
| Relato | `observation` | Immutable record of an animal seen at a time and place. Kinds: avistamento, emergência, perdido (tutor's own pet), achado (holding a found animal). |
| Caso | `chain` | Revisable hypothesis that several relatos concern one animal or situation. Timeline of Blocos. |
| Bloco | `chain_event` | One timeline entry: relato linked, status, vet visit, "Estou indo", desfecho. |
| Elo | `chain_link` | Relato↔caso association: sugerido / afirmado / confirmado / rejeitado / retratado. The system suggests and humans confirm. |
| Conversa | `conversation` | Chat for one caso. |
| Alerta | `alert` | Geo-targeted notification sent in waves; "Estou indo" claim with expiry. |
| Zona privada | `private_zone` | Home or feeding point the user declares. Never shown precisely. |
| Nível de confiança | `trust_tier` | T0 anônimo · T1 telefone verificado · T2 colaborador com histórico · T3 protetor/mantenedor verificado (territory) · T4 organização verificada: ONG (CNPJ) or CCZ (service area). Moderação is a staff role. |
| Precisão de local | — | exata / aproximada / oculta. |

## 2. Design stance

- **Closing the loop beats gamification.** Sending outcome photos to contributors is the best-evidenced retention lever (P5). Points, leaderboards and streaks are weak or harmful (P6).
- **Nearby, specific, personal asks beat broadcast.** Alert a few nearby helpers with one concrete task, widen in waves until enough people accept, then stop (P3, P4).
- **Two products, one platform.** Most people contribute once, and about 10% do about 80% of the work ([PP §1][pp1]). So: a ~10-second flow for the many, and a case tool for the core. Optimize for the *second* relato, not for engagement (P1, P5, P8).
- **Private, outcome-scored reputation beats public scores.** Reputation decides who gets alerted first and how much a vote weighs. It is never shown as a number or a rank (P6, P11).
- **Humans confirm identity.** The system suggests Elos and people confirm them. Never auto-merge, and never auto-reject a newcomer's relato (P2, P16).
- **Abuse-resistance by default.** Invariant: no public data lets a stranger find a specific home, colony or valuable animal at full precision. No money moves through the platform. The crowd is never pointed at people (P13–P15).
- **Measure resolution, not activity.** Count animals reached, transported and reunited. Never reward publishing speed or volume, which was Citizen's KPI trap ([GT §3][gt3]).

## 3. Principles

### P1 — Primeiro relato sem login: foto → local → enviar

- **Evidence**
  - The announced length was the strongest predictor of survey breakoff. A 30-min survey had ~40% higher breakoff than a 10-min one (moderate; borrowed: surveys) — [Galesic, via PP §3][pp3].
  - Most contributors take part only once; 17–40% (avg 27%) come back a second time (strong; borrowed: Zooniverse) — [Sauermann & Franzoni 2015][pp1]. Colab in Saquarema: 6,902 downloads vs 1,392 requests in one year (weak) — [PP §1][pp1].
  - 65% of Brazilian internet users are phone-only, and 39% ran out of data in the last 3 months (TIC Domicílios 2025) — [PA §4][pa4].
- **Mechanism**
  - The camera opens directly. Photo → device location (pin can be dragged) → "Enviar". Header copy: "Leva 10 segundos."
  - After sending, everything is optional and skippable: "O animal está ferido ou em perigo?" [Sim, é emergência] [Não], then kind chips (avistamento / perdido / achado), species and condition.
  - The contact ask is framed around the outcome, not an account: "Quer saber o que aconteceu com esse animal?" → phone OTP → T1. Without a phone, the user gets a follow link tied to the device (design call).
  - T0 relatos are never blocked. They are rate-limited per device, go into a soft queue ("precisa de confirmação") and start with a lower confidence prior (P11). A T0 emergência still fires wave 1, labeled "relato anônimo" (design call; Q3).
  - Images are compressed on the device, uploads resume after interruption, and relatos queue offline ([PA §4][pa4]). The later WhatsApp intake keeps the same 3-step contract.
- **Metric:** camera-open → enviar completion; median time to enviar; % of T0 relatos that add a phone; second-relato rate (P5).
- **Failure mode:** anonymous spam and fake emergências (rate limits, soft queue, private reputation); no contact channel, so the loop can't close; thin relatos without species (enrich later with ML or people).
- **Phase:** MVP (app/PWA). WhatsApp intake later (Q1).

### P2 — Duplicado vira contribuição

- **Evidence**
  - In a FixMyStreet trial, reporters were offered a subscription to an existing nearby report instead of filing a duplicate (weak, practitioner; borrowed: 311) — [mySociety 2019, PP §3][pp3].
  - On Wikipedia, more good-faith newcomers were rejected, and that rejection predicts the decline. Replicated on 769 wikis (strong; borrowed: Wikipedia) — [Halfaker 2013][pp1], [GT §1][gt1].
  - iNaturalist identity consensus needs >2/3 agreement and ≥2 IDs, and can be revoked later (moderate) — [GT §1][gt1]. Casos are revisable hypotheses and are never auto-merged — [ST §2][st2].
- **Mechanism**
  - A relato is always saved as its own immutable record. If open casos fall inside the space-time gate for that kind ([ST §7][st7]), show up to 3 cards: "É este animal? Adicione sua foto ao caso." [Sim, é ele] [Não, é outro] [Não sei].
  - "Sim" creates an `afirmado` Elo plus a "novo relato" Bloco. "Não sei" creates a `sugerido` Elo for caso members to vote on. "Não" opens a new caso.
  - An Elo becomes `confirmado` when the tutor of a perdido caso, a T3 on the caso, or ≥2 independent T2+ voters with >2/3 agreement confirm it. This combines GT B3 and ST §7 (design call). The same quorum sets `rejeitado`; the person who asserted the link can set `retratado`. Other people's votes stay hidden until you vote, to prevent herding.
  - Only `confirmado` Elos move the caso's "último avistamento" marker ([ST §7][st7]).
  - The confirmation message gives credit and never corrects: "Seu relato virou o Bloco 7 do caso do Thor." The UI never says "duplicado" or "já foi relatado".
- **Metric:** % of in-gate relatos linked vs. starting a new caso; Elo precision (confirmado / (confirmado + rejeitado)); rate of later caso merges (duplicates we missed); second-relato rate for first-timers whose relato was linked vs. not linked.
- **Failure mode:** lookalike cats at colonies cause transitive over-merge (check pairwise against the caso's representative photos; merges are reversible); social pressure to tap "Sim" (keep "Não sei" first-class); the reporter feels absorbed into someone else's caso (attribution, P5).
- **Phase:** MVP (suggestions from place and time, human votes). v2: the re-ID score counts as one voter with capped weight.

### P3 — Alertas por proximidade, em ondas, até alguém aceitar

- **Evidence**
  - Stockholm RCT: dispatching volunteers within 500 m raised bystander CPR from 48% to 62% (+14 pp), with no survival difference (strong; borrowed: CPR dispatch) — [Ringh 2015][pp2].
  - Responder funnel for 1,985 alerted volunteers: 75.6% saw the alert, 37.7% accepted, 27.1% arrived, 14.3% gave care (moderate; borrowed) — [Monash survey][pp2]. Victoria GoodSAM alerts the 3 nearest within 400–500 m (metro) and keeps alerting until 3 accept (moderate) — [MJA 2025][gt3].
  - Personalized help requests on Facebook got more responses, with no diffusion effect across group sizes (weak–moderate) — [Fatkin & Lansdown][pp2]. Compassion fade starts at the 2nd victim (moderate) — [Västfjäll 2014][pp2].
- **Mechanism**
  - Wave 1 goes to the K nearest T1+ helpers with Disponibilidade on, inside ring r0. Stop when N accept, with N = 1–3 depending on severity (GT C1). If N isn't reached in T minutes, widen the ring and raise K. After the last ring, escalate to the T3/T4 on duty (ONG, CCZ).
  - The notes disagree on ring size. GT C1 starts at ~300–500 m in urban areas; ST §7 gives 2–5 km for emergências, doubling after each missed target. We start with the small ring and use ST's range as the ceiling (design call; E3). Perdido cats get smaller radii (ST §7: indoor cat 500 m).
  - Each alert covers one animal and one concrete micro-task: "Cão ferido a ~400 m. Pode confirmar se ainda está lá e mandar uma foto?" [Estou indo] [Não posso agora]. The caso lists a ladder of roles: confirmar · fotografar · água/comida · transporte · lar temporário.
  - "37 animais precisam de ajuda perto de você" is never a call to action.
- **Metric:** per-alert funnel enviado → visto → aceito → chegou → ajudou; time to first accept; % of emergências that reach N per ring; alerts sent per helper who acted (Monash ≈7 as a CPR baseline, [PP §2][pp2]; expect worse for animals).
- **Failure mode:** alert fatigue and opt-outs (P7 budget); swarms in the dense centro (cap, then stop); nobody responds in periferias (escalation); helpers sent into unsafe sites (safety tips before dispatch, never routed into a human conflict, GT C5).
- **Phase:** MVP (fixed rings, manual escalation). v2: r0/K/T adapt per area, and ordering within the P8 load cap uses reliability.

### P4 — "Estou indo" com prazo: nem multidão, nem ninguém

- **Evidence**
  - London GoodSAM 2023/24: 22.4% of alerts were accepted, and 47.5% of those who accepted never arrived (moderate; borrowed: CPR) — [LAS report][gt3].
  - A top reason for declining was "mission no longer available" (moderate; borrowed) — [BMC 2025][pp2]. HeartRunner tells accepters who drift out of range that they are no longer needed (moderate) — [GT §3][gt3].
  - In the lab, bystanders reduce helping (g = −0.35, strong). In CCTV of 219 real public conflicts, someone intervened in ~9 of 10, and more often when more people were present (strong, observational) — [Fischer 2011; Philpot 2020][pp2].
- **Mechanism**
  - "Estou indo" creates a Bloco with an ETA and reveals the exact location to the claimer (P13). The caso header shows live state: "Ninguém a caminho · você é a pessoa mais próxima" / "Ana está indo · chega em ~15 min".
  - At most 2 concurrent claims (GT C2). Once N is reached, pending alerts are withdrawn: "Já tem gente indo. Obrigado por estar disponível."
  - At the ETA: "Ainda a caminho?" [Cheguei] [Preciso de mais tempo] [Não vou conseguir]. With no check-in by ETA + buffer, the claim expires, the header goes back to "ninguém a caminho" and the next ring is alerted.
  - Releasing a claim before expiry costs nothing. A silent expiry only feeds private reliability (P11). If nobody has accepted after the last ring, escalate to an institution and show honest status (P5).
- **Metric:** claim → arrival rate; % of claims that expire silently; % of emergências with 0 arrivals within the target time ("ninguém foi") and with more than N arrivals (pile-on); time from relato to first arrival.
- **Failure mode:** claim-and-abandon blocks others (TTL); punitive scoring deters claims (keep scoring private and forgiving); a territorial protetor claims a caso to block others (expiry, plus the disputa button in P16); fake "Cheguei" (location ping on check-in, design call).
- **Phase:** MVP.

### P5 — Fechar o ciclo: foto do desfecho para todos que ajudaram

- **Evidence**
  - FixMyStreet (n = 399,364): a successful first experience was associated with a 57% higher probability of filing a second report (strong for association, observational; borrowed: 311) — [Sjoberg 2017][pp4].
  - Boston: residents shown photos of the city fixing their own requests made 60% more requests, across 38% more categories, over 13 months. Showing the backlog did not lower trust (strong; borrowed: 311) — [Buell 2021][pp4].
  - Petco Love Lost: posters confirm only ~1/3 of reunions (weak, search summary) — [PA §1][pa1]. About 20% of Brazilians trust local government (strong) — [OECD 2023][pp6].
- **Mechanism**
  - Every desfecho Bloco (no veterinário · em lar temporário · adotado · voltou para o tutor · óbito) asks for a photo. The photo is pushed to everyone who has a relato or Bloco on the caso, with attribution: "Sua foto de 14/10 ajudou a localizar o Thor." For óbito, notify without a photo; details are opt-in (design call).
  - Feedback is tiered, following Toronto's 311 plan (weak): avistamento → "Adicionado ao caso X"; emergência → milestones; long casos → a periodic narrative.
  - Casos from first-time reporters are tagged "primeiro relato" and go to the top of responder queues.
  - Unresolved casos get honest status: "Ainda sem ajuda há 6 h — 3 pessoas notificadas." Never promise municipal action.
  - The tutor and claimers get a closure prompt: "O Thor voltou pra casa? [Sim, enviar foto] [Ainda não]".
- **Metric:** **North Star: share of first-time reporters who send a second relato within 90 days** (the 90-day window is a design call; the citizen-science baseline is ~27% return, [PP §1][pp1]). Also: % of casos with an outcome photo; time to first response for first-timers vs. veterans; confirmed-reunion rate.
- **Failure mode:** casos that go silent (auto-archive with an honest note); notification overload (P7); fabricated outcome photos (live-photo badge, P11); distress from sad outcomes (no graphic photo in pushes).
- **Phase:** MVP.

### P6 — Reconhecimento: agradecimento entre pessoas, sem pontos

- **Evidence**
  - Randomized, purely symbolic awards raised Wikipedia newcomer retention for four quarters (strong; borrowed: Wikipedia) — [Gallus 2017][pp1]. Barnstars given to 200 top editors raised their productivity ~60% over 90 days (strong, narrow sample) — [Restivo & van de Rijt 2012][pp1].
  - Badges, points and leaderboards had no significant effect on learning (moderate; borrowed: education), and only ~5–30% of users respond to badges (moderate). Broken streaks cause drop-off (moderate–strong) — [PP §1][pp1].
  - Contingent incentives predict quantity and intrinsic motivation predicts quality (strong, k = 183) — [Cerasoli 2014][pp1]. Moving feedback from private to public inflated perfect ratings from 33% to 85% (strong) — [Filippas & Horton][gt1].
- **Mechanism**
  - An "Agradecer" button on every Bloco, with an optional one-line note. It arrives as a push and is kept on the caso under "Agradecimentos". At desfecho, the resolver is prompted: "Quer agradecer quem ajudou?", listing every contributor, including avistamento authors.
  - A private profile page, "Animais que você ajudou", lists casos with their outcome photos. Only the user sees it, and they can share it if they choose. No totals are shown to others.
  - Badges exist only for verified roles (T3/T4). They show status, not rank.
  - Never build points, levels, leaderboards, streaks or public counts of rescues.
- **Metric:** thanks per resolved caso; 90-day retention of thanked vs. unthanked newcomers (E6).
- **Failure mode:** thanks go only to visible protetores (the prompt lists all contributors); thanks become clique currency; a count of animals helped turns into a de facto score and a hoarding incentive (keep it private, and never count "animais recebidos").
- **Phase:** MVP (thanks, history). v2: E6.

### P7 — Orçamento de notificações

- **Evidence**
  - Users receive a median of 56 notifications a day (n = 278) (moderate) — [Pielot 2018][pp3].
  - RCT (n = 237): batching notifications 3×/day improved attention, mood and sense of control. Hourly batching was about the same as control. Turning notifications off entirely raised anxiety and FoMO (moderate–strong; borrowed: general phone use) — [Fitz 2019][pp3].
- **Mechanism**
  - Real-time push is reserved for (a) Alertas inside your radius while Disponibilidade is on, and (b) your own casos and claims: an expiring claim, a reply to your relato, a desfecho.
  - Everything else goes into a digest, at most 1–3 per day ([PP §3][pp3]; default 1, design call).
  - Each user has a daily alert budget, quiet hours, a radius setting and per-caso mute (GT C1). Notifications default to on, never "all off".
  - Running out of budget never silences prompts about your own claims. Escalations go to the next helper instead of hitting the same person twice.
- **Metric:** mutes, opt-outs and uninstalls vs. alerts received per week; alert "visto" rate; actions taken from digests.
- **Failure mode:** the budget suppresses the one alert that mattered (next-helper routing); a digest is too slow (only non-urgent items go there); WhatsApp template costs later.
- **Phase:** MVP.

### P8 — Proteger o núcleo: limite de casos, disponibilidade, carga distribuída

- **Evidence**
  - For shelter volunteers, open-intake policies were the biggest stressor; euthanasia was not linked to compassion fatigue (moderate; borrowed: shelters) — [Faunalytics][pp2]. Perceived support goes with lower burnout, τb = −.230 (weak) — [Kennesaw][pp2].
  - Volunteers dispatched by app show psychological impact, and debriefing is recommended (moderate; borrowed: CPR) — [Kragh 2021][gt3].
  - Curitiba: 113 confirmed hoarding cases (36.3% involving animals), clustered in dense, lower-income areas (strong) — [Cunha 2017][gt4]. Protetores in Alagoa Grande (PB) assist ~18 animals each and earn ≤2 minimum wages (weak) — [PP §2][pp2].
- **Mechanism**
  - Disponibilidade is opt-in, with modes "disponível", "só transporte", "só castração", "lotada" and "pausa". Flags expire on their own and ask to be refreshed (GT C4).
  - Each T2/T3 helper has a caseload cap. It is configurable, and the default is set with the pilot protetores (design call). Routing skips anyone at their cap.
  - Routing spreads the load: within a ring, helpers with fewer active casos come before more reliable ones (design call). Otherwise reliability-first ordering (GT C2) would pile alerts onto the best people.
  - "Pausa" carries no guilt: "Pausa ativada. Seus alertas param até você voltar." "Passar o caso" hands the caso off with a Bloco, and leaving a caso takes one tap. Emergência claimers get a check-in after the caso, with links to support resources (GT C5).
  - Hoarding welfare signal: an account that keeps taking animals in with no adoption, transfer or vet outcomes gets a confidential staff check. It is never public (GT F9).
- **Metric:** Gini of active casos across T2/T3 helpers per city; % of helpers at cap; 90-day churn of T3 helpers; pausa → return rate.
- **Failure mode:** caps in sparse areas leave nobody to go (escalate to institutions, show honest status); guilt-tripping in the Conversa, e.g. "cadê as protetoras?" (norms, P16); stale flags.
- **Phase:** MVP (disponibilidade, pausa, handoff, cap). v2: load-aware routing, Gini dashboard, hoarding signal.

### P9 — Foto de identificação pública; foto do ferimento sob toque

- **Evidence**
  - Meta-analysis of 12 studies: content warnings raised anticipatory anxiety and had only trivial effects on distress (d = 0.02) and avoidance (d = 0.06) (moderate–strong) — [Bridgland 2023][pp5].
  - Instagram-style blur screens raised anxiety whether or not people uncovered the image, and most uncovered it anyway (moderate) — [Flinders][pp5]. Whether blur helps moderators is contested — [PP §5][pp5].
  - There is no study of graphic stray-animal photos and willingness to *physically* help. Faunalytics calls the evidence insufficient (weak) — [PP §5][pp5].
- **Mechanism**
  - Photos have two roles. The "foto de identificação" (face or body) is public and feeds re-ID. The "foto do ferimento" is an attachment. The emergência flow asks: "Agora uma foto do rosto ou do corpo inteiro."
  - An injury photo is a media item with `sensitive=true` (rules in `docs/domain/photo-pipeline.md`). Injury photos never appear on the map, in feeds, in alert previews or on share cards. Claimers and T2+ caso members can open them with a tap, labeled "Foto de ferimento — para triagem".
  - The tap exists for consent and context. It does not protect against distress, and we don't present it as a safety feature.
  - The share card (OpenGraph, for WhatsApp) shows the ID photo, the status and a concrete need: "Precisa de transporte até 18h".
- **Metric:** % of emergências with an ID photo; how often responders open injury photos; distress complaints; E8.
- **Failure mode:** the reporter uploads only the wound (prompt for another photo; a moderator can recrop); hiding wounds lowers triage quality (responders always have access); treating blur as a solved problem.
- **Phase:** MVP.

### P10 — Blocos primeiro, conversa depois: conter a indignação

- **Evidence**
  - Each moral-emotional word raised retweet diffusion by ~20% across 563,312 tweets (strong for political Twitter; transferring it here is an inference) — [Brady 2017][pp5].
  - 49% of Brazilian donors stopped giving after negative news (moderate) — [PDB 2024][pp6]. Protetores tend to reject professionalization and work through gift relations (moderate, qualitative) — [Osório 2016–17][pp2].
- **Mechanism**
  - Caso page order: header (status, needs, who is going) → Bloco timeline → Conversa. One-tap actions create Blocos: "Ainda está lá", "Levei ao vet", "Preciso de transporte", "Desfecho".
  - The Conversa has pinned rules (P16) and rate limits for new accounts. Moderators can put flagged casos into "modo lento" (v2).
  - Share text is built from the structured fields and is about the action needed. There are no reshare counters and no outrage framing.
  - Accusations against people are sent to the P15 flow, not discussed in the Conversa.
- **Metric:** share of caso updates made as Blocos vs. messages; flagged messages per caso; resolution time vs. chat volume (observational).
- **Failure mode:** Blocos feel bureaucratic to gift-economy protetores (keep them one tap); outrage moves to Instagram (out of our control; we just don't amplify it); the chat turns into a turf fight (disputa, P16).
- **Phase:** MVP (Blocos, chat, rules). v2: modo lento, classifiers.

### P11 — Verdade sem pagar por ela: confiança que decai, foto ao vivo, reputação por desfecho

- **Evidence**
  - In Waze, a report stays visible longer or shorter depending on reactions: "Not there" shortens it, and unconfirmed reports expire (moderate). Only 26% of Waze crash reports matched official records (moderate) — [GT §2][gt2].
  - Peer prediction and BTS need large populations, a common prior and payments. In experiments they collapse into uninformative equilibria (strong) — [Gao 2014][gt2].
  - Scammers send AI-edited "found" photos of the owner's own pet (weak, several news cases) — [GT §5][gt5]. Fear of retaliation silences public negative feedback (strong) — [Tadelis 2016][gt1].
- **Mechanism**
  - `confiança(t) = prior(trust_tier, evidência) × decay(Δt, meia-vida por status) ± confirmações` (GT §2). Pins fade as confidence decays. Half-lives come from ST §7, e.g. emergência 2–6 h, colônia 60–90 d ([ST §7][st7]).
  - "Ainda está lá" / "Não está mais" votes are accepted only from users who are physically near and were there recently. Votes are weighted by private reputation and audit-logged.
  - Evidence ranking: "Foto ao vivo" (taken with the in-app camera, with device location at capture and server time) ranks above a gallery upload, which ranks above a forwarded or WhatsApp image (EXIF lost). Live photos get a badge. Gallery uploads are never blocked, only ranked lower.
  - When a caso resolves, each relato and claim is scored against the outcome with a proper scoring rule, shrunk toward the prior when outcomes are few. The score sets alert order and vote weight and is never displayed. T2+ users spot-check random samples.
- **Metric:** calibration (shown confidence vs. animal actually present on arrival); wasted-trip rate; share of live vs. gallery photos; vote-reversal rate.
- **Failure mode:** brigading "não está mais" to hide an animal (proximity, trust and audit); honest reporters penalized because animals move (score against what the reporter could have known); low-end phones ranked lower (never blocked).
- **Phase:** MVP (decay, proximity votes, live badge). v2: outcome scoring, weighted votes, image forensics.

### P12 — Níveis de confiança e resistência a Sybil

- **Evidence**
  - Without a logically central identity authority, Sybil attacks are always possible, and vouching fails without a trusted root (strong, foundational) — [Douceur 2002][gt1].
  - ILY (BH, 2023) validated profiles by WhatsApp number (weak) — [PA §2][pa2]. Ostrom's commons principles held up empirically in reviews (moderate) — [GT §1][gt1].
- **Mechanism**
  - Privileges unlock with verified outcomes, not with time or volume (table below). Vouching is never the only gate.
  - Rate limits are stricter for content containing phone numbers, Pix keys or URLs.
  - Resolved: ONGs and CCZs are T4 (organizations, service area); protetores are T3 (individuals, territory); moderação is a staff role, not a tier ([glossary](../domain/glossary.md)).
- **Metric:** abuse incidents (scams, fake emergências) by tier; median time for good-faith users to reach T2; % of cities with at least one T3/T4 anchor.
- **Failure mode:** SIM farms (device and behavior signals); excluding people without documents (T1 stays phone-only); a clique capturing T3 in a bairro (staff confirmation and term limits, GT F2); political turnover at the CCZ (the platform stays useful without government).
- **Phase:** MVP (T0, T1, manual onboarding for T3/T4). v2: automatic T2 promotion, vouching flow.

| Tier | Identity root | Unlocks | Still cannot |
|---|---|---|---|
| T0 anônimo | device | send relatos (rate-limited, soft queue); map at aproximada; follow own relato | chat, claim, vote, receive alertas |
| T1 telefone verificado | phone OTP (SMS/WhatsApp) | Conversa, "Estou indo", receive alertas, agradecer | weighted votes; exata without a claim |
| T2 colaborador com histórico | T1 + verified outcomes | weighted "ainda está lá" and Elo votes; propose links | merge/split casos |
| T3 protetor/mantenedor verificado | 2 T3 vouches + staff review | exata in own territory; mark comunitário; merge/split; routing flags | delete others' casos (flag only) |
| T4 organização verificada (ONG, CCZ) · staff role separate | ONG: CNPJ · CCZ: gov e-mail domain · staff: internal | receive escalations; takedown; override sensitive locations | — |

### P13 — Local é arma: aproximado por padrão

- **Evidence**
  - Colonies are repeatedly poisoned with chumbinho: BH (10 cats), Vila Isabel (≥10), Camaçari (8), Cariacica (10 dogs, 20 cats), Jundiaí (17 cats). There was armed theft of 6 purebred dogs in Guarulhos, and a fighting ring with 41 arrested (weak–moderate, news) — [GT §5][gt5]. No case yet links a platform's sightings to an attack; the risk is plausible but undocumented.
  - iNaturalist auto-obscures sensitive taxa to a 0.2°×0.2° cell (moderate) — [GT §5][gt5]. Fresh random noise on each request averages out to the true point, so masks must be stable — [ST §5][st5]. Ring's opt-out default drew a privacy backlash — [PA §1][pa1].
- **Mechanism**
  - Precision follows the table below. Users opt *up* to more precision; it is never opt-out.
  - EXIF is stripped on publish and kept server-side. Timestamps are coarsened for sensitive targets. Every read of an exata location is audit-logged ([ST §5][st5]).
  - "Comunitário" status (set by T3 or the mantenedor) turns off perdido/achado calls to action for that animal. A private owner-match path lets lost purebreds bypass the publication delay.
- **Metric:** % of relatos published at aproximada/oculta; a red-team test trying to reconstruct zonas privadas from the public API (pass/fail every release); time for claimers to locate the animal (does masking slow rescue?).
- **Failure mode:** too coarse to find the animal (exata on claim); breed-classifier errors (reporter or staff override); background landmarks leak location (blur option); well-meaning "rescuers" remove a comunitário animal (status flag, disputa).
- **Phase:** MVP.

| Situation | Public | Claimer / alerted helper | T3+ in territory |
|---|---|---|---|
| Default relato (avistamento, perdido, achado) | aproximada: stable cell (GT A1 ~300–500 m; ST res-9) | exata on claim | exata |
| Emergência in public space | aproximada (design call; GT A4 and ST §7 would show exata) | exata while active | exata; coarsens after desfecho (GT A4) |
| Colony, feeding point, comunitário, high-value or pit-bull-type breed | coarse cell (ST res-7 for colonies) + 6–24 h delay if not an emergency (GT A2) | exata for verified helpers only | exata |
| Inside a zona privada | oculta (aggregates only) | exata only if the reporter opts in | exata only if the reporter opts in |

### P14 — Defesa contra golpes: contato mascarado, sinais secretos, sem dinheiro

- **Evidence**
  - Golpe do pet perdido: a fake "finder" asks for R$100–150 by Pix and disappears. The 2026 variant uses AI-edited photos of the owner's own pet plus threats (weak, several news cases) — [GT §5][gt5]. Only 8.9% of money lost to Pix scams was returned (moderate) — [GT §5][gt5].
  - 234 look-alike Pix keys diverted donations during the RS floods (weak) — [GT §5][gt5]. Fake finders have hijacked owners' accounts with verification codes (weak) — [PA §1][pa1].
  - Advice across sources: keep identifying marks out of public posts and ask for a video call (weak) — [PA §1][pa1].
- **Mechanism**
  - The tutor's phone number is never public. All contact goes through the Conversa or a relayed number.
  - When creating a perdido relato, the tutor records 1–2 "sinais secretos" (a scar, a collar detail, a behavior), stored privately. Contact between achado and perdido unlocks only after the finder states or shows them (a photo of the mark, or a live video with a requested gesture).
  - Public photos are downsized and watermarked. High-res copies are kept for re-ID.
  - No money moves through the platform (repo invariant, CLAUDE.md rule 10): no Pix keys shown on casos, no vaquinhas, no escrowed rewards. A text label "Recompensa oferecida (paga só na entrega)" is allowed, with no amount field (design call).
  - Money patterns in the Conversa (Pix key formats, "manda pix", "taxa", "frete", "gasolina", "código") trigger an inline warning, and new accounts go to the staff queue. We warn but don't block: "Nunca pague antes de ver o animal pessoalmente. O Alerta Patinha nunca pede Pix nem código." The same banner appears on the first achado↔perdido contact.
- **Metric:** scam reports per 1,000 perdido casos; how often a warning leads the user to report or block; % of first contacts that pass the sinais-secretos check.
- **Failure mode:** scammers move the victim to WhatsApp (show the banner early); false positives when people discuss real vet costs (warn only); a genuine finder can't answer the secret marks (live-video alternative); donors still want to give (Q2).
- **Phase:** MVP (relay, sinais secretos, no money, pattern warnings). v2: classifier, image forensics.

### P15 — Nunca apontar a multidão para pessoas

- **Evidence**
  - Citizen app: a ~7-hour manhunt, a reward raised from $10k to $30k, a push to 848,816 users. The man was innocent, and LAPD cut ties (moderate) — [Vice on Citizen][gt3].
  - TJMG upheld R$4,000 against someone who accused a person of a crime and published their data in a dispute over a rescued dog, and awarded R$5,000 over a mistreatment video that vets later contradicted (moderate, court decisions) — [GT §5][gt5], [PA §5][pa5].
  - After the 2025 STF ruling, platforms are liable under notice-and-takedown, but crimes against honor still require a court order (legal analysis) — [PA §5][pa5]. Nextdoor's friction form claimed 75% fewer profiling posts (weak, company claim) — [GT §3][gt3].
- **Mechanism**
  - No names, faces, addresses or license plates of alleged abusers appear in any public content or Conversa. A caso is about the animal's needs.
  - "Denunciar maus-tratos" is a private, structured form (o quê, quando, onde, evidências). It is routed to the Delegacia, the MP or the municipal channel, can be exported for a BO, and is never published. Copy: "Sua denúncia vai para as autoridades, não para o público. Não podemos garantir a ação delas."
  - When a chat message combines accusation terms with a person identifier, it is held for review and the user sees: "Denúncias vão pelo botão Denunciar. Não publique nomes ou endereços."
  - No bounties, and no "procura-se" for people, ever.
- **Metric:** person-identifying content held per 1,000 messages; denúncias filed and forwarded; legal notices received.
- **Failure mode:** users feel silenced and vent elsewhere (accepted: our job is not to amplify); authorities don't act (honest copy); hoarding suspicions get posted publicly (route them to the P8 welfare check).
- **Phase:** MVP.

### P16 — Moderação: regras visíveis, remoções explicadas, notificação e retirada

- **Evidence**
  - RCT across 2,190 r/science discussions: posting the rules raised newcomer compliance by >8 pp and newcomer participation by ~70% (strong) — [Matias 2019][gt6].
  - Explaining removals lowered future removals, and bot explanations worked about as well as human ones. 37% of users didn't understand why their post was removed (strong/moderate) — [Jhaver 2019][gt6].
  - Over-aggressive quality control drives newcomers away (strong; borrowed: Wikipedia). Citizen measured staff by publishing speed and volume (moderate) — [GT §6][gt6].
- **Mechanism**
  - A rules card appears the first time someone enters any Conversa and on a newcomer's first caso: "Não divulgue endereço residencial · Não peça nem ofereça dinheiro · Denúncias de maus-tratos vão pelo botão Denunciar."
  - Every removal is explained, with a template, and a bot may send it: "Removemos sua mensagem porque tinha um endereço residencial (regra 1)." Newcomer content goes to soft queues and is never auto-deleted.
  - Moderation is split by harm class (GT §6). The community (T2/T3) handles links, duplicates, staleness and off-topic posts. Staff handle doxxing, accusations, fraud, extortion, impersonation, overrides of sensitive locations and hoarding.
  - Every item has "Denunciar conteúdo". Reports are triaged by severidade × confiança × exposição into an SLA queue with a decision log (notice-and-takedown).
  - Graduated sanctions: explicação → limite temporário → rebaixamento de nível → banimento. A "Disputa" button opens staff mediation. Veterans get reply templates for correcting newcomers kindly. Moderators are never measured on volume or speed.
- **Metric:** newcomer rule-violation rate; repeat removals after an explained removal; % of takedowns within SLA; % of held newcomer relatos released.
- **Failure mode:** banner blindness (rotate variants, E9); staff capacity during surges; territorial stewards weaponizing flags (stewards can flag but not delete).
- **Phase:** MVP.

## 4. Anti-patterns we will not build

- **Points per relato, global leaderboards:** they reward duplicates and bad photos, and show no significant effect in meta-analyses ([PP §1][pp1]).
- **Streaks:** emergencies are not a daily habit, and broken streaks cause drop-off ([PP §1][pp1]).
- **Public star ratings of protetores/ONGs:** ratings inflate, retaliation silences negatives, and turf wars escalate ([GT §1][gt1]).
- **Public counts of "animais resgatados/recebidos":** a Goodhart target that also rewards hoarding ([GT §1][gt1]).
- **Cash or material rewards per relato, bounties, escrowed rewards:** they push quantity over quality, invite fraud, and enabled Citizen's manhunt ([GT §3][gt3]).
- **Mandatory sign-up or long forms before the first relato:** stated effort drives breakoff ([PP §3][pp3]).
- **"Alguém ajuda!" broadcasts and "N animais perto de você" lists as the main call to action:** no specific ask, nobody visibly claiming it, and compassion fade ([PP §2][pp2]).
- **Auto-merging relatos, or auto-rejecting a newcomer's relato:** wrong merges are irreversible pollution, and rejection repeats Wikipedia's decline ([GT §6][gt6]).
- **Silent closure:** it forfeits the +57% and +60% repeat effects ([PP §4][pp4]).
- **Gore on the map, feed or share cards; outrage-optimized share text or reshare counters** ([PP §5][pp5]).
- **Blur or content warnings sold as protection:** they don't reduce distress ([PP §5][pp5]).
- **Routing every caso to the top protetores:** that rebuilds the open-intake burnout machine ([PP §2][pp2]).
- **Exact public location by default; random jitter on every render; opt-out precision:** all three expose targets ([GT §7][gt7], [ST §5][st5], [PA §1][pa1]).
- **Public tutor phone numbers; Pix keys on casos** ([GT §5][gt5]).
- **"Procura-se" for people; naming or locating alleged abusers** ([GT §3][gt3]).
- **KPIs for ops or moderation based on publishing speed or volume** ([GT §6][gt6]).
- **Promising municipal action:** only ~20% trust local government ([PP §6][pp6]).
- **Vouching as the only gate to T3** ([GT §1][gt1]).
- **BTS or peer-prediction payments** ([GT §2][gt2]).

## 5. Evidence we deliberately do NOT rely on

- **Identifiable victim effect:** meta-analysis r = .05; bias-corrected r ≈ .002; a 2024 replication failed (contested) ([PP §2][pp2]). Casos center on one animal for identification, not for persuasion.
- **Moral licensing:** published d = 0.31, bias-corrected −0.05 to 0.18, and three replications failed (contested) ([PP §2][pp2]). We still show a "next step" after each relato, justified by the funnel.
- **Foot-in-the-door:** weak, and nearly half of 120 groups showed no effect or the wrong direction (classic) ([PP §3][pp3]). The micro-role ladder is justified by lower effort per step, not by compliance.
- **Nudge effect sizes:** after bias correction there is no average effect, and nudge units see ~1/6 of published effects ([PP §3][pp3]). Defaults are used, but measured.
- **Peer prediction / BTS:** every precondition fails here (population, common prior, payments) ([GT §2][gt2]).
- **Gamification meta-analyses from education (g = .574/.740):** the gains are driven by levels and narrative in classrooms, and do not transfer to emergencies ([PP §1][pp1]).
- **"Sad faces raise donations":** n ≈ 45–54, with simulated donations only (weak) ([PP §2][pp2]).
- **Bystander apathy as a universal rule:** real public conflicts show that someone usually helps, so we design for visible coordination, not against assumed apathy ([PP §2][pp2]).
- **Vendor re-ID accuracy claims (Pupz >94%, Petco's "512 points"):** unverified. Re-ID is a capped-weight voter ([PA §7][pa7]).
- **Specific Kraut & Resnick claims (uniqueness messages, goal-setting):** unverified in this research ([GT §1][gt1]).

## 6. Experiments backlog

Rule: never hold out safety mechanisms (P13–P15) or the closure itself. Only form, timing and wording vary (design call).

| # | Hypothesis | Primary metric | Minimal design |
|---|---|---|---|
| E1 | An outcome photo beats text-only closure for first-timers (P5) | second relato ≤ 90 d | Randomize first-time reporters 50/50 on push format; both groups get closure |
| E2 | The "Leva 10 segundos" header raises completion (P1) | camera-open → enviar | A/B header copy vs. no copy |
| E3 | A small first ring (~300–500 m) reaches N no slower than a 2 km ring, with fewer opt-outs (P3) | time to N accepts; opt-outs per 100 alerts | Switchback by area × week |
| E4 | Personal state copy ("você é a pessoa mais próxima · 0 a caminho") beats a generic alert (P4) | accept rate | A/B alert copy |
| E5 | A shorter claim buffer raises claim → arrival without double dispatch (P4) | claim → arrival; double-dispatch rate | Randomize two buffer lengths per claim |
| E6 | Prompting resolvers to thank contributors raises newcomer retention, a Gallus replication (P6) | 90-day relato/claim by thanked newcomers | Randomize the thank prompt per caso at desfecho |
| E7 | A 1×/day digest keeps engagement with fewer mutes than 3×/day (P7) | mutes/opt-outs; actions from digest | Randomize new users |
| E8 | Tap-to-view injury photos in alerts don't lower acceptance vs. ID photo only (P9) | accept rate; distress reports | A/B among T1+ helpers |
| E9 | The rules card's wording changes newcomer compliance and participation, a Matias replication (P16) | newcomer violations; newcomer messages | Randomize two card variants per caso |
| E10 | Showing the duplicate card before enviar links more relatos than after, without hurting completion (P2) | linked-relato rate; completion | A/B card position |

## 7. Open questions for the owner

1. **When does WhatsApp intake ship?** The notes argue it is probably the main channel for the typical reporter (97% use WhatsApp daily; Colab's install → report drop) ([PP §6][pp6]). The brief says "later". Should a minimal WhatsApp follow/alert channel be in MVP?
2. **Is "no money" permanent?** CLAUDE.md treats it as a standing invariant. GT §7 says only "at launch", and PP §7 recommends caso-linked Pix with receipts ([PP §7][pp7]). Confirm it is permanent, or name what would justify donations to verified recipients.
3. **Anonymous emergências.** Should a T0 emergência fire wave 1 immediately (speed), or wait for a phone number or a second relato (abuse resistance)?
4. **Escalation anchor.** Which ONG or CCZ in the pilot city will accept escalations? Without an on-duty T3/T4, the "nobody went" path dead-ends.
5. **Minors (ECA Digital, in force since 2026-03-17).** Do we gate Conversa by age, or restrict adult↔minor chat, in MVP ([PA §5][pa5])?

[pp1]: <../research/research_notes/Stray pet platform research/participation_psychology.md#1-what-drives-and-sustains-contribution-in-crowdsourced-civic--citizen-science--vgi-platforms>
[pp2]: <../research/research_notes/Stray pet platform research/participation_psychology.md#2-prosocial-behavior-toward-animals-identifiable-victim-empathy-distance-compassion-fatigue-moral-licensing-bystander-effect-and-countermeasures>
[pp3]: <../research/research_notes/Stray pet platform research/participation_psychology.md#3-behavioral-economics-of-reporting-friction-effort-defaults-small-asks-progressive-disclosure-timing-notification-fatigue>
[pp4]: <../research/research_notes/Stray pet platform research/participation_psychology.md#4-closing-the-loop-does-feedback-increase-repeat-reporting>
[pp5]: <../research/research_notes/Stray pet platform research/participation_psychology.md#5-emotional-content-graphic-images-content-warningsblur-outrage-dynamics>
[pp6]: <../research/research_notes/Stray pet platform research/participation_psychology.md#6-brazil-specific-evidence-volunteering-whatsapp-mobilization-trust-donations-pix-vaquinhas-animal-protection>
[pp7]: <../research/research_notes/Stray pet platform research/participation_psychology.md#7-design-implications-for-the-platform-each-tied-to-evidence-and-anti-patterns>
[gt1]: <../research/research_notes/Stray pet platform research/game_theory_trust_safety.md#1-collective-action-public-goods-ostrom-and-reputation-system-design>
[gt2]: <../research/research_notes/Stray pet platform research/game_theory_trust_safety.md#2-incentive-compatible-truthful-reporting-verification-peer-prediction-stale-and-false-reports>
[gt3]: <../research/research_notes/Stray pet platform research/game_theory_trust_safety.md#3-coordination-convergence-vs-nobody-acting-claims-and-timeouts-evidence-from-volunteer-responder-dispatch-apps-vigilantism-citizen>
[gt4]: <../research/research_notes/Stray pet platform research/game_theory_trust_safety.md#4-sociology-of-brazils-animal-protection-field-protetores-ongs-ccz-hoarding-donations-territory-community-animals>
[gt5]: <../research/research_notes/Stray pet platform research/game_theory_trust_safety.md#5-abuse-vectors-and-scams-and-how-comparable-platforms-mitigate-them>
[gt6]: <../research/research_notes/Stray pet platform research/game_theory_trust_safety.md#6-moderation-models-community-vs-staff-trust-tiers-rate-limits-progressive-trust-report-triage>
[gt7]: <../research/research_notes/Stray pet platform research/game_theory_trust_safety.md#7-concrete-mechanism-recommendations-problem--mechanism--failure-mode>
[pa1]: <../research/research_notes/Stray pet platform research/prior_art_brazil_context.md#1-international-prior-art-models-scale-matching-tech-business-model-praise-criticism-failures>
[pa2]: <../research/research_notes/Stray pet platform research/prior_art_brazil_context.md#2-brazilian-prior-art-existing-apps-and-sites-status-features-and-why-none-became-the-default>
[pa4]: <../research/research_notes/Stray pet platform research/prior_art_brazil_context.md#4-brazil-numbers-with-provenance>
[pa5]: <../research/research_notes/Stray pet platform research/prior_art_brazil_context.md#5-legal-lgpd-marco-civil-arts-15-and-19-plus-the-stf-ruling-animal-cruelty-law-community-animal-laws-defamation-eca-digital>
[pa7]: <../research/research_notes/Stray pet platform research/prior_art_brazil_context.md#7-gaps-and-opportunities-synthesized>
[st2]: <../research/research_notes/Stray pet platform research/spatiotemporal_chains.md#2-linking-sightings-into-chains-clustering-track-association-probabilistic-record-linkage-human-in-the-loop-mergesplit-and-re-id-pipelines>
[st5]: <../research/research_notes/Stray pet platform research/spatiotemporal_chains.md#5-location-privacy-geo-masking-k-anonymity-geo-indistinguishability-inaturalist-obscuration-and-protecting-reporters-feeders-and-colonies>
[st7]: <../research/research_notes/Stray pet platform research/spatiotemporal_chains.md#7-concrete-recommendations-default-parameters-algorithm-pipeline-data-model>
