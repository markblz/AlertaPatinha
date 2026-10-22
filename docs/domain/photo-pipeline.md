# Photo pipeline (`src/media`)

Status: design draft, 2026-10-21. Owner module: `media`. Callers go through `src/media/public.py` only: `observations`, `chains`, `moderation`, and later `intake` and `matching`.
Sources: **AP** = [ai_pipelines.md](<../research/research_notes/Stray pet platform research/ai_pipelines.md>), **CTS** = [core_tech_stack.md](<../research/research_notes/Stray pet platform research/core_tech_stack.md>), **STC** = [spatiotemporal_chains.md](<../research/research_notes/Stray pet platform research/spatiotemporal_chains.md>), **GTS** = [game_theory_trust_safety.md](<../research/research_notes/Stray pet platform research/game_theory_trust_safety.md>). Anything not taken from those notes is marked **(design call)**. In the tables, "n/i" means the notes don't give a license, so check it before adopting the component.

## 1. Invariant (read this first)

> **Uploaded bytes are never served before re-encoding and metadata stripping. Originals live only in a private quarantine bucket.**
> ([CTS Q7, Q12](<../research/research_notes/Stray pet platform research/core_tech_stack.md>); [AP §1, §7](<../research/research_notes/Stray pet platform research/ai_pipelines.md>); repo rules 2 and 7 in [CLAUDE.md](../../CLAUDE.md))
>
> Corollary of rule 2: every S3 variant is *derived* data. It has to be rebuildable from Postgres plus the quarantined original, and the worker job is idempotent per `media_id`.

How it is enforced (all design calls):
- **Two credentials.** The API role can only presign writes into `quarantine`. Only the worker role can write `media-public`. No role can copy an object from quarantine to public.
- **Public URLs come only from `media.variant` rows with `public=true`.** Public serializers never see quarantine keys.
- The uploader's preview uses the local `blob:` URL and never a server URL.
- Moderators see the stripped private master. A raw original can be opened only at trust level T4. Any read of a raw original or of `media.evidence.gps` writes `geo.location_access_log` through `geo.public` (repo rule 5; [STC §3](<../research/research_notes/Stray pet platform research/spatiotemporal_chains.md>)).
- **CI test.** Upload fixtures (JPEG with EXIF GPS, HEIC, PNG with XMP) and assert two things: every public variant carries zero metadata, and every public key lives under `media-public/`.

**Main failure mode:** an original that still contains EXIF GPS gets published and exposes the reporter's home. That location is personal data under LGPD Art. 5 I ([AP §1](<../research/research_notes/Stray pet platform research/ai_pipelines.md>)).

## 2. Flow

```
 PWA (Next.js)                         api: media.public                    object storage
 ─────────────                         ─────────────────                    ──────────────
 <input type=file accept=image/* capture=environment>
  │ ① read EXIF GPS + DateTimeOriginal as a *hint* (canvas re-encode drops EXIF)
  │ ② createImageBitmap → (Offscreen)Canvas, ~1600–2048 px, WebP/JPEG q≈0.75–0.8
  │ ③ IndexedDB outbox; client UUIDv7 = idempotency key
  ├─ POST /media/uploads ───────────▶ create_upload(): presign, ~5 min TTL,
  │                                   content-type + max-size conditions
  ├─ bytes ─────────────────────────────────────────────────────────────▶ quarantine/up/…
  └─ POST /media/uploads/{id}/complete ▶ complete_upload(): ONE transaction =
                                         media.asset(state=pending) + defer(process_media)
 intake (WhatsApp): media id → short-lived URL → ingest_bytes() ────────▶ quarantine/wa/…

 worker: procrastinate queue `media` (CPU-bound, concurrency = cores)
  1  sniff magic bytes (not extension); ≤ ~20 MB; pixel cap        ─ fail → state=rejected
  2  decode: pyvips (libheif) │ fallback Pillow + pillow-heif       JPEG/PNG/WebP/HEIC/AVIF
  3  EXIF → media.evidence (GPS, DateTimeOriginal, OffsetTime, Make/Model)        [PRIVATE]
  4  auto-orient (apply Orientation, then drop the tag)
  5  PDQ on the oriented, unblurred image + 3 extra rotations → bit(256), quality Q
  6  quality: Laplacian variance, min resolution, PDQ Q ≥ 50          → flags, never blocks
  ┄┄ v2 (pixel-changing steps run BEFORE public encode) ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄
  7  EgoBlur faces + plates (score 0.1–0.3)             → blurred raster for public variants
  8  animal detect/crop: RF-DETR │ MDv6-MIT/Apache       → media.detection + private crops
  9  VLM attributes + graphic_injury                    → sensitive flag (tap-to-view)
  ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄
 10  encode, strip=True: detail ~1600 px + card ~640 px WebP ──────────▶ media-public/v1/{sha}/…
     unblurred master ~1600 px + re-ID crops 256–384 px (stripped) ───▶ media-private/…
 11  ThumbHash (~25 B) → media.asset
  ┄┄ v3 ┄┄
 12  embeddings (body + face crop) → matching.reid_vector (halfvec, model_id + version)
  ▼
 commit: state=ready + outbox event `media.ready` → Centrifugo publish after commit
```

