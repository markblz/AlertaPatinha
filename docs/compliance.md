# Alerta Patinha: compliance design

Status: draft v0 · 2026-10-21 · Audience: product + engineering · Basis: research notes in `docs/research/research_notes/Stray pet platform research/`

## 1. Disclaimer and scope

- **This is not legal advice.** It is an engineering design document distilled from research notes dated 2026-10-21. Some legal findings in those notes rest on secondary sources or search summaries, and the notes say which. Anything marked **⚖ lawyer** must be validated by Brazilian counsel before the feature ships.
- **No law is invented here.** Every law number, article, date and price below appears in a linked note. When the product needs an answer the notes do not give (deadlines, exemptions, thresholds), it is listed as an open question rather than filled in from memory.
- **In scope:** the web/PWA, the live map (*exato* vs *aproximado*), casos/chains and per-case chat, geo-targeted help alerts, the photo pipeline (EXIF, blur, future re-ID), WhatsApp intake (LLM + STT), access tiers, hosting and vendors, and the brand.
- **Out of scope:** incorporation and tax, payments and donations (there are none at launch), labor, accessibility law, and app-store review policies.
- **Note legend** (links are relative to `docs/`):
  - **PA** = [prior_art_brazil_context.md](<research/research_notes/Stray pet platform research/prior_art_brazil_context.md>) (law: §5)
  - **AI** = [ai_pipelines.md](<research/research_notes/Stray pet platform research/ai_pipelines.md>)
  - **TS** = [core_tech_stack.md](<research/research_notes/Stray pet platform research/core_tech_stack.md>)
  - **GT** = [game_theory_trust_safety.md](<research/research_notes/Stray pet platform research/game_theory_trust_safety.md>)
  - **NM** = [naming.md](<research/research_notes/Stray pet platform research/naming.md>)
  - **SC** = [spatiotemporal_chains.md](<research/research_notes/Stray pet platform research/spatiotemporal_chains.md>), cited only for the precision matrix

**Access tiers used throughout.** The trust ladder comes from [GT §6](<research/research_notes/Stray pet platform research/game_theory_trust_safety.md>) and the precision matrix from [SC §5](<research/research_notes/Stray pet platform research/spatiotemporal_chains.md>).

| Tier | Who | Location precision served |
|---|---|---|
| T0 | Anonymous visitor or device session (`anon_session`, [TS Q8](<research/research_notes/Stray pet platform research/core_tech_stack.md>)) | Public geometry only. Design call: T0 may file reports, which are queued as lower-trust. GT §6 lets T0 only view, while TS Q8 allows anonymous reports. |
| T1 | Phone-verified (WhatsApp OTP) | Public geometry, plus exact for a caso they claim or join (logged) |
| T2 | Reliable reporter (outcome-based private score) | Same as T1, with weighted "ainda está lá" votes |
| T3 | Trusted local: protetor or mantenedor, vouched by 2 trusted users **plus** staff review | Exact inside their declared territory |
| T4 | Verified org: ONG (CNPJ) or CCZ (government e-mail domain) | Exact inside their service area |
| Staff | Moderators and ops | Exact, logged, purpose-bound |

"Public geometry" means the stable display cell (H3 res-7/8) derived once at write time. There is **no public exact display, emergencies included** (design call, [location-privacy.md](domain/location-privacy.md)): an exact public emergency pin reveals where the reporter is standing in real time. Rescue speed is served by giving the exact point to alerted helpers and claimers (logged). SC §5's public-exact emergency option is recorded there as a rejected alternative, to revisit with pilot data.

## 2. Personal-data map

Base facts ([PA §5](<research/research_notes/Stray pet platform research/prior_art_brazil_context.md>)): personal data is data relating to an identified or identifiable natural person (LGPD art. 5, I). Legal bases are in art. 7. Sensitive data, including biometrics, falls under art. 11. Children's and teens' data must be processed in their best interest (art. 14). Animal photos are not personal data in themselves. The ANPD Guia de Legítimo Interesse (2 Feb 2024) says a legitimate-interest assessment (LIA) is recommended but not mandatory, and that legitimate interest (LI) **cannot** be used for sensitive data. Retention values marked *proposal* are design choices that appear in no law or note.

