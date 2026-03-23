from __future__ import annotations

from pathlib import Path

from app.db import DEFAULT_DB_PATH, get_connection
from app.schemas import TranslationPairCreate


class TranslationRepository:
    def __init__(self, db_path: str | Path = DEFAULT_DB_PATH) -> None:
        self.db_path = db_path

    def add_pair(self, pair: TranslationPairCreate) -> None:
        with get_connection(self.db_path) as conn:
            conn.execute(
                """
                INSERT OR IGNORE INTO translation_pairs (
                    source_language,
                    target_language,
                    sentence,
                    translation
                ) VALUES (?, ?, ?, ?)
                """,
                (
                    pair.source_language.lower(),
                    pair.target_language.lower(),
                    pair.sentence.strip(),
                    pair.translation.strip(),
                ),
            )
            conn.commit()

    def get_candidates(self, source_language: str, target_language: str) -> list[dict]:
        """
        Returns examples in the requested direction.

        It supports both:
        1. direct pairs already stored as source_language -> target_language
        2. reversed reuse of stored target_language -> source_language pairs
           by swapping sentence and translation.
        """
        src = source_language.lower()
        tgt = target_language.lower()

        query = """
        SELECT source_language, target_language, sentence, translation
        FROM translation_pairs
        WHERE (source_language = ? AND target_language = ?)
           OR (source_language = ? AND target_language = ?)
        """

        candidates: list[dict] = []
        with get_connection(self.db_path) as conn:
            rows = conn.execute(query, (src, tgt, tgt, src)).fetchall()

        for row in rows:
            if row["source_language"] == src and row["target_language"] == tgt:
                candidates.append(
                    {
                        "source_language": src,
                        "target_language": tgt,
                        "sentence": row["sentence"],
                        "translation": row["translation"],
                        "direction": "direct",
                    }
                )
            else:
                candidates.append(
                    {
                        "source_language": src,
                        "target_language": tgt,
                        "sentence": row["translation"],
                        "translation": row["sentence"],
                        "direction": "reversed",
                    }
                )

        return candidates
