from pathlib import Path
from typing import Any

from app.core.config import settings
from app.rag.chunker import create_chunks
from app.rag.embeddings import AzureEmbeddingService
from app.rag.loader import load_document
from app.rag.vector_store import ChromaVectorStore
from app.services.azure_service import AzureChatService


class HRRAGPipeline:
    def __init__(self) -> None:
        self.embedding_service = AzureEmbeddingService()

        self.vector_store = ChromaVectorStore(
            persist_directory=settings.chroma_path,
        )

        self.chat_service = AzureChatService()

    def index_document(self, file_path: str | Path) -> int:
        pages = load_document(file_path)

        chunks = create_chunks(
            pages=pages,
            chunk_size=120,
            overlap=20,
        )

        if not chunks:
            raise ValueError(
                "No readable text was found in the document."
            )

        texts = [
            chunk.text
            for chunk in chunks
        ]

        embeddings = (
            self.embedding_service.create_embeddings(texts)
        )

        self.vector_store.add_chunks(
            chunks=chunks,
            embeddings=embeddings,
        )

        return len(chunks)

    def ask(
        self,
        question: str,
        number_of_results: int = 3,
    ) -> dict[str, Any]:
        if not question.strip():
            raise ValueError("Question cannot be empty.")

        question_embedding = (
            self.embedding_service.create_embedding(question)
        )

        matches = self.vector_store.search(
            query_embedding=question_embedding,
            number_of_results=number_of_results,
        )

        if not matches:
            return {
                "answer": (
                    "I could not find this information in "
                    "the uploaded HR policies."
                ),
                "sources": [],
            }

        context_parts: list[str] = []
        sources: list[dict[str, Any]] = []

        for match in matches:
            metadata = match["metadata"]
            source = metadata.get("source", "Unknown source")
            page = metadata.get("page", "Unknown page")

            context_parts.append(
                f"Source: {source}, Page: {page}\n"
                f"{match['text']}"
            )

            sources.append(
                {
                    "source": source,
                    "page": page,
                    "text": match["text"],
                    "distance": match["distance"],
                }
            )

        context = "\n\n".join(context_parts)

        answer = self.chat_service.generate_answer(
            question=question,
            context=context,
        )

        return {
            "answer": answer,
            "sources": sources,
        }