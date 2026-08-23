import logging

from fastapi import APIRouter, HTTPException

from app.rag.langchain_pipeline import LangChainHRPipeline
from app.schemas.chat import ChatRequest, ChatResponse


logger = logging.getLogger("hr_assistant")

router = APIRouter(
    prefix="/api/chat",
    tags=["Chat"],
)

pipeline = LangChainHRPipeline()


@router.post("", response_model=ChatResponse)
def ask_question(request: ChatRequest) -> ChatResponse:
    logger.info(
        "CHAT REQUEST RECEIVED: question_length=%s",
        len(request.question),
    )

    logger.info(
        "CHAT QUESTION: %s",
        request.question,
    )

    try:
        result = pipeline.ask(request.question)

        logger.info(
            "CHAT RESPONSE CREATED: sources=%s",
            len(result.get("sources", [])),
        )

        return ChatResponse(**result)

    except ValueError as error:
        logger.warning("CHAT VALIDATION ERROR: %s", error)

        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    except Exception as error:
        logger.exception("CHAT PROCESSING ERROR")

        raise HTTPException(
            status_code=500,
            detail="Failed to process the question.",
        ) from error