The order departs from the plain step list on purpose: anything that changes pixels has to run before the public encode (step 10). In MVP, steps 7–9 do nothing. A Relato never waits on its photos. Until `media.ready` arrives it shows "foto processando", and public APIs return only `ready` variants **(design call)**.

## 3. Stage notes

| Stage | Decision | Source |
|---|---|---|
| Client compression | Downscale to ~2048 px at q≈0.8 (AP), or ~1600 px at q≈0.75 (CTS). A 3–5 MB photo becomes ~300–600 KB (AP) or ~150–400 KB (CTS). Send the EXIF read before compression as `client_hint` fields, stored with `evidence.source='client_exif'`. | [AP §1](<../research/research_notes/Stray pet platform research/ai_pipelines.md>), [CTS Q5](<../research/research_notes/Stray pet platform research/core_tech_stack.md>) |
| Upload | Presigned POST to quarantine with ~5 min TTL, so a flaky network costs one retry from the outbox. Use resumable or chunked upload only for uncompressed fallbacks larger than ~5 MB **(design call)**. | [CTS Q7](<../research/research_notes/Stray pet platform research/core_tech_stack.md>), [AP §1](<../research/research_notes/Stray pet platform research/ai_pipelines.md>) |
| Enqueue | Write the `media.asset` row and defer the job in the same transaction, which avoids the dual-write bug. Watch commit latency for the PG18 NOTIFY commit lock at high enqueue rates. | [CTS Q6, Q4](<../research/research_notes/Stray pet platform research/core_tech_stack.md>) |
| EXIF | Treat EXIF as **evidence, not truth.** Without OffsetTime, assume America/Sao_Paulo and record the uncertainty. Screenshots and edited files carry misleading EXIF. WhatsApp media usually has none (unverified, needs testing). Server EXIF mostly matters for uncompressed paths because canvas strips it client-side. | [AP §1](<../research/research_notes/Stray pet platform research/ai_pipelines.md>), [GTS §2](<../research/research_notes/Stray pet platform research/game_theory_trust_safety.md>) |
| Variants | **WebP for every derivative at MVP.** AVIF is smaller but much slower to encode on CPU, so consider it only for the detail view, once measured bytes per view justify it (no 2026 benchmark exists). Encoder quality ≈ 75–80 **(design call)**. Convert to sRGB before stripping, because strip drops the ICC profile **(design call)**. | [AP §1](<../research/research_notes/Stray pet platform research/ai_pipelines.md>) |
| Placeholder | **ThumbHash only.** It preserves aspect ratio and alpha and usually looks better than BlurHash, so BlurHash is dropped **(design call)**. | [AP §1](<../research/research_notes/Stray pet platform research/ai_pipelines.md>) |
| PDQ | Hash the oriented image and its rotations, because PDQ is not rotation-invariant and the 8 dihedral variants hash differently. Store the hashes as `bit(256)`. Search by brute-force Hamming distance over a geo-filtered set: `bit_count(pdq # :q) <= 31`. Use a long time window (365 d) so that old photos circulating again get caught **(design call)**. | [AP §1](<../research/research_notes/Stray pet platform research/ai_pipelines.md>) |
| Repost ≠ identity | A PDQ hit means "same photo", not "same animal at a new time". It sets `repost_of` with the badge "foto repetida — pode ser antiga" and writes an Elo `sugerido` with `method='model'`. **It never merges anything.** | [AP §1](<../research/research_notes/Stray pet platform research/ai_pipelines.md>), [STC §2](<../research/research_notes/Stray pet platform research/spatiotemporal_chains.md>) |
| Quality | Combine Laplacian variance on a downscaled grayscale image, a minimum resolution, and PDQ Q ≥ 50. Reject only extreme cases. Otherwise ask "Foto com pouca qualidade — consegue mandar outra?", because in an emergency a blurry photo beats no photo. | [AP §1](<../research/research_notes/Stray pet platform research/ai_pipelines.md>) |
| Privacy blur (v2) | Run EgoBlur faces and plates on every public derivative with a recall-oriented threshold of 0.1–0.3: a blurred wall costs nothing, while a missed face is a privacy incident. Blurring faces is enough; small bystanders don't need full-body blur. The unblurred master stays private. | [AP §2](<../research/research_notes/Stray pet platform research/ai_pipelines.md>) |
| Sensitive (tap-to-view) | Ask for `graphic_injury: none\|mild\|severe` inside the same VLM attribute call, at no extra cost. Use SafeSearch or Rekognition "violence/medical" ≥ LIKELY only as a second opinion, if evaluation shows misses. **Unknown or uncertain is treated as blurred.** **MVP rule (design call):** set `sensitive=true` when kind=emergência and condition ∈ {ferido, atropelado, bicheira, morto}, plus reporter self-flag and moderator override. WhatsApp photos already go through the intake LLM call, so they get the graphic_injury field in MVP. | [AP §2, §7](<../research/research_notes/Stray pet platform research/ai_pipelines.md>) |
| Detection (v2) | A closed-set detector covers cão and gato. Use RF-DETR nano/small or MDv6 (animal/person/vehicle), with a VLM fallback when nothing is detected. Produce one annotation per animal, so a photo with several animals becomes several observations under one sighting group (Wildbook-style). | [AP §2](<../research/research_notes/Stray pet platform research/ai_pipelines.md>), [STC §7](<../research/research_notes/Stray pet platform research/spatiotemporal_chains.md>) |
| Attributes (v2) | Use PT-BR folk coat colors, not breed names: caramelo, preto, branco, tigrado/rajado, malhado, frajola, tricolor, cinza, amarelo. Distill these later into a linear probe on the re-ID embedding. | [AP §2](<../research/research_notes/Stray pet platform research/ai_pipelines.md>) |

