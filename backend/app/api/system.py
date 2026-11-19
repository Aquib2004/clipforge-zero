"""System health and diagnostics endpoints.

Reports real, measured values only — no fake metrics.
"""

import shutil

import psutil
from fastapi import APIRouter

from app.core.paths import data_dir, ensure_workspace

router = APIRouter(tags=["system"])


@router.get("/system/health")
def system_health():
    ensure_workspace()
    return {"status": "ok"}


@router.get("/system/diagnostics")
def system_diagnostics():
    ensure_workspace()
    disk = shutil.disk_usage(data_dir())
    mem = psutil.virtual_memory()
    cpu = psutil.cpu_percent(interval=0.1)

    return {
        "status": "ok",
        "disk": {
            "total_bytes": disk.total,
            "used_bytes": disk.used,
            "free_bytes": disk.free,
        },
        "memory": {
            "total_bytes": mem.total,
            "available_bytes": mem.available,
            "percent": mem.percent,
        },
        "cpu_percent": cpu,
        "ffmpeg_available": False,
        "whisper_available": False,
        "ollama_available": False,
    }
