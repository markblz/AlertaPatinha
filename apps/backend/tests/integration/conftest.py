import asyncio
import os
from collections.abc import Iterator
from pathlib import Path

import asyncpg
import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient

from api.main import app
from tests.conftest import TEST_DB_NAME

_BACKEND_DIR = Path(__file__).resolve().parents[2]
OWNED_TABLES = (
    "observations.observation",
    "geo.location_access_log",
    "geo.private_zone",
    "identity.session",
    "identity.actor",
)


def _dsn(database: str) -> str:
    url = os.environ["DATABASE_URL"].replace("postgresql+asyncpg://", "postgresql://")
    return url.rsplit("/", 1)[0] + "/" + database


async def _ensure_database() -> None:
    admin = await asyncpg.connect(_dsn("postgres"))
    try:
        exists = await admin.fetchval("SELECT 1 FROM pg_database WHERE datname = $1", TEST_DB_NAME)
        if not exists:
            await admin.execute(f'CREATE DATABASE "{TEST_DB_NAME}"')
    finally:
        await admin.close()


@pytest.fixture(scope="session")
def database() -> str:
    try:
        asyncio.run(_ensure_database())
    except (OSError, asyncpg.PostgresError) as exc:
        pytest.skip(f"Postgres not reachable ({exc}); run `make up`")
    cfg = Config()  # no ini file: keeps alembic from reconfiguring pytest's logging
    cfg.set_main_option("script_location", str(_BACKEND_DIR / "alembic"))
    command.upgrade(cfg, "head")
    return _dsn(TEST_DB_NAME)


async def _truncate(dsn: str) -> None:
    conn = await asyncpg.connect(dsn)
    try:
        # TRUNCATE skips row-level triggers, so append-only tables can be reset.
        await conn.execute(f"TRUNCATE {', '.join(OWNED_TABLES)} RESTART IDENTITY CASCADE")
    finally:
        await conn.close()


@pytest.fixture(autouse=True)
def clean_db(database: str) -> str:
    asyncio.run(_truncate(database))
    return database


@pytest.fixture
def client() -> Iterator[TestClient]:
    with TestClient(app) as c:
        yield c


@pytest.fixture
def other_client() -> Iterator[TestClient]:
    """A second device: separate cookie jar."""
    with TestClient(app) as c:
        yield c


def fetchval(dsn: str, sql: str, *args: object) -> object:
    async def run() -> object:
        conn = await asyncpg.connect(dsn)
        try:
            return await conn.fetchval(sql, *args)
        finally:
            await conn.close()

    return asyncio.run(run())


def execute(dsn: str, sql: str, *args: object) -> None:
    async def run() -> None:
        conn = await asyncpg.connect(dsn)
        try:
            await conn.execute(sql, *args)
        finally:
            await conn.close()

    asyncio.run(run())
