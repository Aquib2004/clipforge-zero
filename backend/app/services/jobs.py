"""Job service helpers."""

from app.models.job import Job, JobStatus, JobType


def create_job(db, job_id: str, project_id: str | None, type: JobType) -> Job:
    job = Job(id=job_id, project_id=project_id, type=type, status=JobStatus.QUEUED)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def update_job(db, job_id: str, **kwargs) -> Job | None:
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        return None
    for key, value in kwargs.items():
        setattr(job, key, value)
    db.commit()
    db.refresh(job)
    return job
