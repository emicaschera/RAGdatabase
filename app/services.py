from __future__ import annotations

from app.prompt_builder import build_translation_prompt
from app.repository import TranslationRepository
from app.retrieval import Retriever
from app.stammering import has_stammering


class TranslationService:
    def __init__(
        self,
        repository: TranslationRepository,
        retriever: Retriever,
    ) -> None:
        self.repository = repository
        self.retriever = retriever

    def add_pair(
        self,
        source_language: str,
        target_language: str,
        sentence: str,
        translation: str,
    ) -> None:
        from app.schemas import TranslationPairCreate

        payload = TranslationPairCreate(
            source_language=source_language,
            target_language=target_language,
            sentence=sentence,
            translation=translation,
        )
        self.repository.add_pair(payload)

    def generate_prompt(
        self,
        source_language: str,
        target_language: str,
        query_sentence: str,
    ) -> tuple[str, list[dict]]:
        normalized_source = source_language.lower()
        normalized_target = target_language.lower()

        candidates = self.repository.get_candidates(
            source_language=normalized_source,
            target_language=normalized_target,
        )

        retrieved_pairs = self.retriever.retrieve(
            query_sentence=query_sentence,
            candidates=candidates,
        )

        prompt = build_translation_prompt(
            source_language=normalized_source,
            target_language=normalized_target,
            query_sentence=query_sentence,
            retrieved_pairs=retrieved_pairs,
        )

        return prompt, retrieved_pairs


class StammeringService:
    @staticmethod
    def detect(
        source_sentence: str,
        translated_sentence: str,
    ) -> bool:
        return has_stammering(
            source_sentence=source_sentence,
            translated_sentence=translated_sentence,
        )