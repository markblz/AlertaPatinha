from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute

from api import errors
from api.config import get_settings
from api.identity import router as identity
from api.observations import router as observations
from api.routers import health


def _operation_id(route: APIRoute) -> str:
    # Stable, readable ids: the generated TypeScript client (web today, native
    # app later) names its functions after these.
    return f"{route.tags[0]}_{route.name}" if route.tags else route.name


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="Alerta Patinha API",
        version="0.1.0",
        generate_unique_id_function=_operation_id,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    errors.install(app)
    app.include_router(health.router)
    app.include_router(identity.router)
    app.include_router(observations.router)
    return app


app = create_app()
