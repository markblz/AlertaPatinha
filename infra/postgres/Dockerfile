# PostGIS 3.6 on PostgreSQL 18 + pgvector (re-ID embeddings) + h3-pg (grid
# indexing, display cells, alert fan-out). Extensions are CREATEd by the
# Alembic baseline, not here: this image only makes them installable.
#
# The upstream postgis image is amd64-only. ARM hosts (Graviton, OCI Ampere)
# need a different base: see docs/adr/0002-postgres-postgis-single-source-of-truth.md.
FROM postgis/postgis:18-3.6

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-18-pgvector \
        postgresql-18-h3 \
    && rm -rf /var/lib/apt/lists/*
