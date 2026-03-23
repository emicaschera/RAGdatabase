from pydantic import BaseModel, Field


class TranslationPairCreate(BaseModel):
    source_language: str = Field(min_length=2, max_length=2)
    target_language: str = Field(min_length=2, max_length=2)
    sentence: str = Field(min_length=1)
    translation: str = Field(min_length=1)


class PromptResponse(BaseModel):
    prompt: str
    retrieved_pairs: list[dict]


class StammeringResponse(BaseModel):
    has_stammer: bool


class OkResponse(BaseModel):
    status: str = "ok"
