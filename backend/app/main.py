from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.chat import router as chat_router

settings.chroma_path.mkdir(parents=True, exist_ok=True)
settings.upload_path.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="HR policy question-answering assistant",
)

app.include_router(chat_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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