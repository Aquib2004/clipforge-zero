"""Project repository."""

from app.models.project import Project, ProjectStatus


class ProjectRepository:
    def __init__(self, db):
        self.db = db

    def list(self):
        return (
            self.db.query(Project)
            .filter(Project.status != ProjectStatus.DELETED)
            .order_by(Project.created_at.desc())
            .all()
        )

    def get(self, project_id: str):
        return self.db.query(Project).filter(Project.id == project_id).first()

    def create(self, **kwargs) -> Project:
        project = Project(**kwargs)
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def soft_delete(self, project_id: str) -> bool:
        project = self.get(project_id)
        if not project:
            return False
        project.status = ProjectStatus.DELETED
        self.db.commit()
        return True
