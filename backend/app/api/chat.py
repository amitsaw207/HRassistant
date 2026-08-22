from fastapi import APIRouter, HTTPException

from app.rag.pipeline import HRRAGPipeline
from app.schemas.chat import ChatRequest, ChatResponse


router = APIRouter(
    prefix="/api/chat",
    tags=["Chat"],
)

pipeline = HRRAGPipeline()


@router.post("", response_model=ChatResponse)
def ask_question(request: ChatRequest) -> ChatResponse:
    try:
        result = pipeline.ask(request.question)

        return ChatResponse(**result)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing the question.",
        ) from error