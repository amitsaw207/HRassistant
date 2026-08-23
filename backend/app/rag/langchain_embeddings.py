from langchain_core.embeddings import Embeddings

from app.rag.embeddings import AzureEmbeddingService


class HRLangChainEmbeddings(Embeddings):
    def __init__(self) -> None:
        super().__init__()
        self.azure_service = AzureEmbeddingService()

    def embed_query(self, text: str) -> list[float]:
        return self.azure_service.create_embedding(text)

    def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        embeddings: list[list[float]] = []

        for index, text in enumerate(texts, start=1):
            print(
                f"Creating LangChain embedding "
                f"{index} of {len(texts)}..."
            )

            embedding = self.azure_service.create_embedding(text)
            embeddings.append(embedding)

        return embeddings