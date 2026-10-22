# AI & Media Pipelines for a Brazilian Stray/Lost-Pet Platform (image pipeline, detection, re-ID, WhatsApp, LLM intake, STT)

Research date: 2026-10-21. Prices in USD unless noted. "Unverified this session" means the claim comes from a canonical project page or prior knowledge and was not re-fetched; treat it as lower confidence.

## 1. Image pipeline: formats, EXIF/GPS, privacy stripping, resizing, placeholders, dedup, quality, client-side compression

### Takeaway
Use libvips (pyvips) or imgproxy for server-side processing. libvips is about 2x faster than Pillow-SIMD and uses about 10x less memory on the reference benchmark. Read EXIF GPS and timestamp at ingest as private evidence, then publish only re-encoded, metadata-free derivatives. Add PDQ hashes for repost/duplicate detection (Hamming ≤31 as the starting threshold) and a quality gate. The main failure mode is publishing an original file with GPS still in it, which can expose a reporter's home location.

### Cited Findings
- **libvips vs Pillow performance (official libvips benchmark, run 12 Aug 2025, libvips 8.18):** The test is load, crop, shrink 10%, sharpen and save on a 10k×10k RGB TIFF. pyvips (`vips.py`) took 0.69 s with 109 MB peak memory. Pillow-SIMD 9.5 took 1.51 s with 1,040 MB. Single-threaded libvips took 0.77 s with 52 MB. ImageMagick took about 4.4 s with about 1.5 GB. The page notes that Pillow and OpenCV do not auto-thread and that the test is I/O-heavy, which favors libvips. — [libvips wiki: Speed and memory use](https://github.com/libvips/libvips/wiki/Speed-and-memory-use)
- **imgproxy object detection:** imgproxy can detect objects and blur them with a `blur_detections` URL option, positioned as an anonymization feature. Docker images tagged `-ml` ship a bundled face-detection model. Custom DarkNet or ONNX YOLO models can be loaded, so a license-plate model could be plugged in. — [imgproxy docs 3.25.x: object detection](https://docs.imgproxy.net/3.25.x/features/object_detection); [3.24.x](https://docs.imgproxy.net/3.24.x/features/object_detection)
- **PDQ perceptual hash (Meta ThreatExchange):** The recommended starting threshold is Hamming distance ≤31, to be tuned on your own data. A quality score Q measures how featureless an image is, and hashes with Q ≤49 should be discarded. A faiss-based matcher reached about 4,000 images/s. PDQ "does not guarantee exact rotational invariance": the 8 dihedral variants (90° rotations and flips) give different hashes. Reference implementations exist in C++, Python, Java, PHP and WASM. — [PDQ README](https://github.com/facebook/ThreatExchange/blob/main/pdq/README.md)
- **LGPD:** Lei 13.709/2018 defines personal data as information related to an identified or identifiable natural person (Art. 5, I). Precise GPS of where a reporter stood, often their home or street, combined with their WhatsApp number, falls under this definition. — [Lei 13.709/2018 (Planalto)](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm)
- *(Unverified this session, canonical project pages)*:
  - HEIC/HEIF decoding in Python is available via `pillow-heif`. — [pillow-heif](https://github.com/bigcat88/pillow_heif)
  - libvips reads HEIF through libheif. — [libvips](https://github.com/libvips/libvips)
  - ThumbHash encodes a placeholder in about 25 bytes. It preserves aspect ratio and alpha and generally looks better than BlurHash. — [ThumbHash](https://evanw.github.io/thumbhash/); [BlurHash](https://blurha.sh/)
  - Pillow's `ImageOps.exif_transpose` applies the EXIF Orientation tag and removes it. — [Pillow ImageOps docs](https://pillow.readthedocs.io/en/stable/reference/ImageOps.html)

### Inferences
- **Ingest order (keep it boring):**
  1. Accept JPEG/PNG/WebP/HEIC/AVIF up to about 20 MB.
  2. Sniff magic bytes, not the extension.
  3. Decode with pyvips (libheif built in) or Pillow + pillow-heif.
  4. Read EXIF (DateTimeOriginal, OffsetTime, GPSLatitude/Longitude, Make/Model) into a private `photo_evidence` row.
  5. Auto-orient.
  6. Re-encode the derivatives: WebP or AVIF at about 1600 px long edge for detail view, about 640 px for cards, a 256–384 px crop for re-ID/embeddings, and a ThumbHash string. All derivatives are metadata-stripped (`strip=True` in pyvips save, or don't pass `exif=` in Pillow).
  7. Keep the original in a private bucket with short retention.
- **Key invariant:** nothing public is ever served from the original object key. Only derivatives produced by the strip step are public.
- **EXIF as evidence, not truth:**
  - WhatsApp re-encodes media and typically drops EXIF, so photos arriving via WhatsApp will usually lack GPS and time. Treat EXIF as a bonus for web/app uploads only, and rely on the WhatsApp location pin and message timestamp instead.
  - EXIF time has no timezone unless OffsetTime is present. Assume America/Sao_Paulo and record the uncertainty.
  - Screenshots and edited images have misleading EXIF.
- **imgproxy vs in-process pyvips:**
  - imgproxy (Go + libvips) suits on-the-fly variants behind a CDN with signed URLs. It keeps CPU-heavy resizing out of the FastAPI workers.
  - pyvips in a Celery/RQ/Arq worker is simpler for a fixed set of derivatives.
  - For an MVP, pre-generate 3 variants in a worker. Add imgproxy when the frontend needs arbitrary sizes.
- **AVIF vs WebP:**
  - AVIF gives smaller files but encodes much more slowly on CPU.
  - WebP encodes fast and is universally supported.
  - Recommendation: WebP for all derivatives at MVP, with AVIF for the large detail view only if bandwidth costs justify it.
- **Duplicate/repost detection:**
  - Compute PDQ on the auto-oriented image.
  - Also hash the 4 rotations, since PDQ isn't rotation-invariant and street photos often arrive rotated.
  - Store as `bit(256)` in Postgres. Brute-force Hamming over a geo/time-filtered candidate set is cheap; the faiss route is only needed at very large scale.
  - Use PDQ to auto-link reposts of the same photo, which is common when one injured-dog photo circulates in neighborhood WhatsApp groups. Do not use it for animal identity: same animal, different photo is the re-ID problem.
- **Blur/quality gate:**
  - Variance of Laplacian on a downscaled grayscale crop (OpenCV), plus a minimum resolution and PDQ quality ≥50.
  - Reject only extremes. For emergencies, a blurry photo is better than no photo, so flag "low quality, please send another" instead of blocking.
- **Client-side compression:**
  - In the web/PWA, downscale to about 2048 px and re-encode to JPEG or WebP at about 0.8 quality via canvas/OffscreenCanvas before upload. This typically cuts a 3–5 MB phone photo to about 300–600 KB.
  - Read EXIF GPS client-side *before* compressing if you want it as evidence, because canvas re-encode drops EXIF.
  - Use resumable/chunked uploads for poor 3G/4G coverage.

### Gaps
- No 2026 benchmark found comparing AVIF vs WebP encode speed with libvips 8.18.
- Did not verify which imgproxy features (object detection, AVIF autoquality) are Pro-only vs open source, or imgproxy Pro pricing.
- Did not verify current browser HEIC decode support (Safari vs Chrome), or whether iOS `<input type=file>` still transcodes HEIC to JPEG by default.
- Did not verify that WhatsApp Cloud API media strips EXIF. This is inferred from common knowledge and should be tested.

## 2. Animal detection & attributes, privacy blurring (faces/plates), sensitive-content handling, licenses, CPU feasibility

### Takeaway
Use Apache/MIT-licensed detectors and avoid AGPL Ultralytics weights unless you buy an enterprise license or open-source the whole service:
- MegaDetector v6 MIT/Apache variants (animal/person/vehicle)
- RF-DETR (Apache 2.0) for crops
- EgoBlur (Apache 2.0) for faces and plates
- A cheap moderation API or VLM pass to blur graphic injuries behind a tap

Species, coat color and size are best obtained from a VLM/LLM call at MVP, not a custom classifier.

### Cited Findings
- **Ultralytics YOLO26 is AGPL-3.0 and RF-DETR is Apache 2.0.** Roboflow, the RF-DETR vendor, says using Ultralytics code, architectures or trained weights can require releasing the full source of the larger derivative application. Ultralytics sells an Enterprise License to avoid this. Roboflow claims RF-DETR is the first real-time model above 60 AP on COCO. Roboflow is not a neutral source. — [Roboflow: YOLO26 vs RF-DETR](https://roboflow.com/compare/yolo26-vs-rf-detr); [Roboflow vs Ultralytics blog](https://blog.roboflow.com/roboflow-vs-ultralytics/)
- **Other permissive options:** Lightly lists RF-DETR, YOLOX and LibreYOLO as Apache 2.0/MIT alternatives. Lightly frames Ultralytics as requiring a commercial license for production, which is stronger than Roboflow's "compliance question" framing; both are vendors. — [Lightly: Best Ultralytics alternatives 2026](https://lightly.ai/blog/best-ultralytics-alternatives-in-2026)
- **MegaDetector v6:** Released with a focus on "computational efficiency, performance, modernizing of model architectures, and licensing", with YOLOv9, YOLOv11 and RT-DETR variants. PyTorch-Wildlife 1.2.4 added MIT YOLO and Apache RT-DETR variants (`MDV6-mit-yolov9-c/e`, `MDV6-apa-rtdetr-c/e`). The PyTorch-Wildlife repo is MIT-licensed. The default MDv6 compact model is Ultralytics-based, so check the per-weight license. — [Microsoft Biodiversity: MegaDetectorV6](https://microsoft.github.io/Biodiversity/base/models/detection/ultralytics_based/megadetectorv6/); [past releases](https://microsoft.github.io/Biodiversity/releases/past_releases/); [WILDLABS announcement](https://wildlabs.net/node/16685)
- **EgoBlur (Meta):**
  - FasterRCNN-based face and license-plate detectors, released under Apache 2.0 for commercial and non-commercial use.
  - Used internally at Meta since 2020 for Project Aria.
  - The face model's default score threshold is 0.1, which favors recall.
  - Sources: [HF model card](https://huggingface.co/projectaria/EgoBlur); [Project Aria EgoBlur](https://projectaria.com/tools/egoblur); [arXiv 2308.13093](https://arxiv.org/abs/2308.13093). The LICENSE file in the GitHub repo was not directly checked.
- **Google Cloud Vision SafeSearch:**
  - $1.50 per 1,000 images for units 1,001–5M, and $0.60 per 1,000 above 5M. The first 1,000 units per month are free.
  - SafeSearch is free when billed together with Label Detection.
  - Figures come from localized Google pricing pages. — [Cloud Vision pricing (es)](https://cloud.google.com/vision/docs/pricing?hl=es); [Cloud Vision pricing](https://cloud.google.com/vision/pricing?hl=hu)
  - *(Unverified this session)* SafeSearch returns likelihoods for adult, spoof, medical, violence and racy.
- **AWS Rekognition DetectModerationLabels:**
  - About $0.001/image for the first 1M images, $0.0008 for the next 9M, falling to $0.0004 above 100M.
  - Free tier is 5,000 images/month for 12 months. Bulk async analysis is supported.
  - Figures are from a third-party guide consistent with AWS's worked example. — [AWS Rekognition pricing](https://aws.amazon.com/rekognition/pricing/); [Wring pricing guide](https://wring.co/blog/aws-rekognition-pricing-guide)
- *(Unverified this session, licenses from memory of the repos)*:
  - Grounding DINO is Apache 2.0. — [IDEA-Research/GroundingDINO](https://github.com/IDEA-Research/GroundingDINO)
  - OWLv2 is Apache 2.0. — [google-research/big_vision / scenic OWL-ViT](https://github.com/google-research/scenic/tree/main/scenic/projects/owl_vit)
  - Florence-2 is MIT. — [microsoft/Florence-2-large](https://huggingface.co/microsoft/Florence-2-large)
  - YOLO-World is GPL-3.0. — [AILab-CVC/YOLO-World](https://github.com/AILab-CVC/YOLO-World)

### Inferences
- **Closed vs open-vocabulary detection:**
  - The platform needs only a few classes: dog, cat, person, vehicle, plus maybe horse/cattle/bird.
  - COCO-trained closed detectors (RF-DETR, or MegaDetector "animal" + species classification) cover dog and cat directly. Open-vocabulary detectors (Grounding DINO, OWLv2) are slower and only pay off for odd classes such as "puppy in a box" or "animal under a car".
  - Recommendation: RF-DETR-nano/small or MDv6-MIT for crop + person/vehicle boxes, with a VLM fallback when nothing is detected.
- **CPU feasibility:** small real-time detectors (nano/small, about 640 px input) are generally CPU-viable at roughly hundreds of ms per image with ONNX Runtime/OpenVINO. Async processing of a few thousand photos/day fits on 2–4 vCPUs. This is an inference only; no 2026 CPU latency figure was found for RF-DETR or MDv6.
- **Attributes (species, coat color, pattern, size, collar, injury visible, puppy/adult):**
  - Cheapest high-quality route at MVP is one multimodal LLM call per photo with a JSON schema (see Q5).
  - Later, distill into a small classifier head on top of the re-ID embedding (linear probe) to drop per-image API cost to near zero.
  - Coat color vocabulary should be PT-BR folk categories, not breed names: caramelo, preto, branco, tigrado/rajado, malhado, frajola, tricolor, cinza, amarelo. "Caramelo" is the iconic SRD.
- **Privacy blurring:**
  - Run EgoBlur faces + plates (or imgproxy `blur_detections` with a face/plate ONNX model) on every *public* derivative.
  - Keep the unblurred original private for moderators.
  - Use a recall-oriented threshold (0.1–0.3), since a false blur on a wall is harmless and a missed face is a privacy incident.
  - Persons are also detected by MegaDetector/RF-DETR. Blurring whole small-in-frame bystanders is probably unnecessary; faces suffice.
- **Graphic injury content:**
  - The goal is "blur behind a tap", not removal. Emergencies are the platform's purpose and the images are often gory: fractures, myiasis/bicheira, hit-by-car.
  - Option A: Rekognition or SafeSearch "violence/medical" likelihood ≥ LIKELY → `sensitive=true`.
  - Option B: add a `graphic_injury: none|mild|severe` field to the same VLM attribute call, which costs nothing extra.
  - Recommendation: B at MVP, with user self-flag and moderator override, and A as a second opinion only if B shows misses in evaluation.
  - Failure mode: a false negative traumatizes users on the public map. Default unknown/uncertain to blurred.
- **Licensing failure mode:** an AGPL model behind a FastAPI service over a network triggers AGPL §13 source-offer obligations for the combined work. That is fine only if the platform is fully open source by design; otherwise use the MIT/Apache weights.

### Gaps
- No measured CPU latency found for RF-DETR, MDv6-MIT or EgoBlur on typical cloud vCPUs.
- Did not verify the exact license text on MDv6 MIT/Apache weights or the EgoBlur repo LICENSE file.
- No open, permissively licensed "gore/graphic injury" classifier was identified. SafeSearch/Rekognition category accuracy on animal injuries specifically is unknown and needs local evaluation.
- YOLOv12 and newer non-Ultralytics YOLO variants (and their licenses) were not researched.

## 3. Animal re-identification: SOTA, realistic accuracy for street photos of SRD dogs/cats, vector search design, human-in-the-loop, compute

### Takeaway
Published "near-perfect" numbers come from aligned, frontal face crops from pet-shop/adoption sites. For example, PetFace dog verification AUC is 99.45% and dog re-ID top-1 is 77.86% even on that curated data. Commercial claims (98–99%) are company-reported with no independent audit. For in-the-wild street photos of mixed-breed dogs and cats, plan for a candidate-ranking aid, not automatic identification:
- Hard-filter by species, geo radius and time window.
- Rank by embedding similarity plus attributes.
- Show the top 10–20 to humans for confirmation.

Licensing is the hidden constraint. MegaDescriptor is CC-BY-NC-4.0 and DINOv3 has a custom license.

### Cited Findings
- **PetFace (ECCV 2024 oral):**
  - Dataset: 257,484 individuals across 13 animal families. The dog subset has 46,755 individuals and 168,348 images.
  - Images are 224×224 face crops aligned by species-specific landmarks, sourced from pet-shop and adoption websites.
  - Re-ID top-1 with ArcFace ResNet-50: dog 77.86%, cat 54.29%. Joint training across species gave dog 68.75% and cat 70.30%.
  - Verification AUC on unseen individuals:
    - PetFace ArcFace: dog 99.45%, cat 97.71%
    - MegaDescriptor: dog 93.75%, cat 87.30%
    - CLIP: dog 91.86%, cat 85.10%
    - ImageNet: dog 97.18%, cat 81.58%
  - Within the top-10 dog breeds, PetFace scored about 98.3% vs MegaDescriptor 86.25% and CLIP 80.78%.
  - Average re-ID accuracy across families: ArcFace 51.23%, Softmax 41.88%.
  - Sources: [arXiv 2407.13555 (html v2)](https://arxiv.org/html/2407.13555v2); [ECCV oral](https://eccv2024.ecva.net/virtual/2024/oral/1070); [project page](https://dahlian00.github.io/PetFacePage/)
- **WildlifeDatasets / MegaDescriptor (WACV 2024):**
  - MegaDescriptor outperforms CLIP and DINOv2 "by a significant margin" on animal re-ID datasets. DINOv2 performed poorly even at larger input size. — [WACV 2024 paper](https://openaccess.thecvf.com/content/WACV2024/html/Cermak_WildlifeDatasets_An_Open-Source_Toolkit_for_Animal_Re-Identification_WACV_2024_paper.html); [arXiv 2311.09118](https://arxiv.org/abs/2311.09118v1)
  - MegaDescriptor-L-384 is Swin-L (`swin_large_patch4_window12_384`, 228.8M params) with 384×384 input, pretrained on all available re-ID datasets. **License: CC-BY-NC-4.0 (non-commercial).** — [HF model card](https://huggingface.co/BVRA/MegaDescriptor-L-384)
- **AnimalCLEF 2025 (DS@GT):** A triplet-learning head on top of frozen backbones improved MegaDescriptor by 0.13 (averaged BAKS/BAUS) but DINOv2 by only about 0.03. The authors argue general-purpose embedding spaces are harder to reshape for fine-grained identity. — [arXiv 2509.12353](https://arxiv.org/html/2509.12353v1)
- **WildlifeReID-10k (CVPRW 2025):** More than 10k identities, about 33 species, more than 140k images. It is a multi-species benchmark and not dog-specific. — [CVPRW 2025](https://openaccess.thecvf.com/content/CVPR2025W/FGVC/html/Adam_WildlifeReID-10k_Wildlife_re-identification_dataset_with_10k_individual_animals_CVPRW_2025_paper.html)
- **Free-roaming dogs (closest to strays):** BIFOR (Ecological Informatics 2025) released YT-BB-Dog (2,723 dogs from YouTube) and Sibetan, which has 59 free-roaming dogs recorded by 12 cameras in Bali. The method improved rank-1 by more than 9% over baseline on Sibetan; absolute numbers were not retrieved. — [HAL hal-05492220](https://hal.inrae.fr/ASTRE/hal-05492220v1)
- **DINOv3 vs re-ID backbones:** A 2026 jaguar re-ID diagnostic paper benchmarks frozen DINOv3 ViT/ConvNeXt alongside MiewID and MegaDescriptor-L. Results were not retrieved. — [arXiv 2604.09690](https://arxiv.org/pdf/2604.09690)
- **DINOv3 license (14 Aug 2025):**
  - Custom "DINOv3 License": non-exclusive, worldwide, royalty-free, non-transferable.
  - Prohibits ITAR, military, warfare and weapons end uses.
  - Redistribution of materials or derivatives must be under the same agreement.
  - A developer issue flags it as needing legal review. DINOv2 was Apache 2.0.
  - Sources: [DINOv3 License](https://ai.meta.com/resources/models-and-libraries/dinov3-license); [GitHub issue #31](https://github.com/facebookresearch/dinov3/issues/31)
- **Fine-tuned CLIP for animal ID:** A CLIP ViT-L/14 fine-tuned for animal identification exists on HF from AvitoTech. License and metrics were not checked. — [HF AvitoTech/Zer0int-CLIP-L-for-animal-identification](https://huggingface.co/AvitoTech/Zer0int-CLIP-L-for-animal-identification)
- **Commercial claims:**
  - Petco Love Lost claims more than 170,000 US reunions, an organization-reported total. — [Shelly Palmer, Dec 2025](https://shellypalmer.com/2025/12/ai-for-good-the-technology-helping-thousands-of-lost-pets-every-week/)
  - An older CBS piece cites 100,000. — [Yahoo/CBS](https://tech.yahoo.com/ai/articles/ai-using-facial-recognition-help-163225345.html)
  - A GovTech article reports 98% correct identification from a *frontal face photo* against a 25,000-pet database. The vendor is unclear and no protocol is given. — [GovTech](https://www.govtech.com/products/facial-recognition-to-reconnect-pets-owners-in-baltimore.html)
  - No independent evaluation, false-match rate or methodology was found.
- **Nose-print biometrics:**
  - Petnow claims 98.97% recognition (CEO, "auto-focusing"). Other outlets round to 98–99%. All figures are company-reported, and no Korean government mandate was confirmed. — [TechCrunch 2023](https://techcrunch.com/2023/09/20/petnow-claims-to-be-able-to-identify-dogs-and-cats-from-their-snouts); [Freethink](https://www.freethink.com/?p=71818)
- **pgvector (latest 0.8.7):**
  - HNSW defaults: `m=16`, `ef_construction=64`, `hnsw.ef_search=40`.
  - Indexable dimensions: `vector` up to 2,000, `halfvec` up to 4,000, `bit` up to 64,000.
  - Filters apply *after* the index scan. With `ef_search=40`, a filter matching 10% of rows returns about 4 rows on average.
  - Since 0.8.0, iterative index scans (`hnsw.iterative_scan = strict_order|relaxed_order`, `hnsw.max_scan_tuples` default 20,000) mitigate this.
  - Recommended alternatives: an exact search with a B-tree/GiST index on the filter when the filter is selective, partial indexes for few distinct values, and partitioning for many.
  - Source: [pgvector README](https://github.com/pgvector/pgvector)

### Inferences
- **Realistic accuracy for street photos of SRD dogs/cats** (inference from the evidence above; no direct benchmark exists). Street sightings differ from PetFace on almost every axis:
  - non-frontal poses
  - full-body rather than face
  - distance and night lighting
  - motion blur
  - many near-identical "caramelo" or black SRDs
  - lost-pet reference photos that are owner selfies or indoor shots, a domain gap

  Expect top-1 identification well below PetFace's 77.86% (dog) and 54.29% (cat), plausibly in the 20–50% range. Expect top-10/20 *after* geo/time filtering to be meaningfully higher, because the filter shrinks the gallery from millions to tens or hundreds.
  - Design target: **"the true match is on the first screen of candidates" (recall@10–20)**, measured on your own data.
  - Never auto-merge cases on embedding similarity alone.
- **Pipeline (v2):**
  1. Detect and crop the animal (Q2).
  2. Optionally detect the head for a face crop.
  3. Embed both the body crop and the face crop, if the face is visible and large enough.
  4. Store per-photo vectors.
  5. Query: `WHERE species = $1 AND ST_DWithin(geom, $pt, radius) AND seen_at BETWEEN $t0 AND $t1`. Use an exact cosine scan over the filtered rows, typically fewer than 10k, so it is fast and needs no HNSW. Use HNSW + `iterative_scan=relaxed_order` only for wide-radius or no-filter "global" searches.
  6. Re-rank with attribute agreement (coat color, size, sex, collar).
  7. Optionally use local-feature matching (e.g., ALIKED/LightGlue as in wildlife-tools' WildFusion) for the top-k.
- **Dimension and storage:**
  - 768–1024-d `halfvec` is about 1.5–2 KB per vector. 1M photos is about 2 GB plus HNSW overhead, which is fine on a single Postgres.
  - Store the model name and version with each vector and re-embed on model upgrade. Embeddings from different models are not comparable; this is the key invariant.
- **Thresholds:** don't ship a global cosine threshold. Calibrate per species on a labeled validation set, and present ranked candidates with "possible match" language. Use the threshold only to decide whether to *notify* an owner, at a high-precision operating point.
- **Backbone choice and licensing:**
  - MegaDescriptor (CC-BY-NC) is fine for research and prototyping, but the "NC" clause is risky for anything with revenue, sponsorship or a commercial partner. Get legal review.
  - DINOv3 is commercially usable under a custom license, but its re-ID performance vs MegaDescriptor is unproven for pets.
  - DINOv2 (Apache 2.0), SigLIP 2 (Apache 2.0, unverified this session) and CLIP fine-tunes are the permissive fallbacks.
  - Recommended path: start with a permissive general backbone (SigLIP 2 or DINOv2/v3) zero-shot, collect confirmed matches from human-in-the-loop, then fine-tune an ArcFace head on your own SRD data. This is where the real accuracy gains are, as PetFace's ArcFace vs CLIP gap shows.
- **Cold start:**
  - Day 1 has no lost-pet gallery. Re-ID value first comes from linking sightings to sightings ("is this the same caramelo seen yesterday 300 m away?") to build chains.
  - Owner-uploaded lost-pet photos come next. Ask owners for 3–5 photos (side, front, face close-up).
  - Collect human-confirmed pairs from day 1, since they are the training set.
- **Nose-print biometrics** are irrelevant for street photos of strays because they need a cooperative close-up. They are possibly useful only for the owner-side registration of known pets, and that is a separate product.
- **Compute:**
  - Embedding a 384 px crop with a ViT-B/L on CPU is roughly 0.1–1 s; a GPU is about 10–50× faster in batch. This is an inference with no sourced figure.
  - At thousands of photos/day, CPU workers suffice. Rent a GPU only for fine-tuning and bulk re-embedding.

### Gaps
- No public benchmark of re-ID on street or in-the-wild photos of mixed-breed dogs or cats; DogFaceNet numbers were not retrieved.
- PetFace dataset license (commercial use?) was not confirmed. Do not train commercial models on it without checking.
- No head-to-head DINOv3 vs MegaDescriptor vs SigLIP 2 numbers on pets were retrieved.
- Finding Rover accuracy claims were not researched.
- No sourced CPU/GPU latency or cost figures for embedding models.

## 4. WhatsApp Business Platform (as of Oct 2026): API options, pricing, windows, AI-chatbot policy, Brazil specifics, BSPs, unofficial libraries

### Takeaway
Use the official Cloud API; On-Premises is dead since 23 Oct 2025.

Pricing is per delivered template message, and user-to-business messages are free. Since **1 Oct 2026**, two things changed:
- Service replies beyond 1,000/month per number are charged.
- Utility templates inside the 24 h window are charged.

Brazil utility/authentication is $0.0068 per message. Marketing is about $0.0625 per message (secondary sources).

Meta's "AI Providers" clause (§4.7) bans general-purpose AI assistants where AI is the *primary* functionality, as decided at Meta's sole discretion. A task-specific animal-report intake bot is a business using AI incidentally and is outside the ban by the clause's own test. In Brazil, CADE suspended the restriction anyway, and Meta now allows AI providers on +55 at published rates. Unofficial libraries (Baileys/Evolution/WPPConnect) violate WhatsApp's ToS and risk bans. Use them for prototypes only.

### Cited Findings
- **On-Premises API sunset:** The final client expired 23 Oct 2025, and On-Prem "can't be used to send messages anymore". Cloud API offers up to 1,000 msgs/s (4× On-Prem) and optional local data storage at rest. — [Meta: On-Premises API sunset](https://developers.facebook.com/docs/whatsapp/on-premises/sunset); [360dialog update](https://wa.360dialog.com/partner-updates/january-whatsapp-business-platform-updates)
- **Pricing model (Meta pricing docs):**
  - Per-message pricing since 1 Jul 2025, charged per delivered template. "Meta does not charge for messages from users to businesses."
  - Rates depend on category (marketing, utility, authentication) and the recipient's country code.
  - Service (non-template) messages: the first 1,000 per business phone number per month are free, with no rollover. From the 1,001st they are charged, effective 1 Oct 2026.
  - Utility templates inside an open service window were free from 1 Jul 2025 and are charged from 1 Oct 2026.
  - Accounts without a payment method by 30 Sep 2026 stop delivering service messages once charging begins.
  - The webhook pricing `type` changes from `free_customer_service` to `regular`.
  - Volume tiers apply only to utility and authentication. They are per market and category, aggregated across the business portfolio, and reset monthly.
  - Sources: [Meta pricing docs](https://developers.facebook.com/docs/whatsapp/pricing); [pricing.md](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing.md)
- **Customer service window:** A 24 h window opens when the user messages or calls and resets with each new user message. Free-form messages are allowed only while it is open; outside it, templates only. Click-to-WhatsApp ad entry points open a *free entry point window* of up to 7 days. — [Meta pricing docs](https://developers.facebook.com/docs/whatsapp/pricing)
- **Brazil rates:**
  - Meta's own doc states the current Brazil utility and authentication rate is **0.68¢ ($0.0068) per message**.
  - Brazil marketing is reported at about **$0.0625 per message** by third-party guides.
  - Older third-party figures conflict: $0.008 utility, $0.0315 auth, R$0.31–0.38 marketing.
  - Brazil's service-message rate after the free 1,000 is published only in the CSV/PDF rate cards and was not retrieved.
  - Sources: [Meta pricing.md](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing.md); [MessageCentral Brazil guide](https://www.messagecentral.com/blog/whatsapp-business-api-pricing-in-brazil); [go4whatsup Brazil 2026](https://www.go4whatsup.com/brazil/whatsapp-business-api-pricing/)
- **BRL billing:** Available for new Brazil accounts from 1 Jul 2026 (all eligible customers by 16 Jul 2026), for Solution Providers and direct integrators with a Brazil Sold-To. Existing accounts must migrate to BRL by **30 Jun 2027**. — [Meta pricing.md](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing.md)
- **Meta Business Agent:** Meta's own AI agent product is priced at $2.00 per 1M tokens, "roughly 4–5 cents per message". — [Meta pricing docs](https://developers.facebook.com/docs/whatsapp/pricing)
- **AI Providers clause (§4.7 "Provedores de IA", Meta Terms for WhatsApp Business Platform, PT-BR page last updated 23 Sep 2026):**
  - Covers AI/ML technology suppliers and developers, including LLMs, generative AI platforms and "assistentes de inteligência artificial de uso geral".
  - They are "estritamente proibidos de acessar ou usar a Plataforma do WhatsApp Business, direta ou indiretamente" when the AI is "a funcionalidade principal (em vez de incidental ou auxiliar)". Meta decides at its sole discretion.
  - There is a country exception list.
  - Data clause: if you keep an AI Provider as your Solution Provider, Platform data (including anonymized, aggregated or derived forms) may not be used to create, develop, train or improve AI models. You *may* fine-tune a model for your exclusive use.
  - Source: [Meta Terms for WhatsApp Business Platform](https://www.facebook.com/legal/Meta-Terms-for-WhatsApp-Business-Platform)
- **Timeline:**
  - Terms changed Oct 2025, enforced for new users from 15 Oct 2025 and for existing users from **15 Jan 2026**.
  - OpenAI (ChatGPT), Perplexity and Microsoft shut down their WhatsApp bots.
  - Sources: [TechCrunch 18 Oct 2025](https://techcrunch.com/2025/10/18/whatssapp-changes-its-terms-to-bar-general-purpose-chatbots-from-its-platform/); [windowsforum](https://windowsforum.com/windows-news.4/whatsapp-business-api-bans-third-party-ai-providers-by-jan-15-2026.391662/)
- **What remains allowed:**
  - Vendor interpretations list support bots for a specific business, order tracking, booking and FAQ bots with a defined knowledge base as allowed. Open-ended "answer anything" frontier-model wrappers are prohibited. — [monochat blog (vendor)](https://monochat.ai/blog/whatsapp-ai-chatbot-policy-2026)
  - Meta's AI Providers pricing page says the policy does not change how Meta charges "all other businesses using the WhatsApp Business Platform".
- **AI-provider exceptions by country (Meta docs):**
  - Italy (+39) from 16 Feb 2026, charged until 12 May 2026 then free.
  - **Brazil (+55) from 11 Mar 2026, "charged at the published rates"**, per the AI Provider rate CSV updated 15 Oct 2026.
  - EU/EEA countries from 11 Mar 2026, free from 13 May 2026.
  - Türkiye from 15 Oct 2026.
  - The analytics API adds an `AI_BOT` pricing category.
  - Sources: [Meta: AI Providers pricing](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing/ai-providers/); [TechCrunch Italy](https://techcrunch.com/2026/01/28/whatsapp-will-now-charge-ai-chatbots-to-operate-in-italy/); [TechCrunch Europe](https://techcrunch.com/2026/03/05/meta-will-allow-rival-ai-chatbots-on-whatsapp-in-europe-but-for-a-fee/)
  - Secondary coverage reports $0.0625 per AI-provider non-template message in Brazil. — [mezha.net](https://mezha.net/eng/bukvy/cade_rules_against/)
- **CADE (Brazil antitrust):**
  - The Superintendência-Geral imposed a *medida preventiva* in Jan 2026 and opened an inquiry into abuse of dominance favoring Meta AI.
  - A federal court in DF briefly suspended the measure.
  - On 4 Mar 2026 the CADE Tribunal unanimously upheld it, suspending the new terms until the inquiry ends.
  - A daily fine of R$250k applied from 17 Mar 2026 for non-compliance. On 23 Apr 2026 CADE maintained the fine until Meta proves reopened access without extra charges.
  - The inquiry is ongoing. No later status was found.
  - Sources: [Mercado&Consumo](https://mercadoeconsumo.com.br/04/03/2026/noticias/cade-mantem-medida-preventiva-que-obriga-meta-a-permitir-chatbots-de-ia-no-whatsapp/); [MacMagazine](https://macmagazine.com.br/post/2026/03/04/tribunal-do-cade-mantem-liminar-contra-termos-de-ia-do-whatsapp-no-brasil/); [Convergência Digital](https://convergenciadigital.com.br/mercado/cade-sustenta-multa-ao-whatsapp-por-manter-restricao-de-uso-a-ia-generativa-na-plataforma/); [TecMundo](https://www.tecmundo.com.br/mercado/412590-whatsapp-continua-sujeito-a-multa-de-r-250-mil-por-descumprir-medida-do-cade.htm)
- **Unofficial libraries:**
  - Baileys (used by Evolution API) emulates WhatsApp Web and breaks WhatsApp's terms. Meta's anti-fraud systems can ban the number, appeals are opaque and reversals rare, and numbers get "flagged in weeks to months".
  - Risk is described as lower for purely reactive messaging and higher for proactive or bulk messaging.
  - All sources are vendor blogs and no primary Meta enforcement statistics were found. — [pasqualepillitteri.it](https://pasqualepillitteri.it/en/news/12969/integrate-whatsapp-evolution-api-vs-cloud-api); [ChatDaddy](https://help.chatdaddy.tech/article/ban-type-distribution); [Zylos](https://zylos.ai/research/2026-01-26-whatsapp-api-automation); [bot.space](https://www.bot.space/blog/whatsapp-api-vs-unofficial-tools-a-complete-risk-reward-analysis-for-2025)

### Inferences
- **Policy classification:** an intake bot that only collects animal-emergency and sighting reports, asks for missing fields, and links to the case on the map has AI as an *ancillary* means to a specific service. It is not a "general-purpose AI assistant". To stay clearly on that side:
  - Constrain scope: refuse off-topic questions with a fixed message.
  - Never expose a free chat with the LLM.
  - Document the bot's purpose in the WABA profile.

  Meta's "sole discretion" language is the residual risk. In Brazil, the CADE measure plus Meta's +55 AI-provider exception reduce it further.
- **Data-use constraint (important for re-ID training):** §4.7 restricts using Platform data to train or improve AI models in the AI-Provider-as-Solution-Provider case, while allowing exclusive-use fine-tuning. Photos received via WhatsApp feeding a self-trained re-ID model could plausibly fall in scope. Get legal review, and prefer LLM vendors with no-training/zero-retention terms for WhatsApp traffic.
- **Message cost model:**
  - Intake is user-initiated, so it happens inside the 24 h window and the bot's replies are *service* messages. The first 1,000/month per number are free; beyond that, the Brazil service rate applies (not retrieved).
  - Follow-ups after 24 h (e.g., "alguém respondeu ao seu alerta", "o caso foi resolvido") need **utility** templates at $0.0068 each.
  - Never use **marketing** templates (about $0.0625) for case updates. Misclassified templates get re-categorized by Meta.
- **Media and location handling (Cloud API webhooks, unverified this session):**
  - Inbound image, audio (voice notes are OGG/Opus), document and location messages arrive as webhooks.
  - Media carry a media ID that must be exchanged for a short-lived download URL with the access token. Download immediately in a worker.
  - Location messages carry latitude/longitude and optional name/address. This is the best geodata the platform will get, so ask for "📎 → Localização" early.
- **BSP vs direct Cloud API:**
  - Direct Cloud API means no markup and full control, but you handle business verification, display-name approval, template approval and webhooks yourself. It is feasible with FastAPI.
  - BSPs active in Brazil (Twilio, 360dialog, Gupshup, Zenvia, Blip/Take) add markup or platform fees plus inbox, flow-builder and support.
  - For a civic platform with in-house engineering, direct Cloud API (or a no-markup BSP) is cheapest. Meta Tech Provider status matters only if onboarding other organizations' numbers (e.g., partner ONGs).

### Gaps
- Brazil's exact service-message rate (post-1 Oct 2026), the Brazil marketing rate from Meta's own rate card, and BRL-denominated rates were not retrieved. The CSV/PDF rate cards were not accessible via fetch.
- BSP-specific Brazil pricing and markups (Twilio, 360dialog, Zenvia, Blip, Gupshup) were not retrieved. A third-party figure of 15–35% typical BSP markup appeared in search summaries without a clearly attributable source.
- Current status of the CADE inquiry after Apr 2026 is unknown.
- The country-exception list linked from §4.7 was not opened directly.
- Template approval SLAs and business verification requirements for nonprofits or civic entities in Brazil were not researched.

## 5. LLM structuring of PT-BR informal messages: extraction, spelling, relative time, geocoding, slot-filling, model choice, cost, guardrails, evaluation

### Takeaway
This is a single-call extraction task per turn: a schema-constrained JSON output, followed by deterministic code that decides which critical slot to ask for next. A small model is sufficient. Claude Haiku 5.5 is $0.10/$0.50 per MTok, GPT-5-nano is $0.05/$0.40, and Gemini 2.5 Flash-Lite is $0.10/$0.40. A whole multi-turn report costs roughly $0.001–0.003 in LLM tokens on these models, versus about $0.02–0.05 on Sonnet-class models.

Relative-time resolution and geocoding should be done in code, not by the LLM. The LLM should normalize phrases such as "ontem à tarde" into a structured relative expression. Prompt injection risk is bounded by never giving the model tools with side effects and by treating its output as untrusted data.

### Cited Findings
- **Anthropic pricing (per 1M tokens, Anthropic API reference cached 2026-10-06):**

  | Model | ID | Input | Output | Notes |
  |---|---|---|---|---|
  | Haiku 5.5 | `claude-haiku-5-5` | $0.10 | $0.50 | Prompts ≤100K; $0.50/$2.50 beyond |
  | Sonnet 5.5 | `claude-sonnet-5-5` | $2 | $10 | Cache reads $0.20 |
  | Opus 5.5 | `claude-opus-5-5` | $4 | $20 | Cache reads $0.20 |
  | Haiku 4.5 | — | $1 | $5 | Previous generation |

  — [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- **Anthropic structured outputs and tool use:**
  - Structured outputs via `output_config.format` constrain responses to a JSON schema.
  - Strict tool use (`strict: true`) guarantees schema-valid tool inputs.
  - Forced `tool_choice` (`any`/`tool`) returns 400 on Opus 5.5, Sonnet 5.5 and Fable 5.1; use structured outputs instead.
  - Haiku 5.5 runs adaptive thinking by default with effort default `medium`, billed as output tokens. Set effort `low` for extraction.
  - Mid-conversation `system` messages provide an operator channel separate from user content.
  - Source: [Anthropic structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs); [prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- **OpenAI pricing (per 1M tokens, standard):**

  | Model | Input | Output | Cached input |
  |---|---|---|---|
  | gpt-5-nano | $0.05 | $0.40 | $0.005 |
  | gpt-5-mini | $0.25 | $2.00 | — |
  | gpt-5.4-nano | $0.20 | $1.25 | — |
  | gpt-5.4-mini | $0.75 | $4.50 | — |
  | gpt-6-luna | $0.10 | $0.50 | — |

  Batch is about 50% off. — [OpenAI API pricing](https://developers.openai.com/api/docs/pricing)
- **Google Gemini pricing (per 1M tokens, paid tier):**

  | Model | Input | Audio input | Output | Notes |
  |---|---|---|---|---|
  | gemini-2.5-flash-lite | $0.10 | $0.30 | $0.40 | |
  | gemini-3.1-flash-lite | $0.25 | $0.50 | $1.50 | |
  | gemini-3.5-flash-lite | $0.30 | $0.30 | $2.50 | |
  | gemini-3.6/3.8-flash | $0.75 | — | $3.75 | Through 31 Dec 2026, doubling 1 Jan 2027 |

  All have a free tier. — [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing)
- **Geocoding costs (Google Maps Platform):**
  - Since 1 Mar 2025 the $200 monthly credit is replaced by per-SKU free caps. Geocoding gets 10,000 free requests/month.
  - Google's example: 2M monthly geocodes went from $7,900 to $5,050.
  - Third-party guides list Geocoding at $5.00 per 1,000 for the first 100k after the free cap, and free caps of 10k for Essentials, 5k for Pro and 1k for Enterprise SKUs.
  - Sources: [Google: March 2025 changes](https://developers.google.com/maps/billing-and-pricing/march-2025); [Google pricing overview](https://developers.google.com/maps/billing/overview/); [Woosmap 2026 breakdown](https://www.woosmap.com/blog/google-maps-api-pricing-breakdown)

### Inferences
- **Schema** (one `Report` object, every field nullable plus a `confidence` and `source_span`):
  - `kind` (emergency | sighting | lost | found)
  - `species` (cachorro | gato | outro)
  - `count`
  - `coat_colors[]` (enum of PT-BR folk colors)
  - `size` (pequeno | médio | grande)
  - `age_class` (filhote | adulto | idoso)
  - `sex`
  - `collar`
  - `condition` (enum: ferido, atropelado, magro/desnutrido, sarna, bicheira, prenhe, filhotes, agressivo, preso/amarrado, morto, saudável)
  - `urgency` (0–3)
  - `location_text`
  - `location_landmarks[]`
  - `neighborhood`, `city`
  - `time_expression_raw` and `time_expression` (structured: `{anchor: now|today|yesterday|weekday, part_of_day: manhã|tarde|noite|madrugada, offset_minutes}`)
  - `contact_ok`
  - `notes_normalized`, the spelling-corrected summary in standard PT-BR
- **Relative time:** the LLM outputs only the structured expression. Python then resolves it against the WhatsApp message timestamp in America/Sao_Paulo into an interval:
  - "agora há pouco" becomes [-30 min, now].
  - "ontem à tarde" becomes yesterday 12:00–18:00.

  Storing intervals, not points, is what makes chain linking by time robust.
- **Geocoding Brazilian free text** ("perto da padaria da praça", "em frente ao posto Ipiranga da av. Brasil"):
  1. Prefer the WhatsApp location pin.
  2. Otherwise geocode `location_text + neighborhood + city`, biased to the user's last known area. Use Google Geocoding/Places Text Search; Nominatim/OSM is weaker on Brazilian landmarks and POIs.
  3. Show the result on a map link or echo "Rua X, Bairro Y — confere?" and require confirmation before publishing.
  4. Never publish an unconfirmed LLM-guessed coordinate.
- **Slot-filling dialogue:**
  - Code computes `missing_critical = {species, location, kind, (condition if emergency)}`.
  - Ask for at most one or two fields per turn, using pre-written PT-BR question templates. The LLM may paraphrase but not invent questions.
  - Stop asking after 2 failed attempts and file the report as incomplete.
  - Detect inconsistencies in code too, e.g., "gato" in text while the photo detector says dog. Ask "Na foto parece um cachorro — é isso mesmo?"
  - This keeps behavior deterministic and testable. The LLM is a parser, not the dialogue manager.
- **Cost per report (assumptions: 4 bot turns, each with a 2,000-token cached system prompt and schema, about 800 fresh tokens and about 400 output tokens including low-effort thinking, plus 2 photos at about 1,600 tokens each):**
  - Haiku 5.5: about $0.0016 for text turns plus about $0.0003 for images, so **about $0.002/report, or about $2 per 1,000 reports**.
  - gpt-5-nano and Gemini 2.5 Flash-Lite: similar or lower.
  - Sonnet 5.5: about **$35–45 per 1,000**.
  - Opus 5.5: about **$70–90 per 1,000**.
  - Recommendation: a small model by default, escalating to Sonnet-class only when schema validation fails twice or confidence is low (expected below 5% of turns).
- **Self-hosted open-weight models** (e.g., Qwen-family 7–14B on a GPU) are only cost-competitive at very high sustained volume. API prices of $0.05–0.10/M input are below what a dedicated GPU costs at civic-platform volumes. Self-host only for sovereignty or privacy requirements.
- **Guardrails and prompt injection:**
  - User text and transcripts go in a clearly delimited data field.
  - The model has no tools with side effects. Output is schema-validated (Pydantic) and every field is enum or length-bounded.
  - Free-text fields are never rendered as HTML or used in instructions to other models without escaping.
  - Rate-limit per WhatsApp number.
  - Moderation for abuse or doxxing, e.g., people's addresses or names in `notes`: strip CPF and phone-number patterns from public fields.
  - The main failure mode is an injected message making the bot reply off-scope. With template-only questions plus a scope classifier, the worst case is a malformed report, not a harmful reply.
- **Evaluation:**
  - Build a gold set of about 300–500 real anonymized messages: misspellings, gírias, regional terms, audio transcripts, multi-animal and multi-message reports.
  - Field-level precision and recall per slot, plus exact-match on `species`, `kind` and `urgency`.
  - Time-interval IoU against human labels.
  - Geocode error in meters.
  - "Questions asked per completed report" as the UX metric.
  - Re-run on every prompt or model change. Track cost per completed report, not per call.

### Gaps
- No PT-BR-specific benchmark comparing small models (Haiku 5.5, gpt-5-nano, Gemini Flash-Lite, Qwen) on informal extraction was found. This must be measured locally.
- Haiku 5.5's cache-read price and minimum cacheable prefix were not retrieved.
- Google Places Text Search per-1,000 price was not confirmed from Google directly.
- Nominatim usage policy limits were not re-verified.

## 6. Voice notes (PT-BR speech-to-text)

### Takeaway
Use an API at MVP:
- gpt-4o-mini-transcribe at $0.003/min, gpt-transcribe at $0.0045/min, or gpt-4o-transcribe at $0.006/min.
- Alternatively, send the audio directly to a multimodal LLM so transcription and extraction happen in one call: Gemini 2.5 Flash-Lite audio input is $0.30/M tokens.

Self-host faster-whisper (MIT) on CPU once volume justifies it. Expect clean-speech WER around 4–6%. Noisy, spontaneous street voice notes are realistically 15–25%+ WER, so the extraction step must tolerate transcription errors and confirm critical fields.

### Cited Findings
- **OpenAI transcription pricing:**

  | Model | Price | Notes |
  |---|---|---|
  | gpt-4o-transcribe | $0.006/min | $2.50/$10 per 1M tokens |
  | gpt-4o-mini-transcribe | $0.003/min | |
  | gpt-transcribe | $0.0045/min | |
  | gpt-4o-transcribe-diarize | $0.006/min | |
  | Whisper | $0.006/min | |
  | gpt-live-transcribe | $0.017/min | Live |

  — [OpenAI API pricing](https://developers.openai.com/api/docs/pricing)
- **faster-whisper (MIT, CTranslate2):**
  - CPU benchmark on 13 min of audio with the `small` model, i7-12700K, 8 threads: int8 took 1m42s (about 7.6× real-time), int8 batch=8 took 51s. openai/whisper fp32 took 6m58s.
  - GPU benchmark with large-v2 on an RTX 3070 Ti: int8 batch=8 took 16s for 13 min.
  - Supports large-v3, turbo and distil-large-v3, and converted fine-tunes.
  - Source: [faster-whisper README](https://github.com/SYSTRAN/faster-whisper)
- **Whisper on Portuguese:**
  - FLEURS (read speech, general Portuguese): large-v3 about 3.9% WER, large-v3-turbo about 4.2%. — [Handy model leaderboard (secondary)](https://models.handy.computer/languages/pt)
  - A vendor guide cites about 5–6% WER for Whisper large-v3 on clean Brazilian Portuguese and says Deepgram Nova-3 is less tested in PT. — [VexaScribe (vendor)](https://vexascribe.com/pt/blog/comparacao-precisao-transcricao)
- **Spontaneous Brazilian Portuguese is much harder:**
  - Whisper large-v2 got 14.50% WER on about 17 h of spontaneous life-history interviews, as cited in a BRACIS 2024 paper.
  - On the NURC-SP corpus (about 239 h of São Paulo-accented spontaneous speech), the best result was Distil-Whisper fine-tuned on NURC-SP at 24.22% WER, vs wav2vec2-XLSR-53 at 33.73%.
  - Source: [BRACIS 2024 NURC-SP](https://sol.sbc.org.br/index.php/bracis/article/view/33550)
- **CORAA v1** (290.77 h of BR-PT spontaneous and prepared speech): fine-tuned wav2vec2 XLSR-53 got 24.18% WER on the CORAA test set and 20.08% on Common Voice. A search summary of another version quoted 27.35% and 16.01%. — [arXiv 2110.15731](https://arxiv.org/abs/2110.15731)
- The CAMÕES benchmark found zero-shot ASR models perform better on Brazilian than European Portuguese. — [arXiv 2508.19721](https://arxiv.org/pdf/2508.19721)
- **Deepgram Nova-3 pricing (third-party, unconfirmed):**
  - About $0.0043/min pre-recorded.
  - Monolingual streaming about $0.0077/min, with a promotional $0.0048.
  - Multilingual streaming about $0.0092/min.
  - Keyterm prompting adds about $0.0013/min.
  - $200 free credit.
  - Sources: [convertaudiototext](https://convertaudiototext.com/blog/deepgram-nova-3-explained); [Soniox vs Deepgram](https://soniox.com/pricing/stt/soniox-vs-deepgram)

### Inferences
- **Typical voice note:** 15–60 s. At 30 s average:

  | Option | Cost per voice note | Per 1,000 reports |
  |---|---|---|
  | gpt-4o-mini-transcribe | $0.0015 | $1.50 |
  | gpt-4o-transcribe | $0.003 | $3.00 |
  | Gemini 2.5 Flash-Lite native audio | — | about $0.30 |

  The Gemini figure assumes about 32 audio tokens/s (unverified this session) and includes extraction in the same call.
- **Self-hosting:** at about 7–8× real-time per 8-thread CPU with `small` int8, a single 8-vCPU box transcribes about 1,000 thirty-second notes in about 1 hour of compute. That means CPU self-hosting of `small`/`medium` is viable; large-v3-turbo on CPU is slower, with no sourced figure.
  - API cost is low enough ($1.5–3 per 1,000 reports) that self-hosting is mainly a privacy or sovereignty decision, not a cost one, until well over 100k reports/month.
- **Accuracy mitigations:**
  - Pass a prompt or keyterms with domain vocabulary: caramelo, vira-lata, SRD, bicheira, sarna, atropelado, the city's neighborhood names, local street names.
  - Have the LLM extraction step flag low-confidence location tokens for confirmation.
  - Always echo back the parsed location.
- **Pipeline:**
  1. The webhook delivers an audio media ID.
  2. A worker downloads the OGG/Opus and transcodes if needed.
  3. STT produces the transcript.
  4. The transcript is stored, privately, with the original audio under short retention.
  5. The transcript feeds the same extraction prompt as text.

  Audio of people's voices is personal data under LGPD. Delete raw audio after transcription plus a short dispute window.

### Gaps
- No head-to-head PT-BR WER comparison of gpt-4o-transcribe, Deepgram Nova-3, Google Chirp and Whisper large-v3/turbo on noisy, spontaneous, WhatsApp-style audio was found. Run a local eval on about 200 real voice notes.
- Google Cloud Speech-to-Text (Chirp) PT-BR pricing and accuracy were not researched.
- Gemini audio tokens-per-second and current OpenAI model accuracy on Brazilian regional accents were not verified.

## 7. Recommendations: phased plan, self-host vs API, cost per 1,000 reports

### Takeaway
- **MVP:** web/PWA + Cloud API intake, a deterministic slot-filling loop around a small LLM, API STT, a pyvips derivative pipeline with EXIF evidence capture and stripping, EgoBlur blurring, and a VLM-based graphic flag.
- **v2:** a self-hosted detector plus a permissive embedding backbone in pgvector, with human-confirmed "possible match" suggestions filtered by species, geo and time.
- **v3:** a fine-tuned SRD re-ID model on confirmed pairs, self-hosted STT if needed, and owner-side registration photos.

WhatsApp utility/service messaging, not AI, will dominate variable cost per report.

### Cited Findings
- Brazil utility template rate is $0.0068 per message, and service replies are charged after 1,000/month per number from 1 Oct 2026. — [Meta pricing docs](https://developers.facebook.com/docs/whatsapp/pricing); [pricing.md](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing.md)
- Haiku 5.5 is $0.10/$0.50 per MTok. — [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- gpt-4o-mini-transcribe is $0.003/min. — [OpenAI pricing](https://developers.openai.com/api/docs/pricing)
- Rekognition moderation is about $0.001/image. — [AWS Rekognition pricing](https://aws.amazon.com/rekognition/pricing/)
- Google Geocoding has 10k free/month, then about $5/1,000 (third-party figure). — [Google March 2025](https://developers.google.com/maps/billing-and-pricing/march-2025); [Woosmap](https://www.woosmap.com/blog/google-maps-api-pricing-breakdown)
- libvips derivative generation costs about 0.7 s and about 100 MB for a 100 MP image. Phone photos at 12 MP are an order of magnitude cheaper. — [libvips benchmark](https://github.com/libvips/libvips/wiki/Speed-and-memory-use)

### Inferences
- **Phase 1 – MVP (0–3 months):**
  - Ingest: PWA upload with client-side resize to about 2048 px; Cloud API webhook for images, audio and location.
  - Image worker (pyvips + pillow-heif fallback):
    - EXIF evidence capture into a private table
    - auto-orient
    - WebP 1600/640 px + ThumbHash
    - strip metadata
    - PDQ hash for repost linking
    - Laplacian blur score
  - Privacy: EgoBlur faces + plates on public derivatives (CPU).
  - Graphic content: a field in the VLM attribute call, with default-blur on uncertainty.
  - LLM: Haiku 5.5 (or gpt-5-nano or Gemini 2.5 Flash-Lite) with a JSON schema and effort low. A deterministic slot-filler, a code-side time resolver, and geocode-with-confirmation.
  - STT: gpt-4o-mini-transcribe, or Gemini native audio.
  - WhatsApp: direct Cloud API, utility templates only for follow-ups, and a strict on-topic scope.
  - **API cost per 1,000 reports** (2 photos, 1 voice note of 30 s, 4 bot turns, 2 follow-up utility templates, ≤1 geocode):

    | Item | Cost |
    |---|---|
    | LLM | about $2 |
    | STT | about $1.5 |
    | Moderation API (optional) | about $2 |
    | Geocoding (beyond free tier) | ≤$5 |
    | WhatsApp utility follow-ups | about $13.6 |
    | WhatsApp service replies beyond 1,000/month | unknown Brazil rate × about 4/report |
    | **Total excluding service replies and infrastructure** | **about $15–25** |

    Infrastructure (Postgres, object storage, 2–4 vCPU workers) is a fixed cost.
- **Phase 2 – v2 matching (3–9 months):**
  - Self-hosted animal detection/cropping with RF-DETR (Apache) or MDv6-MIT/Apache on CPU (ONNX).
  - Embeddings from SigLIP 2, DINOv2 or DINOv3 (legal check), or MegaDescriptor only if the NC license is acceptable, on body and face crops.
  - pgvector `halfvec` with SQL pre-filtering on species, `ST_DWithin` and time window. Exact scan for filtered queries, HNSW + `iterative_scan` for global ones.
  - Attribute re-ranking.
  - Candidate UI: "Pode ser o mesmo animal?" with top 10–20 and one-tap confirm/reject. Log every decision as training data.
  - Owner-side lost-pet flow requesting 3–5 photos.
  - Incremental cost is CPU only, roughly $0 API cost per 1,000 reports. A GPU is optional for batch re-embeds.
  - **Success metric:** recall@10 among filtered candidates on a held-out set of human-confirmed pairs. Do not report top-1 publicly.
- **Phase 3 – v3 (9–18 months):**
  - Fine-tune an ArcFace/metric head on confirmed SRD pairs (thousands of pairs needed), with a periodic re-embed job and versioned vectors.
  - Distill attribute and graphic classifiers from logged VLM outputs to cut per-image API calls.
  - Self-host faster-whisper if volume exceeds about 100k voice notes/month or privacy policy requires it.
  - Consider the Meta Business Agent or AI-provider pricing only if scope broadens.
  - Clear the §4.7 data-use clause with counsel before training on WhatsApp-sourced media.
- **Self-host vs API rule of thumb:**
  - Self-host anything per-image that runs on every photo: resizing, blurring, detection, embeddings. These are cheap on CPU and avoid sending bystanders' faces to third parties.
  - Use APIs for language and speech until volume is very high: LLM extraction, STT, geocoding. They are cents per 1,000 operations and quality improves without maintenance.
- **Key invariants:**
  1. Public media is always derived and stripped, never the original.
  2. Embeddings are comparable only within one model version.
  3. Coordinates published on the map are user-confirmed or come from a device pin.
  4. A match is never asserted without human confirmation.
- **Main failure modes:**
  - GPS leak of reporters' homes.
  - False "it's your dog!" notifications eroding trust.
  - WhatsApp number ban from unofficial libraries.
  - A WhatsApp bill surprise from service-message charging since Oct 2026.

### Gaps
- Infrastructure cost (managed Postgres with PostGIS/pgvector, object storage, CDN egress) was not researched here.
- No sourced CPU throughput numbers for detector and embedding models; the cost and latency of v2 workers are estimates.
- Brazil service-message rate missing (see Q4), which is the largest unknown in per-report cost.
