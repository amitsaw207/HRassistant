from dataclasses import dataclass

from app.rag.loader import DocumentPage


@dataclass
class DocumentChunk:
    text: str
    chunk_index: int
    metadata: dict


def split_words(
    text: str,
    chunk_size: int = 120,
    overlap: int = 20,
) -> list[str]:
    """
    Split text into word-based chunks.

    This is intentionally simple for the first version.
    Token-based chunking can be added later.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")

    if overlap < 0:
        raise ValueError("overlap cannot be negative")

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    words = text.split()

    if not words:
        return []

    chunks: list[str] = []
    start = 0
    step = chunk_size - overlap

    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunks.append(" ".join(chunk_words))
        start += step

    return chunks


def create_chunks(
    pages: list[DocumentPage],
    chunk_size: int = 120,
    overlap: int = 20,
) -> list[DocumentChunk]:
    """Create chunks while retaining document and page metadata."""
    chunks: list[DocumentChunk] = []
    chunk_index = 0

    for page in pages:
        page_chunks = split_words(
            text=page.text,
            chunk_size=chunk_size,
            overlap=overlap,
        )

        for chunk_text in page_chunks:
            chunks.append(
                DocumentChunk(
                    text=chunk_text,
                    chunk_index=chunk_index,
                    metadata={
                        "source": page.source,
                        "page": page.page_number,
                        "chunk_index": chunk_index,
                    },
                )
            )

            chunk_index += 1

    return chunks