from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from api.config import get_settings

_settings = get_settings()
# Tests drive the app from several event loops (one per TestClient); pooled
# asyncpg connections are bound to the loop that opened them.
engine = create_async_engine(
    _settings.database_url,
    pool_pre_ping=True,
    **({"poolclass": NullPool} if _settings.env == "test" else {}),
)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with SessionLocal() as session:
        yield session
