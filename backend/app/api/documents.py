import logging

from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.core.config import settings
from app.rag.langchain_pipeline import LangChainHRPipeline
from app.schemas.document import (
    DocumentListResponse,
    DocumentSummary,
     DocumentUpdateResponse,
    DocumentUploadResponse,
)

logger = logging.getLogger("hr_assistant")

router = APIRouter(
    prefix="/api/documents",
    tags=["Documents"],
)

pipeline = LangChainHRPipeline()

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
}


@router.post(
    "/upload",
    response_model=DocumentUploadResponse,
)
async def upload_document(
    file: UploadFile = File(...),
) -> DocumentUploadResponse:
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="A file name is required.",
        )

    original_name = Path(file.filename).name
    extension = Path(original_name).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Use PDF, DOCX, or TXT.",
        )

    settings.upload_path.mkdir(
        parents=True,
        exist_ok=True,
    )

    saved_path = settings.upload_path / original_name
    file_contents = await file.read()

    if not file_contents:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty.",
        )

    saved_path.write_bytes(file_contents)

    try:
        chunks_indexed = pipeline.index_document(
            file_path=saved_path,
        )
    except Exception as error:
        if saved_path.exists():
            saved_path.unlink()

        raise HTTPException(
            status_code=500,
            detail=f"Document indexing failed: {error}",
        ) from error

    return DocumentUploadResponse(
        filename=original_name,
        chunks_indexed=chunks_indexed,
        message="Document uploaded and indexed successfully.",
    )


@router.get(
    "",
    response_model=DocumentListResponse,
)
def list_documents() -> DocumentListResponse:
    settings.upload_path.mkdir(
        parents=True,
        exist_ok=True,
    )

    documents: list[DocumentSummary] = []

    for path in sorted(settings.upload_path.iterdir()):
        if not path.is_file():
            continue

        extension = path.suffix.lower().replace(".", "")

        size_kb = round(
            path.stat().st_size / 1024,
            2,
        )

        updated_at = datetime.fromtimestamp(
            path.stat().st_mtime,
            tz=timezone.utc,
        )

        documents.append(
            DocumentSummary(
                filename=path.name,
                file_type=extension.upper(),
                size_kb=size_kb,
                updated_at=updated_at,
                status="Indexed",
            )
        )

    return DocumentListResponse(
        documents=documents,
    )

@router.put(
    "/{filename}",
    response_model=DocumentUpdateResponse,
)
async def update_document(
    filename: str,
    file: UploadFile = File(...),
) -> DocumentUpdateResponse:
    existing_name = Path(filename).name

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="A replacement file is required.",
        )

    replacement_name = Path(file.filename).name
    extension = Path(replacement_name).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Use PDF, DOCX, or TXT.",
        )

    if replacement_name != existing_name:
        raise HTTPException(
            status_code=400,
            detail=(
                "The replacement file must have the same name "
                "as the existing policy."
            ),
        )

    saved_path = settings.upload_path / existing_name
    file_contents = await file.read()

    if not file_contents:
        raise HTTPException(
            status_code=400,
            detail="The replacement file is empty.",
        )

    try:
        settings.upload_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        saved_path.write_bytes(file_contents)

        chunks_indexed = pipeline.update_document(
            existing_filename=existing_name,
            replacement_path=saved_path,
        )

        return DocumentUpdateResponse(
            filename=existing_name,
            chunks_indexed=chunks_indexed,
            message=(
                "Policy updated and chunks re-indexed successfully."
            ),
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Policy update failed: {error}",
        ) from error