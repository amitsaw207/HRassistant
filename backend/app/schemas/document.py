from datetime import datetime

from pydantic import BaseModel


class DocumentUploadResponse(BaseModel):
    filename: str
    chunks_indexed: int
    message: str


class DocumentSummary(BaseModel):
    filename: str
    file_type: str
    size_kb: float
    updated_at: datetime
    status: str

class DocumentUpdateResponse(BaseModel):
    filename: str
    chunks_indexed: int
    message: str


class DocumentListResponse(BaseModel):
    documents: list[DocumentSummary]