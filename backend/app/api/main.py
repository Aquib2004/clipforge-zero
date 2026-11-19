"""Top-level API router. Sub-routers are registered here."""

from fastapi import APIRouter

api_router = APIRouter()


def include_routers() -> None:
    from app.api import health, projects, system

    api_router.include_router(health.router, prefix="/api")
    api_router.include_router(system.router, prefix="/api")
    api_router.include_router(projects.router, prefix="/api")
