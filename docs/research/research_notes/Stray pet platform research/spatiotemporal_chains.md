# Spatio-temporal chains: animal movement, case linking, temporal logic and location privacy for a Brazilian stray/lost-pet platform

Notes are as of 2026-10-21. "[EXTRAPOLATION]" marks parameters I derived from cited data that no source states directly. "[canonical ref, not fetched]" marks well-known references cited from prior knowledge that I did not re-open this session. Treat them as pointers and check them before quoting.

---

## 1. Empirical animal movement: how far lost/stray dogs and cats travel, time-to-recovery, and what default radii and decay curves follow

### Takeaway
Lost cats are usually found very close to where they escaped. The median is 50 m, 75% are within 500 m, indoor-only cats have a median of 39 m, and outdoor-access cats have a median of 300 m. The chance of finding a lost cat alive flattens after about 60 days. Lost dogs are recovered faster: the median is about 2 days in one study and 71–93% are recovered, mostly through agencies, tags and signs. I found no peer-reviewed distance-travelled data for lost dogs. Free-roaming dogs in Latin America and similar settings have small home ranges (median 95% range about 6–8 ha, roughly 135–160 m equivalent radius) with heavy tails up to km². Brazil-specific urban GPS data for stray dogs appears not to exist.

### Cited Findings

