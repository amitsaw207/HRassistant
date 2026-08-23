import logging
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request

from app.core.config import settings
from app.api.chat import router as chat_router
from app.api.documents import router as documents_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger("hr_assistant")

settings.chroma_path.mkdir(parents=True, exist_ok=True)
settings.upload_path.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="HR policy question-answering assistant",
)

app.include_router(chat_router)
app.include_router(documents_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.perf_counter()

    logger.info(
        "REQUEST START: %s %s",
        request.method,
        request.url,
    )

    try:
        response = await call_next(request)

        duration = time.perf_counter() - start_time

        logger.info(
            "REQUEST END: %s %s - status=%s - duration=%.2fs",
            request.method,
            request.url.path,
            response.status_code,
            duration,
        )

        return response

    except Exception:
        logger.exception(
            "REQUEST FAILED: %s %s",
            request.method,
            request.url.path,
        )
        raise
    
@app.get("/")
def root() -> dict[str, str]:
    return {
        "application": settings.app_name,
        "status": "running",
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "healthy",
        "environment": settings.app_env,
    }

