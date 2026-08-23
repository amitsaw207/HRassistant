from openai import OpenAI

from app.core.config import settings


class AzureEmbeddingService:
    def __init__(self) -> None:
        self.client = OpenAI(
            base_url=settings.azure_openai_endpoint,
            api_key=settings.azure_openai_api_key,
        )

        self.deployment_name = (
            settings.azure_openai_embedding_deployment
        )

    def create_embedding(self, text: str) -> list[float]:
        response = self.client.embeddings.create(
            model=self.deployment_name,
            input=text,
        )

        return response.data[0].embedding

    def create_embeddings(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        embeddings: list[list[float]] = []

        for index, text in enumerate(texts, start=1):
            print(
                f"Creating embedding {index} of {len(texts)}..."
            )

            embedding = self.create_embedding(text)
            embeddings.append(embedding)

        return embeddings