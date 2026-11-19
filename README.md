# ClipForge Zero

Open-source, local-first AI video intelligence and short-form content studio.

Transform long-form videos into intelligently selected, contextually complete, professionally edited short videos for YouTube Shorts, Instagram Reels, and similar platforms — without expensive SaaS subscriptions or mandatory paid AI services.

## Current status: Phase 1 — Foundation

| Feature | Status | Evidence |
|---|---|---|
| Repository structure | Implemented | This repo |
| Backend initialization (FastAPI) | Implemented | `backend/app/main.py` |
| Frontend initialization (Vite + React) | Implemented | `frontend/` |
| Configuration (Pydantic Settings) | Implemented | `backend/app/core/config.py` |
| Database (SQLAlchemy + SQLite + Alembic) | Implemented | `backend/app/db/`, `alembic/` |
| Structured logging | Implemented | `backend/app/core/logging.py` |
| Security foundation | Implemented | `backend/app/core/security.py` |
| Workspace management | Implemented | `backend/app/core/paths.py` |
| Health endpoint | Implemented | `GET /api/system/health` |
| Diagnostics endpoint | Implemented | `GET /api/system/diagnostics` |
| Project CRUD | Implemented | `GET/POST/PATCH/DELETE /api/projects` |
| Background job skeleton | Implemented | `backend/app/workers/job_worker.py` |
| Tests | Implemented | `backend/app/tests/` |

## Philosophy

- **Functional before decorative:** every control works or is explicitly disabled.
- **Local-first:** your videos, transcripts, clips, and configuration stay on your machine by default.
- **Free-first:** open-source software and optional free API tiers; no mandatory paid services.
- **Optional AI:** Ollama, Gemini, and Groq through a provider abstraction. The app works without any AI provider.
- **Honest engineering:** no fake progress, fake scores, or deceptive functionality.

## Stack

**Backend:** Python 3.11–3.12, FastAPI, Pydantic v2, SQLAlchemy 2, SQLite, Alembic, pytest, ruff, mypy  
**Frontend:** React, TypeScript, Vite, Tailwind CSS v4, Lucide icons, Vitest  
**Video engine (future phases):** FFmpeg, FFprobe, OpenCV, Faster-Whisper

## Hardware (this machine)

| Resource | Detected |
|---|---|
| OS | Windows 11 Home, 64-bit |
| CPU | Intel Core i3-1005G1 (2 cores / 4 threads) |
| RAM | 12 GB |
| GPU | Intel UHD Graphics (integrated, no CUDA) |
| Free disk | ~75 GB (C: drive) |

This is a **low-resource** class machine. Defaults use CPU-only processing, small Whisper models, and sequential jobs.

## Getting started

### Prerequisites

- Python 3.11 or 3.12 (3.12 used for the venv)
- Node.js and npm
- FFmpeg (required from Phase 2 onward — not installed by default)

### Backend

```powershell
# From the project root
cd clipforge-zero
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\uvicorn app.main:app --reload --host 127.0.0.1 --port 8765
```

The API is available at `http://127.0.0.1:8765`.  
Health check: `http://127.0.0.1:8765/api/system/health`

### Frontend

```powershell
cd clipforge-zero/frontend
npm install
npm run dev
```

The dev server runs on `http://localhost:5173` and proxies API calls to the backend.

### Configuration

Copy `.env.example` to `.env` and adjust as needed. Secrets (Gemini/Groq API keys) are never stored in `.env` — they go through the UI Vault backed by the OS keychain.

## Project structure

```
clipforge-zero/
├── backend/           # Python FastAPI application
├── frontend/          # React + Vite + TypeScript frontend
├── data/              # Local workspace (projects, cache, exports, logs) — gitignored
├── alembic/           # Database migrations
├── tests/             # Backend tests
└── docs/              # Documentation (to be added)
```

## License

MIT License. See `LICENSE`.