## 4. Libraries and models

| Component | Choice | License | Phase | Why |
|---|---|---|---|---|
| Client resize | `createImageBitmap` + (Offscreen)Canvas | browser API | MVP | Largest saving on prepaid mobile data ([CTS Q5](<../research/research_notes/Stray pet platform research/core_tech_stack.md>)) |
| Object store (dev) | SeaweedFS 4.48 | Apache-2.0 | MVP | Maintained S3 API. MinIO CE is archived and has published no binaries since Oct 2025 ([CTS Q7](<../research/research_notes/Stray pet platform research/core_tech_stack.md>)) |
| Object store (prod) | Cloudflare R2, or in-country S3 (Magalu Cloud) | commercial | MVP | R2 egress is free, but R2 has no South America location, so it is an LGPD international transfer under ANPD SCCs. Magalu prices were not retrieved ([CTS Q7](<../research/research_notes/Stray pet platform research/core_tech_stack.md>)) |
| Jobs | procrastinate 3.10.0 | MIT | MVP | Enqueues in the same transaction as the write, with no separate broker ([CTS Q6](<../research/research_notes/Stray pet platform research/core_tech_stack.md>)) |
| Decode/encode | **pyvips 3.2.0** (libvips) | n/i | MVP | 0.69 s / 109 MB, against Pillow-SIMD 9.5 at 1.51 s / 1,040 MB. Single-threaded libvips takes 0.77 s / 52 MB and ImageMagick ~4.4 s / ~1.5 GB. The benchmark runs load + crop + shrink + sharpen + save on a 10k×10k TIFF (libvips 8.18, 12 Aug 2025). It is I/O-heavy, which favours libvips, and Pillow doesn't auto-thread ([AP §1](<../research/research_notes/Stray pet platform research/ai_pipelines.md>)) |
| Decode fallback | Pillow 13.0.0 + pillow-heif | n/i | MVP | HEIC decoding in Python. `ImageOps.exif_transpose` applies the orientation and removes the tag (unverified this session) ([AP §1](<../research/research_notes/Stray pet platform research/ai_pipelines.md>), [CTS Q6](<../research/research_notes/Stray pet platform research/core_tech_stack.md>)) |
| On-the-fly sizes | imgproxy (Go + libvips) | n/i; the open-source vs Pro feature split is unverified | option | Serves arbitrary sizes behind a CDN with signed URLs, and keeps resize CPU out of FastAPI. Its source must be `media-private` masters and **never quarantine** ([AP §1](<../research/research_notes/Stray pet platform research/ai_pipelines.md>)) |
| Placeholder | ThumbHash | n/i | MVP | ~25 bytes ([AP §1](<../research/research_notes/Stray pet platform research/ai_pipelines.md>)) |
| Repost hash | PDQ (Meta ThreatExchange) | n/i | MVP | Reference implementations exist in C++, Python, Java, PHP and WASM. A faiss matcher reaches ~4,000 img/s but is unnecessary at our scale ([AP §1](<../research/research_notes/Stray pet platform research/ai_pipelines.md>)) |
| Blur score | OpenCV variance of Laplacian | n/i | MVP | Cheap gate that only raises a flag ([AP §1](<../research/research_notes/Stray pet platform research/ai_pipelines.md>)) |
| Face/plate blur | **EgoBlur** (FasterRCNN) | Apache-2.0 (repo LICENSE file not checked) | v2 (notes: MVP) | Used inside Meta since 2020. Face default threshold is 0.1. Alternative: imgproxy `blur_detections` with a face/plate ONNX model ([AP §2](<../research/research_notes/Stray pet platform research/ai_pipelines.md>)) |
| Animal detect | **RF-DETR** nano/small; **MDv6** `MDV6-mit-yolov9-c/e`, `MDV6-apa-rtdetr-c/e` (PyTorch-Wildlife 1.2.4) | Apache-2.0; MIT / Apache. Check each weight file: the default MDv6 compact is Ultralytics-based | v2 | Permissive. Hundreds of ms per image on CPU with ONNX Runtime/OpenVINO is an inference, not a measurement ([AP §2](<../research/research_notes/Stray pet platform research/ai_pipelines.md>)) |
| ✗ Rejected | Ultralytics YOLO26; YOLO-World | AGPL-3.0; GPL-3.0 | never | AGPL §13 obliges a source offer for the whole network service unless we buy an enterprise license ([AP §2](<../research/research_notes/Stray pet platform research/ai_pipelines.md>)) |
| Open-vocabulary fallback | Grounding DINO / OWLv2 / Florence-2 | Apache-2.0 / Apache-2.0 / MIT (all unverified) | v2, only if needed | Slower. Worth it only for unusual scenes such as "animal under a car" ([AP §2](<../research/research_notes/Stray pet platform research/ai_pipelines.md>)) |
| Attributes + graphic | One VLM call with a JSON schema (Haiku 5.5-class) | commercial API | v2 (MVP for WhatsApp photos) | Cheapest high-quality route. `graphic_injury` comes in the same call ([AP §2, §5](<../research/research_notes/Stray pet platform research/ai_pipelines.md>)) |
| Second opinion | Google SafeSearch / AWS Rekognition | commercial | v2, only if needed | SafeSearch: $1.50 per 1k (units 1,001–5M), first 1k per month free. Rekognition: ~$0.001/img for the first 1M. Accuracy on animal injuries is unknown ([AP §2](<../research/research_notes/Stray pet platform research/ai_pipelines.md>)) |
| Re-ID backbone (zero-shot) | **SigLIP 2** or **DINOv2**; **DINOv3** after legal review | Apache-2.0 (SigLIP 2 unverified) / Apache-2.0 / custom "DINOv3 License" | v3 | Permissive backbones to start. The DINOv3 license bans ITAR, military and weapons uses and requires redistribution under the same agreement; a developer issue flags it for legal review ([AP §3](<../research/research_notes/Stray pet platform research/ai_pipelines.md>)) |
| Re-ID baseline | MegaDescriptor-L-384 (Swin-L, 228.8M params, 384 px) | **CC-BY-NC-4.0** | offline eval only | It beats CLIP and DINOv2 on animal re-ID but is non-commercial, which is risky with sponsors or partners ([AP §3](<../research/research_notes/Stray pet platform research/ai_pipelines.md>)) |
| ✗ Unchecked | AvitoTech CLIP-L animal-ID fine-tune; PetFace dataset | not checked / commercial use unconfirmed | none | Do not train production models on these until their licenses are checked ([AP §3](<../research/research_notes/Stray pet platform research/ai_pipelines.md>)) |
| Re-ID fine-tune | ArcFace head trained on SRD-BR pairs | ours | v3b | The real accuracy gains come from here. PetFace ArcFace beats CLIP by 99.45% vs 91.86% AUC on dogs ([AP §3](<../research/research_notes/Stray pet platform research/ai_pipelines.md>)) |
| Top-k re-rank | ALIKED/LightGlue (wildlife-tools WildFusion) | n/i | v3, optional | Local-feature matching, run on the top-k only ([AP §3](<../research/research_notes/Stray pet platform research/ai_pipelines.md>)) |
| Vectors | pgvector 0.8.7 `halfvec` | n/i | v3 | Keeps vectors in the same database. Indexable up to 4,000 dims ([AP §3](<../research/research_notes/Stray pet platform research/ai_pipelines.md>), [CTS Q2](<../research/research_notes/Stray pet platform research/core_tech_stack.md>)) |

