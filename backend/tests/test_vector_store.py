from pathlib import Path

from app.rag.chunker import DocumentChunk
from app.rag.vector_store import ChromaVectorStore


def test_vector_store_add_and_search(tmp_path: Path) -> None:
    store = ChromaVectorStore(
        persist_directory=tmp_path,
        collection_name="test_collection",
    )

    chunks = [
        DocumentChunk(
            text="Employees receive annual leave.",
            chunk_index=0,
            metadata={
                "source": "leave-policy.txt",
                "page": 1,
                "chunk_index": 0,
            },
        )
    ]

    embeddings = [[0.1, 0.2, 0.3]]

    store.add_chunks(
        chunks=chunks,
        embeddings=embeddings,
    )

    results = store.search(
        query_embedding=[0.1, 0.2, 0.3],
        number_of_results=1,
    )

    assert len(results) == 1
    assert results[0]["text"] == (
        "Employees receive annual leave."
    )