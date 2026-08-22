from pathlib import Path
from typing import Any

import chromadb

from app.rag.chunker import DocumentChunk


class ChromaVectorStore:
    def __init__(
        self,
        persist_directory: Path,
        collection_name: str = "hr_policies",
    ) -> None:
        self.client = chromadb.PersistentClient(
            path=str(persist_directory)
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={
                "description": "HR policy document chunks",
            },
        )

    def add_chunks(
        self,
        chunks: list[DocumentChunk],
        embeddings: list[list[float]],
    ) -> None:
        if not chunks:
            return

        if len(chunks) != len(embeddings):
            raise ValueError(
                "The number of chunks must equal the number of embeddings."
            )

        ids = [
            self._create_id(chunk)
            for chunk in chunks
        ]

        documents = [
            chunk.text
            for chunk in chunks
        ]

        metadatas = [
            chunk.metadata
            for chunk in chunks
        ]

        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def search(
        self,
        query_embedding: list[float],
        number_of_results: int = 3,
    ) -> list[dict[str, Any]]:
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=number_of_results,
            include=[
                "documents",
                "metadatas",
                "distances",
            ],
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        matches: list[dict[str, Any]] = []

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances,
        ):
            matches.append(
                {
                    "text": document,
                    "metadata": metadata,
                    "distance": distance,
                }
            )

        return matches

    def count(self) -> int:
        return self.collection.count()

    @staticmethod
    def _create_id(chunk: DocumentChunk) -> str:
        source = chunk.metadata.get("source", "unknown")
        page = chunk.metadata.get("page", 1)
        index = chunk.metadata.get("chunk_index", 0)

        return f"{source}-page-{page}-chunk-{index}"