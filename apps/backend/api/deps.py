from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from api.config import Settings, get_settings
from api.db import get_session
from api.errors import api_error
from src.geo.public import Tier, Viewer
from src.identity.public import Principal, resolve_token

DbSession = Annotated[AsyncSession, Depends(get_session)]
AppSettings = Annotated[Settings, Depends(get_settings)]


def _token(request: Request, settings: Settings) -> str | None:
    # Native apps send a Bearer header; the web app rides an HttpOnly cookie.
    # Same token, same table: a future Capacitor/Expo shell needs no new auth.
    auth = request.headers.get("authorization", "")
    if auth.lower().startswith("bearer "):
        return auth[7:].strip() or None
    return request.cookies.get(settings.session_cookie_name)


async def get_principal(request: Request, db: DbSession, settings: AppSettings) -> Principal | None:
    token = _token(request, settings)
    return await resolve_token(db, token) if token else None


OptionalPrincipal = Annotated[Principal | None, Depends(get_principal)]


async def require_principal(principal: OptionalPrincipal) -> Principal:
    if principal is None:
        raise api_error(401, "session_required", "Start a session first.")
    return principal


CurrentPrincipal = Annotated[Principal, Depends(require_principal)]


def viewer_of(principal: Principal | None) -> Viewer:
    if principal is None:
        return Viewer.public()
    return Viewer(id=principal.actor_id, tier=Tier(principal.tier), is_staff=principal.is_staff)
