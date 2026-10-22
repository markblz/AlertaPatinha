# Game Theory, Mechanism Design, Community Sociology and Trust & Safety for a Brazilian Stray/Lost-Pet Civic Platform

Research date: 2026-10-21. Evidence grades used below: **[strong]** = peer-reviewed / RCT / large-N; **[moderate]** = peer-reviewed observational, official reports, primary docs; **[weak]** = news reports, company claims, forum posts, single cases; **[unverified]** = recalled background knowledge not re-checked in this session (kept only in Gaps/Inferences).

---

## 1. Collective action, public goods, Ostrom, and reputation-system design

### Takeaway
Sighting/emergency data is a classic public good: anyone can use it, and reporting it costs the reporter something. The literature says three things about such goods. Reputation scores drift upward and get gamed (Goodhart's law). Gamified badges steer only a minority of users. Only a trusted central identity authority can stop Sybil attacks. Ostrom-style governance (clear boundaries, local rule-making, graduated sanctions, recognition by authorities) shows up in online communities, and it becomes more formal as communities grow.

### Cited Findings
**Ostrom and online commons**
- Reviews of Ostrom's design principles for commons (clear boundaries, rules fitted to local conditions, collective-choice arrangements, monitoring, graduated sanctions, conflict-resolution mechanisms, recognition of the right to organize, nested enterprises) found the main critiques were theoretical rather than empirical. The principles held up well empirically **[moderate]** — [Cox et al., Lincoln Institute WP](https://www.lincolninst.edu/app/uploads/2024/04/1707_925_Cox20Final.pdf); [P2P Foundation summary](https://wiki.p2pfoundation.net/Design_Principles_for_Global_Commons)
- A quantitative study of ~80,000 self-governed communities (Minecraft servers, Reddit, World of Warcraft guilds) applied Ostrom's institutional frameworks. Formal governance rose with community age, size and engagement, and communities favored weak norms over strict requirements **[moderate]** — [Governing online goods (deepai summary)](https://deepai.org/publication/governing-online-goods-maturity-and-formalization-in-minecraft-reddit-and-world-of-warcraft-communities) (full text not retrieved; methods unverified)
- A small Croatian scientists' online community met most of Ostrom's principles but failed two, attributed to missing technical prerequisites and small size **[weak/moderate]** — [DOAJ record](https://doaj.org/article/dbc927fad6074c86bed855ac749cc90d); [Indiana DLC](https://dlc.dlib.indiana.edu/dlc/handle/10535/3180?show=full)
- Poblet & Sierra (2020) treat online *mutual help* as a commons and assess a mobile help app against Ostrom's principles. This is the closest design analog to a civic pet-help app, but it is a design study, not a field test **[weak]** — [Poblet & Sierra PDF](https://iiia.csic.es/media/filer_public/fb/fa/fbfaeb68-499f-439b-925f-b212e83fa767/ijc-1029_poblet.pdf)

**Kraut & Resnick, *Building Successful Online Communities* (MIT Press 2012)**
- The book is organized around five design problems: starting a community, attracting newcomers, encouraging commitment, encouraging contribution, and regulating misbehavior. Each design claim is backed by theory, experiments or observational studies. Its contribution claims build on public-goods theory, and its commitment claims build on identity- and bond-formation theory **[moderate]** — [Penguin Random House listing](https://penguinrandomhouse.com/books/655422/building-successful-online-communities-by-robert-e-kraut-and-paul-resnick-with-sara-kiesler-moira-burke-yan-chen-niki-kittur-joseph-konstan-yuqing-ren-and-john-riedl); [Bookshare](https://www.bookshare.org/browse/book/1610999); [HCL community wiki summarizing newcomer claims](https://ds-infolib.hcltechsw.com/ldd/lcwiki.nsf/dx/Dealing_with_Newcomers_in_Online_Communities)

**Reputation systems: inflation, retaliation, Goodhart**
- eBay: the median seller has 100% positive feedback and the 10th percentile is 98.21% (Nosko & Tadelis 2015). Roughly 90% of UberX trips in Chicago in early 2017 were rated 5 stars **[strong]** — [Filippas et al. working paper](https://www.tse-fr.eu/sites/default/files/TSE/documents/conf/2021/filippas.pdf); [NBER w25857](https://www.nber.org/papers/w25857.pdf)
- Leaving negative feedback costs buyers more than leaving positive feedback (fear of retaliation: Dellarocas & Wood 2008; Bolton et al. 2013), so dissatisfied users go silent and scores skew positive **[strong]** — [Digitopoly (Tadelis/Nosko summary)](https://digitopoly.org/2014/07/23/fixing-the-reputation-score-at-ebay/); [Tadelis 2016, Annual Review of Economics](https://ideas.repec.org/a/anr/reveco/v8y2016p321-340.html)
- Online labor market: the share of perfect ratings rose from 33% to 85% over six years, and at least 35–45% of the rise came from lower rater standards ("reputation inflation"). Inflation began when feedback moved from private to public **[strong]** — [Filippas & Horton, CESifo WP 6750](https://cesifo.org/DocDL/cesifo1_wp6750.pdf)
- Stack Overflow badges steer behavior in ways consistent with a formal model, and badge placement can induce specific activities (Anderson, Huttenlocher, Kleinberg, Leskovec, WWW 2013) **[strong]** — [WWW'13 paper](https://archives.iw3c2.org/www2013/proceedings/p95.pdf). A later re-analysis found only ~5–30% of badge earners respond to the incentive and attributes part of the earlier effect to a statistical artifact ("phantom steering") **[moderate]** — [KAIS 2021](https://link.springer.com/article/10.1007/s10115-021-01637-6)

**iNaturalist "Research Grade" as a consensus model**
- An observation reaches Research Grade when it has a date, coordinates, and a photo or sound, is not captive or cultivated, and its community taxon is supported by more than 2/3 of identifiers with at least 2 IDs. Conservative (ancestor) IDs are weighted differently, and the community can later vote that the date, location or wild status is wrong, which removes Research Grade **[moderate]** — [iNaturalist help: Data Quality Assessment](https://help.inaturalist.org/support/solutions/articles/151000169936); [GBIF dataset description](https://gbif.org/dataset/50c9509d-22c7-4a22-a47d-8c48425ef4a7); [forum: finer points](https://forum.inaturalist.org/t/the-finer-points-of-research-grade-logic/12532) (forum = illustrative)

**Sybil resistance**
- Douceur (2002): without a logically centralized trusted authority, Sybil attacks are always possible except under unrealistic assumptions of resource parity. Web-of-trust vouching also fails without a trusted identification root **[strong, foundational]** — [Microsoft Research](https://www.microsoft.com/en-us/research/publication/the-sybil-attack/); [PDF](https://courses.csail.mit.edu/6.895/fall02/papers/Douceur/iptps02-douceur.pdf)

**Newcomer quality control backfiring**
- Wikipedia (Halfaker, Geiger, Morgan, Riedl 2013): the share of good-faith newcomers stayed stable after 2006, but more of them had their work rejected, and rejection predicts the retention decline. Semi-automated revert tools (e.g., Huggle) are partly to blame, and policy processes calcified against newcomer proposals **[strong]** — [Meta-Wiki research page](https://meta.wikimedia.org/wiki/Research:The_Rise_and_Decline); [UMN news](https://cse.umn.edu/college/news/wikipedia-inadvertently-causing-its-own-decline-participation)
- A CHI 2018 replication across 769 wikis found the same dynamics describe the average Wikia wiki **[strong]** — [Community Data Science blog](https://blog.communitydata.science/category/publications/papers/page/4/)

### Inferences
- **Public-good structure.** A sighting is non-rival and non-excludable, its value to the community is high, and its private cost (time, data, risk, emotional load) is real. Free riding is therefore the default for casual citizens. Most of the work will be done by a small, high-valuation group (protetores), as in Olson's "privileged group" logic (theory-based, not tested here). The design goals follow: (a) push the casual reporter's marginal cost toward zero (one photo plus auto-location, WhatsApp intake), and (b) give the core group tools and recognition rather than points.
- **Goodhart risk is specific here.** If reputation counts "rescues" or "sightings", users will farm easy or duplicate reports. Worse, it rewards *accumulating* animals, which feeds the hoarding failure mode (Section 4). Measure verified outcomes instead (reunions, confirmed sightings, claim-to-arrival reliability), keep scores coarse or private, and decay them. The private→public inflation result (Filippas & Horton) argues against public star ratings of protetores and ONGs.
- **Retaliation silences negative signal.** In a small, territorial field where actors know each other, users will rarely post public negative feedback about an ONG or protetor. Negative signals need private, structured channels to staff (Section 6).
- **iNaturalist consensus transfers well** to "is this the same animal / does this sighting belong to this chain" decisions: a 2/3 supermajority, at least 2 independent confirmations, and later revocability. It transfers poorly to *urgent* emergencies, where waiting for consensus costs time.
- **Sybil defense needs a central root.** Phone verification is the practical minimum. gov.br login (if feasible) or CNPJ verification for ONGs gives a stronger root. Vouching by already-trusted users must not be the only gate (Douceur).

### Gaps
- No empirical study found that applies Ostrom's principles specifically to Wikipedia or to a civic animal-welfare platform.
- Specific Kraut & Resnick design claims were not verified in this session. Recalled, **[unverified]**: "telling users their contribution is unique increases contribution" (MovieLens experiments), "specific challenging goals increase contribution", and "socializing newcomers with welcoming, low-risk tasks raises retention".
- No data found on Waze's internal reputation/karma weighting for reports.

---

## 2. Incentive-compatible truthful reporting: verification, peer prediction, stale and false reports

### Takeaway
Peer-prediction and Bayesian Truth Serum mechanisms have elegant guarantees but are impractical here. They need large populations, common priors and monetary payments, they add cognitive load, and in experiments they collapse into uninformative equilibria. The practical toolkit is cheaper: (a) Waze-style decaying confidence driven by confirmations and "not there" votes, (b) iNaturalist-style supermajority consensus for identity and linking, (c) server-side metadata checks treated as *signals*, not proof, (d) trusted-source cross-checking as done by Brazil's Fogo Cruzado, and (e) outcome-based reputation scored after the fact.

### Cited Findings
**Peer prediction / BTS practicality**
- BTS incentivizes truthfulness only for a large enough population, and the required size depends on an unknown prior. It can leave participants with negative payments and is not numerically robust. The original peer-prediction method relies on a common prior shared by agents and center. BTS drops center knowledge of the prior but still assumes it is shared **[strong]** — [Faltings, Jurca, Radanovic: Peer Truth Serum (arXiv 1704.05269)](https://arxiv.org/pdf/1704.05269)
- BTS requires respondents to report a prediction of others' answers on top of their own answer, which makes the task cognitively harder **[moderate]** — [Peer Truth Serum arXiv](https://arxiv.org/pdf/1704.05269); [Witkowski & Parkes AAAI'12 (Robust BTS)](https://econcs.seas.harvard.edu/resource/witkowskiaaai12pdf)
- In a controlled online experiment, peer-prediction mechanisms induced *uninformative equilibria*: participants coordinated on reports independent of their information (Gao et al., EC 2014) **[strong]** — [Gao et al. EC'14](https://econcs.seas.harvard.edu/resource/gaoec14pdf)
- Field evidence (Rigol & Roth, lab-in-the-field with Indian farmers rating neighbors): without monetary incentives, respondents lied in favor of family and friends. Monetary accuracy incentives improved report quality. Robust BTS was "empirically incentive compatible", but only after the authors imposed structure on the data **[moderate]** — [PEDL working paper](https://grp.cepr.org/publications/pedl-working-paper/paying-truth-efficacy-peer-prediction-mechanism-field); [UK gov R4D record](https://www.gov.uk/research-for-development-outputs/paying-for-the-truth-the-efficacy-of-a-peer-prediction-mechanism-in-the-field)
- A related impossibility result: strictly eliciting honest reports from a *heterogeneous* group with different private beliefs is impossible, and modified (divergence-based) BTS reaches truthfulness only as a weak equilibrium **[moderate; exact paper attribution not verified]** — [EPFL Infoscience record](https://infoscience.epfl.ch/record/215879)

**Decaying confidence (Waze)**
- Official Waze help: a report's display lifetime "changes according to the number of Wazers who react to" it. Tapping "Not there" shortens it, and unconfirmed reports expire. Exact timers are not published **[moderate]** — [Waze Help: report police](https://support.google.com/waze/answer/13739289); [Waze Help: road hazards](https://support.google.com/waze/answer/13739290?hl=en); [Waze forum](https://www.waze.com/discuss/t/newbie-how-long-do-reported-hazards-remain-on-map/64592) (forum = **[weak]**)
- Crowdsourced report reliability: in a Tennessee FHWA-supported study, Waze crash reports arrived ~2.2 min sooner than the official log, but only 26% of Waze crash reports matched official records. A Norfolk flood model classified ~71.7% of Waze flood reports as trustworthy **[moderate; figures from search excerpts, exact source document among the three links not confirmed]** — [ROSA P / DOT](https://rosap.ntl.bts.gov/view/dot/60057); [Iowa State dissertation](https://www.imse.iastate.edu/files/2018/07/Amin-NaseriMostafa-dissertation.pdf); [NSF PAR](https://par.nsf.gov/servlets/purl/10291591)

**Consensus grading (iNaturalist)** — see Section 1: 2/3 supermajority, at least 2 IDs, plus metadata prerequisites (date, location, media) and community-revocable flags **[moderate]** — [iNaturalist help](https://help.inaturalist.org/support/solutions/articles/151000169936)

**Brazilian analog: Fogo Cruzado (crowdsourced shooting reports)**
- Users can report gunfire anonymously. The team cross-checks each report against other reports in the same area and against official police information, then publishes verified data via an open API **[weak/moderate]** — [Olhar Digital](https://olhardigital.com.br/2021/07/29/tira-duvidas/fogo-cruzado-entenda-como-funciona-o-aplicativo-que-mapeia-tiroteios/); [Exame](https://exame.com/brasil/apps-sao-usados-para-trocar-informacoes-sobre-tiroteios-no-rio)
- Critics (Revista Oeste, ideologically aligned outlet) allege such crowdsourced counts can exceed official records **[weak]** — [Revista Oeste](https://revistaoeste.com/revista/edicao-95/a-realidade-fuzilada/)

**Cost of false/stale reports (from lost-pet scams, Section 5)**
- Brazilian scammers send fabricated or AI-edited "found" images of a lost pet to the owner and demand Pix transfers **[weak, multiple news cases]** — [Estado de Minas, 10/07/2026](http://www.em.com.br/gerais/2026/07/7458985-golpe-com-inteligencia-artificial-atinge-tutores-de-animais-perdidos-em-bh.html); [Metrópoles](https://www.metropoles.com/colunas/mirelle-pinheiro/golpista-usa-ia-para-fingir-resgate-de-cachorro-e-engana-familia)

### Inferences
- **Do not deploy BTS or peer-prediction payments.** The platform has no money flowing to reporters (and should not, see Section 5), its populations are tiny per event (a few people saw *this* dog on *this* corner), there is no common prior, and users are in an emotional emergency. Every precondition fails. A cheaper and more robust substitute is the **delayed ground truth** that many cases eventually produce: animal found, rescued, reunited, or confirmed absent. Score reporters with a proper scoring rule on resolved events, and use spot-checks by trusted users on a random sample ("gold" tasks).
- **Model a sighting as a belief that decays.** `confidence(t) = prior(source_trust, evidence) × decay(Δt, species/mobility) ± confirmations`. Only geofenced users (physically near, recently) may vote "ainda está lá / não está mais", and votes are weighted by voter trust. Different animals need different half-lives: an injured, immobile animal decays slowly, while a healthy roaming dog decays fast. This handles staleness without punishing honest reporters.
- **Metadata checks are signals, not proof.** EXIF GPS and timestamps are trivially editable, and photos arriving via WhatsApp typically lose EXIF (known platform behavior, **[unverified]** this session). The strongest *practical* evidence of presence is in-app live capture (camera opened in-app, device location at capture time, server timestamp). Treat gallery uploads as lower-trust. AI-edited images (as in the BH scams) argue for a "foto ao vivo" path and, later, image-forensics checks.
- **Asymmetric error costs** should set the thresholds. A false emergency wastes a volunteer trip, which is costly but bounded. A false "found" claim directed at a grieving owner enables extortion, which is high harm. A precise sighting of a vulnerable colony or a valuable dog leaks location to poisoners or thieves, which is irreversible. Confirmation requirements should scale with harm, not be uniform.
- The **Fogo Cruzado model** (anonymous intake, then staff/trusted cross-check, then publication) is a proven Brazilian template for "publish only after corroboration" layers. It is needed for anything that names places tied to people (e.g., suspected maus-tratos locations).

### Gaps
- No published validation of Waze's "not there" mechanism or its timers. Durations are proprietary.
- No study found measuring false-report rates on any lost/stray-pet platform (PawBoost, Petco Love Lost, Facebook groups).
- No evidence found on how well animal re-identification models perform on Brazilian SRD (vira-lata) dogs and street cats. This is likely covered by another researcher, but it matters for automated chain-linking confidence.

---

## 3. Coordination: convergence vs. nobody acting; claims and timeouts; evidence from volunteer-responder dispatch apps; vigilantism (Citizen)

### Takeaway
Volunteer-responder apps show that **alert acceptance is low and highly variable (1.3% to ~22% of alerts)**, that **about half of those who accept never arrive**, and that the systems tune small radii and caps on the number alerted, keeping alerts going until a target number accepts. Even when responders arrive first and do more, hard outcomes do not always improve. Responders bear measurable psychological load. Citizen shows what happens when a platform turns crowds toward *people* and adds money: a wrongful manhunt, and police cutting ties.

### Cited Findings
**Radius, caps, acceptance, arrival**
- London (GoodSAM), 2023/24: volunteers were alerted for 29.3% (n=3,592) of cardiac arrests and accepted 22.4% (n=806) of alerts. 47.5% (n=383) of accepters **did not arrive**, and 20.7% (n=167) arrived before the ambulance **[moderate, service report]** — [London Ambulance Service Cardiac Arrest Annual Report 2023/24](https://www.londonambulance.nhs.uk/wp-content/uploads/2024/12/Cardiac-Arrest-Annual-Report-2023-24-1-1.pdf)
- An earlier GoodSAM study: alerts were accepted in only 1.3% (53/4,196) of London cases and 5.4% (51/1,001) of East Midlands cases. London alerted up to 3 responders within 200 m, East Midlands up to 5 within 800 m. Adjusted odds of survival to discharge were ~3.15 and 3.19 when a responder accepted, but acceptance was "low" **[moderate, observational]** — [PMC8757292](https://pmc.ncbi.nlm.nih.gov/articles/PMC8757292/); [NIHR Evidence alert](https://evidence.nihr.ac.uk/alert/more-people-survived-cardiac-arrest-first-aiders-goodsam-alert/)
- Denmark HeartRunner: configurable radius of 1,800 m, alarms to up to 20 nearest volunteers, and a volunteer who accepts and then moves out of range is told they are no longer needed **[moderate, trial protocol]** — [HeartRunner Trial protocol NCT03835403](https://cdn.clinicaltrials.gov/large-docs/03/NCT03835403/Prot_SAP_002.pdf)
- Victoria, Australia (GoodSAM): alerts the 3 nearest volunteers within 400–500 m (metro) or 5 km (regional) and **keeps alerting until 3 accept**. Volunteers have no legal obligation to accept **[moderate]** — [MJA 2025](https://www.mja.com.au/journal/2025/222/10/smartphone-activated-volunteer-responders-and-survival-discharge-after-out)
- Sweden SMS Lifesavers: ~1,500 m radius and ~21,000 volunteers (Karolinska). The NEJM evaluation reported ~30% more bystander CPR **[strong for CPR outcome; news summary]** — [Karolinska Innovations](https://karolinskainnovations.ki.se/20years/2020/09/30/heartrunner-sweden/); [CBS News on NEJM](https://www.cbsnews.com/news/mobile-app-helps-save-cardiac-arrest-victims)
- Skåne: the number of community first responders doubled from 11,000 to 22,450 over the audit period **[moderate]** — [Region Skåne quality report](https://www.skane.se/siteassets/organisation_politik/publikationer_dokument/kvalitetsutvardering-av-systemet-sms-livraddare-skane.pdf)
- SAMBA RCT (Sweden, Heartrunner AED-retrieval arm, 1.3 km radius): **no significant increase** in bystander AED use **[strong, RCT]** — [2 Minute Medicine summary](https://www.2minutemedicine.com/visualabstract-smartphone-dispatch-of-volunteer-responders-may-not-increase-bystander-use-of-automated-external-defibrillator-in-out-of-hospital-cardiac-arrest/)
- Copenhagen (Andelius et al., JACC 2020): when volunteers arrived before EMS, bystander defibrillation was 21.2% vs 6.7% and bystander CPR 85.3% vs 76.8%, but 30-day survival did not differ significantly **[strong, observational]** — [TCTMD](https://www.tctmd.com/news/smartphone-app-boosts-bystander-response-cardiac-arrest); [SCA Aware](https://www.sca-aware.org/index.php/sca-news/smartphone-activation-of-citizen-responders-facilitates-cpr-and-defibrillation-in-out-of)

**Responder wellbeing and safety**
- Several *Resuscitation Plus* studies document psychological impact on app-dispatched volunteers and recommend considering professional debriefing (Kragh et al. 2021, Denmark; Källestedt et al. 2022, Sweden, qualitative; Ganter et al. 2025, longitudinal). An RCT of structured debriefing (NCT07607808, target n=75) has no results yet **[moderate]** — [Kragh 2021 PDF](https://vbn.aau.dk/ws/files/448968710/Kragh_et_al._2021_._Immediate_psychological_impact_on_citizen_responders_dispatched_through_a_mobile_application_to_out_of_hospital_cardiac_arrests.pdf); [Ganter 2025, PMC11995795](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11995795/); [Källestedt 2022 DOAJ](https://doaj.org/article/df2270437bde4a08b3d0102fc52b289c); [ClinicalTrials NCT07607808](https://clinicaltrials.gov/study/NCT07607808)
- The HeartRunner trial protocol explicitly examines whether activating citizen responders is physically and psychologically safe **[moderate]** — [Protocol](https://ClinicalTrials.gov/ProvidedDocs/03/NCT03835403/Prot_SAP_002.pdf)

**Citizen app: vigilantism and engagement incentives**
- Citizen launched in 2016 as "Vigilante" ("Can injustice survive transparency?"). Apple removed it in Nov 2016 for risking physical harm, and it relaunched as Citizen in 2017 **[moderate, investigative journalism]** — [Vice](https://www.vice.com/en/article/inside-crime-app-citizen-vigilante)
- In May 2021, Citizen ran a ~7-hour livestreamed manhunt for a Palisades-fire "arson suspect". The reward rose from $10k to $30k, a reward push went to 848,816 LA users, and the man was **innocent**. Leaked Slack shows the CEO tying the hunt to signup growth ("Blast to all of la") and a staffer's ToS objection being ignored. Employees were measured on how fast and how many incidents they published. A covert "Street Team" posed as ordinary users to encourage engagement **[moderate]** — [Vice](https://www.vice.com/en/article/inside-crime-app-citizen-vigilante); [Fox LA](https://www.foxla.com/news/citizen-app-sets-off-manhunt-for-man-falsely-accused-of-starting-palisades-fire); [Input](https://www.inputmag.com/tech/messages-show-citizen-ceos-unhinged-hunt-for-wrongly-ided-arson-suspect)
- LAPD cut ties with Citizen after the episode, per emails obtained by Motherboard via public-records request **[moderate]** — [Techdirt (on Motherboard emails)](https://archive.techdirt.com/articles/20220129/19233148382/emails-show-lapd-cut-ties-with-citizen-app-after-started-vigilante-manhunt-targeting-innocent-person.shtml)

**Nextdoor: design friction against profiling**
- In 2016 Nextdoor added a multi-step form for crime and safety posts that requires more descriptors when race is mentioned. The company claimed a 75% reduction in racially profiling posts in test markets, graded blind by staff and outside reviewers. This is a company claim with no independent verification **[weak]** — [Nextdoor blog](https://blog.nextdoor.com/2016/08/24/reducing-racial-profiling-on-nextdoor); [GeekWire Q&A](https://www.geekwire.com/2016/qa-nextdoor-ceo-explains-social-network-cracking-racial-profiling/)

### Inferences
- **Both failure modes are real, and they are spatially split.** In dense, middle-class areas (centro) the risk is convergence: several protetores show up, territorial friction follows, and people get alert fatigue. In periferias and rural edges the risk is that nobody acts. Fixed-radius broadcast fails both. Recommended: **adaptive radius plus target-acceptance** (Victoria model). Alert the nearest K qualified users, expand the radius in rings until N accept (N = 1–3 depending on severity), then **stop alerting**.
- **Claims must expire.** London's 47.5% non-arrival among accepters means "Estou a caminho" is a weak commitment. Mechanism: claim → ETA → automatic expiry (e.g., ETA + buffer) unless the user checks in (location ping or "cheguei") → case returns to the pool and the next ring is alerted. Track claim-to-arrival reliability as a *private* reputation feature that decides who is alerted first next time. Allow multiple claims up to a cap (e.g., 2), because a single claim plus a no-show is the worst case.
- **"Ninguém assumiu" must be visible.** Bystander diffusion of responsibility (classic social psychology, not re-verified here) is reduced when the state is explicit and the ask is personal: "Você é a pessoa mais próxima; 0 pessoas a caminho". After a timeout, escalate to institutional actors (verified ONG on duty, CCZ, Defesa Civil in disasters).
- **Volunteer outcomes may not move hard outcomes** (SAMBA null; Andelius no survival difference). Measure success by *resolution* (animal reached, transported, reunited), not by alerts sent or "engagement". Avoid Citizen's KPI trap of rewarding publish speed and volume.
- **Responder safety and wellbeing apply strongly here.** Injured strays bite, owners may be hostile, and some sites are dangerous (areas under trafficker/militia control). Provide safety guidance, never send responders toward human conflict, and offer debrief and psychological-support resources. Compassion fatigue among protetores is the pet-world version of responder distress.
- **Never point the crowd at people.** The Citizen lesson for this platform: no bounties, no "find the abuser" threads, no posting faces or addresses of suspects. Maus-tratos reports should go through structured forms to authorities (a Nextdoor-style friction pattern), not open chat.

### Gaps
- No acceptance or arrival data found for PulsePoint, and no responder-app study that measures *alert fatigue* directly (opt-out or uninstall rates vs. alert frequency). Acceptance rates are the closest proxy.
- No empirical study found of claim/assignment-with-timeout mechanisms in animal-rescue or lost-pet contexts.
- No Brazilian evidence found on volunteer-responder apps. The SAMU/Corpo de Bombeiros context was not researched.

---

## 4. Sociology of Brazil's animal-protection field (protetores, ONGs, CCZ, hoarding, donations, territory, community animals)

### Takeaway
The field is large, informal, under-resourced and care-driven, and much of it runs on women's unpaid labor. It is organized through social-media groups (Orkut, then Facebook, Instagram, WhatsApp). Since 2021–22 the legal frame bars CCZs from killing healthy animals and treats harming dogs and cats as a serious crime. Laws on community dogs (cão comunitário) give a formal role to a named community caretaker, the "mantenedor/cuidador principal". Hoarding is real, measurable and concentrated in lower-income dense areas. Donation and Pix fraud by fake or opportunistic "protetores" is documented, as are reputational conflicts among real ones.

### Cited Findings
**Who protetores are, and how they organize**
- Anthropologist Andréa Osório (UFF) studies street-animal protectors in Rio. Her work traces paths into protection (childhood pet memories, adult value shifts) and street-cat protectors organized online on Orkut (2011) and Facebook (netnography of a group created in 2009). It also documents common accusations against protectors (irrationality, misanthropy, sentimentalism), which she reads through ecofeminism and care theory as care work done mostly by women **[moderate, qualitative]** — [Osório publications (Academia)](https://uff.academia.edu/AndreaOsorio); [R@U article](https://www.rau2.ufscar.br/index.php/rau/article/download/56/53); [Iluminuras issue](https://seer.ufrgs.br/index.php/iluminuras/issue/view/2971)
- Osório also contrasts historic street-animal removal during São Paulo's modernization with today's rescue groups, and documents Rio's municipal animal-protection secretariat (SEPDA) shifting the state's stance **[moderate]** — [Teoria e Sociedade](https://bib44.fafich.ufmg.br/index.php/rts/article/download/76/63)
- An MPRJ journal article analyzes animal protectors through social-movement theory, based on fieldwork including Rio's Núcleo de Proteção Animal **[moderate]** — [Revista do MPRJ nº 80](https://www.mprj.mp.br/servicos/revista-do-mp/revista-80/artigo-das-pags-19-56)
- Independent protetores in Alagoa Grande (PB): most earn up to 2 minimum wages, and the main difficulty they report is lack of municipal support **[weak, undergraduate thesis]** — [UFPB TCC 2022](https://repositorio.ufpb.br/jspui/handle/123456789/23598)
- A UFMG master's thesis (2023) characterizes animal protectors in Belo Horizonte from an epidemiology and zoonoses angle **[moderate]** — [UFMG dissertation](https://repositorio.ufmg.br/bitstream/1843/60837/3/LISLIE%20DISSERTA%c3%87%c3%83O%20CORRIGIDA.pdf)

**Scale (Instituto Pet Brasil surveys; conflicting figures)**
- One IPB edition (cited in 2022 documents): ~184,960 animals under ONGs/protetores, 96% dogs and 4% cats **[moderate]** — [Balneário Camboriú Controladoria doc](https://controladoria.bc.sc.gov.br/wp-content/uploads/2022/09/Plano-de-Trabalho-Termo-Aditivo-VIVA-BICHO-racao-portal.pdf); [Bem Paraná](https://www.bemparana.com.br/rededobem/sociedade-busca-dar-protecao-a-animais-em-curitiba/)
- 2024 edition per CNN Brasil: ~4.8 million dogs and cats "in vulnerability" and ~201k under ONGs/protetores. The reported split of "92% cats / 8% dogs" inverts the earlier ratio and may be a reporting error, so **treat it with caution** — [CNN Brasil](https://www.cnnbrasil.com.br/nacional/quase-5-milhoes-de-pets-estao-em-situacao-de-vulnerabilidade-no-brasil/)
- ~400 ONGs mapped (370 in 2018) **[moderate]** — [Correio Braziliense blog](https://blogs.correiobraziliense.com.br/maisbichos/pandemia-aumentou-vulnerabilidade-de-animais/)

**State and CCZ relationship; legal frame**
- Lei 14.228/2021 (in force 18/02/2022) bars zoonoses agencies, public kennels and similar bodies from killing dogs and cats, except euthanasia for serious incurable infectious diseases that endanger human or animal health, justified by a technical report. Animal-protection entities get unrestricted access to the supporting documentation **[strong, statute]** — [Planalto L14228](https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2021/lei/l14228.htm); [Câmara](https://www2.camara.leg.br/legin/fed/lei/2021/lei-14228-20-outubro-2021-791889-norma-pl.html)
- In 2026 the TJ-DF blocked euthanasia of an asymptomatic dog diagnosed with leishmaniasis, an example of protetor/CCZ disputes reaching the courts **[moderate]** — [Conjur](https://www.conjur.com.br/2026-mar-27/tj-df-impede-eutanasia-de-cadela-com-leishmaniose-por-estar-assintomatica//?print=1)
- A municipality that authorized slaughter of abandoned animals reversed course after public backlash (headline-level only) **[weak]** — [Itatiaia](https://www.itatiaia.com.br/brasil/municipio-que-autorizou-abate-de-animais-abandonados-volta-atras-apos-repercussao-negativa/)
- Lei 14.064/2020 ("Lei Sansão") added §1º-A to art. 32 of Lei 9.605/98: maus-tratos against dogs or cats carry 2–5 years' reclusão, a fine, and a ban on keeping animals, which takes it out of the low-offense category **[strong, statute + doctrine]** — [Dizer o Direito](https://www.dizerodireito.com.br/2020/09/lei-140642020-aumenta-pena-do-crime-de.html?m=1); [Jus.com.br](https://jus.com.br/artigos/98331/crime-de-maus-tratos-aos-animais-e-a-lei-n-14-064-de-2020)

**Cão/gato comunitário institutions**
- SP state Lei 12.916/2008, art. 4º §§1–2: a recognized community dog is collected for sterilization and registration and **returned to its community of origin** after its *cuidador principal* is identified and signs a commitment term. A "cão comunitário" is defined as one with "laços de dependência e de manutenção" with the community but no single owner **[strong, statute]** — [ALESP](https://www.al.sp.gov.br/repositorio/legislacao/lei/2008/lei-12916-16.04.2008.html); [Animal Legal & Historical Center](https://www.animallaw.info/node/37538)
- Municipal bills (Curitiba, Juiz de Fora PL 105/2026, Aracruz) and state bills (SP PL 1/2026, SC) create a registered *cuidador/mantenedor* who must feed the animal, look after its welfare and notify the municipal protection network. RS Lei 15.254/2019 reportedly defines community dogs and requires tutor registration (**not verified** against official text) **[moderate/weak]** — [Tribuna PR on Curitiba bill](https://www.tribunapr.com.br/noticias/curitiba-regiao/projeto-de-lei-em-curitiba-exclui-gatos-e-foca-apenas-em-caes-comunitarios/); [Câmara JF](https://www.camarajf.mg.gov.br/sal/mostrapft.php?n=302673); [Câmara POA minutes](https://www.camarapoa.rs.gov.br/draco/sessoes_plenarias/83086/1555965598.pdf)

**Hoarding (acumuladores)**
- Curitiba, Sep 2013–Apr 2015: of 226 complaints, 113 were confirmed hoarding cases (6.45 per 100k inhabitants): 42.5% object, 36.3% animal, 21.2% mixed. There was a spatial cluster in the north of the city, and cases rose with population density and fell with neighborhood income **[strong, peer-reviewed]** — [Cunha et al., Cad. Saúde Pública 2017](https://scielosp.org/article/csp/2017.v33n2/e00001316)
- A separate Curitiba study reported at least 65 animal-hoarding residences holding 724 dogs **[moderate]** — [PMC10959369](https://pmc.ncbi.nlm.nih.gov/articles/PMC10959369); sociodemographic follow-up: [PMC8829411](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8829411/)
- Legal and journalistic commentary frames some hoarders as self-identified "defensores da vida" (rescuers) **[weak]** — [Jus.com.br](https://jus.com.br/artigos/119887/acumuladores-de-animais-ou-defensores-da-vida)

**Donation culture and fraud (see Section 5 for details)**
- Documented cases include fake rescue profiles collecting donations, a mass operation of look-alike Pix keys diverting protectors' donations during the 2024 RS floods, and a former municipal animal-welfare secretary arrested (June 2026) on allegations of using her protector image to raise donations **[weak, news]** — [Diário do Nordeste](https://diariodonordeste.verdesmares.com.br/seguranca/dupla-e-presa-apos-criar-perfil-falso-para-ajudar-gatos-e-abandonar-os-animais-nas-ruas-de-fortaleza-1.3235675); [Baguete](https://www.baguete.com.br/noticias/casal-de-atores-e-preso-por-golpe-com-pix); [Metrópoles](https://www.metropoles.com/colunas/mirelle-pinheiro/ex-secretaria-de-bem-estar-animal-e-presa-por-eutanasia-via-pix)

### Inferences
- **Actor map (for trust-tier design):**
  - *Protetores independentes*: highest local knowledge and commitment, lowest resources, informal and often unregistered (no CNPJ). They are the core "privileged group" and need power tools, not gamification.
  - *ONGs*: a CNPJ makes them verifiable, they have capacity limits, and they depend on donations, so they are reputation-sensitive and potentially competitive.
  - *CCZ/zoonoses*: legal authority, legally constrained (Lei 14.228), historically distrusted by protetores. They are a recognized-authority anchor (Ostrom principle 7) if they are present on the platform.
  - *Mantenedores of community dogs and cats*: legally recognized caretakers in some jurisdictions. Their animals are *not* "lost" or "stray" in the platform sense, so mistakes here cause conflict (Section 5).
- **Territoriality and credibility.** A field that runs on reputation in WhatsApp and Facebook groups, with public accusations of being "sentimental" or a "fake protetora", will bring its conflicts onto the platform. Per-chain chat is where they will happen. Designs that make credit and blame *public and rankable* (leaderboards, public star ratings of protetores) are likely to escalate turf conflicts. That expectation rests on theory plus the reputation-inflation and retaliation evidence above; no direct Brazilian study was found.
- **Burnout and hoarding are linked risks.** A protetor overwhelmed by intake, with low income and social pressure to "never say no", is exactly the profile that can slide into hoarding. The platform must avoid becoming a funnel that pushes more animals onto a few known protetores. Load-aware routing (capacity flags such as "lotada / não posso receber") is a welfare mechanism, not just UX.
- **Class and territory.** Hoarding clusters in denser, lower-income areas (Curitiba), protetores often have low income (PB), and app-based help skews toward smartphone-rich, well-connected areas. Expect coverage to be densest where need is lowest. WhatsApp intake and an institutional escalation path matter for equity.

### Gaps
- No Brazilian peer-reviewed study found that quantifies protetor burnout or compassion fatigue. Searches surfaced only general studies of women's unpaid care load (Think Olga "Esgotadas"), which is not specific to animal protection: [Correio Braziliense blog](https://blogs.correiobraziliense.com.br/coletivo-filhas-da-mae/2023/10/27/estamos-esgotadas/).
- No sociological study found that directly documents conflicts among protetores, ONGs and CCZ, or "periferia vs centro" differences in protection activity. Evidence is indirect (hoarding geography, income of protetores, court disputes).
- IPB figures conflict across editions (dog/cat ratio). The primary IPB report was not retrieved.
- RS Lei 15.254/2019 was not verified against the official text.

---

## 5. Abuse vectors and scams (and how comparable platforms mitigate them)

### Takeaway
Every abuse vector the brief anticipated has documented Brazilian cases:
- the lost-pet "found it, send Pix" scam, now using AI-edited photos of the owner's *own* pet and adding threats;
- extortion ("pay or the animal dies");
- donation fraud via fake protetores and look-alike Pix keys;
- poisoning of cat colonies with chumbinho;
- theft of purebred dogs for resale;
- organized dog fighting;
- defamation liability for online accusations of maus-tratos.

The common enabler is **publicly exposed contact data plus precise location plus an identifiable animal**. Mitigations seen elsewhere are mostly advice plus friction: never pay before return, verify via video, masked contacts, and microchip checks.

### Cited Findings
**Golpe do pet perdido / falso resgate (Brazil)**
- Pattern: after an owner posts a lost-pet ad with photo and phone on social media, scammers claim to have found the animal (often "in another city"), ask for R$100–150 for fuel, tolls or food via Pix, and disappear **[weak, news]** — [Folha do Interior, 26/08/2026](https://www.folhadointerior.com.br/golpistas-usam-animais-perdidos-para-enganar-tutores-e-pedir-dinheiro-via-pix/)
- Evolution, 2026: scammers use AI to edit the owner's own pet photo into "found" scenes (behind a car, on a sofa). When asked for a live video or location details, they threaten the owner ("we know where you live") or the animal. The administrator of a BH lost-pet page receives such reports "com frequência" **[weak, news]** — [Estado de Minas, 10/07/2026](http://www.em.com.br/gerais/2026/07/7458985-golpe-com-inteligencia-artificial-atinge-tutores-de-animais-perdidos-em-bh.html)
- Ponta Grossa (PR): AI-generated image of the dog, a first Pix of R$300, then demands for more and a threat to kill the animal **[weak]** — [Metrópoles](https://www.metropoles.com/colunas/mirelle-pinheiro/golpista-usa-ia-para-fingir-resgate-de-cachorro-e-engana-familia)
- DF: callers claiming to have the dog demanded transfers, and a boletim de ocorrência for *extorsão* was filed at the 2ª DP (Asa Norte) **[weak]** — [Metrópoles DF](https://www.metropoles.com/distrito-federal/cao-desaparece-e-dono-e-vitima-de-golpe-apos-bandidos-pedirem-resgate)
- BH (2023): victim made three Pix transfers totaling R$588 **[weak]** — [Estado de Minas 2023](https://www.em.com.br/gerais/2023/11/6663077-criminosos-aplicam-golpe-de-pix-em-anuncio-de-cachorro-desaparecido.html)
- Campo Grande (MS): R$500 demanded with photos; the owner went to police first, and the case was registered as extortion **[weak]** — [Nova Lima News](https://novalima.news/mulher-perde-cachorro-e-criminoso-tenta-aplicar-golpe-de-r-500-para-devolver-o-animal-em-cg/)
- Recovery is poor: only 8.9% of money lost to Pix scams between Jan 2022 and Apr 2026 was returned. The MED (Mecanismo Especial de Devolução) exists but does not guarantee refunds **[moderate, news analysis of BCB data]** — [O POVO+](https://mais.opovo.com.br/reportagens-especiais/2026/07/24/a-cada-rs-100-em-golpes-no-pix-instituicoes-devolvem-apenas-rs-890.html); [Serasa](https://www.serasa.com.br/premium/blog/golpe-do-pix-premiado-entenda-como-funciona/)

**Comparable platforms abroad (US)**
- PawBoost-linked scams: a "finder" asks the owner for a Google verification code to "prove ownership", which hijacks the owner's number. PawBoost's co-founder advises calling the number rather than replying by text **[weak, news]** — [CBS Colorado](https://www.cbsnews.com/colorado/news/scammers-targeting-coloradans-castle-rock-missing-pets/); [WKBW](https://wkbw.com/news/local-news/beware-of-lost-pet-scam)
- Fake shelter "emergency surgery" calls with spoofed shelter numbers. Shelters state they never request payment by phone for lost-pet care, and advise paying rewards only after the pet is back in hand. Other variants include a fake "Urgent Care Team" (Dallas) and fake paid "satellite pet location" services **[weak]** — [WSVN Broward](https://wsvn.com/news/local/broward/scammers-targeting-lost-pet-owners-in-broward-humane-society-warns/); [WFAA Dallas](https://wfaa.com/article/news/local/dallas-county/dallas-animal-services-scam-targeting-people-lost-pets/287-7e145f64-5a0a-4b33-9734-a36d415357b0); [Local10 (flyers as vector)](https://www.local10.com/news/local/2025/02/10/scammers-use-lost-pet-flyers-to-get-to-victims-in-south-florida/)
- Recommended verification: microchip scan at a shelter or vet, a photo or video of the pet, and calling back through an independently verified number **[weak]** — [HSNT](https://www.hsnt.org/post/beware-common-scams-targeting-pet-owners-of-missing-pets)

**Donation fraud and fake protetores**
- Ceará, June 2024: an actor couple allegedly created **234 Pix keys** resembling protectors' keys to divert donations for animals rescued in the RS floods (relying on one-digit typos) **[weak, news]** — [Baguete](https://www.baguete.com.br/noticias/casal-de-atores-e-preso-por-golpe-com-pix)
- Fortaleza, May 2022: a pair arrested in flagrante for a fake cat-rescue profile, charged with estelionato and falsidade ideológica, who allegedly abandoned the animals **[weak]** — [Diário do Nordeste](https://diariodonordeste.verdesmares.com.br/seguranca/dupla-e-presa-apos-criar-perfil-falso-para-ajudar-gatos-e-abandonar-os-animais-nas-ruas-de-fortaleza-1.3235675)
- Canoas (RS), June 2026, Operação Carrasco: a former municipal animal-welfare secretary was arrested on allegations of using her protector image to raise donations while ~498 animals were euthanized during her 8 months in office (police allegations, no verdict) **[weak]** — [Metrópoles](https://www.metropoles.com/colunas/mirelle-pinheiro/ex-secretaria-de-bem-estar-animal-e-presa-por-eutanasia-via-pix)
- Vila Velha (ES), 2021: a family indicted for estelionato and maus-tratos **[weak]** — [A Gazeta](https://www.agazeta.com.br/es/policia/familia-e-indiciada-por-estelionato-e-maus-tratos-de-animais-em-vila-velha-0221). Alagoas: police say ONG members raised over R$300k in donations (headline-level only) — [TNH1](https://www.tnh1.com.br/noticia/nid/integrantes-de-ong-arrecadaram-mais-de-r-300-mil-com-doacoes-voluntarias-diz-policia/)

**Fake sales and fake "adoption"**
- A scheme passed off mixed-breed dogs as purebreds using internet photos of supposed parents. A foundation describes such actors as posing as caretakers while engaged in illegal commerce (headline-level detail) **[weak]** — [Metrópoles](https://www.metropoles.com/brasil/esquema-mutilava-caes-vira-latas-para-venda-como-animais-de-raca)
- No Brazilian police or Procon alert was found specifically on the fake-adoption "frete via Pix" scam. Fake Pix receipts against veterinary clinics are documented (Rio, Jul 2026) **[weak]** — [BandNews](https://www.band.com.br/bandnews-fm/rio-de-janeiro/noticias/mulher-e-presa-acusada-de-aplicar-golpe-do-falso-pix-em-clinica-202607271614)

**Theft for resale, breeding and fighting**
- Guarulhos (SP), 2025: an armed group intercepted a van carrying 6 purebred dogs (up to R$10k each, all microchipped) **[weak]** — [SBT News](https://sbtnews.sbt.com.br/noticia/brasil/policia-procura-caes-de-raca-levados-em-assalto-em-guarulhos)
- Polícia Civil de Goiás article (author opinion, not statistics): stolen dogs are passed to drug dealers and then to clandestine kennels, and sold below market. A stolen Yorkshire was traced via a classifieds sale ad **[weak]** — [PC-GO](https://goias.gov.br/policiacivil/furto-de-caes-o-por-que/); [PC-GO recovery](https://goias.gov.br/policiacivil/?p=85649)
- Mairiporã (SP), Dec 2019: an international pit-bull fighting ring was dismantled, with 41 arrested (including physicians, veterinarians, a military police officer and foreigners) and 19 dogs rescued (some dead). Another 33 pit bulls were later found in Itu **[moderate, police + press]** — [Gov. Paraná](https://www.parana.pr.gov.br/Audio/Policia-Civil-do-Parana-prende-40-pessoas-em-rinha-internacional-de-caes); [Tribuna de Jundiaí](https://tribunadejundiai.com.br/policia/apos-fechar-rinha-de-caes-policia-resgata-33-pit-bulls-em-itu/); [Band B](https://www.bandab.com.br/seguranca/justica-mantem-um-preso-e-libera-40-dos-detidos-em-rinha-de-caes-mais-caes-sao-localizados/)

**Poisoning of colonies**
- Chumbinho (an illegal rodenticide) poisonings are recurrent:
  - BH ONG BastAdotar (Feb 2025): 10 cats dead, chumbinho found at necropsy
  - Vila Isabel (RJ) zoo colony: at least 10 cats dead, with suspicious bait found
  - Camaçari (BA) luxury condominium: 8 bodies, chumbinho confirmed
  - Cariacica (ES): a merchant arrested for selling chumbinho after 10 dogs and 20 cats died
  - Jundiaí (SP): 17 cats dead

  **[weak, news; multiple independent cases]** — [SBT News](https://sbtnews.sbt.com.br/noticia/policia/policia-investiga-a-morte-de-10-gatos-por-envenenamento-em-ong-de-bh); [Tupi](https://www.tupi.fm/?p=2055171); [Correio 24h](https://www.correio24horas.com.br/bahia/gatos-sao-mortos-por-envenenamento-em-condominio-de-luxo-em-camacari-0321); [CNN Brasil](https://www.cnnbrasil.com.br/nacional/sudeste/es/homem-e-preso-por-vender-chumbinho-apos-30-animais-morrerem-envenenados/); [Tribuna de Jundiaí](https://tribunadejundiai.com.br/policia/moradora-de-jundiai-perde-17-gatos-e-4-sao-internados-apos-envenenamento-em-massa/)

**Doxxing, harassment and defamation exposure**
- TJMG: using a social network to accuse someone of a crime, publish their personal data and incite third parties exceeded freedom of expression. The court upheld R$4,000 in moral damages plus a public retraction **[moderate, court decision]** — [TJMG decision PDF](https://bd.tjmg.jus.br/bitstreams/f05e811d-7c53-4a30-95ca-8fd451a1b93d/download)
- The singer Zé Neto, accused of maus-tratos, sued celebrity protector Luisa Mell (headline-level; outcome not verified) **[weak]** — [Compre Rural](https://comprerural.com/ze-neto-acusado-de-maus-tratos-processa-luisa-mell/)
- iNaturalist precedent for location protection: sensitive taxa (IUCN Near Threatened or worse, or curator-flagged) are auto-obscured to a random point in a 0.2°×0.2° cell (~22×22 km at the equator). True coordinates are visible only to the observer and to curators of projects the observer joins **[moderate]** — [iNaturalist help: sensitive species](https://help.inaturalist.org/en/support/solutions/articles/151000233080-how-does-inaturalist-protect-the-locations-of-sensitive-species-); [iNat Vermont privacy post](https://inaturalist.ca/posts/9649-understanding-your-privacy-settings-for-inaturalist-vermont)

### Inferences
- **Threat model by data element:**

| Exposed data | Attacker | Harm | Minimum control |
|---|---|---|---|
| Owner phone and name on a lost-pet post | Scammer / extortionist | Pix loss, threats | Masked in-app contact; no public phone; auto-warn on money requests |
| Lost-pet photos (high-res, unique marks) | Scammer (AI edits) | Convincing fake "found" proof | Keep 1–2 "secret marks" private for ownership challenges; watermark and down-res public photos |
| Exact home location of a guardian | Stalker, thief, harasser | Doxxing, burglary | Never publish home coordinates; snap to a coarse cell |
| Exact location of a cat colony or feeding point | Poisoner, hostile neighbor/condomínio | Mass killing | Auto-obscure colonies (iNat-style "sensitive taxon" rule); exact location only to the mantenedor and verified orgs |
| Sightings of valuable breeds or pit bulls with location | Thieves, fighting rings | Theft, fighting | Breed-based auto-obscuring; delay publication; verified-only exact location |
| Maus-tratos accusation with a person's identity | Mob, vigilante | Harassment; **defamation liability** (TJMG) | Structured private report → authorities; no names, faces or addresses in public |
| Donation Pix key in chat or on a case | Fraudster with a look-alike key | Diverted donations | Only platform-verified keys (CPF/CNPJ name match), copy-button, no free-text keys |

- **Scams migrate off-platform.** Even with in-app masking, scammers will try to move victims to WhatsApp. Detect Pix keys, phone numbers and "manda pix" patterns in chat, show inline warnings, and never let the platform itself carry a reward offer (Citizen lesson plus extortion risk).
- **Community animals are a misclassification hazard.** Well-meaning "rescuers" may remove a registered cão comunitário from its territory, or report it as "abandoned", and so trigger conflict with its mantenedor. The platform should let mantenedores mark a "comunitário" status, which suppresses "stray/lost" calls to action.

### Gaps
- No official Brazilian police or Procon advisory found that names "golpe do pet perdido" specifically. Evidence is news reports plus police BOs mentioned in articles.
- No national statistics on dog theft or colony poisoning, and no evidence linking any *platform's* sighting data to a theft or poisoning event. That link is a plausible risk, not a documented case.
- How PawBoost, Petco Love Lost or Nextdoor actually implement contact masking or scam detection was not documented in sources found. Only advice-level mitigations were found.
- Legal analysis of platform liability (Marco Civil art. 19, LGPD for location data) was not researched here and should come from the legal researcher.

---

## 6. Moderation models: community vs. staff, trust tiers, rate limits, progressive trust, report triage

### Takeaway
The best evidence supports a few clear practices: show norms visibly to newcomers, explain removals, and avoid blunt automated rejection of good-faith newcomers. Reputation and badge systems shape behavior for only a fraction of users, and their scores inflate over time. Trust tiers anchored to a central identity root are needed for Sybil resistance. Friction forms (Nextdoor) are a promising but weakly evidenced tool against harmful descriptive content.

### Cited Findings
- **Visible norms work.** A randomized field experiment across 2,190 r/science discussions (2016, ~13M subscribers) found that posting the community rules raised newcomer rule compliance by more than 8 percentage points and newcomer participation by about 70% on average (Matias, PNAS 2019) **[strong, RCT]** — [PMC6525516](https://pmc.ncbi.nlm.nih.gov/articles/PMC6525516); [SSRC citation](https://just-tech.ssrc.org/citation/preventing-harassment-and-increasing-group-participation-through-social-norms-in-2190-online-science-discussions/)
- **Explaining removals works.** In a large-scale Reddit analysis (Jhaver, Bruckman, Gilbert 2019), removal explanations lowered the odds of a user's future removals, and bot explanations were about as effective as human ones. In a survey of 907 users, 37% did not understand why their post was removed. A 2023 quasi-experiment found that *bystanders* who saw explanations increased their posting and interactivity **[strong/moderate]** — [Discourse Meta summary](https://meta.discourse.org/t/transparency-in-moderation-really-matters/133261); [MetaFilter](https://metafilter.com/184083/Does-Transparency-in-Moderation-Really-Matter); [arXiv 2309.08361](https://arxiv.org/abs/2309.08361v2)
- **Over-aggressive quality control drives away newcomers** (Wikipedia, replicated across 769 wikis), see Section 1 **[strong]** — [Meta-Wiki](https://meta.wikimedia.org/wiki/Research:The_Rise_and_Decline)
- **Governance formalizes with growth.** Across ~80k communities, formal rules increase with size and age, and communities favor weak norms **[moderate]** — [deepai summary](https://deepai.org/publication/governing-online-goods-maturity-and-formalization-in-minecraft-reddit-and-world-of-warcraft-communities)
- **Friction forms for harmful descriptions:** Nextdoor's crime-post form claimed a 75% reduction in profiling, with no significant drop in overall users (company claim) **[weak]** — [Nextdoor blog](https://blog.nextdoor.com/2016/08/24/reducing-racial-profiling-on-nextdoor); [Tech & Social Cohesion](https://techandsocialcohesion.substack.com/p/how-nextdoor-reduced-racial-bias)
- **Staff cross-check before publication** (Fogo Cruzado) is a working Brazilian model for sensitive crowd reports **[weak/moderate]** — [Exame](https://exame.com/brasil/apps-sao-usados-para-trocar-informacoes-sobre-tiroteios-no-rio)
- **Engagement KPIs corrupt moderation:** at Citizen, staff were measured by how fast and how many incidents they published, and a ToS objection was overridden **[moderate]** — [Vice](https://www.vice.com/en/article/inside-crime-app-citizen-vigilante)
- **Sybil:** a logically central identity authority is required (Douceur) **[strong]** — [MSR](https://www.microsoft.com/en-us/research/publication/the-sybil-attack/)

### Inferences
- **Split moderation by harm class, not by volume:**
  - *Community-moderated (trusted users, with Ostrom-style local monitors)*: duplicates, chain merges and splits, staleness ("não está mais"), species/identity consensus, off-topic chat. These are low-harm and reversible, with cheap errors.
  - *Staff-moderated (with SLA)*: doxxing, accusations against identifiable people, donation and Pix fraud, extortion reports, colony/location-sensitivity overrides, impersonation of ONGs or CCZ, and hoarding welfare concerns. These are high-harm with legal exposure, and community moderators in a territorial field have conflicts of interest.
- **Progressive trust ladder** (privileges unlock with verified outcomes, not time or volume):
  0. Visitor: sees coarse map only.
  1. Phone-verified: can post sightings and emergencies (rate-limited) and chat.
  2. Reliable reporter: can confirm/deny ("ainda está lá") with weighted votes and propose chain links.
  3. Trusted local (protetor/mantenedor, vouched by 2 trusted users *plus* staff review): sees exact locations within their territory, can merge chains, can mark animals "comunitário".
  4. Verified organization (CNPJ, or a government email domain for CCZ): official badge, can receive donations via verified keys, sees exact locations in their service area, gets escalations.

  Vouching is never the *only* gate (Douceur).
- **Rate limits** on new accounts: posts per hour, chain creations per day, outbound chat messages to strangers. Rate limits should be stricter for content containing phone numbers, Pix keys or URLs.
- **Norm display at the point of action** (Matias): short PT-BR rules shown in every new chain chat, e.g. "não divulgue endereço residencial; não peça/ofereça dinheiro; denúncias de maus-tratos vão pelo botão de denúncia". Removals always come with an explanation (Jhaver), templated and bot-sent if needed.
- **Avoid the Wikipedia trap:** auto-flagging and auto-rejection should route good-faith newcomer reports to soft queues ("needs confirmation") rather than deleting them. In an emergency product, a false rejection may cost an animal's life.
- **Report triage score** = severity (category) × confidence (reporter trust + evidence) × exposure (views, recency). This puts doxxing and extortion at the top regardless of volume.

### Gaps
- No evidence found on moderation in WhatsApp-based civic intake bots, or on Brazilian civic platforms' moderation outcomes (e.g., Colab, Fogo Cruzado internal metrics).
- No independent evaluation of the Nextdoor forms (company claim only).
- No evidence found on comparative effectiveness of volunteer local moderators vs. staff in safety-critical civic apps.

---

## 7. Concrete mechanism recommendations (problem → mechanism → failure mode)

### Takeaway
The minimum viable trust-and-safety core is as follows:
- **coarse-by-default location**, with role-gated exact location and auto-obscuring of sensitive targets;
- **masked contact and no in-platform money** at launch;
- **decaying-confidence sightings with geofenced confirmations**;
- **claims with TTL, plus an adaptive alert radius that stops once enough people accept**;
- **phone-verified progressive trust, anchored by verified orgs and CCZ**;
- **no public accusations of people**;
- **outcome-based private reputation instead of public karma**.

Key invariant: *no data element that lets a stranger find a specific home, colony or valuable animal is publicly exposed at full precision.* Main failure mode: the platform becomes a scam, theft and poisoning targeting tool, or it turns crowds against people, as Citizen did.

### Cited Findings
(Evidence anchors for each mechanism, detailed in Sections 1–6.)
- Coarse location and sensitive-taxon obscuring precedent — [iNaturalist geoprivacy](https://help.inaturalist.org/en/support/solutions/articles/151000233080-how-does-inaturalist-protect-the-locations-of-sensitive-species-)
- Decaying, reaction-driven report lifetime — [Waze Help](https://support.google.com/waze/answer/13739290?hl=en)
- Supermajority consensus with at least 2 IDs — [iNaturalist DQA](https://help.inaturalist.org/support/solutions/articles/151000169936)
- Low acceptance and high no-show of accepted alerts; caps and stop-when-N-accept — [LAS 2023/24](https://www.londonambulance.nhs.uk/wp-content/uploads/2024/12/Cardiac-Arrest-Annual-Report-2023-24-1-1.pdf); [PMC8757292](https://pmc.ncbi.nlm.nih.gov/articles/PMC8757292/); [MJA 2025](https://www.mja.com.au/journal/2025/222/10/smartphone-activated-volunteer-responders-and-survival-discharge-after-out)
- Responder psychological load → debrief — [Kragh 2021](https://vbn.aau.dk/ws/files/448968710/Kragh_et_al._2021_._Immediate_psychological_impact_on_citizen_responders_dispatched_through_a_mobile_application_to_out_of_hospital_cardiac_arrests.pdf)
- Bounties and crowd-on-person dynamics → harm — [Vice on Citizen](https://www.vice.com/en/article/inside-crime-app-citizen-vigilante)
- Lost-pet extortion via exposed contacts and AI images — [EM 2026](http://www.em.com.br/gerais/2026/07/7458985-golpe-com-inteligencia-artificial-atinge-tutores-de-animais-perdidos-em-bh.html); [Folha do Interior](https://www.folhadointerior.com.br/golpistas-usam-animais-perdidos-para-enganar-tutores-e-pedir-dinheiro-via-pix/)
- Look-alike Pix keys — [Baguete](https://www.baguete.com.br/noticias/casal-de-atores-e-preso-por-golpe-com-pix); poor Pix recovery (8.9%) — [O POVO+](https://mais.opovo.com.br/reportagens-especiais/2026/07/24/a-cada-rs-100-em-golpes-no-pix-instituicoes-devolvem-apenas-rs-890.html)
- Reputation inflation, retaliation, Goodhart — [Filippas & Horton](https://cesifo.org/DocDL/cesifo1_wp6750.pdf); [Tadelis 2016](https://ideas.repec.org/a/anr/reveco/v8y2016p321-340.html)
- Peer-prediction impracticality — [Gao et al. EC'14](https://econcs.seas.harvard.edu/resource/gaoec14pdf); [PTS arXiv](https://arxiv.org/pdf/1704.05269)
- Norms display and removal explanations — [Matias PNAS 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6525516); [Jhaver et al.](https://meta.discourse.org/t/transparency-in-moderation-really-matters/133261)
- Newcomer rejection harms — [Halfaker et al.](https://meta.wikimedia.org/wiki/Research:The_Rise_and_Decline)
- Sybil requires a central root — [Douceur](https://www.microsoft.com/en-us/research/publication/the-sybil-attack/)
- Community-dog legal role (mantenedor) — [SP Lei 12.916/2008](https://www.al.sp.gov.br/repositorio/legislacao/lei/2008/lei-12916-16.04.2008.html)
- Defamation exposure for online accusations — [TJMG](https://bd.tjmg.jus.br/bitstreams/f05e811d-7c53-4a30-95ca-8fd451a1b93d/download)

### Inferences

**A. Location and data exposure**

| # | Mechanism | Solves | Failure mode / mitigation |
|---|---|---|---|
| A1 | **Two-layer location:** every point stores `exact` server-side plus a public `display_geom` (snapped hex cell, e.g. ~300–500 m for sightings, coarser for guardian homes). The UI labels "exato" vs "aproximado", as the brief requires. | Doxxing, theft targeting, colony poisoning | Too coarse to find the animal → exact location revealed on *claim* to the claimer only, or to tier ≥3 in territory. Repeated snapping can be averaged to de-fuzz, so use a stable per-entity offset, not per-render randomness. |
| A2 | **Sensitive-target auto-obscure** (iNat "sensitive taxon" analog): cat colonies and feeding points, community animals, high-value breeds, pit-bull-type dogs, and any animal at a residence → coarse cell plus delayed publication (e.g., 6–24 h) for non-emergencies. | Poisoning, theft, fighting-ring sourcing | Breed classifiers err, so allow reporter and staff overrides. Delay harms reunions of lost purebreds, so the owner-match path (private) bypasses the delay. |
| A3 | **Photo hygiene:** strip EXIF on publish (keep server-side for verification), down-res public images, optional auto-blur of faces, house numbers and license plates, keep 1–2 owner "secret marks" private. | Re-identification of homes and people; AI-edit scams | Background landmarks still leak location, so add a "background blur" option for sensitive cases. |
| A4 | **Emergency exact-location TTL:** emergencies in public space show exact location while active and decay to coarse after resolution or expiry. | Long-term exposure of feeding spots and shelters | Some users need history (CCZ planning), so give aggregated heatmaps only. |

**B. Truthful reporting and staleness**

| # | Mechanism | Solves | Failure mode / mitigation |
|---|---|---|---|
| B1 | **Decaying confidence** per sighting (half-life by animal state: injured/immobile vs. roaming) plus **geofenced "ainda está lá / não está mais"** votes weighted by voter trust. | Stale map, wasted trips | Brigading "não está" to hide an animal, so require proximity plus trust and keep a vote audit log. |
| B2 | **"Foto ao vivo" capture path** (in-app camera, device location, server time) ranked above gallery uploads; WhatsApp intake treated as lower-evidence until confirmed. | Fabricated or recycled photos, AI fakes | Excludes low-end phones and low connectivity, so never *block* gallery uploads, only rank them lower. |
| B3 | **iNat-style consensus for chain linking** ("mesmo animal?"): link when more than 2/3 of qualified voters agree, at least 2 independent, revocable. Later, re-ID model scores act as one "voter" with capped weight. | Wrong merges polluting chains | Herding on the first ID, so hide others' votes until you vote. Too few voters in periferias, so allow staff or org resolution. |
| B4 | **Outcome-based private reputation:** score reports against eventual resolution (found, rescued, reunited, confirmed absent) with a proper scoring rule. Use it for alert priority and vote weight, not public display. | Free riding on low-quality reports; Goodhart | Few resolved outcomes means sparse signal, so use shrinkage toward the prior. Never count "animals received" (hoarding incentive). |
| B5 | **No BTS / peer-prediction payments.** Use spot-checks by trusted users on random samples instead. | (Avoids a mechanism that fails here) | n/a |

**C. Coordination**

| # | Mechanism | Solves | Failure mode / mitigation |
|---|---|---|---|
| C1 | **Adaptive ring alerting with target-accept N** (start small, ~300–500 m urban, expand by rings; stop at N accepts, N = 1–3 by severity; per-user daily alert budget and quiet hours). | Convergence vs. nobody; alert fatigue | Sparse periferia, so escalate to orgs or CCZ after T minutes. Dense centro, so the cap prevents swarms. |
| C2 | **Claims with TTL:** "Estou a caminho" plus ETA; auto-release at ETA + buffer unless there is a check-in; max 2 concurrent claimers; reliability score feeds C1 priority. | Claim-and-abandon (London: 47.5% of accepters didn't arrive) | Punitive scoring deters claiming, so score privately and forgive releases made *before* expiry ("não vou conseguir"). |
| C3 | **Explicit "ninguém assumiu" state** plus personal ask ("você é a pessoa mais próxima"). | Diffusion of responsibility | Guilt and burnout, so respect capacity flags. |
| C4 | **Capacity flags** for protetores and ONGs ("lotado", "só transporte", "só castração") used in routing. | Overload, burnout, hoarding drift | Flags go stale, so they auto-expire and need refresh. |
| C5 | **Safety and wellbeing:** pre-dispatch safety tips (bite risk, traffic, unsafe areas), never route to human conflict, post-case check-in and debrief resources. | Responder injury and distress | Liability of advice, so keep guidance generic and refer to professionals. |

**D. Anti-vigilantism and defamation**

| # | Mechanism | Solves | Failure mode / mitigation |
|---|---|---|---|
| D1 | **No accusations against identifiable persons in public content.** Maus-tratos goes through a structured private report (Nextdoor-style friction), routed to Delegacia, MP or the municipal channel, with export for a BO. Chat filters for CPF, address and face images in accusation contexts. | Doxxing, mobs, defamation (TJMG precedent) | Users vent on Instagram anyway, so the platform cannot control that. Its job is to not amplify. |
| D2 | **No bounties or rewards via the platform**, and no "procura-se" for humans. | Citizen-style manhunts, extortion | Owners want to offer rewards for lost pets, so allow a "recompensa oferecida (paga só na entrega)" text label, never escrowed money. |

**E. Money and scams**

| # | Mechanism | Solves | Failure mode / mitigation |
|---|---|---|---|
| E1 | **Masked contact:** in-app or relayed chat; owner phone never public; "found" claims require a proof-of-possession challenge (live video with a requested gesture, or answering private secret-mark questions). | Golpe do pet perdido, extortion, verification-code hijack | Scammers redirect to WhatsApp, so show a warning banner on first contact: "Nunca pague antes de ver o animal; ninguém da plataforma pede código". |
| E2 | **Money-pattern detection** in chat (Pix keys, "manda pix", "taxa", "frete", "gasolina") triggers inline warnings and staff-queue escalation for new accounts. | Off-platform payment fraud | False positives on legitimate vet-cost discussions, so warn rather than block. |
| E3 | **Donations only to verified recipients** (CNPJ or verified CPF), Pix key shown via copy button with the holder name; no free-text keys in campaigns; transparency receipts (vet invoices) as data blocks on the chain. | Look-alike keys, fake protetores | Excludes informal protetores, so allow a verified-CPF tier with lower caps and receipt requirements. |
| E4 | **Impersonation protection:** reserved names and badges for verified ONGs and CCZ; lookalike-name detection. | Fake ONG profiles | Ongoing cost of verification. |

**F. Identity, trust and governance (Ostrom mapping)**

| # | Mechanism | Ostrom principle | Failure mode / mitigation |
|---|---|---|---|
| F1 | **Phone verification** (minimum root) plus optional gov.br or CNPJ for higher tiers; device and behavior signals; rate limits for new accounts. | Clear boundaries; Sybil defense (Douceur) | SIM farms; exclusion of the undocumented, so tier 1 stays open with phone only. |
| F2 | **Progressive trust ladder** (Section 6), with privileges unlocked by verified outcomes. | Graduated rights | Clique capture of tier 3 in a territory, so vouching needs staff confirmation and term limits. |
| F3 | **Territorial (bairro/município) local stewards** drawn from verified protetores and orgs; local rule tweaks (e.g., CCZ hours, partner clinics). | Rules fitted to local conditions; collective choice | Turf wars, so stewards cannot delete others' cases, only flag them, and staff handle disputes. |
| F4 | **Graduated sanctions:** explanation → temporary posting limit → tier demotion → ban; always explained (Jhaver). | Graduated sanctions; monitoring | Inconsistent enforcement, so use public policy pages and templates. |
| F5 | **Cheap conflict resolution:** "disputa" button on a chain (e.g., two protetores claim the same animal, or a mantenedor objects to removal of a community dog) → staff mediation. | Conflict resolution | Volume, so prioritize cases with animal-welfare risk. |
| F6 | **Formal recognition by CCZ and municipalities** (verified agency accounts; data-sharing MoUs). | Recognition of the right to organize; nested enterprises | Political turnover, so keep the platform valuable without government. |
| F7 | **Norms shown at the point of action** in PT-BR (Matias), plus soft queues instead of auto-rejection for newcomers (Halfaker). | Monitoring; newcomer retention | Banner blindness, so rotate concise variants and A/B test them. |
| F8 | **Reputation never public as a single number.** Use badges for verified status, not rank; no rescue leaderboards. | Avoid Goodhart, inflation, turf rivalry | Less "gamified" engagement, which is acceptable: the core group is intrinsically motivated. |
| F9 | **Hoarding welfare signal:** accounts accumulating intake with no adoption, transfer or vet outcomes go to a confidential staff welfare check and referral (never public). | Animal welfare | Stigmatization; privacy, so keep it staff-only and human-reviewed. |

### Gaps
- None of these mechanisms has been tested on a Brazilian lost/stray-pet platform. Their parameters (radii, half-lives, cell sizes, N accepts) are design hypotheses and should be A/B tested or piloted.
- The legal feasibility of masking, of storing exact locations, and of platform liability for chat content (Marco Civil, LGPD, ECA where minors are involved) needs input from the legal research thread.
- Equity effects (WhatsApp-only users, low-end devices, periferias with low connectivity) are not evidenced. Plan pilot measurements by region and income.
