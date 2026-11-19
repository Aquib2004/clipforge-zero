"""In-process background job worker.

Polls the database for QUEUED jobs and runs them one at a time.
This is intentionally simple: no Redis, no Celery, no external queue.
"""

import threading
import time
from datetime import datetime

from app.api.deps import SessionLocal
from app.models.job import Job, JobStatus
from app.services.jobs import update_job

worker_instance = None


class JobWorker:
    def __init__(self) -> None:
        self._thread: threading.Thread | None = None
        self._stop = False

    def start(self) -> None:
        self._stop = False
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop = True

    def _loop(self) -> None:
        while not self._stop:
            db = SessionLocal()
            try:
                job = (
                    db.query(Job)
                    .filter(Job.status == JobStatus.QUEUED)
                    .order_by(Job.id.asc())
                    .first()
                )
                if job:
                    self._run_job(db, job)
            finally:
                db.close()
            time.sleep(1)

    def _run_job(self, db, job: Job) -> None:
        job.status = JobStatus.RUNNING
        job.start_time = datetime.utcnow()
        db.commit()
        try:
            # Phase 1: no pipeline stages yet. Job completes immediately
            # as a placeholder until Phase 2+ adds real work.
            update_job(
                db,
                job.id,
                status=JobStatus.COMPLETED,
                progress=100,
                end_time=datetime.utcnow(),
                current_stage="done",
            )
        except Exception as exc:  # noqa: BLE001
            update_job(
                db,
                job.id,
                status=JobStatus.FAILED,
                error=str(exc),
                end_time=datetime.utcnow(),
            )


def get_worker() -> JobWorker:
    global worker_instance
    if worker_instance is None:
        worker_instance = JobWorker()
    return worker_instance
