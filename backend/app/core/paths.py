"""Workspace path helpers.

All user data lives under `data/` (configurable via CLIPFORGE_DATA_DIR).
Subdirectories: projects, cache, temp, exports, logs.
"""

from pathlib import Path


def workspace_root() -> Path:
    """Return the project root (parent of the `backend` package)."""
    return Path(__file__).resolve().parents[2]


def data_dir() -> Path:
    from app.core.config import settings

    p = Path(settings.data_dir)
    if not p.is_absolute():
        p = workspace_root() / p
    return p


def projects_dir() -> Path:
    return data_dir() / "projects"


def cache_dir() -> Path:
    return data_dir() / "cache"


def temp_dir() -> Path:
    return data_dir() / "temp"


def exports_dir() -> Path:
    return data_dir() / "exports"


def logs_dir() -> Path:
    return data_dir() / "logs"


def ensure_workspace() -> None:
    """Create all workspace subdirectories if they do not exist."""
    for d in (
        data_dir(),
        projects_dir(),
        cache_dir(),
        temp_dir(),
        exports_dir(),
        logs_dir(),
    ):
        d.mkdir(parents=True, exist_ok=True)
