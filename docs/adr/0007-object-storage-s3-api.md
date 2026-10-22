# ADR-0007 — Object storage behind the S3 API; originals never served

**Status:** accepted · 2026-10-21

## Context
Photos are central (every relato). They carry EXIF GPS (personal data under
LGPD), bystanders' faces and plates, and sometimes graphic injuries. MinIO
Community Edition's repo was archived and stopped shipping binaries/images
in Oct 2025.

## Decision
- Code talks only to the **S3 API** (presigned PUT/GET).
- Dev: **SeaweedFS 4.48** (`infra/seaweedfs/s3.json` holds dev-only keys).
- Prod: open between **Cloudflare R2** (free egress, but no South America region → LGPD international transfer, needs ANPD SCCs) and an **in-country S3** (Magalu Cloud / AWS sa-east-1, egress ~US$0.15/GB). Likely split: quarantine/originals in Brazil, public stripped variants on R2/CDN. ⚖ lawyer + cost check before M1 deploy.
- Two buckets: `quarantine` (private, originals) and `public` (re-encoded, metadata-stripped variants only).

## Consequences
- Provider is swappable by config.
- Every public byte passed through the pipeline (`docs/domain/photo-pipeline.md`).

## Alternatives rejected
MinIO CE (archived), serving uploads directly (EXIF/faces leak), Garage
(fine, but needs layout bootstrap in dev; license not re-verified).
