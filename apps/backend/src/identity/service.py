from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.identity.domain.tokens import IssuedSession, Principal, hash_token, new_token
from src.identity.repository.models import ActorRow, SessionRow


async def start_anonymous_session(session: AsyncSession) -> IssuedSession:
    actor = ActorRow(tier=0)
    session.add(actor)
    await session.flush()
    token = new_token()
    session.add(SessionRow(actor_id=actor.id, token_hash=hash_token(token)))
    await session.flush()
    return IssuedSession(principal=Principal(actor_id=actor.id, tier=actor.tier), token=token)


async def resolve_token(session: AsyncSession, token: str) -> Principal | None:
    row = (
        await session.execute(
            select(ActorRow.id, ActorRow.tier)
            .join(SessionRow, SessionRow.actor_id == ActorRow.id)
            .where(SessionRow.token_hash == hash_token(token), SessionRow.revoked_at.is_(None))
        )
    ).first()
    return Principal(actor_id=row.id, tier=row.tier) if row else None
