# media — Fotos

**Milestone:** M1 · **Owns schema:** `media` · **May depend on:** nothing

## Responsibility
Presigned uploads, private quarantine of originals, processing job (decode, EXIF read+strip, variants, ThumbHash, PDQ), public variant URLs.

## Public surface (planned — `public.py`)
- `create_upload(viewer, content_type) -> PresignedUpload`
- `get_public_variants(photo_id) -> Variants`
- `private_evidence(photo_id) -> ExifEvidence  # GPS/time, never public`

## Invariant
Uploaded bytes are never served. Spec: docs/domain/photo-pipeline.md.

## Layout when code arrives
`public.py` → `service/` → `repository/` (ORM models, queries) → `domain/` (pure logic).
Add this module's schema to `alembic/env.py` OWNED_SCHEMAS (already listed) and a
layers contract in `.importlinter` with its first layer.
