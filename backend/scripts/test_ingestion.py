from pathlib import Path

from app.rag.chunker import create_chunks
from app.rag.loader import load_document


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    policy_path = project_root / "data" / "uploads" / "leave-policy.pdf"

    pages = load_document(policy_path)

    print(f"Pages loaded: {len(pages)}")

    for page in pages:
        print(f"\nSource: {page.source}")
        print(f"Page: {page.page_number}")
        print(f"Characters: {len(page.text)}")
        print(f"Preview: {page.text[:150]}")

    chunks = create_chunks(
        pages=pages,
        chunk_size=40,
        overlap=8,
    )

    print(f"\nChunks created: {len(chunks)}")

    for chunk in chunks:
        print("\n--- Chunk ---")
        print(f"Index: {chunk.chunk_index}")
        print(f"Metadata: {chunk.metadata}")
        print(chunk.text)


if __name__ == "__main__":
    main()