| # | Data item | LGPD class | Legal basis and reasoning | Retention | Who can see it | Engineering rule |
|---|---|---|---|---|---|---|
| D1 | Exact point of a sighting or emergency | Personal data when it reveals where the reporter stood or a home or workplace ([AI §1](<research/research_notes/Stray pet platform research/ai_pipelines.md>), PA §5) | LI + LIA for the civic map and chains. No public exact display exists, so no consent flow is needed for it | While the caso is active. Helper/claimer exact access ends on resolution or claim expiry ([GT §7 A4](<research/research_notes/Stray pet platform research/game_theory_trust_safety.md>)). *Proposal:* coarsen the stored point 12 months after archive ⚖ lawyer | Tiers above. The public never sees it | Stored in a column only the backend reads. `display_geom` is derived at write time ([TS Q2](<research/research_notes/Stray pet platform research/core_tech_stack.md>)) |
| D2 | Watch-area centre for alerts (often the user's home) | Personal data (home location, [TS Q9](<research/research_notes/Stray pet platform research/core_tech_stack.md>)) | Consent: alerts are opt-in | Until the user removes it | Owner only; never exposed | Store it coarsened or encrypted. Matching uses H3 cells or a buffered polygon |
| D3 | *Zonas privadas* (declared home, feeding points) | Personal data | Consent (declared by the user) | Until removed | Owner; staff for a stated purpose only | Any report inside one gets `privacy_class=near_reporter_home` ([SC §5](<research/research_notes/Stray pet platform research/spatiotemporal_chains.md>)) |
| D4 | Original photo + EXIF (GPS, DateTimeOriginal, Make/Model) | Personal data: EXIF GPS can expose a reporter's home ([AI §1](<research/research_notes/Stray pet platform research/ai_pipelines.md>)) | LI (verification and fraud evidence) | "Short" per AI §1. *Proposal:* 30 days, longer only under legal hold | Staff and moderators | Private quarantine bucket in Brazil. A private `photo_evidence` row. Never served publicly |
| D5 | Bystander faces, licence plates and house numbers in photos | Personal data. Faces become **sensitive (biometric, art. 11)** if templates are created (PA §5 inference) | LI for publishing the blurred version. LI cannot cover sensitive data, so no face templates are ever created | Unblurred only inside D4 | Public sees blurred derivatives only | Detector-only blur run in-house ([AI §2, §7](<research/research_notes/Stray pet platform research/ai_pipelines.md>)), so bystanders' faces are not sent to third parties |
| D6 | Public animal photo derivatives | Not personal data per se (PA §5); residual risk from backgrounds | LI | Life of the caso | Per caso visibility | Re-encoded, stripped and blurred. Only derivatives are ever public |
| D7 | Animal re-ID embeddings and PDQ hashes (future) | Not human biometrics (PA §5). Linked to the reporter through the photo, so treated as personal data | LI | While the source photo is retained. Re-embed when the model changes | Internal only | Store model name and version. Never auto-merge casos on similarity ([AI §3](<research/research_notes/Stray pet platform research/ai_pipelines.md>)) |
| D8 | Phone number + display name | Personal data | LI + LIA: Sybil defence needs a central identity root ([GT §1](<research/research_notes/Stray pet platform research/game_theory_trust_safety.md>)), plus scam resistance. ⚖ lawyer: whether another art. 7 basis fits better | Account lifetime; erased on deletion | Never public. Contact goes through a masked relay ([GT §7 E1](<research/research_notes/Stray pet platform research/game_theory_trust_safety.md>)) | OTP goes via a WhatsApp authentication template, so Meta is a processor abroad (§3.1) |
| D9 | Per-caso chat messages | Personal data; may hold third parties' data | LI (coordinating the caso) | Life of the caso. *Proposal:* 12 months after archive ⚖ lawyer | Chain members; staff when a message is reported | Postgres is the record; Centrifugo history is only a reconnect buffer ([TS Q4](<research/research_notes/Stray pet platform research/core_tech_stack.md>)). Pix, phone and "taxa" patterns trigger warnings ([GT §7 E2](<research/research_notes/Stray pet platform research/game_theory_trust_safety.md>)) |
| D10 | WhatsApp voice notes (raw OGG/Opus) | Personal data (voice, [AI §6](<research/research_notes/Stray pet platform research/ai_pipelines.md>)) | LI (the user started the report) | Delete after transcription plus a short dispute window (AI §6). *Proposal:* 7 days | Staff only | No speaker identification, so no voice biometrics |
| D11 | Transcripts and LLM-extracted report fields | Personal data (may contain names and addresses) | LI | Same as the report or chat they belong to | Reporter and staff. Public fields are sanitized | Strip CPF and phone patterns from public fields ([AI §5](<research/research_notes/Stray pet platform research/ai_pipelines.md>)). Never publish an unconfirmed LLM-guessed coordinate |
| D12 | Application access logs (IP, timestamps, session or account id, device-fingerprint hash) | Personal data | Legal obligation where Marco Civil art. 15 applies, otherwise LI for security. ⚖ lawyer (§3.2) | 6 months ([PA §5](<research/research_notes/Stray pet platform research/prior_art_brazil_context.md>)) | Security staff. Disclosed only on a court order | Kept in Brazil and access-controlled |
| D13 | `location_access_log` (who saw which exact point, and why) | Personal data of both viewer and reporter | LI (accountability) | *Proposal:* same as D12 ⚖ lawyer | Staff and audit | Append-only. One row per exact serialization |
| D14 | Device push tokens (Web Push subscriptions) | Personal data (device identifier) | Consent (opt-in notifications) | Until the user unsubscribes or the endpoint returns 404/410 ([TS Q9](<research/research_notes/Stray pet platform research/core_tech_stack.md>)) | System only | Delete dead endpoints automatically |
| D15 | Maus-tratos denúncia content, which may identify a third party | Personal data of the reporter and the alleged abuser; concerns an alleged crime | ⚖ lawyer (not covered by the notes) | Until forwarded, plus any legal hold ⚖ lawyer | Staff. Authorities receive an export | Never public ([GT §7 D1](<research/research_notes/Stray pet platform research/game_theory_trust_safety.md>)) |
| D16 | Minors' data (any row above when the user is under 18) | Children's and teens' data under art. 14 | Any art. 7 or art. 11 basis if the minor's best interest prevails (Enunciado CD/ANPD nº 1/2023). LI is possible with extra safeguards (ANPD 2024 guide) ([PA §5](<research/research_notes/Stray pet platform research/prior_art_brazil_context.md>)) | Same as the category | Never exact in public; reporter identity never shown | Protected-mode defaults (§3.5) |
| D17 | T3/T4 verification data (CNPJ, CPF, gov.br level, vouches) | Personal data (CPF) | LI (impersonation and fraud defence, [GT §7 E4, F1](<research/research_notes/Stray pet platform research/game_theory_trust_safety.md>)) | While the tier is active | Staff only | *Proposal:* store the verification result, not document images |

## 3. Obligations by law or regulation

### 3.1 LGPD (Lei 13.709/2018)

| Requirement (source) | Product or engineering rule we adopt | Open question |
|---|---|---|
| Legal basis per purpose. LIA is recommended; LI cannot be used for sensitive data ([PA §5](<research/research_notes/Stray pet platform research/prior_art_brazil_context.md>)) | One written LIA per purpose before launch: map, chains, alerts, intake bot, logs, and later re-ID. Consent only for optional features: alerts and push, WhatsApp notifications | ⚖ lawyer: is LI enough for chains that keep exact points that T1 claimers can see? |
| Minimization. PA §5 notes that the exato/aproximado model fits the principle | Precision tiers (§1). Stable masking. Only derived media is ever public | None |
| Data-subject rights under art. 18: access, correction, deletion, portability (PA §5) | Self-service export (JSON) and delete. *Proposal:* deletion unlinks the reporter, and sightings stay as de-identified animal observations | ⚖ lawyer: response deadlines (not in the notes). Is keeping de-identified sightings acceptable? How do legal holds (D12, D15) interact with deletion? |
| *Encarregado* (DPO). Not covered by the notes | Name a privacy contact in the PT-BR privacy notice from day 1 anyway | ⚖ lawyer: is appointment mandatory, or is there an exemption for a small or nonprofit operator? |
| RIPD (DPIA). Not covered by the notes; only the LIA is | Write a RIPD-style assessment before shipping each of: exact location, the photo pipeline, WhatsApp/LLM intake, re-ID | ⚖ lawyer: is it mandatory here, and in what format? |
| Security-incident notification. Not covered by the notes | Incident runbook. The data inventory plus D13 let us list affected people within hours. Encrypt backups and apply the pgBackRest 2.60 advisory ([TS Q11](<research/research_notes/Stray pet platform research/core_tech_stack.md>)) | ⚖ lawyer: deadlines and thresholds for notifying ANPD and data subjects |
| International transfers by contract must use the ANPD SCCs (Res. CD/ANPD 19/2024), adopted verbatim; adaptation deadline 2025-08-23 ([TS Q7, Q10](<research/research_notes/Stray pet platform research/core_tech_stack.md>)). Cloudflare R2 has **no South America location or jurisdiction**, so using it is a transfer | Primary DB, backups and logs with PII stay in Brazil (TS Q10). *Design call:* originals and quarantine stay in-country (Magalu Cloud S3 or a BR host), and only stripped and blurred derivatives plus the PMTiles basemap go on R2. VLM and moderation APIs receive the blurred derivative or animal crop, never the original. Every foreign processor is recorded in the RoPA with country and SCC status: Cloudflare, Sentry, Meta, the LLM/STT vendors, and Google geocoding or moderation if used | ⚖ lawyer: whether Cloudflare signs or offers the ANPD SCCs is unverified (TS Q7). Res. CD/ANPD 32/2026 (Brazil–EU adequacy) is single-source and unverified (TS Q10). Is Cloud API "optional local data storage at rest" available for Brazil ([AI §4](<research/research_notes/Stray pet platform research/ai_pipelines.md>))? |
| Transparency (TS Q10) | A PT-BR privacy notice that explains exato vs aproximado and who sees what | None |
| Regulator context: ANPD made a regulatory agency by Lei 15.352/2026 (secondary source, PA §5) | Informational | None |

### 3.2 Marco Civil da Internet (Lei 12.965/2014), art. 15: access logs

| Requirement (source) | Rule we adopt | Open question |
|---|---|---|
| A provider "constituído na forma de pessoa jurídica … com fins econômicos" keeps application access logs for **6 months**, confidential and secure. §1: a court order can extend the duty to providers outside the article. §2: police, administrative authorities or the MP can request longer precautionary retention. §3: disclosure always needs a court order ([PA §5](<research/research_notes/Stray pet platform research/prior_art_brazil_context.md>)) | Keep D12 for exactly 6 months **whatever the operator's legal form** (the safe default per PA §5). A legal-request workflow with two separate paths: a *preservation hold* (§2, freezes specific records) and *disclosure* (court order only, logged) | ⚖ lawyer: does a nonprofit operator fall outside art. 15 ("fins econômicos")? If it does, is 6-month retention still proportionate under LGPD? |
| (Same) | T0 posts also log IP, timestamp and session, so a court order about an anonymous post can still be answered | ⚖ lawyer: is anonymous public posting compatible with these duties? |

### 3.3 Marco Civil art. 19 after the STF ruling (Temas 987 and 533, judged 26/06/2025)

| Requirement (source) | Rule we adopt | Open question |
|---|---|---|
| Art. 19 was declared partially unconstitutional. For crimes and illicit acts in general, until Congress legislates, a platform is liable for third-party content it fails to remove after a takedown request ([PA §5](<research/research_notes/Stray pet platform research/prior_art_brazil_context.md>)) | "Denunciar" on every post, photo, chat message and profile, plus a public web form for affected non-users. Each notice becomes a ticket recording `received_at`, category, decision, reason, `decided_at` and the reply to the notifier. Removals carry templated explanations ([GT §6](<research/research_notes/Stray pet platform research/game_theory_trust_safety.md>)) | ⚖ lawyer: the minimum content of a valid extrajudicial notice (raised in the pending embargos) |
| Serious crimes (attempted coup, terrorism, inducement to self-harm or suicide, racism, homophobia, crimes against women and children) create liability if the platform does not act "imediatamente" (PA §5) | These categories are **auto-hidden on receipt** pending staff review. *Proposal SLA:* other categories decided within 24 h. A staffed on-call rota | ⚖ lawyer: what does "imediatamente" mean operationally, and is a 24 h SLA defensible? |
| **Crimes against honor** (calúnia, difamação, injúria) stay under art. 19's court-order rule. Effects are prospective (PA §5) | Our ToS forbids accusing identifiable people (§3.4), so that content is removed **under the ToS** on notice. This is a contractual choice, not a legal duty | ⚖ lawyer: risk from removing more than the law requires, and consistency with a later court order |
| E-mail, closed videoconference and **instant-messaging** services stay under art. 19 (PA §5) | Per-caso chat goes through the same notice workflow regardless | ⚖ lawyer: does per-caso chat count as "mensageria instantânea" or as UGC? |
| Acórdão published Nov 2025. Twelve embargos de declaração were scheduled for 10 Jun 2026, asking for a 6-month implementation period (Toffoli reportedly proposed 60 days), minimum notice requirements, and a definition of covered providers. The thesis text (self-regulation, transparency reports, legal representative) was not verified (PA §5) | *Proposal:* count notices received, decided and removed by category from day 1, so a transparency report is cheap later | ⚖ lawyer: the final thesis after the embargos, and whether a legal-representative duty applies to us |

### 3.4 Honor, defamation and anti-vigilantism

| Requirement (source) | Rule we adopt | Open question |
|---|---|---|
| Courts award damages for online accusations of maus-tratos: TJMG 2017 R$5,000 (vet statements showed no abuse); TJMG R$4,000 + public retraction (accusation **plus publishing personal data**); TJSC R$2,000 + removal; TJSP R$20,000 at first instance (URL unconfirmed). *Users* get sued, and exposing personal data aggravates damages ([PA §5](<research/research_notes/Stray pet platform research/prior_art_brazil_context.md>), [GT §5](<research/research_notes/Stray pet platform research/game_theory_trust_safety.md>)) | **Never name, photograph or locate an alleged abuser in public content.** No "find the abuser" threads, no "procura-se" for people, no bounties ([GT §3, §7 D1–D2](<research/research_notes/Stray pet platform research/game_theory_trust_safety.md>); the Citizen manhunt lesson). Maus-tratos goes through a structured private form with Nextdoor-style friction, as a staff-moderated category ([GT §6](<research/research_notes/Stray pet platform research/game_theory_trust_safety.md>)) | ⚖ lawyer: platform (not user) liability for such posts after the STF ruling. The notes found no case law (PA §5 gaps) |
| Abuse reports should go privately to authorities: police, MP, municipal animal-welfare departments, Ibama/Disque Denúncia (PA §5), with export for a BO (GT D1). Precedent: Jundiaí's app routes anonymous complaints with photo and exact location to the city department (PA §2) | Denúncia → staff queue → export package for a BO at the delegacia (Polícia Civil), the Ministério Público, or the municipal animal-welfare channel. Ibama/Disque Denúncia are listed in the note; when each applies is not | ⚖ lawyer: which authority for which case type (domestic vs wild animal, municipality)? May we pass the reporter's identity without consent? |
| SinPatinhas lets the government "negativar" people responsible for mistreatment. A civic platform should never mirror or publish that list ([PA §3](<research/research_notes/Stray pet platform research/prior_art_brazil_context.md>)) | No import, display or inference of any abuser list | None |
| Lost-pet extortion cases ("pay or the animal dies") were registered as *extorsão* (DF, MS) ([GT §5](<research/research_notes/Stray pet platform research/game_theory_trust_safety.md>)) | Masked contact, proof-of-possession challenge, money-pattern warnings, and a "registre BO" prompt with the case export (GT E1–E2) | None |

### 3.5 ECA Digital (Lei 15.211/2025)

| Requirement (source) | Rule we adopt | Open question |
|---|---|---|
| In force since **17 Mar 2026** (date set by Lei 15.352/2026). Applies to products and services directed at minors or likely to be accessed by them ("acesso provável"), foreign providers included. Duties: **age verification**, **protection by default**, faster response to harmful content ([PA §5](<research/research_notes/Stray pet platform research/prior_art_brazil_context.md>)) | Assume we are in scope: an open app with photos, maps and chat between strangers, and teens often feed or rescue strays (PA §5 inference) | ⚖ lawyer: confirm applicability; the regulatory decrees and ANPD guidance were not retrieved |
| Minimum-age policy | Set a minimum account age in the ToS (the number is ⚖ lawyer). Users under 18 above that age get **modo protegido** | ⚖ lawyer: the age threshold |
| Protection by default (PA §5 inference: no precise-location sharing, restricted contact from adults) | Modo protegido: the user's own reports are always public at cell precision. No *exato* publishing. No 1:1 relay contact with adults, only moderated per-caso chat. No dispatch or claim alerts (responder safety, [GT §7 C5](<research/research_notes/Stray pet platform research/game_theory_trust_safety.md>)). Reporter identity never shown. **Unknown age (T0) gets the same defaults** for chat and *exato* | ⚖ lawyer: are these defaults sufficient? |
| Age-assurance level | MVP: a self-declared birth year at phone verification, with unknown age treated as a minor. Upgrade to whatever the decrees or ANPD require | ⚖ lawyer: is self-declaration acceptable given the "age verification" duty? |
| Faster response to harmful content | Reuse the STF fast lane (§3.3): "crimes against children" is auto-hidden on receipt | None |

### 3.6 Lei 9.605/98 art. 32 and Lei 14.064/2020 ("Lei Sansão"): maus-tratos

| Requirement (source) | Rule we adopt | Open question |
|---|---|---|
| Art. 32: detenção of 3 months to 1 year plus a fine. **§1-A (Lei 14.064/2020): for dogs and cats, reclusão of 2–5 years, a fine and a ban on keeping animals.** §2: penalty raised by 1/6 to 1/3 if the animal dies. Consolidated text as redacted by Lei 15.355/2026, in force 12/03/2026 ([PA §5](<research/research_notes/Stray pet platform research/prior_art_brazil_context.md>); [GT §4](<research/research_notes/Stray pet platform research/game_theory_trust_safety.md>)) | Two separate flows. **Injured-animal emergency** is about the animal: public under the tier rules. **Suspected maus-tratos by a person** goes to the private denúncia (§3.4). For denúncias: keep the original + EXIF + server timestamps, take a *proposal* SHA-256 at ingest for integrity, and set `legal_hold` to suspend purges (D4, D10). Export a dossier for BO or MP. The platform never adjudicates or publishes conclusions | ⚖ lawyer: evidence retention period, chain-of-custody expectations, any duty to report, and handling of art. 15 §2 preservation requests |

### 3.7 Community-animal laws

| Requirement (source) | Rule we adopt | Open question |
|---|---|---|
| SP Lei 12.916/2008, art. 4 §§1–2: a recognized community dog is sterilized, registered and **returned to its community** once its *cuidador principal* signs a commitment term ([GT §4](<research/research_notes/Stray pet platform research/game_theory_trust_safety.md>)). RS Lei 13.193/2009 creates the cão comunitário and bans euthanasia of street dogs. Porto Alegre created a Cadastro de Animal Comunitário (Feb 2026). SP PL 1/2026 and PL 25/2026 are bills only; the RJ code is unverified ([PA §5](<research/research_notes/Stray pet platform research/prior_art_brazil_context.md>)). RS Lei 15.254/2019 is unverified; municipal bills exist in Curitiba, Juiz de Fora (PL 105/2026) and Aracruz | A first-class `comunitário` status set by a mantenedor (T3) or an org. It suppresses lost, stray and "found pet" calls to action (PA §5, [GT §5](<research/research_notes/Stray pet platform research/game_theory_trust_safety.md>)). Colony and community locations show at res-7 or are hidden, and exact access needs mantenedor approval (logged, [GT §7 A2](<research/research_notes/Stray pet platform research/game_theory_trust_safety.md>)). A "disputa" button routes to staff mediation (GT F5). *Proposal:* an optional field for a municipal cadastro ID where one exists | ⚖ lawyer: does a platform label have any legal effect? Do we carry liability if users remove a registered community animal after seeing it on the map? |

### 3.8 Consumer law (CDC / Procon)

- The STF ruling puts marketplaces under the CDC ([PA §5](<research/research_notes/Stray pet platform research/prior_art_brazil_context.md>)). At launch the platform moves no money: no payments, no reward escrow, no donations. A reward is only a text label, "recompensa oferecida (paga só na entrega)" ([GT §7 D2](<research/research_notes/Stray pet platform research/game_theory_trust_safety.md>)). CDC exposure is therefore low.
- The notes found no Procon advisory on the "golpe do pet perdido" (GT §5 gaps).
- ⚖ lawyer, before adding verified-recipient donations (GT E3): CDC and financial-regulation exposure.

## 4. Platform and vendor terms

### 4.1 WhatsApp Business Platform ([AI §4](<research/research_notes/Stray pet platform research/ai_pipelines.md>), [TS Q8](<research/research_notes/Stray pet platform research/core_tech_stack.md>))

| Term or fact | What it means for us | Our rule |
|---|---|---|
| On-Premises API: the final client expired 23 Oct 2025 | Cloud API is the only official path | Cloud API, called directly or through a no-markup BSP |
| **§4.7 "Provedores de IA"** (PT-BR terms page updated 23 Sep 2026). AI/ML providers, including LLMs and general-purpose assistants, are prohibited when AI is "a funcionalidade principal (em vez de incidental ou auxiliar)", at Meta's sole discretion. Enforced from 15 Oct 2025 for new users and 15 Jan 2026 for existing ones | A task-specific intake bot uses AI incidentally (AI §4 inference). Meta's discretion is the residual risk | Strict scope: off-topic messages get a fixed refusal. No free-form chat with the LLM. The bot's purpose is documented in the WABA profile. Questions come from code templates; the LLM is only a parser |
| **Brazil status.** CADE's Superintendência-Geral imposed a medida preventiva (Jan 2026). A DF court briefly suspended it. The CADE Tribunal unanimously upheld it on 4 Mar 2026, suspending the new terms until the inquiry ends. A R$250k daily fine has applied since 17 Mar 2026 and was maintained on 23 Apr 2026. The inquiry is ongoing, with no later status found. Meta allows AI providers on +55 from 11 Mar 2026, "charged at the published rates" (CSV updated 15 Oct 2026) | The suspension could be lifted | Comply with §4.7 as if it were enforced. Do not rely on CADE |
| **Data-use clause.** If an AI Provider is your Solution Provider, Platform data (including anonymized, aggregated or derived forms) may not be used to create, develop, train or improve AI models. Fine-tuning a model for your exclusive use is allowed | Training our re-ID model on photos received via WhatsApp plausibly falls in scope | Tag every media row with `source`. Training jobs exclude `source=whatsapp` until counsel clears it (AI §7, Phase 3). Use LLM and STT vendors with no-training, zero-retention terms for WhatsApp traffic |
| 24 h customer-service window. Free-form messages only inside it; templates outside. Utility/authentication rate in Brazil is $0.0068; marketing is about $0.0625 (third-party figure). Misclassified templates get re-categorized | Follow-ups after 24 h need templates | Case updates use **utility** templates only, never marketing |
| Authentication templates have a fixed body ("<VERIFICATION_CODE> is your verification code.") and an expiry of 1–90 min. Meta recommends confirming the user's WhatsApp number before sending | OTP flow | Confirm the number first. SMS as fallback |
| Opt-in rules | **Not covered by the notes** | Explicit in-product opt-in for WhatsApp notifications anyway (consent basis, D14). ⚖ lawyer / Meta policy check |
| Unofficial libraries (Baileys, Evolution, WPPConnect) break the ToS and risk a number ban | Bans are rarely reversed | Prototypes only, never on the production number |
| Billing: from 1 Oct 2026, service messages beyond 1,000/month per number are charged, and so are utility templates inside the window. A payment method was required by 30 Sep 2026. BRL migration is due by 30 Jun 2027 | An unexpected bill could cut off service | A budget alarm on the `pricing` webhook type |
| Business-verification requirements for nonprofits | **Not researched** (AI §4 gaps) | Open question §7 |

### 4.2 Maps, tiles and geodata ([TS Q3](<research/research_notes/Stray pet platform research/core_tech_stack.md>))

- **OSM tile policy:** capacity is limited, there is no SLA, and access may be withdrawn. Offline use and prefetch are not permitted, and apps need a unique User-Agent, a Referer and **visible attribution**. Rule: never use `tile.openstreetmap.org` in production.
- **Protomaps PMTiles (ODbL)**, self-hosted as a Brazil extract. Rule: visible OSM/ODbL attribution on every map view, including list and static fallbacks that render tiles. Check the exact attribution text against OSMF/Protomaps guidance, which the notes do not quote.
- **OpenFreeMap** allows commercial use but has no SLA, so it is for dev and fallback only. **Stadia and MapTiler free tiers** are non-commercial (MapTiler pauses when over quota), so they are not used in production.
- **Photon and Nominatim**, self-hosted, are built on OSM data. **Google Geocoding** is proposed in [AI §5](<research/research_notes/Stray pet platform research/ai_pipelines.md>) for landmark text. The notes do not cover Google's terms on storing results or using them with a non-Google map. ⚖ lawyer or a vendor-terms check is needed before combining it with MapLibre.
- Open: how far ODbL share-alike reaches into our database, for example bairro labels reverse-geocoded from OSM. Not in the notes.

### 4.3 ML model and dataset licenses ([AI §2–§3](<research/research_notes/Stray pet platform research/ai_pipelines.md>))

| Model or asset | License (verification status per note) | Allowed use | Our decision |
|---|---|---|---|
| MegaDescriptor-L-384 | **CC-BY-NC-4.0** (HF model card) | Non-commercial only. "NC" is risky with revenue, sponsorship or a commercial partner | Offline benchmarking only. Not in production until ⚖ lawyer rules on "non-commercial" for our operator and funding |
| PetFace dataset | Not confirmed | Unknown | Do not train or ship on it |
| DINOv3 | Custom "DINOv3 License" (14 Aug 2025): royalty-free, non-transferable; bans ITAR, military, warfare and weapons uses; derivatives must be redistributed under the same agreement | Commercial use permitted under those terms | Candidate backbone after ⚖ lawyer reviews the redistribution clause |
| DINOv2 | Apache 2.0 | Permissive | Default fallback backbone |
| SigLIP 2 | Apache 2.0 (unverified this session) | Permissive if confirmed | Zero-shot candidate; verify the license first |
| AvitoTech CLIP-L animal-ID fine-tune | Not checked | Unknown | Blocked until checked |
| Ultralytics YOLO26, and the default MegaDetector v6 compact model (Ultralytics-based) | **AGPL-3.0** | §13 network use obliges a source offer for the combined service | Banned, unless we buy an enterprise license or open-source the whole service |
| MegaDetector v6 MIT/Apache variants (`MDV6-mit-yolov9-c/e`, `MDV6-apa-rtdetr-c/e`) | MIT / Apache 2.0, per weight (exact license text not verified) | Commercial OK | Allowed; pin the license file for each weight |
| RF-DETR | Apache 2.0 | Commercial OK | Allowed (default detector) |
| EgoBlur (faces, plates) | Apache 2.0 (model card; repo LICENSE not checked) | Commercial OK | Allowed; check the LICENSE before shipping |
| Grounding DINO, OWLv2 / Florence-2 | Apache 2.0 / MIT (unverified) | Permissive if confirmed | Optional, for unusual classes; verify first |
| YOLO-World | GPL-3.0 (unverified) | Copyleft | Avoid |
| faster-whisper | MIT | Commercial OK | Allowed for self-hosted STT later |
| PDQ (Meta ThreatExchange), imgproxy `blur_detections` | Not recorded in the notes; imgproxy's OSS vs Pro split is unverified | Unknown | Verify before depending on them |

### 4.4 Infrastructure licenses ([TS Q4, Q7, Q8](<research/research_notes/Stray pet platform research/core_tech_stack.md>))

- **Chosen:** Valkey (BSD-3) instead of Redis 8 (tri-licensed RSALv2/SSPLv1/AGPLv3). Also Centrifugo (Apache-2.0), h3-pg (Apache-2.0), procrastinate (MIT), SeaweedFS (Apache-2.0) and supercluster (ISC).
- **AGPL, acceptable only unmodified:** Garage (believed AGPLv3, unverified) and Zitadel (AGPL-3.0 since v3; not adopted). AGPL obligations attach to modified versions offered over a network (TS Q4).
- **Avoid:** MinIO CE. The repo is archived and no binaries have been published since Oct 2025. This is a maintenance problem, not a license one.

## 5. Brand protection: "Alerta Patinha" ([NM Q2–Q5](<research/research_notes/Stray pet platform research/naming.md>))

What the naming note actually verified (live lookups, 2026-10-21):
- **Domains:** `alertapatinha` and `alertapatinhas` returned RDAP **404 on all four TLDs** (.com.br, .org.br, .app.br, .com), 8 variants in total. A 404 means no registration object exists. It is strong evidence the name is free but not a guarantee, since a domain can be reserved or frozen; confirm at checkout.
- **INPI (radical search only):** "patinha" returns 332 processes. None is an alert, SOS or rescue mark except two dead ones: S.O.S. PATINHA (902681753, NCL 44, extinct) and SOS PATINHAS (928580741, NCL 44, archived). The phrase "Alerta Patinha" was not listed as a separate query. No phonetic or figurative search was run.
- **Not verified:** Instagram handles (login wall), .org.br/.app.br eligibility rules (for example, whether .org.br needs a nonprofit CNPJ), an app-store search for the exact phrase "alerta patinha" (an iOS search for "patinha" returned only unrelated pet apps), and misspelling or hyphenated variants.
- **Known weaknesses:** the name is 13 characters long, and it sits in a crowded "Patinhas…" NGO naming space, so its distinctiveness is at risk. Four same-concept apps launched in 2026 (AchaPet, BichoAí, EncontraPet, Pets – Perdidos e Achados). The note reads INPI as first-to-file.

Actions:
1. Register all 8 domains now: alertapatinha and alertapatinhas, each in .com.br, .org.br, .app.br and .com. Redirect them all to one canonical domain (design call).
2. File at INPI promptly. The note recommends **NCL 09 and 42**, "and probably 45". File the word mark first and a mixed mark once the logo exists (design call). The applicant must be the operating entity (§7 Q1). ⚖ lawyer (trademark attorney): class scope and a phonetic search before filing.
3. Check Instagram, TikTok and Play/App Store handles by hand while logged in.

## 6. Engineering rules checklist (each one testable)

1. [ ] Every published image variant is re-encoded with **all** metadata stripped (EXIF, XMP, GPS), and no public URL resolves to an original or quarantine object key. *Test: a fixture with GPS EXIF yields public variants with zero metadata.*
2. [ ] Every public variant passes face and plate blur (EgoBlur-class detector, threshold ≤0.3, [AI §2](<research/research_notes/Stray pet platform research/ai_pipelines.md>)). No human-face embedding or template is ever persisted.
3. [ ] Exact coordinates are serialized only to staff, to T4 inside its service area, to T3 inside its territory, to the reporter of that relato, or to the active claimers and alerted helpers of that caso while it is open. Never to the public. *Contract tests cover REST, GeoJSON, tiles and Centrifugo payloads.*
4. [ ] Public geometry is derived once at write time and stays stable per entity (H3 cell or HMAC-seeded jitter); no noise is generated per request. Emergency pins drop to the cell on resolution or expiry.
5. [ ] Every serialization of an exact coordinate writes an append-only `location_access_log` row (viewer, tier, entity, purpose, timestamp).
6. [ ] A report inside a zona privada gets `near_reporter_home`: res-7/8 cell, day-level time, not listed on the reporter's profile. No public "reports by this user" map exists.
7. [ ] Colonies, comunitário animals and high-value-breed sightings are auto-obscured (res-7 or hidden), and non-emergencies among them are published with a 6–24 h delay ([GT §7 A2](<research/research_notes/Stray pet platform research/game_theory_trust_safety.md>)). Exact access needs mantenedor approval, which is logged.
8. [ ] Public text (posts, LLM output, chat previews) is scanned for CPF, phone, Pix-key and address patterns, which are masked before publication. In chat, money patterns trigger a warning rather than a block.
9. [ ] No field or flow publishes the name, face or address of an alleged abuser. Maus-tratos is reachable only through the private denúncia form and its authority export. No reward money or bounties go through the platform.
10. [ ] Every takedown notice produces a ticket with all fields from §3.3. STF serious-crime categories are hidden at `received_at`. Other categories get a decision within 24 h (*proposal*, ⚖ lawyer). The SLA is monitored.
11. [ ] Application access logs are kept for exactly 6 months, in Brazil, under restricted access, and disclosed only against a court order. Preservation holds extend only the named records.
12. [ ] Scheduled purges delete raw WhatsApp audio after 7 days and originals plus EXIF evidence after 30 days (*proposals*), unless `legal_hold=true`.
13. [ ] The primary DB, backups and logs containing PII live in Brazil. No external processor receives personal data until it is in the RoPA with its country and transfer mechanism.
14. [ ] LLM, VLM and STT calls go only to vendors on no-training or zero-retention terms. Requests carry the blurred derivative or animal crop, never the original. User text sits in a delimited data field. The model has no tools with side effects, and its output is validated against a schema.
15. [ ] WhatsApp runs on the official Cloud API only. Off-topic messages get the fixed refusal. Case updates use utility templates only.
16. [ ] Every media row records its `source`, and every training-set build excludes `source=whatsapp` until §4.7 is cleared.
17. [ ] A model registry pins a license for each weight. CI fails if production config loads a weight licensed CC-BY-NC, AGPL, GPL or unknown.
18. [ ] Under-18 and unknown-age accounts get modo protegido (§3.5). *Test: such an account cannot publish exato, cannot receive dispatch alerts, and has no 1:1 relay.*
19. [ ] Every map view shows visible OSM/ODbL attribution, and `tile.openstreetmap.org` never appears in production config.
20. [ ] Sentry runs with `send_default_pii=False`, and a log linter rejects exact coordinates in any log line ([TS Q11](<research/research_notes/Stray pet platform research/core_tech_stack.md>)).

## 7. Open questions for a lawyer (ranked by how much they unblock)

1. **Operating entity.** Will an associação/OSC or a company operate the platform? The answer drives Marco Civil art. 15 ("fins econômicos"), MegaDescriptor's "NC" clause, .org.br eligibility, who applies at INPI, and WhatsApp business verification.
2. **Post-STF liability scope.** What is the final thesis after the June 2026 embargos (implementation period, minimum notice content, covered providers, transparency or legal-representative duties)? Is per-caso chat "mensageria instantânea" (art. 19) or UGC? What is our platform liability for accusation posts that slip past the filters?
3. **Exact location to alerted helpers.** Is LI + LIA enough to reveal an emergency's exact point to phone-verified (T1) helpers who were alerted or who claimed the caso? Is a RIPD required, and what is our liability if a helper misuses it (poisoning, theft)?
4. **WhatsApp §4.7 data clause.** Does it bar training re-ID on WhatsApp-received photos? Does the CADE suspension cover the data clause too, and what is the inquiry's current status? What are Meta's opt-in rules?
5. **ECA Digital.** Do we fall under "acesso provável"? What minimum age and what age-assurance level are acceptable? Are the modo protegido defaults sufficient, given the decrees and ANPD guidance we have not yet read?
6. **International transfers.** Will each vendor (Cloudflare, Meta, Sentry, the LLM/STT vendors, Google) execute the ANPD SCCs? Do US-hosted LLM and STT on WhatsApp voice notes need extra measures? Is Res. CD/ANPD 32/2026 real and relevant?
7. **LGPD duties the notes did not cover.** Encarregado appointment and exemptions, when a RIPD is mandatory, incident-notification deadlines and thresholds, and the deadline for answering rights requests.
8. **Handling maus-tratos evidence.** How long to keep it, chain-of-custody expectations, any duty to report, sharing the reporter's identity with police, and which authority (Polícia Civil, MP, municipal, Ibama/Disque Denúncia) for which case.
9. **Model licenses.** Does "non-commercial" in CC-BY-NC fit a nonprofit with sponsors? What do DINOv3's redistribution and "same agreement" clauses mean for derived embeddings?
10. **Trademark.** Is "Alerta Patinha" distinctive enough in the crowded "Patinhas…" space? Confirm the NCL 09/42/45 scope and run a phonetic search.
11. **Community animals.** Does a platform `comunitário` label have legal effect? Do we carry liability for removals that users make after seeing the map? Verify RS Lei 15.254/2019.
12. **Geodata terms.** How far does ODbL share-alike reach into our database? Does Google Maps Platform allow storing geocoding results and using them on a MapLibre/OSM map?
13. **Consumer and financial regulation** if verified donations or rewards ever flow through the platform.
