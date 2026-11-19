"""Model tests: Project, Job, ApplicationSettings."""

from app.models.job import JobStatus, JobType
from app.models.project import Project


def test_project_defaults():
    project = Project(id="p-1", name="Test", status="active", language="en")
    assert project.status == "active"
    assert project.language == "en"


def test_job_status_enum():
    assert JobStatus.QUEUED == "queued"
    assert JobStatus.COMPLETED == "completed"
    assert JobType.ANALYZE == "analyze"
