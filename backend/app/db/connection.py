import os
import sqlite3
from pathlib import Path

from app.db.seed_curriculum import seed_curriculum

_connection: sqlite3.Connection | None = None

SCHEMA_PATH = Path(__file__).parent / "schema.sql"


def _default_db_path() -> str:
    configured_path = os.environ.get("PYVENTURER_DB_PATH")
    if configured_path:
        return configured_path
    if os.environ.get("VERCEL"):
        return "/tmp/pyventurer.db"
    return "pyventurer.db"


def get_connection() -> sqlite3.Connection:
    global _connection
    if _connection is None:
        db_path = _default_db_path()
        _connection = sqlite3.connect(db_path, check_same_thread=False)
        _connection.row_factory = sqlite3.Row
        _connection.execute("PRAGMA journal_mode=WAL")
        _connection.executescript(SCHEMA_PATH.read_text())
        seed_curriculum(_connection)
    return _connection


def reset_connection() -> None:
    global _connection
    if _connection is not None:
        _connection.close()
    _connection = None
