import os
import sqlite3
from pathlib import Path

_connection: sqlite3.Connection | None = None

SCHEMA_PATH = Path(__file__).parent / "schema.sql"


def get_connection() -> sqlite3.Connection:
    global _connection
    if _connection is None:
        db_path = os.environ.get("PYVENTURER_DB_PATH", "pyventurer.db")
        _connection = sqlite3.connect(db_path, check_same_thread=False)
        _connection.row_factory = sqlite3.Row
        _connection.execute("PRAGMA journal_mode=WAL")
        _connection.executescript(SCHEMA_PATH.read_text())
    return _connection


def reset_connection() -> None:
    global _connection
    if _connection is not None:
        _connection.close()
    _connection = None
