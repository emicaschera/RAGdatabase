from __future__ import annotations

import sqlite3
from pathlib import Path


DEFAULT_DB_PATH = Path("data") / "translations.db"


# SCHEMA_SQL = """
# CREATE TABLE IF NOT EXISTS translation_pairs (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     source_language TEXT NOT NULL,
#     target_language TEXT NOT NULL,
#     sentence TEXT NOT NULL,
#     translation TEXT NOT NULL,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );
#
# CREATE INDEX IF NOT EXISTS idx_lang_direction
# ON translation_pairs(source_language, target_language);
# """

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS translation_pairs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_language TEXT NOT NULL,
    target_language TEXT NOT NULL,
    sentence TEXT NOT NULL,
    translation TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(source_language, target_language, sentence, translation)
);

CREATE INDEX IF NOT EXISTS idx_lang_direction
ON translation_pairs(source_language, target_language);
"""


def get_connection(db_path: str | Path = DEFAULT_DB_PATH) -> sqlite3.Connection:
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str | Path = DEFAULT_DB_PATH) -> None:
    with get_connection(db_path) as conn:
        conn.executescript(SCHEMA_SQL)
        conn.commit()
