# ADR-0010 — The system suggests identity; humans confirm

**Status:** accepted · 2026-10-21

## Context
Even on clean frontal face crops, the best open re-ID gets dog top-1 ≈ 78%
and cat ≈ 54% (PetFace, ECCV 2024). No benchmark exists for street photos of
SRD (vira-lata) animals; the researchers' estimate is 20–50% top-1.
Commercial 98% claims are unaudited. Heuristic linking has the same weakness
at colonies of look-alike cats.

## Decision
- No code path confirms an elo or merges casos automatically.
- Suggestions carry `score_bits`, `method` and `evidence`; humans confirm (guardian, T3 on the caso, ≥2 independent T2+ voters with >2/3 agreement, or staff).
- Re-ID (M6): SQL filter by species/space/time first, then rank by embedding, show top 10–20 to a human.
- Model licenses: permissive only in production (MegaDescriptor CC-BY-NC → benchmarking only; Ultralytics AGPL → avoid; prefer RF-DETR/MegaDetector MIT/Apache variants).

## Consequences
Slower than automatic matching; dramatically fewer false "found your dog"
moments. Confirmed/rejected pairs become the Brazilian evaluation set.
