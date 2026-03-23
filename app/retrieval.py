from __future__ import annotations

import re
from typing import Any

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


_WHITESPACE_RE = re.compile(r"\s+")


def normalize_text(text: str) -> str:
    text = text.lower().strip()
    text = _WHITESPACE_RE.sub(" ", text)
    return text


class Retriever:
    def __init__(self, top_k: int = 4) -> None:
        self.top_k = top_k
        self.vectorizer = TfidfVectorizer(
            analyzer="char_wb",
            ngram_range=(3, 5),
            lowercase=True,
        )

    def retrieve(self, query_sentence: str, candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
        if not candidates:
            return []

        normalized_query = normalize_text(query_sentence)
        normalized_sentences = [normalize_text(item["sentence"]) for item in candidates]

        matrix = self.vectorizer.fit_transform(normalized_sentences + [normalized_query])
        sentence_vectors = matrix[:-1]
        query_vector = matrix[-1]

        similarities = cosine_similarity(query_vector, sentence_vectors).flatten()

        ranked_items: list[dict[str, Any]] = []
        for candidate, score in zip(candidates, similarities, strict=False):
            enriched = dict(candidate)
            enriched["score"] = round(float(score), 4)
            ranked_items.append(enriched)

        ranked_items.sort(key=lambda item: item["score"], reverse=True)
        return ranked_items[: self.top_k]
