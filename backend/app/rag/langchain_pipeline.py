from pathlib import Path
from typing import Any

from langchain_core.documents import Document

from app.core.config import settings
from app.rag.chunker import create_chunks
from app.rag.langchain_vector_store import LangChainVectorStore
from app.rag.loader import load_document
from app.services.langchain_chat import LangChainChatService


class LangChainHRPipeline:
    def __init__(self) -> None:
        langchain_path = (
            settings.chroma_path.parent / "chroma-langchain"
        )

        self.vector_store = LangChainVectorStore(
            persist_directory=langchain_path,
            collection_name="hr_policies_langchain",
        )

        self.chat_service = LangChainChatService()

    def index_document(
        self,
        file_path: str | Path,
    ) -> int:
        pages = load_document(file_path)

        chunks = create_chunks(
            pages=pages,
            chunk_size=120,
            overlap=20,
        )

        documents = [
            Document(
                page_content=chunk.text,
                metadata=chunk.metadata,
            )
            for chunk in chunks
        ]

        self.vector_store.add_documents(documents)

        return len(documents)

    def ask(
        self,
        question: str,
        number_of_results: int = 3,
    ) -> dict[str, Any]:
        if not question.strip():
            raise ValueError("Question cannot be empty.")

        documents = self.vector_store.search(
            question=question,
            number_of_results=number_of_results,
        )

        if not documents:
            return {
                "answer": (
                    "I could not find this information in "
                    "the uploaded HR policies."
                ),
                "sources": [],
            }

        context_parts: list[str] = []
        sources: list[dict[str, Any]] = []

        for document in documents:
            source = document.metadata.get(
                "source",
                "Unknown source",
            )

            page = document.metadata.get(
                "page",
                "Unknown page",
            )

            context_parts.append(
                f"Source: {source}, Page: {page}\n"
                f"{document.page_content}"
            )

            sources.append(
                {
                    "source": source,
                    "page": page,
                    "text": document.page_content,
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

    def update_document(
        self,
        existing_filename: str,
        replacement_path: str | Path,
    ) -> int:
        replacement_path = Path(replacement_path)

        if not replacement_path.exists():
            raise FileNotFoundError(
                f"Replacement file not found: {replacement_path}"
            )

        self.vector_store.delete_by_source(
            source=existing_filename,
        )

        new_chunks = self.index_document(
            file_path=replacement_path,
        )

        return new_chunks