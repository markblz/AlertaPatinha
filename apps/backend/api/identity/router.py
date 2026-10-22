from typing import Literal

from fastapi import APIRouter, Response
from pydantic import BaseModel

from api.deps import AppSettings, CurrentPrincipal, DbSession, OptionalPrincipal
from api.errors import responses
from src.identity.public import start_anonymous_session

router = APIRouter(prefix="/api/v1/sessions", tags=["sessions"])


class StartSessionIn(BaseModel):
    # "token": native apps keep it in secure storage and send it as Bearer.
    # "cookie" (default): browsers never see the token from JS.
    delivery: Literal["cookie", "token"] = "cookie"


class SessionOut(BaseModel):
    tier: int
    token: str | None = None


@router.post("/anonymous", response_model=SessionOut, status_code=201)
async def start_anonymous(
    response: Response,
    db: DbSession,
    settings: AppSettings,
    principal: OptionalPrincipal,
    body: StartSessionIn | None = None,
) -> SessionOut:
    if principal is not None:
        response.status_code = 200
        return SessionOut(tier=principal.tier)

    issued = await start_anonymous_session(db)
    await db.commit()
    if body is not None and body.delivery == "token":
        return SessionOut(tier=issued.principal.tier, token=issued.token)
    response.set_cookie(
        settings.session_cookie_name,
        issued.token,
        max_age=settings.session_cookie_max_age_days * 86400,
        httponly=True,
        secure=settings.secure_cookies,
        samesite="lax",
        path="/",
    )
    return SessionOut(tier=issued.principal.tier)


@router.get("/me", response_model=SessionOut, responses=responses(401))
async def me(principal: CurrentPrincipal) -> SessionOut:
    return SessionOut(tier=principal.tier)
