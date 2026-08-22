from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        max_length=1000,
    )


class SourceResponse(BaseModel):
    source: str
    page: int | str
    text: str
    distance: float


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceResponse]