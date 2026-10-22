"""The database itself enforces CLAUDE.md rule 4 and the audit log's append-only rule."""

import uuid

import asyncpg
import pytest

from tests.integration.conftest import execute

INSERT_RELATO = """
INSERT INTO observations.observation (
  client_id, source, kind, species, valid_time, time_precision, publish_at,
  true_geom, loc_source, privacy_class, display_mode, display_cell, h3_r9, h3_r7
) VALUES (
  $1, 'web', 'sighting', 'dog', tstzrange(now() - interval '1 hour', now()), 'approx', now(),
  'SRID=4326;POINT(-46.6333 -23.5505)', 'gps', 'public_place', 'approximate',
  '89a8100c02fffff', '89a8100c02fffff', '87a8100c0ffffff'
)
"""


def test_a_relato_cannot_be_edited(clean_db: str) -> None:
    execute(clean_db, INSERT_RELATO, uuid.uuid4())

    with pytest.raises(asyncpg.RaiseError, match="immutable"):
        execute(clean_db, "UPDATE observations.observation SET species = 'cat'")


def test_a_relato_cannot_be_deleted(clean_db: str) -> None:
    execute(clean_db, INSERT_RELATO, uuid.uuid4())

    with pytest.raises(asyncpg.RaiseError, match="insert-only"):
        execute(clean_db, "DELETE FROM observations.observation")


def test_moderation_may_set_hidden_at(clean_db: str) -> None:
    execute(clean_db, INSERT_RELATO, uuid.uuid4())

    execute(clean_db, "UPDATE observations.observation SET hidden_at = now()")


def test_the_access_log_is_append_only(clean_db: str) -> None:
    execute(
        clean_db,
        "INSERT INTO geo.location_access_log (tier, observation_id, purpose) VALUES (0, $1, 't')",
        uuid.uuid4(),
    )

    with pytest.raises(asyncpg.RaiseError, match="append-only"):
        execute(clean_db, "UPDATE geo.location_access_log SET purpose = 'x'")
    with pytest.raises(asyncpg.RaiseError, match="append-only"):
        execute(clean_db, "DELETE FROM geo.location_access_log")
