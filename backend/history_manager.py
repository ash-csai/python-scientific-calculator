import os
import sqlite3
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_FILE = str(PROJECT_ROOT / "calculator_history.db")


def get_db_path(db_path: str | None = None) -> str:
    return db_path or DB_FILE


def _connect(db_path: str | None = None) -> sqlite3.Connection:
    connection = sqlite3.connect(get_db_path(db_path), timeout=30.0)
    connection.row_factory = sqlite3.Row
    return connection


def init_db(db_path: str | None = None) -> None:
    db_path = get_db_path(db_path)
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = _connect(db_path)
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS calculation_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                expression TEXT NOT NULL,
                result TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                is_favorite INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        columns = {row[1] for row in conn.execute("PRAGMA table_info(calculation_history)")}
        if "is_favorite" not in columns:
            conn.execute("ALTER TABLE calculation_history ADD COLUMN is_favorite INTEGER NOT NULL DEFAULT 0")
        conn.commit()
    finally:
        conn.close()


def add_history(expression: str, result, db_path: str | None = None) -> None:
    if expression is None or not str(expression).strip():
        return
    if isinstance(result, str) and result.lower().startswith("error"):
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = _connect(db_path)
    try:
        conn.execute(
            """
            INSERT INTO calculation_history (expression, result, timestamp, is_favorite)
            VALUES (?, ?, ?, 0)
            """,
            (str(expression).strip(), str(result), timestamp),
        )
        conn.commit()
    finally:
        conn.close()


def get_all_history(db_path: str | None = None):
    conn = _connect(db_path)
    try:
        rows = conn.execute(
            "SELECT id, expression, result, timestamp, is_favorite FROM calculation_history ORDER BY id DESC"
        ).fetchall()
    finally:
        conn.close()
    return [(row["id"], row["expression"], row["result"], row["timestamp"], row["is_favorite"]) for row in rows]


def search_history(query: str, db_path: str | None = None):
    conn = _connect(db_path)
    try:
        rows = conn.execute(
            "SELECT id, expression, result, timestamp, is_favorite FROM calculation_history WHERE expression LIKE ? ORDER BY id DESC",
            (f"%{query}%",),
        ).fetchall()
    finally:
        conn.close()
    return [(row["id"], row["expression"], row["result"], row["timestamp"], row["is_favorite"]) for row in rows]


def clear_history(db_path: str | None = None) -> None:
    conn = _connect(db_path)
    try:
        conn.execute("DELETE FROM calculation_history")
        conn.commit()
    finally:
        conn.close()

