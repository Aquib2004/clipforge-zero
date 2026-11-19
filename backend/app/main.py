"""ClipForge Zero FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.main import api_router, include_routers
from app.core.logging import setup_logging
from app.core.paths import ensure_workspace
from app.db.session import init_db

# Configure logging, workspace, and database at import time
setup_logging()
ensure_workspace()
init_db()
include_routers()

app = FastAPI(title="ClipForge Zero", version="0.1.0")

# Strict CORS — only the local frontend dev server is allowed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/")
def root():
    return {"name": "ClipForge Zero", "version": "0.1.0", "status": "running"}
