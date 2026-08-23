from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.rag.langchain_embeddings import HRLangChainEmbeddings


class LangChainVectorStore:
    def __init__(
        self,
        persist_directory: Path,
        collection_name: str = "hr_policies_langchain",
    ) -> None:
        self.embeddings = HRLangChainEmbeddings()

        self.vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=self.embeddings,
            persist_directory=str(persist_directory),
        )

    def add_documents(
        self,
        documents: list[Document],
    ) -> list[str]:
        if not documents:
            return []

        return self.vector_store.add_documents(documents)

    def search(
        self,
        question: str,
        number_of_results: int = 3,
    ) -> list[Document]:
        return self.vector_store.similarity_search(
            query=question,
            k=number_of_results,
        )

    def count(self) -> int:
        result = self.vector_store.get()

        ids = result.get("ids", [])

        return len(ids)

    def delete_by_source(self, source: str) -> None:
        self.vector_store._collection.delete(
            where={
                "source": source,
            }
        )