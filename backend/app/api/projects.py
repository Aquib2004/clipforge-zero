"""Project CRUD API."""

import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.paths import ensure_workspace, projects_dir
from app.core.security import safe_workspace_path
from app.models.project import Project, ProjectStatus
from app.schemas.project import (
    ProjectCreate,
    ProjectList,
    ProjectRead,
    ProjectUpdate,
)

router = APIRouter(tags=["projects"])


@router.get("/projects", response_model=list[ProjectList])
def list_projects(db: Session = Depends(get_db)):
    return (
        db.query(Project)
        .filter(Project.status != ProjectStatus.DELETED)
        .order_by(Project.created_at.desc())
        .all()
    )


@router.post("/projects", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)):
    project_id = str(uuid.uuid4())
    project = Project(
        id=project_id,
        name=payload.name,
        source_title=payload.source_title,
        source_creator=payload.source_creator,
        source_url=payload.source_url,
        language=payload.language,
        output_location=payload.output_location,
    )
    db.add(project)
    db.commit()
    db.refresh(project)

    # Create the project's workspace directory
    try:
        ensure_workspace()
        safe_workspace_path(projects_dir(), project_id).mkdir(parents=True, exist_ok=True)
    except Exception as exc:  # noqa: S110
        # Directory creation failure must not block project creation
        import logging

        logging.getLogger(__name__).warning(
            "Failed to create project directory for %s: %s", project_id, exc
        )

    return project


@router.get("/projects/{project_id}", response_model=ProjectRead)
def get_project(project_id: str, db: Session = Depends(get_db)):
    project = (
        db.query(Project)
        .filter(Project.id == project_id, Project.status != ProjectStatus.DELETED)
        .first()
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.patch("/projects/{project_id}", response_model=ProjectRead)
def update_project(project_id: str, payload: ProjectUpdate, db: Session = Depends(get_db)):
    project = (
        db.query(Project)
        .filter(Project.id == project_id, Project.status != ProjectStatus.DELETED)
        .first()
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(project, field, value)
    project.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(project)
    return project


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: str, db: Session = Depends(get_db)):
    project = (
        db.query(Project)
        .filter(Project.id == project_id, Project.status != ProjectStatus.DELETED)
        .first()
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    project.status = ProjectStatus.DELETED
    project.updated_at = datetime.utcnow()
    db.commit()
    return None