## 5. Re-identification (v3)

### 5.1 What accuracy to expect
PetFace (ECCV 2024) uses 224×224 face crops aligned by landmarks and scraped from pet-shop and adoption sites. That is the best case, and it is still not near-perfect ([AP §3](<../research/research_notes/Stray pet platform research/ai_pipelines.md>)):

| PetFace metric | Dog | Cat |
|---|---|---|
| Re-ID top-1, ArcFace R50, trained per species | 77.86% | 54.29% |
| Re-ID top-1, trained jointly across species | 68.75% | 70.30% |
| Verification AUC on unseen animals: PetFace / MegaDescriptor / CLIP / ImageNet | 99.45 / 93.75 / 91.86 / 97.18% | 97.71 / 87.30 / 85.10 / 81.58% |

- **No benchmark exists for street photos of mixed-breed dogs and cats.** The closest data is BIFOR's Sibetan set: 59 free-roaming dogs and 12 cameras, with only relative gains reported ([AP §3](<../research/research_notes/Stray pet platform research/ai_pipelines.md>)).
- Street sightings differ on almost every axis: non-frontal poses, full body, distance, night, motion blur, many look-alike caramelo and black SRDs, and owner selfies taken indoors. The notes **infer** a top-1 of about 20–50%, which is an inference and has not been measured.
- Vendor claims of 98–99% (Petnow; GovTech's frontal-face figure) are company-reported, with no audit or published false-match rate.
- **Target metric:** recall@10–20 after space-time filtering, meaning "the true match appears on the first screen". **Never publish a top-1 figure.**

### 5.2 Search: filter first, rank second
pgvector applies filters **after** the HNSW scan. With `ef_search=40` and a filter that matches 10% of rows, about 4 rows come back. Iterative scans (`strict_order|relaxed_order`, `max_scan_tuples` default 20,000) reduce the problem. For selective filters the notes recommend an exact scan over the filtered rows, which usually number under 10k ([AP §3](<../research/research_notes/Stray pet platform research/ai_pipelines.md>)).

```sql
-- matching.reid_vector copies species, H3 res-9 cell and valid_time from the Relato. Relatos are
-- immutable, so the copy cannot drift. It holds no exact coordinates and runs no cross-schema SQL
-- (repo rules 3 and 5)                                                          (design call)
WITH gallery AS MATERIALIZED (            -- MATERIALIZED stops the planner from choosing HNSW + post-filter
  SELECT relato_id, media_id, crop_kind, vec
  FROM   matching.reid_vector
  WHERE  model_id = :model_id             -- INVARIANT: only compare vectors from the same model version
    AND  species  = :species
    AND  h3_r9 = ANY(:gate_cells)         -- geo.public: gridDisk covering the per-status hard gate (STC §7)
    AND  valid_time && tstzrange(:t0, :t1)            -- widened time window
    AND  relato_id <> :query_relato_id)
SELECT relato_id, media_id, crop_kind, 1 - (vec <=> :q) AS cos_sim
FROM gallery ORDER BY vec <=> :q LIMIT 200;           -- → attribute re-rank → show top 10–20
```
- Global search, used for a lost pet with no area or a wide radius: HNSW (`halfvec_cosine_ops`) with `SET LOCAL hnsw.iterative_scan = relaxed_order`, plus one partial index per species, since species has few distinct values ([AP §3](<../research/research_notes/Stray pet platform research/ai_pipelines.md>)).
- Re-rank on agreement of coat, size, sex and collar, using Fellegi–Sunter weights. Bin cosine similarity into levels and learn m/u for each level from labelled answers ([STC §2, §7](<../research/research_notes/Stray pet platform research/spatiotemporal_chains.md>)).
- Score candidates **per Caso**, taking the max over the Caso's Relatos that have `afirmado` or `confirmado` Elos. Candidate Relatos that belong to no Caso show up as "relatos soltos parecidos" **(design call)**.
- Cold start: on day 1 there is no gallery of lost pets. Value comes first from linking avistamento to avistamento. When an owner registers a lost pet, ask for 3–5 photos (side, front, face close-up) ([AP §3](<../research/research_notes/Stray pet platform research/ai_pipelines.md>)).

### 5.3 Human decision and provenance
- Show the top 10–20 under the prompt "Pode ser o mesmo animal?" with photos side by side and three answers: sim / não / não sei.
- **Never auto-merge.** The model only writes an Elo with `state='sugerido'` and `method='model'`. A human answer appends a new Elo event, `confirmado` or `rejeitado`, with method `reporter|crowd_vote|moderator`. Merging Casos is a separate human action ([STC §2, §7](<../research/research_notes/Stray pet platform research/spatiotemporal_chains.md>)).
- Evidence stored on the Elo **(design call)**: `{"reid": {"model_id", "model_version", "crop_kind", "cos_sim", "rank", "gallery_size"}, "filters": {"species", "radius_m", "window"}, "attrs": {"coat": "agree", "sex": "unknown"}, "score_bits"}`.
- A `sugerido` Elo never moves "última vez visto" ([STC §4](<../research/research_notes/Stray pet platform research/spatiotemporal_chains.md>)). Every answer is logged as a labelled pair.

### 5.4 Thresholds (starting values, to be calibrated)

| Parameter | Initial value | Source |
|---|---|---|
| PDQ repost match / discard | Hamming ≤ 31 / discard when Q ≤ 49 | [AP §1](<../research/research_notes/Stray pet platform research/ai_pipelines.md>) |
| EgoBlur score | 0.1–0.3 (favours recall) | [AP §2](<../research/research_notes/Stray pet platform research/ai_pipelines.md>) |
| Candidates shown | top 10–20 | [AP §3](<../research/research_notes/Stray pet platform research/ai_pipelines.md>) |
| Minimum cosine score | **None.** No global cosine threshold; calibrate per species | [AP §3](<../research/research_notes/Stray pet platform research/ai_pipelines.md>) |
| Link posterior | < 0.2 → nothing; 0.2–0.8 → ask; > 0.8 → strong suggestion | [STC §2, §7](<../research/research_notes/Stray pet platform research/spatiotemporal_chains.md>) |
| Exact scan vs HNSW | Exact scan while the filtered gallery is under ~10k rows | [AP §3](<../research/research_notes/Stray pet platform research/ai_pipelines.md>) |
| Notify an owner ("possível avistamento") | Only at a high-precision operating point: precision ≥ 0.95 on held-out pairs **(design call)** | [AP §3](<../research/research_notes/Stray pet platform research/ai_pipelines.md>) |

### 5.5 Evaluation: building a Brazilian SRD dataset (SRD-BR)
- **Positives** are Elos in state `confirmado`. **Hard negatives** are `rejeitado` Elos, plus same-species, same-coat animals inside the gate (caramelo vs caramelo) **(design call)**.
- **Splits:** by Caso, so no identity leaks between sets; by time, training on older data and testing on newer; and by city. Deduplicate across splits with PDQ so reposts don't leak between them.
- **Metrics:** recall@10 and recall@20 inside the filtered gallery (primary), reported per species and per coat stratum, together with gallery size and the time humans take to decide. Measure precision at the notify operating point.
- **Baselines:** (a) attributes plus the space-time score with no embedding; (b) zero-shot SigLIP 2 and DINOv2; (c) MegaDescriptor offline only. **Gate:** a model ships only if it beats baseline (a) on recall@20 **(design call)**.
- **Shadow mode first:** compute suggestions and log them without showing them, then score them against Elos that humans confirm independently **(design call)**. Fine-tune ArcFace once there are thousands of pairs ([AP §7](<../research/research_notes/Stray pet platform research/ai_pipelines.md>)).
- **Legal:** WhatsApp-sourced media gets `training_eligible=false` until counsel clears the §4.7 data clause (see [whatsapp-intake.md](../integrations/whatsapp-intake.md)). Store the model name and version with every vector and re-embed everything when the model is upgraded ([AP §3](<../research/research_notes/Stray pet platform research/ai_pipelines.md>)).

## 6. Storage layout (design call)

```
quarantine/            PRIVATE, no CDN, lifecycle rules, API may only presign PUT/POST here
  up/{yyyy}/{mm}/{dd}/{upload_id}             PWA uploads (client UUIDv7)
  wa/{yyyy}/{mm}/{dd}/{wa_media_id}           WhatsApp media downloaded by intake
  audio/{yyyy}/{mm}/{dd}/{wa_media_id}.ogg    voice notes (intake); deleted after STT + dispute window
media-private/         PRIVATE, worker writes, moderators/matching read via signed GET
  master/{media_id}.webp                      oriented, stripped, UNBLURRED ~1600 px
  crop/{media_id}/{detection_id}.webp         re-ID crops 256–384 px (v2+)
media-public/          PUBLIC behind CDN, immutable keys, long cache TTL
  v1/{sha256(derivative)}/{detail|card}.webp  blurred (v2+), stripped
```
- Public keys are the hash of the **derivative** bytes, not of the original, so holding the original doesn't let anyone guess the URL. Takedown means deleting the object and purging the CDN.
- In dev, SeaweedFS runs with the same bucket names. Code switches between environments only through the endpoint URL ([CTS Q7](<../research/research_notes/Stray pet platform research/core_tech_stack.md>)).

## 7. Data model sketch (design call)

```
media.asset(id uuidv7 pk, source enum[pwa,whatsapp,moderator], uploader_ref, client_upload_id unique,
  state enum[pending,processing,ready,rejected,failed,purged], quarantine_key, original_sha256,
  original_mime, original_bytes, width, height, pdq bit(256), pdq_rot bit(256)[], pdq_quality smallint,
  blur_var real, quality_flags text[], thumbhash text, repost_of uuid null,
  sensitive enum[none,mild,severe,unknown], sensitive_src enum[default,self,model,moderator],
  privacy_blur enum[not_run,applied,none_found,failed], training_eligible bool,
  legal_hold bool, created_at, processed_at, purged_at)
media.variant(media_id, name enum[detail,card,master,crop], bucket, key, mime, w, h, bytes, sha256, public bool)
media.evidence(media_id pk, source enum[server_exif,client_exif], taken_at timestamptz, tz_assumed bool,
  gps geography(Point) null, make, model, software, read_at)     -- PRIVATE; reads → geo.location_access_log
media.detection(id, media_id, kind enum[animal,person,face,plate,vehicle], label, bbox, score,
  model_id, model_version)                                        -- v2
matching.reid_vector(id, media_id, detection_id, crop_kind enum[body,face], model_id, model_version,
  vec halfvec(D), species, h3_r9 h3index, valid_time tstzrange, relato_id, created_at)  -- v3
```
`src/media/public.py` exposes `create_upload`, `complete_upload`, `ingest_bytes(source='whatsapp')`, `get_public_media(ids)`, which returns only variants, ThumbHash and the sensitive flag, `get_private_view(id, actor)`, which is logged, and `find_reposts(id)`. It emits the events `media.ready` and `media.rejected`. When `media.ready` arrives for a Relato that already has an Elo `confirmado` or `afirmado`, `chains` appends a Bloco "nova foto" **(design call)**.

## 8. Retention (design call unless cited)

| Object | Retention | Why |
|---|---|---|
| Quarantine originals | **As long as the Relato exists.** 7 d if rejected or failed. Kept past deletion only while `legal_hold` is set (T4 only, e.g. evidence of maus-tratos) | Repo rule 2 needs originals to rebuild variants. **This conflicts with AP's "short retention"** ([AP §1](<../research/research_notes/Stray pet platform research/ai_pipelines.md>)); see §12. The risk is smaller than it looks: the common paths (client canvas re-encode, WhatsApp) usually arrive without EXIF |
| Voice-note audio | 7 d after transcription | Voices are personal data. The notes say to delete after a short dispute window ([AP §6](<../research/research_notes/Stray pet platform research/ai_pipelines.md>)) |
| `media.evidence.gps` | Exact for 90 d, then coarsened to H3 res-7 | Keep exact location only for as long as it is useful for search |
| Private master and crops | As long as the Relato exists | Derived cache that saves re-decoding HEIC when re-blurring or re-embedding. It can be rebuilt from the original |
| Public variants | As long as the Relato exists; takedown deletes them and purges the CDN | — |
| Embeddings | Until the Relato is deleted or the model is retired (then re-embed) | Embeddings from different models can't be compared ([AP §3](<../research/research_notes/Stray pet platform research/ai_pipelines.md>)) |

An LGPD deletion request cascades to every row above, except objects under `legal_hold`.

## 9. Costs (as far as the notes provide them)

- **R2:** $0.015/GB-month, Class A $4.50/M, Class B $0.36/M, **egress $0**. Free tier: 10 GB-month, 1M Class A and 10M Class B ([CTS Q7](<../research/research_notes/Stray pet platform research/core_tech_stack.md>)). AWS sa-east-1 egress is ~$0.15/GB, a 2020 figure that was not re-verified ([CTS Q10](<../research/research_notes/Stray pet platform research/core_tech_stack.md>)).
- *Arithmetic on those prices:* assume 1M photos at ~200 KB of public variants each (CTS's photo size). That is ~200 GB, or ~$3/month of storage. About 4 writes per photo gives ~4M Class A operations, ~$18 once per million photos. Egress is the line item that R2 removes.
- **CPU:** libvips takes ~0.7 s and ~100 MB on a 100 MP image, and 12 MP phone photos cost about an order of magnitude less. Processing a few thousand photos a day on 2–4 vCPUs is an inference ([AP §2, §7](<../research/research_notes/Stray pet platform research/ai_pipelines.md>)).
- **v2 APIs:** VLM image tokens cost ~$0.0003 per report on Haiku 5.5, assuming 2 photos at ~1,600 tokens each. An optional moderation API adds ~$2 per 1,000 reports ([AP §5, §7](<../research/research_notes/Stray pet platform research/ai_pipelines.md>)).
- **v3:** costs are CPU only, with ~$0 in API fees. A ViT-B/L embedding on a 384 px crop takes ~0.1–1 s on CPU, an unsourced inference. Vectors take 1.5–2 KB each, so 1M photos need ~2 GB plus HNSW overhead, doubled when both body and face are embedded. Rent a GPU only for fine-tuning and bulk re-embedding ([AP §3](<../research/research_notes/Stray pet platform research/ai_pipelines.md>)).

## 10. Phases

| Phase | Scope | Exit criterion |
|---|---|---|
| **MVP** | Client-side compression; presign to quarantine; procrastinate; HEIC decode and orientation; EXIF evidence; WebP 1600/640, stripped; ThumbHash; PDQ plus rotations as a repost flag; quality flags; rule-based `sensitive` + self-flag + moderator override; IAM split and the CI invariant test | Invariant test is green. No public key exists outside `media-public` |
| **v2** | EgoBlur faces and plates; RF-DETR/MDv6 crops; VLM attributes + `graphic_injury`; second-opinion moderation API if evaluation finds misses; imgproxy if the frontend needs arbitrary sizes; AVIF trial for the detail view | Miss rate on faces and gore measured on a labelled sample |
| **v3a** | Zero-shot embeddings (SigLIP 2 / DINOv2 / DINOv3 if legally cleared) in pgvector; candidate UI; shadow mode; SRD-BR dataset | Beats the attributes-only baseline on recall@20 |
| **v3b** | ArcFace fine-tune on confirmed pairs; versioned re-embedding job; attribute and graphic classifiers distilled from logged VLM outputs | Thousands of confirmed pairs; legal sign-off on WhatsApp media |

**This plan departs from the notes:** they put EgoBlur and the VLM graphic flag in MVP and zero-shot embeddings in v2 ([AP §7](<../research/research_notes/Stray pet platform research/ai_pipelines.md>)). If public launch comes before v2, move EgoBlur into MVP. It is CPU-only and Apache-2.0.

## 11. Failure modes

| Failure | Mitigation |
|---|---|
| Original with GPS served to the public | §1 invariant, IAM split, CI fixture test, imgproxy never reads from quarantine |
| Decompression bomb or a malicious file | Sniff magic bytes, cap pixels, cap size; quarantine has no public read |
| HEIC fails to decode | Fall back to Pillow + pillow-heif, then `failed` with the prompt "Não conseguimos abrir a foto — pode mandar de novo?" |
| Rotated or flipped repost escapes PDQ | Hash the rotations. Flips remain a known gap, since all 8 dihedral variants differ |
| PDQ false positive on featureless images | Discard hashes with Q ≤ 49 |
| An old photo recirculates as a "new" emergency | PDQ over a 365 d window flags `repost_of`. A moderator decides; nothing auto-merges |
| A face is missed | Recall-oriented threshold; the unblurred master stays private; anyone can report a public photo |
| Gore shows up on the public map | Unknown is blurred; MVP rules; self-flag; moderator override ([AP §2](<../research/research_notes/Stray pet platform research/ai_pipelines.md>)) |
| Vectors from different models get compared | `model_id` filter in every query; re-embed job on upgrade |
| False "é o seu cachorro!" notification | Never auto-merge; notify only at the high-precision operating point; wording says "possível" ([AP §7](<../research/research_notes/Stray pet platform research/ai_pipelines.md>)) |
| AGPL or non-commercial weights slip in | License allowlist for model weights, checked in CI **(design call)** |
| Worker backlog delays photos on emergencies | Separate `media_urgent` queue for kind=emergência **(design call)**. The Relato never waits on its photos |

## 12. Open questions (blocking marked ⛔)

1. ⛔ Should EgoBlur move into MVP? (See §10.) This is a product decision.
2. ⛔ How long to keep originals. Repo rule 2 (variants rebuildable from originals) conflicts with AP's "short retention" of GPS-bearing files. Options: (a) keep them for the Relato's lifetime, as this doc does now; (b) after extracting evidence, rewrite the stored original with metadata removed losslessly, keeping the pixels identical (tooling not researched); (c) amend rule 2 so the stripped private master becomes the pixel source of truth.
3. ⛔ Check whether presigned POST policies (content-type and size conditions) work on R2, SeaweedFS and Magalu. If not, fall back to presigned PUT with a signed content-type and length, and check the size again in the worker.
4. ⛔ Choose the production bucket: R2 needs Cloudflare to offer the ANPD SCCs (not verified); Magalu's prices and CDN were not retrieved ([CTS Q7](<../research/research_notes/Stray pet platform research/core_tech_stack.md>)).
5. Licenses marked n/i: libvips/pyvips, Pillow, pillow-heif, PDQ, ThumbHash, imgproxy, pgvector, ONNX Runtime. Also the per-weight MDv6 license text and EgoBlur's LICENSE file.
6. Legal review of the DINOv3 license and of MegaDescriptor's NC terms; PetFace dataset license.
7. Test whether WhatsApp Cloud API media really lacks EXIF, and whether iOS `<input type=file>` still converts HEIC to JPEG. Both are unverified ([AP §1](<../research/research_notes/Stray pet platform research/ai_pipelines.md>)).
8. Benchmark the detector, EgoBlur and embedding models on CPU on the target VM. The notes have no sourced latency for any of them.