**Lost cats (Huang et al. 2018, *Animals* 8(1):5; online survey, 1,210 cats, 59% USA / 20% Australia / 14% Canada)**
- Outcomes for 1,044 cats with time data: 58% found alive, 2% found dead, 41% not found. Median time to recovery for cats found alive was 6 days (IQR 2–21). Cats found dead: median 21 days (IQR 6–91). — [Huang 2018, Europe PMC full text](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC5789300/fullTextXML)
- Cumulative probability of being found alive (competing risks): 34% by day 7, 50% by day 30, 56% by day 61, 61% by 1 year, 64% by 4 years. There is little increase after day 61 and few cats are found alive after 90 days. — [Huang 2018](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC5789300/fullTextXML)
- Distance from point of escape, cats found alive (n=477): median 50 m, IQR 9–500 m, max 25 km. Cats found dead: median 200 m (IQR 91–500 m), max 5 km. — [Huang 2018](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC5789300/fullTextXML)
- By outdoor access: indoor-only cats median 39 m (IQR 9–137 m, n=164). Indoor-outdoor unsupervised cats median 300 m (IQR 14–1,609 m, n=150). Outdoor-only cats median 183 m (IQR 9–1,609 m, n=15; not significantly different from indoor-only, p=0.173). — [Huang 2018](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC5789300/fullTextXML)
- The authors recommend a 200 m search radius for indoor-only cats and 2 km or more for outdoor-access cats. — [Huang 2018](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC5789300/fullTextXML)
- Where cats were found alive (n=602): 83% outside, 11% inside someone else's house, 4% inside their own house, <2% in a shelter or municipal facility. Outdoor locations: yard 20%, waiting outside the home 19%, under vegetation 16%, under patio/deck/porch 10%, under the house 5%, storm drain/sewer 4%, garage 4%, cat trap 4%. 89% of owners reported 7 or more hiding places within about 130 m. More curious cats were more likely to be found inside a neighbour's house (6% at the lowest curiosity score vs 17% at the highest, p=0.005). — [Huang 2018](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC5789300/fullTextXML)
- Physical search was weakly associated with being found alive (SHR 1.49, 95% CI 0.97–2.29, p≈0.07). Advertising and contacting facilities had SHR ≈0.5 (p<0.001), which is probably reverse causation (owners advertise when a cat is not quickly found). Trapping (p=0.307) and microchips (p=0.331) showed no evidence of benefit. — [Huang 2018](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC5789300/fullTextXML)
- Lord et al. 2007 (lost cats, Montgomery County, Ohio, n=138): 53% recovered, median 5 days. Of the recovered cats, 66% returned home on their own and 7% were found in the neighbourhood. The best search method (neighbourhood signs) had only a 12% success rate. Only 19% of cats had any ID. — [Lord et al. 2007 lost cat, U. Arizona record](https://experts.arizona.edu/en/publications/search-and-identification-methods-that-owners-use-to-find-a-lost--2/); [OSU news](https://news.osu.edu/lost-dogs-found-more-often-than-lost-cats-study-suggests/)

**Lost dogs**
- Lord et al. 2007 (JAVMA 230(2):211; n=187 dogs, Ohio): 71% recovered, median time to recovery 2 days (range 0.5–21 days). Recoveries came through calling or visiting an animal agency (34.8%), a license tag (18.2%) and neighbourhood signs (15.2%). 48% had some ID. — [PubMed 17223753](https://pubmed.ncbi.nlm.nih.gov/17223753/); [U. Arizona record](https://experts.arizona.edu/en/publications/search-and-identification-methods-that-owners-use-to-find-a-lost-/)
- A university news release on the same work says only a small share of lost dogs (8%) returned home on their own, in contrast to cats ("dogs are sought, cats come home"). — [OSU news](https://news.osu.edu/lost-dogs-found-more-often-than-lost-cats-study-suggests/). Huang 2018 also cites the ASPCA framing.
- Weiss, Slater and Lord 2012 (*Animals*; US national random-digit-dial survey, 1,015 households): 14% of dogs and 15% of cats were lost in the previous 5 years. 93% of lost dogs and 75% of lost cats were recovered. Dogs were recovered mainly through neighbourhood searches and by coming home on their own, with ID tags involved in about 14% of cases. For cats the most common route was returning on their own. — [Weiss 2012, PMC](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4494319/); [ASPCA press release (gives 74% for cats)](https://www.aspca.org/about-us/press-releases/how-many-pets-are-lost-how-many-find-their-way-home-aspca-survey-has-answers)

**Free-roaming / community dogs (home ranges)**
- Warembourg et al. 2021 (*Front. Vet. Sci.* 8:617900): 773 dogs GPS-collared in Chad, Guatemala, Indonesia and Uganda, mostly owned and free-roaming. Median core (50%) home range was 0.25–0.33 ha. Median extended (95%) home range: Chad 7.7 ha (2.5–97.5th percentile 1.1–103), Guatemala 5.7 ha (1.5–27.5), Indonesia 5.6 ha (1.6–26.5), Uganda 5.7 ha (1.3–19.1). The urban/semi-urban site in Guatemala (Poptún) had smaller ranges than the rural sites. — [Warembourg 2021, Europe PMC](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7970034/fullTextXML)
- Puerto Natales, Chile (owned free-roaming male dogs): mean home range 0.65 km² (65 ha), mean maximum distance from home 1.05 km. Dogs rarely went into rural areas. — [Puerto Natales study, ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0168159118302612)
- Navarino Island, sub-Antarctic Chile (33 village and 4 rural dogs, GPS across four seasons): median seasonal home range 15.8–24.4 ha, individual range 1.6 ha to 148.8 km², longest maximum distance from the owner's home 20.4 km. — [Schüttler et al. 2022, AABS](https://www.sciencedirect.com/science/article/abs/pii/S0168159122000685)
- Arequipa, Peru (urban, 23 GPS-collared dogs): core (50%) home ranges 0.00013–0.46 km², extended (95%) 0.0012–3.70 km². Dry water channels worked as "highways": dogs using them moved further, faster and more directionally. — [Raynor et al., bioRxiv 684381](https://www.biorxiv.org/content/10.1101/684381v1.full)
- The literature on free-roaming dogs is mostly rural, and "very little is known" about urban space use. Earlier Latin American studies exist for Brazil, Mexico and Chile. The Brazilian work used GPS, capture–recapture and interviews, and suggested larger ranges in rural than in urban settings. — [Warembourg 2021](https://www.frontiersin.org/articles/10.3389/fvets.2021.617900/pdf)
- Brazil, Cerrado (Fujioka et al., preprint): 105 rural free-ranging dogs GPS-collared for 2 months, home range by 95% AKDE. I could not retrieve the values. — [Authorea preprint](https://radiopharmaconnect.srsweb.org/doi/full/10.22541/au.173347044.42308519/v1)
- Brazil, urban context: in Taboão da Serra (SP) most dogs observed on the street appeared to have owners. — [FMU journal](https://revistaseletronicas.fmu.br/index.php/ASA/article/download/1967/1404/6679). Road-count surveys estimated about 1,428 street dogs in Pinhais and about 480 in Campo Magro (Curitiba metro area), with wide confidence intervals. — [RSD Journal](https://rsdjournal.org/index.php/rsd/article/view/31063)
- Method caveat from movement ecology: in a 44-jaguar Brazil/Argentina study, autocorrelated KDE (AKDE) home ranges were 1.02–4.80× larger than conventional KDE. Naive KDE on autocorrelated fixes underestimates range. — [Morato et al. 2016, PLoS ONE, Europe PMC](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC5193337/fullTextXML)

**Free-roaming / colony cats**
- Horn et al. 2011 (J. Wildl. Manage. 75(5):1177; 42 cats, Champaign-Urbana, Illinois): owned cats had a mean home range under 2 ha. Unowned cats had larger ranges, were more nocturnal and more active. The largest range was 547 ha (a feral male). — [Illinois News Bureau](https://news.illinois.edu/researchers-track-the-secret-lives-of-feral-and-free-roaming-house-cats/); [BioOne record](https://bioone.org/journals/journal-of-wildlife-management/volume-75/issue-5/jwmg.145/Home-Range-Habitat-Use-and-Activity-Patterns-of-Free-Roaming/10.1002/jwmg.145.full)
- Pietermaritzburg, South Africa (GPS-collared urban feral cats): home ranges were small and driven by food. Core areas contained at least one supplemental feeding site, and males ranged more widely than females. — [UKZN ResearchSpace](https://researchspace.ukzn.ac.za/items/7073bf64-e46e-4f08-8302-9f6297f99421/full)
- Chicago TNR cats (GPS; preliminary student-symposium abstract): sterilized males 4.8 ± 0.8 ha, females 3.5 ± 0.5 ha, no significant difference (p=0.49). — [EWU symposium 2025](https://dc.ewu.edu/srcw_2025/ps_2025/p2_2025/36)
- Denmark, owned cats (*Animals* 2022): 95% Brownian-bridge home range 0.033–0.077 km² (3.3–7.7 ha). — [DOAJ record](https://doaj.org/article/ff2102b65e474f69b544cc88711e71c3)
- Rome colony management: about 8,000 cats were neutered and returned to colonies between 1991 and 2000, but about 21% of colony members were new arrivals through abandonment and immigration. Colonies are not closed populations. — [Faunalytics summary of Natoli et al.](https://faunalytics.org/management-of-feral-domestic-cats-in-the-urban-environment-of-rome-italy/). In Italian law, registered caretakers manage colonies and the mayor is the legal "owner". — [Front. Vet. Sci. 2019](https://www.frontiersin.org/journals/veterinary-science/articles/10.3389/fvets.2019.00031/pdf)
- Huang 2018 interprets its finding that "cats stay close to where they are fed" as support for shelter-neuter-return. — [Huang 2018](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC5789300/fullTextXML)

### Inferences
- **Converting area to radius.** For a circle, r = √(A/π). Equivalent radii: 0.3 ha core ≈ 31 m. The 5.6–7.7 ha median 95% dog range ≈ 134–157 m. The 27.5 ha Guatemala 97.5th percentile ≈ 296 m, and 103 ha (Chad 97.5th) ≈ 573 m. 65 ha (Puerto Natales) ≈ 455 m. The 3.7 km² Arequipa max ≈ 1.09 km. TNR cats at 3.5–4.8 ha ≈ 106–124 m, and owned cats under 2 ha ≈ under 80 m. [EXTRAPOLATION: real ranges are not circular, and they elongate along roads and channels, as in Arequipa.]
- **Defaults for linking and search radius [EXTRAPOLATION, needs calibration with platform data]:**

| Status | Initial radius | Expand to | Basis |
|---|---|---|---|
| Lost cat, indoor-only | 200 m | 500 m after 7 d | Huang: median 39 m, 75th pct 137 m; authors recommend 200 m |
| Lost cat, outdoor access | 500 m | 2 km after 7–14 d | Huang: median 300 m, 75th pct 1,609 m; authors recommend ≥2 km |
| Lost dog | 1 km | 3–5 km after 48 h, municipality-wide (shelters/CCZ) after that | No peer-reviewed distance data; median recovery 2 d; agencies are the top recovery route, so push to shelters and CCZ (Centro de Controle de Zoonoses) rather than only widening the radius |
| Community / free-roaming dog | 300 m core link gate | 1 km soft gate | Median 95% range ≈ 135–157 m radius; tails to ~0.5–1 km (Puerto Natales mean max distance 1.05 km) |
| Colony / feral cat | 150 m | 400 m | Feeding-site-centred ranges of ~2–5 ha (≈80–125 m); males and outliers larger |
| Emergency (injured animal) | Helper alert radius by travel time (e.g. 2–5 km urban) | Escalate on no-ack | Animal is assumed stationary; the radius concerns responders, not movement |

- **Decay half-lives for how informative a location is [EXTRAPOLATION]:** freshness f(Δt) = 2^(−Δt/h).
  - Emergency, "is the animal still here?": h = 2–6 h.
  - Lost dog: h = 24–48 h, matching the 2-day median recovery and fast-moving early phase.
  - Lost cat: h = 7 d. Cats hide near the escape point, median found at 6 days, 34% by day 7.
  - Community dog: h = 30 d (high site fidelity; many are owned free-roamers).
  - Colony cat: h = 60–90 d (feeding-site anchored).
- **Case lifetime separate from location freshness [EXTRAPOLATION]:** keep lost-cat chains active for 90 days (few cats are found alive after 90 days and the curve is almost flat after 61), then move them to dormant with a monthly reminder. Lost-dog chains: active 30 days, dormant at 60.
- In Brazil, "stray" covers several statuses: owned free-roaming dogs, *cães comunitários* (community-cared dogs), and truly unowned dogs. Taboão da Serra suggests most street dogs have owners. The status taxonomy should therefore include "community/owned free-roaming", because those animals return home and show strong site fidelity. That makes linking easier and also makes the home location more sensitive.
- Crowdsourced sightings are not GPS fixes. They are clustered where people walk and are heavily autocorrelated (the same feeder reports daily). The AKDE-vs-KDE finding (KDE underestimates by up to ~5×) suggests that any home range estimated from sightings should account for autocorrelation, or simply use generous default priors.

### Gaps
- **No peer-reviewed data on how far lost dogs travel.** Lord 2007 (dogs) reports recovery methods and time but no distances in the retrieved abstract/record. Missing Animal Response material (Kat Albrecht) is practitioner literature and was cited only as an unpublished 2015 source in Huang 2018. The lost-dog radius schedule above is an extrapolation.
- **No Brazilian urban GPS study of stray or community dogs found.** Brazil studies are rural (Cerrado). A Cerrado study of 36 dogs reporting a mean foray range of 165.2 ha (rural 262.55 ha vs peri-urban 11.47 ha) appeared in search results, apparently via [UNESP repository](https://repositorio.unesp.br/bitstreams/a920bc52-bb80-4018-a753-ad7ca4245109/download), but I could not confirm the paper. Treat it as unverified.
- No Brazilian or Latin American GPS study of urban colony cats found. Search summaries mentioned "median urban owned-cat home range about 1–2 ha" and Reading (UK) "1.94 ha mean daily 95% MCP", but I could not tie those figures to a specific verified paper URL.
- No cited data on daily travel distance (km/day) or maximum sustained speed for free-roaming or lost dogs. This is needed for hard speed gating (see §2).
- Lost-pet data are US/Australia/Canada-centric. Brazilian urban structure (walled houses, condominiums, dense favelas, open drainage channels) may change distances, as the Arequipa channel effect suggests.

---

## 2. Linking sightings into chains: clustering, track association, probabilistic record linkage, human-in-the-loop, merge/split, and re-ID pipelines

### Takeaway
Treat each sighting as a first-class observation and each chain as a revisable hypothesis that groups observations about one animal (Wildbook's Encounter → Individual pattern). Score candidate links with a Fellegi–Sunter-style log-likelihood ratio that adds up appearance evidence (photo embedding, coat, size, sex, collar) and a spatio-temporal plausibility term derived from the movement priors in §1. Use hard space-time gates only for blocking. Never auto-merge: suggest, ask people "é o mesmo animal?", and record every link decision with provenance so merges and splits are reversible. Use ST-DBSCAN and SaTScan for hotspot and outbreak detection (abuse or poisoning clusters), not for individual identity.

### Cited Findings
- **Wildbook data model (Wild Me, photo-ID platform for individual wildlife):** An *Encounter* is the base record, one animal at one time and place, and every upload becomes an encounter. A *Sighting* (formerly "Occurrence") groups the encounters of animals seen together, so a group of five yields five encounters. A *Marked Individual* is a named animal with one or more encounters, and a researcher must confirm it. — [Wildbook docs: introduction](https://wildbook.docs.wildme.org/introduction/index.html); [encounter](https://wildbook.docs.wildme.org/introduction/encounter.html); [sighting](https://wildbook.docs.wildme.org/introduction/sighting.html)
- Wildbook matching: detection produces one annotation per animal, and annotations go to ID algorithms. If a study site is set, candidates are restricted to that site. "Wildbook assists in photo ID but never makes a decision for the user." Each encounter records how it was matched: unmatched first encounter, visual inspection, or pattern match. — [Wildbook matching process](https://wildbook.docs.wildme.org/data/matching-process.html)
- **Fellegi–Sunter record linkage:** m = P(field agrees | same entity), u = P(field agrees | different entities). Agreement weight = log2(m/u), disagreement weight = log2((1−m)/(1−u)). Agreement weights are positive and disagreement weights negative. Rare agreements carry more evidence. — [Australian Bureau of Statistics](https://www.abs.gov.au/ausstats/abs@.nsf/Lookup/93275A3BB3B61601CA257BE900110E67); [Splink parameter estimation demo](https://nbviewer.org/github/moj-analytical-services/splink_demos/blob/max_pair/04_Estimating_model_parameters.ipynb)
- Splink, an open-source Fellegi–Sunter implementation, uses "partial match weights" per comparison level, plus a prior `probability_two_random_records_match`. m and u can't be known exactly and have to be estimated (e.g., by EM). — [Splink demo](https://nbviewer.org/github/moj-analytical-services/splink_demos/blob/max_pair/04_Estimating_model_parameters.ipynb); [Real World Data Science case study](https://realworlddatascience.net/case-studies/posts/2023/11/22/splink.html); survey: [(Almost) All of Entity Resolution, arXiv 2008.04443](https://arxiv.org/pdf/2008.04443)
- **ST-DBSCAN** (Birant & Kut 2007, *Data & Knowledge Engineering* 60(1):208–221) extends DBSCAN with a temporal neighbourhood parameter alongside the spatial one and MinPts. It is implemented in the R package `stdbscan` (`eps_temporal`, `min_pts`). — [stdbscan CRAN README](https://archive.linux.duke.edu/cran/web/packages/stdbscan/readme/README.html); [stdbscan reference manual](https://archive.linux.duke.edu/cran/web/packages/stdbscan/refman/stdbscan.html)
- **Space-time permutation scan statistic** (Kulldorff et al. 2005, *PLoS Med* 2(3)) needs only case counts, with no population denominator or controls. It is built into the free SaTScan software. NYC began using it in November 2003 and, per a 2016 CDC report, runs it daily across 35 reportable diseases. Limitations: it detects only outbreaks that start locally, and power drops for less compact clusters. — [Kulldorff 2005, PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC548794); [DIMACS abstract](https://archive.dimacs.rutgers.edu/archive/Events/2006/abstracts/kulldorff.html); [CDC EID 22(10)](https://wwwnc.cdc.gov/eid/article/22/10/16-0097); R implementation: [scanstatistics::scan_permutation](https://search.r-project.org/CRAN/refmans/scanstatistics/html/scan_permutation.html)
- **Animal face re-ID:** the PetFace dataset (ECCV 2024) has 257,484 individuals across 13 animal families and 319 breeds, annotated for sex, breed, color and pattern. It benchmarks re-identification of seen individuals and verification of unseen ones, and cites "finding of lost animals" as a use case. The authors say there is still room to improve identification across multiple families. — [PetFace arXiv 2407.13555](https://arxiv.org/abs/2407.13555v2). A non-peer-reviewed student pet-face model reports top-1 90.7% and top-5 92.5%, and describes volunteers photographing stray cats to build a unique-ID database. — [Society for Science abstract](https://abstracts.societyforscience.org/Home/PrintPdf/24701)
- **Track association and gating:** the Kalman filter is the standard linear-Gaussian state estimator used in multi-target tracking, with gating that discards candidate associations whose Mahalanobis distance exceeds a chi-square threshold. — [Kalman filter, Wikipedia [canonical ref, not fetched]](https://en.wikipedia.org/wiki/Kalman_filter)

### Inferences
- **Why Kalman filtering is a poor fit.** It assumes momentum (constant velocity) and dense fixes. Community and colony animals are range-resident, so a mean-reverting model (an Ornstein–Uhlenbeck-style "home range attractor", as used in AKDE work) fits better. Lost animals are closer to diffusion with an unknown drift. For resident animals use a static bivariate-normal home range around the chain's centroid. For lost animals use a radius that grows with Δt. [EXTRAPOLATION]
- **Spatio-temporal plausibility term [EXTRAPOLATION, worked example]:**
  - Resident dog: a 95% range of 5.7 ha gives r95 ≈ 135 m. For a bivariate normal, r95 = 2.448σ, so σ_animal ≈ 55 m.
  - Add an assumed user-pin location error of σ_loc ≈ 40 m: σ_tot ≈ 68 m. The distance between two independent sightings of the same animal has σ_diff = √2·σ_tot ≈ 96 m, so 95% of same-dog pairs fall within about 235 m.
  - For a 97.5th-percentile dog (27.5 ha) the same calculation gives about 440 m.
  - A 300 m soft gate plus a 1 km hard gate therefore keeps nearly all true pairs.
  - Spatial log-LR term: log[p(d | same) / p(d | different)], with p(d | same) = Rayleigh(σ_diff) and p(d | different) ≈ 2d/R² (uniform within the candidate radius R).
- **Hard gate for lost animals:** reject if d > r_status(Δt) + 3σ_loc, using the expanding radius schedule in §1. Never gate on a speed limit alone until there is speed data (§1 gap).
- **Appearance terms [EXTRAPOLATION, illustrative m/u]:**
  - Coat colour is weak evidence for common Brazilian phenotypes. "Caramelo" mixed-breed dogs are very common, so u is high: with m=0.9 and u=0.3 the weight is about +1.6 bits. A rare pattern (merle or tricolour, u≈0.02) gives about +5.5 bits.
  - Sex: agreement about +0.9 bits (m=0.95, u=0.5); disagreement about −3.3 bits. Sex disagreement is strong negative evidence when both reports are confident.
  - Collar present in both: +3 bits (m=0.8, u=0.1).
  - Photo-embedding similarity: bin cosine similarity into levels and learn m/u per level from labelled yes/no answers.
  - Estimate u from the platform's own coat-colour frequencies per city, not from intuition. This is exactly Fellegi–Sunter's "rare agreement weighs more" principle.
- **Decision thresholds [EXTRAPOLATION; tune on labelled data]:** posterior odds = prior odds × 2^W, with the prior ≈ 1/(number of active chains of that species in the candidate area).
  - Posterior below 0.2: no suggestion.
  - 0.2–0.8: ask chain participants and the reporter "Pode ser o mesmo animal?" with side-by-side photos.
  - Above 0.8: strong suggestion pinned at the top of the chain.
  - Auto-attach only in trivial cases, such as the same reporter, same session and same photo burst. This mirrors Wildbook's "assists but never decides".
- **Use of the human labels:** every yes/no answer is a labelled pair. Over time, use EM plus the labels to re-estimate m/u per city and per species. This is Splink-style training on platform data.
- **Group sightings:** one photo of a colony with five cats should create five observations under one "sighting" container (Wildbook Sighting). Otherwise colony photos will wrongly merge individuals.
- **Merge and split with provenance:** chains are never destroyed. A merge writes a `ChainMerged{from, into, by, reason, evidence_ids}` event and sets `merged_into` on the absorbed chain, which redirects its URL and chat. A split moves selected observation links into a new chain through `LinkRetracted` and `LinkAsserted` events. Chat history stays with the original chain, with a cross-link.
- **Clustering versus identity:**
  - ST-DBSCAN (e.g. eps_space 150 m, eps_time 7 d, MinPts 3) is good for finding places where something keeps being reported, such as a new colony or a dumping/abandonment hotspot. That supports "suggest creating a colony chain" and helps NGOs.
  - It cannot separate individuals at a colony, where appearance must carry the identity decision.
  - The space-time permutation scan, which needs only counts, fits nightly detection of suspicious clusters of emergencies (e.g., several "suspected poisoning" reports in one bairro within 72 h) for NGO or authority alerts. It will miss diffuse patterns.

### Gaps
- No published system I found applies Fellegi–Sunter specifically to lost/stray pet sightings. The proposed m/u values are illustrative only.
- No public accuracy figures retrieved for commercial lost-pet face-matching services in Brazil or the US (e.g., Petco Love Lost). PetFace per-species top-k numbers need the full paper tables.
- Coat-colour frequency of Brazilian street dogs and cats (needed for u) is not available. The platform will have to learn it.
- Pin error when people tap a map, compared with device GPS, is unquantified here. The 40 m σ_loc is an assumption.

---

## 3. Data modeling: event sourcing, bitemporal time, fuzzy times, and H3 vs geohash vs S2 with PostGIS

### Takeaway
Use an append-only event log per chain (event sourcing) with materialised projections for the map and feeds. Every observation carries two time axes: *valid time* (when the animal was seen, stored as an interval with a precision qualifier, EDTF-style) and *transaction time* (when it was reported or recorded, server-set). Store the true location in PostGIS `geography` with GiST for exact radius and KNN queries. Use H3 cells, which are integer IDs with roughly uniform hexagons, for aggregation, privacy display cells and candidate blocking.

### Cited Findings
- **H3 cell sizes (average):**

| Res | Area | Edge |
|---|---|---|
| 5 | 252.9 km² | 9.85 km |
| 6 | 36.13 km² | 3.72 km |
| 7 | 5.161 km² | 1.406 km |
| 8 | 0.737 km² | 531 m |
| 9 | 0.105 km² (105,333 m²) | 201 m |
| 10 | 15,048 m² | 75.9 m |
| 11 | 2,150 m² | 28.7 m |
| 12 | 307 m² | 10.8 m |

  Cell area varies with position relative to the icosahedron vertices: the largest hexagon is about 1.99× the smallest, and pentagons are about 0.5× the average area. Edge lengths for res 7 and above are extrapolated. — [H3 resolution table](https://h3geo.org/docs/core-library/restable/)
- **H3 vs geohash:** geohash is a string-keyed square quadtree on latitude/longitude, with cell area distortion by latitude. H3 indexes are 64-bit integers, and integer operations are usually faster than string operations. H3 has a fixed maximum resolution, while geohash precision is arbitrary. — [H3 docs: geohash comparison](https://h3geo.org/docs/comparisons/geohash)
- **EDTF / ISO 8601-2:2019:** the Library of Congress Extended Date/Time Format, incorporated into ISO 8601-2:2019, has qualifiers `~` (approximate), `?` (uncertain) and `%` (both). At Level 2 they can attach to individual components (e.g., `2015-06?-14`). One guide suggests reading "approximate" as ±2 of the most precise unit given. — [LoC EDTF](https://www.loc.gov/standards/datetime/); [BYU EDTF cheat sheet](https://mormonplaces.byu.edu/edtf.html); [Python `edtf` package](https://pypi.org/project/edtf/2.0)
- **Event sourcing:** state changes are stored as an append-only sequence of events, and current state is a replayable projection. — [Martin Fowler, Event Sourcing [canonical ref, not fetched]](https://martinfowler.com/eaaDev/EventSourcing.html)
- **Bitemporal history:** actual (valid) time and record (transaction) time are separate axes, so "what did we believe on date X about date Y" is answerable. — [Martin Fowler, Bitemporal History [canonical ref, not fetched]](https://martinfowler.com/articles/bitemporal-history.html)
- **PostGIS:** `ST_DWithin` on `geography` uses spatial indexes for radius queries. — [PostGIS ST_DWithin docs [canonical ref, not fetched]](https://postgis.net/docs/ST_DWithin.html). For S2 see [s2geometry.io [canonical ref, not fetched]](https://s2geometry.io/).

### Inferences
- **H3 resolutions to use [EXTRAPOLATION]:**
  - Res 9: block-scale, equivalent-circle radius about 183 m. Matches the cat and community-dog link radius, so use it for candidate blocking (`gridDisk(k=1..2)`).
  - Res 8: neighbourhood-scale, equivalent radius about 484 m. Default public "approximate" display cell for non-sensitive sightings.
  - Res 7: bairro-scale, equivalent radius about 1.28 km. Public display for sensitive locations such as feeding sites, colonies and reporters' homes.
  - Res 6: city sector, about 3.4 km. Heatmap and aggregate statistics.
  - Brazil runs from about +5° to −34° latitude, so geohash distortion is moderate. H3's uniform neighbours and integer keys still make it the better fit for k-ring blocking and hex display.
- **Do not use H3 alone for exact radius queries.** Hex boundaries create edge effects. Pattern: block on an H3 k-ring, then filter precisely with `ST_DWithin(true_geom, :p, :r)`.
- **Fuzzy times such as "ontem à tarde":** parse to `valid_time = tstzrange('yesterday 12:00','yesterday 18:00')`, `time_precision='part_of_day'`, `edtf='2026-10-20T15:00~'` or similar, and keep the original text (`time_text`).
  - Overlap queries (`&&`) handle fuzzy-vs-window filtering.
  - For decay, use the interval midpoint. For "last seen", sort by the upper bound but show the precision ("visto ontem à tarde", not "visto às 15:00").
  - Suggested PT-BR parse table: manhã 06–12, tarde 12–18, noite 18–24, madrugada 00–06, "agora há pouco" = now−1 h…now, "hoje cedo" 05–09. [EXTRAPOLATION]
- **Bitemporal for the map:**
  - The time slider filters on valid time ("animais vistos nos últimos 7 dias").
  - Audit and moderation use transaction time ("o que o mapa mostrava em 10/10").
  - Late reports (seen 3 days ago, reported today) insert into the past without rewriting history.
  - Corrections are new events (`ObservationCorrected`) with their own transaction time.
- **Minimal schema sketch [EXTRAPOLATION]:**

```
observation(id, reporter_id, species, kind[sighting|emergency|found|lost_report],
  valid_time tstzrange, time_precision enum, time_text, edtf,
  reported_at timestamptz default now(),        -- transaction time
  true_geom geography(Point,4326),              -- restricted column / separate table with RLS
  loc_accuracy_m int, loc_source enum[gps|pin|geocode|text],
  privacy_class enum[public_place|near_reporter_home|feeder_site|colony|other_sensitive],
  display_mode enum[exact|approximate|hidden], display_cell h3index, display_geom geography,  -- precomputed, stable
  h3_r9 h3index, h3_r7 h3index, attributes jsonb, photo_ids[], embedding vector)
sighting_group(id, observation_ids[])           -- multi-animal photo (Wildbook "Sighting")
chain(id, species, status enum[lost_pet|community|colony_feral|unknown|emergency],
  state enum[open|active|stale|dormant|resolved|archived|merged], merged_into, resolution enum,
  home_estimate geography, home_sigma_m, created_at)
chain_link(chain_id, observation_id, link_state enum[suggested|asserted|confirmed|rejected|retracted],
  score_bits real, method enum[reporter|model|crowd_vote|moderator], actor_id, evidence jsonb, at timestamptz)
chain_event(id, chain_id, type, payload jsonb, actor_id, valid_time tstzrange, recorded_at)  -- append-only log
location_access_log(user_id, observation_id, at, purpose)   -- who saw exact coordinates
```

- **Key invariant:** an observation exists independently of any chain, and chain membership is only ever expressed through `chain_link` rows that are themselves append-only. If observations are stored *inside* chains, merges and splits become destructive. That is the main failure mode to avoid.

### Gaps
- I did not fetch S2 documentation or benchmarks comparing H3 and S2 for PostGIS workloads. S2's advantage (exact hierarchical containment of square cells) versus H3's (uniform adjacency, hexagons) is from prior knowledge.
- I did not verify whether the `h3-pg` extension is supported on the target managed Postgres provider.
- No source on PT-BR temporal-expression parsing accuracy. The part-of-day mapping is a design assumption to test with users.

---

## 4. Temporal logic and UX: freshness/decay, "last seen" semantics, staleness and archiving, re-confirmation, emergency urgency tiers, time-window views

### Takeaway
Separate three clocks: *location freshness* (how likely the animal is still near the last point, decaying with a status-specific half-life), *case liveness* (whether the chain is still being worked), and *emergency urgency* (time-to-response targets). For emergencies, borrow the validated veterinary triage list colours and target waits (red 0 min, orange 15, yellow 30–60, green 120) and START's simple, observable discriminators. Drive re-confirmation prompts and auto-archiving from half-lives instead of fixed dates.

### Cited Findings
- **Veterinary Triage List (VTL)**, adapted from a human five-level system (Manchester-like), was evaluated in 485 dogs and cats (2012). Target waiting times: red 0 min, orange 15 min, yellow 30–60 min, green 120 min. Agreement with a veterinarian review team was 95.5% for red and 84.3% for orange. VTL triage correlated better than intuitive nurse triage. — [PubMed 22702436](https://pubmed.ncbi.nlm.nih.gov/22702436/)
- A practice article describes the VTL as five levels including blue at 240 min, with 68 discriminators in 8 subcategories (respiratory, circulatory, neurological, trauma, etc.). The blue level and discriminator count are not confirmed by the primary abstract. — [Veterinary Practice News](https://www.veterinarypracticenews.com/?p=48714)
- Human triage scales (ATS, CTAS) define a maximum time per category. The VTL was proposed as a five-point scoring system similar to Manchester. — [Nottingham veterinary review](https://openlabyrinth.nottingham.ac.uk/files/278/MBSs.pdf)
- **START triage** (mass-casualty triage) sorts patients into four groups using fast observable checks: able to walk, breathing after airway repositioning, respiratory rate over 30/min, perfusion (capillary refill / radial pulse) and following commands. The groups are minor (green), delayed (yellow), immediate (red) and expectant (black). — [START, Wikipedia [canonical ref, not fetched]](https://en.wikipedia.org/wiki/Simple_triage_and_rapid_treatment)
- Lost-cat recovery hazard is concentrated early: 34% by day 7, 50% by day 30, little after day 61. Lost-dog median recovery is 2 days. — [Huang 2018](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC5789300/fullTextXML); [PubMed 17223753](https://pubmed.ncbi.nlm.nih.gov/17223753/)
- iNaturalist coarsens dates publicly for obscured observations, but exact dates remain in the API, which is a documented leak vector (see §5). — [iNaturalist geoprivacy help](https://help.inaturalist.org/support/solutions/articles/151000169938)

### Inferences
- **Emergency urgency tiers, PT-BR, for lay reporters [EXTRAPOLATION: VTL timing plus START-style observable questions; a vet must validate this before launch]:**

| Tier | Target response | Lay discriminators (yes/no questions) |
|---|---|---|
| 🔴 Vermelho, imediato | Push alert to nearby helpers and partner clinics within 0–15 min | Not breathing or gasping; heavy bleeding; hit by car and can't stand; seizure; trapped (drain, wire, high place) with immediate danger; suspected poisoning (foaming, tremors) |
| 🟠 Laranja, muito urgente | ≤ 15–60 min | Can't walk but alert; visible fracture or deep wound; puppies or kittens without mother in rain or cold; heat-stroke signs |
| 🟡 Amarelo, urgente | ≤ 2–6 h | Walking but limping or injured; very thin or weak; skin disease with open sores |
| 🟢 Verde, não urgente | ≤ 24–72 h | Healthy-looking stray needing shelter, castration or food |
| ⚫ Óbito / sem ação | Archive and support | Animal dead (record for poisoning and abuse clusters, §2) |

  Use observable questions, START-style, not diagnoses. The colour-plus-target-time pattern lets the system escalate automatically: if a red case gets no "estou indo" ack within the target, widen the radius and notify NGOs or the CCZ.
- **"Last seen" semantics:**
  - Show "última vez visto: [precision-aware relative time] em [precision-aware place]". Compute it from confirmed links only, max(upper(valid_time)).
  - Show "última atualização" (transaction time) separately.
  - Unconfirmed suggested sightings appear as "possível avistamento" and must never move the "last seen" marker.
- **Freshness-driven states [EXTRAPOLATION]:** using f = 2^(−Δt/h) with h from §1:
  - f ≥ 0.5 → *ativo*, full colour on the map.
  - 0.5 > f ≥ 0.125 (1–3 half-lives) → *desatualizado*: faded marker, plus a prompt to the reporter and recent nearby viewers ("Ainda está aí?" / "Você viu este animal recentemente?").
  - f < 0.125 (more than 3 half-lives) with no new block → *dormente*: hidden from the default map layer, still searchable.
  - Chain lifetime caps: lost cat 90 d, lost dog 60 d, emergency 72 h without update, after which the case is archived with a "reabrir" option.
  - Community and colony chains never auto-archive. They go dormant and need a yearly re-confirmation.
- **Re-confirmation design:** make it a one-tap event (`Reconfirmed{still_here: yes|no|moved}`). A "no" is valuable negative evidence: it should lower freshness immediately and, for lost pets, enlarge the search radius.
- **Time-window views:** preset chips "últimas 24 h / 7 dias / 30 dias / tudo", applied to valid time. A slider or animation only on the analytics view. Emergencies always show regardless of window until resolved or archived.

### Gaps
- No validated lay-person triage scale for street animals was found. The VTL is for clinic staff. Field validation with Brazilian vets and NGOs is needed.
- No empirical data on how quickly an injured street animal moves away from the report location. The 2–6 h emergency half-life is an assumption.
- The VTL "blue / 240 min" level is reported by only one practice article.

---

## 5. Location privacy: geo-masking, k-anonymity, geo-indistinguishability, iNaturalist obscuration, and protecting reporters, feeders and colonies

### Takeaway
There is a hard tension: the radius that protects a feeder's home or a colony (hundreds of metres to km) is the same order as the radius you need to find an injured or lost animal (50–500 m). Random noise alone cannot resolve it. Use access tiers instead: exact coordinates go to authenticated, accountable helpers who join a chain, with audit logs. The public sees a *stable* coarse cell, sized by sensitivity, with timestamps also coarsened. Never regenerate fresh noise per request or per report, because averaging repeated noisy reports reveals the true point.

### Cited Findings
- **iNaturalist "obscured"** replaces the public coordinates with a random point inside a 0.2° × 0.2° cell, about 500 km² at the equator. Public positional accuracy is set to the cell diagonal. True coordinates are visible to the observer and, if shared, to trusted individuals, trusted projects and network nodes. **"Private"** hides all location data and excludes the observation from place searches. Taxon geoprivacy is triggered by conservation statuses that note threats from location disclosure, through community flagging and curator or partner review. — [iNaturalist help: geoprivacy](https://help.inaturalist.org/support/solutions/articles/151000169938)
- iNaturalist warns that obscured locations can be inferred through photo landmarks or description text, through *interpolation from the same user's open observations near in space and time*, and because "public dates are coarsened, but exact dates remain in the API". — [iNaturalist help: geoprivacy](https://help.inaturalist.org/support/solutions/articles/151000169938)
- Cell size: about 22 × 22 km at the equator, shrinking toward the poles. The accuracy (diagonal) is about 31 km at the equator. Obscured markers are drawn stemless, true locations with a stem. — [iNaturalist Vermont post](https://inaturalist.ca/posts/9649-understanding-your-privacy-settings-for-inaturalist-vermont); [iNat forum: replicating geoprivacy polygons](https://forum.inaturalist.org/t/replicating-geoprivacy-polygons-in-gis/36905)
- **Geo-indistinguishability** (Andrés et al., ACM CCS 2013, pp. 901–914) generalises differential privacy to locations: protection within radius r at level ℓ, with ε = ℓ/r. The mechanism is the planar Laplace distribution, polar density ε²/(2π)·r·e^(−εr), with radius and angle sampled independently. Discretisation can weaken guarantees, and the paper shows how to keep them at a cost in privacy level. Among prior-independent mechanisms it gives the best privacy for a given utility. — [arXiv 1212.1984](https://arxiv.org/abs/1212.1984v1); [ar5iv HTML](https://ar5iv.arxiv.org/html/1212.1984)
- **Donut geomasking** (Hampton et al. 2010, *Am J Epidemiol*) displaces each point by at least a minimum and at most a maximum distance. The maximum is set so the population inside the circle equals a target k (spatial k-anonymity). — [Hampton 2010, PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC2952889); [RTI summary](https://www.rti.org/publication/mapping-health-data-improved-privacy-protection-with-donut-method-geomasking)
- Allshouse et al. 2010 found that donut and random-perturbation masks assume uniform population density and under-protect people where density varies. They recommend tripling the minimum displacement area. — [Allshouse 2010, PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC2984253). A 2020 *IJHG* study found distance-based donut masking performed worst at privacy protection among the methods compared. — [IJHG 2020](https://ij-healthgeographics.biomedcentral.com/track/pdf/10.1186/s12942-020-00219-z)
- **Lindenmayer & Scheele, "Do not publish"** (*Science* 2017, 356:800–801): published location data enabled poaching of newly described species within months (e.g., Chinese cave geckos), and an online atlas led to trespassers at pink-tailed worm-lizard sites, straining relationships with landowners. They propose withholding or buffering locations, as archaeology does. — [ANU news](https://science.anu.edu.au/news-events/news/scientists-urged-keep-rare-species-habitat-secret); [NESP PDF](https://www.nespthreatenedspecies.edu.au/media/gcib0cbn/6-4-do-not-publish.pdf); [wildlife.org](https://wildlife.org/?p=8400)

### Inferences
- **Threat model specific to this platform:**
  1. People who poison cats or dogs, or harass feeders, locating colonies and feeding points. This is the "do not publish" analogue.
  2. Reporters' home addresses exposed through repeated reports from home ("o gato que eu alimento no meu portão").
  3. Stalking or doxxing through the history of one user's reports.
  4. Theft of identifiable, valuable lost pets (purebred dogs), or reward scams that use exact "last seen" details.
  5. Re-identification through photos with visible facades or house numbers. iNat's "clues in content" warning applies.
- **Stable masking for fixed sensitive places [EXTRAPOLATION, but follows from composition in differential privacy]:**
  - Geo-indistinguishability composes. n independent noisy releases of the *same* point give roughly nε protection, and averaging them converges on the truth.
  - A feeder reporting the same colony daily would leak it within weeks.
  - So for fixed sensitive places, release one stable masked representation: the H3 cell (res 7 for colonies and feeders, res 8 for near-home reports), or a single deterministic jittered point (HMAC(secret, place_id)-seeded). Never sample fresh noise per request or per report.
- **Geo-indistinguishability utility cost [derivation]:** the radial distance under planar Laplace is Gamma(2, ε): mean 2/ε, median ≈1.68/ε, 95th percentile ≈4.74/ε.
  - ℓ = ln 4 within r = 200 m gives ε ≈ 0.0069/m, so mean displacement ≈ 289 m and p95 ≈ 684 m.
  - That is larger than the median lost-cat find distance (50 m) and comparable to the 75th percentile (500 m).
  - Conclusion: noise that protects the reporter destroys the search value. Reserve geo-ind noise for *public aggregate or analytics* layers and use access control for operational precision.
- **Donut/k-anonymity in Brazil:** population density varies enormously within one city (favela vs condomínio vs industrial zone), which is the exact condition under which donut masks under-protect (Allshouse). If k-anonymity is used, compute the radius from IBGE census-tract (setor censitário) population, not from a fixed distance. [EXTRAPOLATION]
- **Proposed access tiers [EXTRAPOLATION]:**

| Viewer | Emergency (non-sensitive public place) | Lost-pet sighting | Community/colony location | Reporter home zone |
|---|---|---|---|---|
| Anonymous public | Exact point (rescue needs it) but no reporter identity, timestamp to the hour | Res-8 cell, day-level time | Res-7 cell, or hidden | Never |
| Logged-in user nearby | Exact point | Res-9 cell | Res-7 cell | Never |
| Chain member / verified helper | Exact point plus reporter contact through in-app chat | Exact | Exact only if the colony caretaker approves; logged | Never (meet at a public point) |
| Moderator / partner NGO | Exact, logged | Exact, logged | Exact, logged | Exact, logged, purpose-bound |

- **Home-zone protection:** let users declare *zonas privadas* (home, feeding point), Strava/iNat-style. Any observation inside one automatically gets privacy_class = near_reporter_home, is shown at res-7 or res-8, has its time coarsened to the day, and is not publicly listed under the reporter's profile.
  - The cross-report linkage leak is the iNat "interpolation" warning: do not show public "reports by this user" maps.
  - Rate-limit and paginate the API.
  - Never return exact times and coordinates for masked items via API (iNat's API date leak is the cautionary tale).
- **Photo EXIF:** strip GPS/EXIF on upload and keep the original server-side under restricted access. Offer face, plate and house-number blurring later.
- **Utility vs. safety:** iNat's 0.2° cell (~22 km) is tuned for biodiversity science, where a regional record is still useful. For animal rescue, ~0.5–1.3 km public cells (H3 res 8/7) plus gated exact access is the right order of magnitude. That is a judgment call to revisit with feeders and NGOs.

### Gaps
- No peer-reviewed data found on harassment or poisoning of cat-colony feeders that is attributable to online maps, in Brazil or elsewhere. The analogy to poaching ("Do not publish") is inferential. Brazilian legal context (e.g., penalties for mistreating dogs and cats, LGPD treatment of location as personal data) is outside this note and belongs with the legal researcher.
- I did not retrieve research on inference attacks against fitness-app privacy zones (Strava), which would quantify how fast home locations leak from endpoint-masked tracks. Worth a follow-up.
- The [Location Privacy in Conservation arXiv paper (1907.07054)](https://arxiv.org/pdf/1907.07054) surfaced but was not read.

---

## 6. Map UX at scale and visual language for precision: clustering, heatmaps vs points, density, time filtering, and how people read uncertainty

### Takeaway
At national scale, pre-aggregate on the server (H3 counts per cell per time window) and switch to client-side Supercluster at city zoom and to individual markers at street zoom. Use heatmaps only for historical density, never for live cases that need action. For precision, draw exact points as stemmed pins. Draw approximate locations as a uniform bordered region (circle for GPS accuracy, hexagon for a privacy cell) with *no centre dot*. User studies show uniform bordered circles give the most accurate and fastest judgments, and people otherwise assume the centre is the true location.

### Cited Findings
- **McKenzie, Hegarty, Barrett & Goodchild 2016** (*IJGIS*) used the Google "blue dot" scenario and crossed glyph type (uniform bordered circle vs Gaussian fade) with centroid dot (present or absent). Participants shown the uniform blue circle answered most in line with the true probability density and answered fastest. Participants reported simple heuristics, and how consistently they used them predicted their judgments. — [ASU record](https://asu.elsevierpure.com/en/publications/assessing-the-effectiveness-of-different-visualizations-for-judgm/)
- Hegarty et al. ("Where are you?") found that people tend to assume they are at the centre of an uncertainty region when combining location estimates. — [Cognitive Science Society proceedings](https://escholarship.org/uc/item/44b4f5md)
- Kray and colleagues (ACM 2018) tested shape, boundary, middle dot and size of the concentric-circle uncertainty glyph with German and Sri Lankan participants. I did not retrieve the results. Edwards & Nelson (2001) found a focus/fading approach worked best for certainty on graduated-circle maps. — [Unpaywall DOI 10.1145/3191762](https://unpaywall.org/10.1145%2F3191762); [Cartographic Perspectives](https://cartographicperspectives.org/index.php/journal/article/view/cp38-edwards-nelson)
- iNaturalist marks obscured locations with stemless markers and true ones with stemmed markers. — [iNaturalist Vermont post](https://inaturalist.ca/posts/9649-understanding-your-privacy-settings-for-inaturalist-vermont)
- **Supercluster** (Mapbox) builds a hierarchical cluster index once at the most detailed zoom and reuses it for lower zooms. It powers Mapbox GL JS. A demo of 400,000 points ran at 60 fps after a few seconds of indexing, and the README cites 6 million points in Leaflet. Options: `radius` (default 40 px), `maxZoom` (default 16), `nodeSize` (KD-tree leaf size). A common production pattern aggregates millions of records server-side into thousands of clusters, then clusters further on the client. — [Mapbox blog](https://blog.mapbox.com/clustering-millions-of-points-on-a-map-with-supercluster-272046ec5c97); [supercluster README](https://cdn.jsdelivr.net/npm/supercluster@9.1.0/README.md); [Kinetica docs](https://docs.kinetica.com/7.2/connectors/kickbox_clustering/)

### Inferences
- **Zoom-tiered rendering [EXTRAPOLATION]:**
  - Country and state zooms (≤8): server H3 res 5–6 counts, as a choropleth or hex bins by status. Never show individual points.
  - City zoom (9–13): server sends active, non-sensitive items for the viewport, and Supercluster clusters them client-side. Clusters are coloured by the most urgent member, with any red emergency in the cluster shown as a badge.
  - Street zoom (≥14): individual markers. Masked items render as their hex cell or circle and never resolve below their privacy cell, whatever the zoom.
  - **Invariant:** the client never receives coordinates more precise than the viewer's access tier. Masking happens server-side before serialisation, not in rendering.
- **Visual legend (PT-BR):**
  - 📍 pin with stem = "Local exato".
  - Bordered translucent circle, no centre dot = "Local aproximado (precisão ~N m)" for GPS or pin uncertainty.
  - Bordered hexagon, no centre dot = "Área aproximada (protegida)" for privacy masking, ideally with a lock icon on tap.
  - Following McKenzie, use uniform fill with a crisp border, not a Gaussian blur. Following Hegarty and iNat's stemless markers, omit the centre dot so users don't treat the centre as truth.
- **Freshness encoding:** opacity and saturation map to freshness f (§4). Emergencies use tier colours. Lost pets use a distinct shape (e.g., a ring), community and colony animals a muted icon. Don't put both urgency and freshness on hue.
- **Heatmaps vs points:**
  - Heatmaps for analytics: abandonment hotspots, where castration campaigns are needed, poisoning-cluster review.
  - Points and clusters for actionable live cases.
  - A heatmap of colony locations at fine resolution is itself a privacy leak. Cap heatmap resolution at H3 res 7 and suppress cells with fewer than k items (e.g., k=3). [EXTRAPOLATION]
- **Time filtering:** server-side valid-time filter chips (24 h / 7 d / 30 d). Cache H3 aggregates per (cell, day, status) so time-window aggregation is cheap.

### Gaps
- I retrieved only the abstract-level results for McKenzie 2016. Effect sizes, and whether results hold for privacy cells (as opposed to GPS error), are unknown. No study found tests hexagon privacy cells vs circles for lay map readers.
- No study found on how Brazilian users specifically interpret "aproximado" markers. Worth a quick usability test.
- Supercluster benchmarks come from older demos and may not reflect current versions or mobile-browser constraints.

---

## 7. Concrete recommendations: default parameters, algorithm pipeline, data model

### Takeaway
Start simple and calibratable. Use status-specific radius and half-life tables (§1), H3 blocking plus a PostGIS exact filter, Fellegi–Sunter-style additive evidence with human confirmation, an append-only event model with bitemporal observations, and access-tiered stable masking. Instrument everything (link votes, reconfirmations, resolutions) so the extrapolated parameters can be re-estimated from Brazilian data within months.

### Cited Findings
- Movement and recovery anchors: lost cats median 50 m (indoor-only 39 m, outdoor-access 300 m), 75% within 500 m, alive-recovery curve flat after ~61 days. — [Huang 2018](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC5789300/fullTextXML). Lost dogs median recovery 2 days. — [PubMed 17223753](https://pubmed.ncbi.nlm.nih.gov/17223753/). Free-roaming dogs median 95% range 5.6–7.7 ha. — [Warembourg 2021](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7970034/fullTextXML)
- Never auto-decide identity, and record match provenance. — [Wildbook matching](https://wildbook.docs.wildme.org/data/matching-process.html)
- Evidence weights log2(m/u). — [ABS](https://www.abs.gov.au/ausstats/abs@.nsf/Lookup/93275A3BB3B61601CA257BE900110E67)
- H3 res 7/8/9 ≈ 5.16 km² / 0.737 km² / 0.105 km². — [H3 table](https://h3geo.org/docs/core-library/restable/)
- Coarse cell plus stemless marker, and the date-leak lesson. — [iNaturalist help](https://help.inaturalist.org/support/solutions/articles/151000169938)
- Emergency target times 0/15/30–60/120 min. — [PubMed 22702436](https://pubmed.ncbi.nlm.nih.gov/22702436/)

### Inferences
**Default parameter table (v0) [EXTRAPOLATION: re-fit after about 3–6 months of data]**

| Status | Link soft gate | Link hard gate | Location half-life h | Case active → dormant | Public display cell | Notify-radius for "help nearby" |
|---|---|---|---|---|---|---|
| Emergency | 100 m / 6 h (dedupe duplicate reports) | 500 m / 24 h | 2–6 h | 72 h no update → archive | Exact (public place), res-8 if near a reporter's home | 2–5 km by tier; escalate ×2 per missed target |
| Lost dog | 1 km + growth | 5 km (48 h), city afterwards | 24–48 h | 60 d | res-9 (exact to members) | 3 km, then city plus shelters and CCZ |
| Lost cat, indoor-only | 200 m | 500 m | 7 d | 90 d | res-9 | 500 m |
| Lost cat, outdoor access | 500 m | 2 km | 7 d | 90 d | res-9 | 2 km |
| Community dog | 300 m | 1 km | 30 d | Never archive; yearly re-confirm | res-8 | 1 km |
| Colony / feral cat | 150 m | 400 m | 60–90 d | Never archive; yearly re-confirm | res-7 (caretaker opt-in for finer) | 500 m (only to verified helpers) |

**Linking pipeline (on every new observation)**
1. **Normalize:** parse fuzzy time to an interval plus precision. Snap location and record accuracy. Strip EXIF. Classify privacy (inside a declared private zone? near a known colony?). Precompute the stable display cell or point.
2. **Detect and embed (later phase):** one annotation per animal in the photo (Wildbook-style), so a multi-animal photo creates multiple observations under one sighting group. Compute the embedding.
3. **Block:** same species, chain state in {open, active, stale, dormant}, H3 res-9 or res-8 `gridDisk` covering the status hard gate, valid-time overlap with an expanded window. Then exact `ST_DWithin`.
4. **Score:** W = Σ partial weights (space-time log-LR from the §2 model, coat, size, sex, collar or accessories, embedding bin, "reporter says it's the same" flag). Convert to a posterior with prior ≈ 1/n_candidates.
5. **Decide:**
   - Below 0.2: nothing.
   - 0.2–0.8: HITL card "É o mesmo animal?" (sim / não / não sei) to the reporter and chain members.
   - Above 0.8: strong suggestion. Owner or moderator confirms, and the system records a `LinkConfirmed` with provenance.
   - The same reporter adding to their own chain counts as an asserted link.
6. **Learn:** labelled pairs feed per-city m/u re-estimation (EM, Splink-style). Track precision and recall of suggestions.
7. **Batch analytics (nightly):** ST-DBSCAN over unlinked sightings to propose colony or community chains. Space-time permutation scan (SaTScan) on emergency categories such as poisoning or abuse, to alert NGOs.

**Main failure modes to design against**
- **Transitive over-merge:** A~B and B~C get merged although A≁C, which happens most at colonies with lookalike cats. Require pairwise checks against the chain's representative photos before a merge, and keep merges reversible.
- **Averaging leak:** fresh random noise on repeated reports of a fixed place. Use stable masks.
- **"Last seen" drift from unconfirmed links:** only confirmed links move the marker.
- **Stale emergencies clogging the map:** half-life fading plus a 72 h archive.
- **Survivorship and observation bias:** sightings cluster where people walk. Don't treat sighting density as animal density without normalising, e.g. by active-user density per H3 cell.

**Key invariant:** observations are immutable facts about (time interval, place, appearance) with transaction-time provenance. Chains are revisable hypotheses built only from append-only link events. Public geometry is derived server-side from the viewer's access tier and is never more precise than that tier allows.

### Gaps
- Every parameter in the v0 table is extrapolated from non-Brazilian, mostly owned-animal studies and needs local calibration. Missing pieces: lost-dog distances, Brazilian urban stray-dog and colony-cat GPS data, user pin error, and coat-colour base rates.
- The emergency triage questions need validation by Brazilian veterinarians or NGOs and a usability test with lay reporters.
