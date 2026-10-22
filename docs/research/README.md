# Research base (2026-10-21)

Evidence behind every design doc. Each note has, per question: takeaway,
cited findings with inline sources and evidence grades, inferences (labelled),
and gaps. The report synthesizes all seven.

**Synthesized report:** [Stray pet platform research](<reports/Stray pet platform research.md>)

| Note | Feeds |
|---|---|
| [participation_psychology](<research_notes/Stray pet platform research/participation_psychology.md>) | behavioral-design, vision |
| [game_theory_trust_safety](<research_notes/Stray pet platform research/game_theory_trust_safety.md>) | behavioral-design, compliance, location-privacy |
| [prior_art_brazil_context](<research_notes/Stray pet platform research/prior_art_brazil_context.md>) | vision, compliance |
| [spatiotemporal_chains](<research_notes/Stray pet platform research/spatiotemporal_chains.md>) | data-model, location-privacy |
| [core_tech_stack](<research_notes/Stray pet platform research/core_tech_stack.md>) | architecture, ADRs 0001–0009 |
| [ai_pipelines](<research_notes/Stray pet platform research/ai_pipelines.md>) | photo-pipeline, whatsapp-intake, ADR-0010 |
| [naming](<research_notes/Stray pet platform research/naming.md>) | brand (chosen: Alerta Patinha) |
| [mobile_native_path](<research_notes/Mobile and native path/mobile_native_path.md>) (2026-10-22) | ADR-0011, photo-pipeline (JPEG client encode, HEIC), frontend zones |

## Where design decisions override the report

The report is evidence; ADRs and domain docs are decisions. Where they differ, the decision wins:

| Report says | Decision | Where |
|---|---|---|
| Active public-place emergencies shown **exact** to everyone | No public exact pins, emergencies included — exact goes to alerted helpers/claimers (logged), because a public pin reveals the reporter's live position | ADR-0004, location-privacy.md |
| Verified orgs "receive donations through verified Pix keys" | No money flows through the platform at launch (CLAUDE.md rule 10); revisit after scam data | CLAUDE.md, behavioral-design Q2 |
| Alert ring starts ~500 m | Start small (~300–500 m), widen ×2 to the 2–5 km cap until N accept — compatible, parameters v0 | data-model.md |

Known weak spots (re-check before relying on them): Brazilian app statuses,
WhatsApp service-message rates in BRL after 2026-10-01, no lost-dog distance
study, no Brazilian GPS data for street dogs/colony cats, no re-ID benchmark
on street photos of SRD animals, several LGPD procedural deadlines.
