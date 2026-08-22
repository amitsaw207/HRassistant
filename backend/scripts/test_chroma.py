from pathlib import Path

from app.rag.chunker import DocumentChunk
from app.rag.vector_store import ChromaVectorStore


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    chroma_path = project_root / "data" / "chroma-test"

    store = ChromaVectorStore(
        persist_directory=chroma_path,
        collection_name="test_collection",
    )

    chunks = [
        DocumentChunk(
            text="Employees receive 20 days of annual leave.",
            chunk_index=0,
            metadata={
                "source": "leave-policy.txt",
                "page": 1,
                "chunk_index": 0,
            },
        ),
        DocumentChunk(
            text="Employees must notify their manager about sick leave.",
            chunk_index=1,
            metadata={
                "source": "sick-policy.txt",
                "page": 1,
                "chunk_index": 1,
            },
        ),
    ]

    fake_embeddings = [
        [0.1, 0.2, 0.3],
        [0.8, 0.7, 0.6],
    ]

    store.add_chunks(
        chunks=chunks,
        embeddings=fake_embeddings,
    )

    print(f"Stored items: {store.count()}")

    results = store.search(
        query_embedding=[0.1, 0.2, 0.3],
        number_of_results=1,
    )

    print("\nSearch result:")
    print(results)


if __name__ == "__main__":
    main()