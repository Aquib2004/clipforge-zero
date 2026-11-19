"""SQLAlchemy engine and session factory backed by SQLite (WAL mode)."""

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from app.core.paths import data_dir
from app.db.base import Base


def database_url() -> str:
    return f"sqlite:///{data_dir() / 'app.db'}"


engine = create_engine(
    database_url(),
    connect_args={"check_same_thread": False},
)


# Enable WAL mode for better concurrent read performance
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.close()


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    """Create all tables defined on Base."""
    Base.metadata.create_all(bind=engine)
