from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from api.db import get_session

router = APIRouter(prefix="/api/v1/health", tags=["health"])

# The domain cannot work without these: geometry, grid cells, embeddings.
REQUIRED_EXTENSIONS = ("postgis", "h3", "h3_postgis", "vector")


@router.get("")
async def live() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/ready")
async def ready(session: Annotated[AsyncSession, Depends(get_session)]) -> dict[str, object]:
    rows = (await session.execute(text("SELECT extname, extversion FROM pg_extension"))).all()
    installed = {name: version for name, version in rows}
    missing = [ext for ext in REQUIRED_EXTENSIONS if ext not in installed]
    if missing:
        raise HTTPException(status_code=503, detail={"missing_extensions": missing})
    return {"status": "ok", "extensions": {ext: installed[ext] for ext in REQUIRED_EXTENSIONS}}
