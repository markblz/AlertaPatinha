"""One error envelope for every failure, documented in OpenAPI, so web and native
clients parse errors one way and map `code` to their own PT-BR copy."""

from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class ErrorBody(BaseModel):
    code: str
    message: str
    errors: list[dict[str, Any]] | None = None  # field-level details for validation_error


class ErrorOut(BaseModel):
    detail: ErrorBody


def api_error(status: int, code: str, message: str) -> HTTPException:
    return HTTPException(status_code=status, detail={"code": code, "message": message})


def responses(*statuses: int) -> dict[int | str, dict[str, Any]]:
    return {status: {"model": ErrorOut} for status in statuses}


async def _validation_error(request: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, RequestValidationError)
    body = ErrorBody(
        code="validation_error",
        message="Some fields are missing or invalid.",
        errors=jsonable_encoder(exc.errors(), exclude={"input", "ctx"}),
    )
    return JSONResponse(status_code=422, content={"detail": body.model_dump()})


def install(app: FastAPI) -> None:
    app.add_exception_handler(RequestValidationError, _validation_error)
