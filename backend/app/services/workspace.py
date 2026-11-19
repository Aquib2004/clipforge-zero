"""Workspace operations."""

from pathlib import Path

from app.core.paths import ensure_workspace, projects_dir


def ensure_workspace_dirs() -> None:
    ensure_workspace()


def project_dir(project_id: str) -> Path:
    return projects_dir() / project_id
