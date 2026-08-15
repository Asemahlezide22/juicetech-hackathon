"""SQLite database setup.

The database file lives at backend/juicetech.db and is created on first run.
Delete that file to reset everything back to seed data.
"""

from pathlib import Path

from sqlmodel import Session as DBSession
from sqlmodel import SQLModel, create_engine

BACKEND_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BACKEND_DIR / "juicetech.db"

engine = create_engine(
    f"sqlite:///{DB_PATH}",
    echo=False,
    # FastAPI serves requests on multiple threads; SQLite needs this to allow it.
    connect_args={"check_same_thread": False},
)


def create_db_and_tables() -> None:
    """Create any tables that do not exist yet."""
    SQLModel.metadata.create_all(engine)


# Columns added after the first version shipped. SQLModel's create_all() only
# creates missing *tables*, never missing columns, so an existing juicetech.db
# would still be on the old shape and every query would fail.
_ADDED_COLUMNS = {
    "station": {
        "latitude": "FLOAT",
        "longitude": "FLOAT",
        "address": "VARCHAR",
    },
}


def migrate() -> None:
    """Add any columns missing from an existing database.

    Safe to run on every startup — it only touches what is actually absent.
    """
    with engine.begin() as conn:
        for table, columns in _ADDED_COLUMNS.items():
            existing = {
                row[1]  # (cid, name, type, notnull, default, pk)
                for row in conn.exec_driver_sql(f"PRAGMA table_info({table})")
            }
            if not existing:
                continue  # table not created yet; create_all will handle it

            for name, sql_type in columns.items():
                if name not in existing:
                    conn.exec_driver_sql(
                        f"ALTER TABLE {table} ADD COLUMN {name} {sql_type}"
                    )


def get_session():
    """FastAPI dependency that yields a database session per request."""
    with DBSession(engine) as session:
        yield session
