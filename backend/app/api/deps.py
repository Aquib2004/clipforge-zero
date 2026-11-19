"""FastAPI dependencies."""

from app.db.session import SessionLocal


def get_db():
    """Yield a SQLAlchemy session and close it after the request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
