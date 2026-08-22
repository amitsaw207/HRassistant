from dataclasses import dataclass
from pathlib import Path

from docx import Document
from pypdf import PdfReader


@dataclass
class DocumentPage:
    text: str
    page_number: int
    source: str


def clean_text(text: str) -> str:
    """Normalize whitespace while preserving readable paragraphs."""
    lines = [line.strip() for line in text.splitlines()]
    non_empty_lines = [line for line in lines if line]

    return "\n".join(non_empty_lines)


def load_pdf(file_path: Path) -> list[DocumentPage]:
    """Extract text from a PDF, keeping one record per page."""
    reader = PdfReader(str(file_path))
    pages: list[DocumentPage] = []

    for page_number, page in enumerate(reader.pages, start=1):
        extracted_text = page.extract_text() or ""
        cleaned = clean_text(extracted_text)

        if cleaned:
            pages.append(
                DocumentPage(
                    text=cleaned,
                    page_number=page_number,
                    source=file_path.name,
                )
            )

    return pages


def load_docx(file_path: Path) -> list[DocumentPage]:
    """Extract text from a DOCX file."""
    document = Document(str(file_path))

    paragraphs = [
        paragraph.text.strip()
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    ]

    text = "\n".join(paragraphs)

    if not text:
        return []

    return [
        DocumentPage(
            text=clean_text(text),
            page_number=1,
            source=file_path.name,
        )
    ]


def load_txt(file_path: Path) -> list[DocumentPage]:
    """Extract text from a TXT file."""
    text = file_path.read_text(encoding="utf-8")
    cleaned = clean_text(text)

    if not cleaned:
        return []

    return [
        DocumentPage(
            text=cleaned,
            page_number=1,
            source=file_path.name,
        )
    ]


def load_document(file_path: str | Path) -> list[DocumentPage]:
    """Load a supported document based on its file extension."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Document not found: {path}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {path}")

    extension = path.suffix.lower()

    if extension == ".pdf":
        return load_pdf(path)

    if extension == ".docx":
        return load_docx(path)

    if extension == ".txt":
        return load_txt(path)

    raise ValueError(
        f"Unsupported file type: {extension}. "
        "Supported types are .pdf, .docx, and .txt."
    )