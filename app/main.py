from __future__ import annotations

from fastapi import Depends, FastAPI, Query

from app.db import init_db
from app.repository import TranslationRepository
from app.retrieval import Retriever
from app.schemas import (
    OkResponse,
    PromptResponse,
    StammeringResponse,
    TranslationPairCreate,
)
from app.services import StammeringService, TranslationService

app = FastAPI(title="RAG Translation Backend", version="1.0.0")


def get_translation_service() -> TranslationService:
    repository = TranslationRepository()
    retriever = Retriever(top_k=4)
    return TranslationService(repository=repository, retriever=retriever)


def get_stammering_service() -> StammeringService:
    return StammeringService()


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/pairs", response_model=OkResponse)
def create_pair(
    payload: TranslationPairCreate,
    service: TranslationService = Depends(get_translation_service),
) -> OkResponse:
    service.add_pair(
        source_language=payload.source_language,
        target_language=payload.target_language,
        sentence=payload.sentence,
        translation=payload.translation,
    )
    return OkResponse()


@app.get("/prompt", response_model=PromptResponse)
def get_prompt(
    source_language: str = Query(..., min_length=2, max_length=2),
    target_language: str = Query(..., min_length=2, max_length=2),
    query_sentence: str = Query(..., min_length=1),
    service: TranslationService = Depends(get_translation_service),
) -> PromptResponse:
    prompt, retrieved_pairs = service.generate_prompt(
        source_language=source_language,
        target_language=target_language,
        query_sentence=query_sentence,
    )
    return PromptResponse(prompt=prompt, retrieved_pairs=retrieved_pairs)


@app.get("/stammering", response_model=StammeringResponse)
def get_stammering(
    source_sentence: str = Query(..., min_length=1),
    translated_sentence: str = Query(..., min_length=1),
    service: StammeringService = Depends(get_stammering_service),
) -> StammeringResponse:
    has_stammer = service.detect(
        source_sentence=source_sentence,
        translated_sentence=translated_sentence,
    )
    return StammeringResponse(has_stammer=has_stammer)