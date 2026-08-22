from app.rag.embeddings import AzureEmbeddingService


def main() -> None:
    print("Creating embedding service...")

    service = AzureEmbeddingService()

    print("Sending test text to Azure...")

    embedding = service.create_embedding(
        "Employees are entitled to annual leave."
    )

    print("Embedding request succeeded.")
    print(f"Vector type: {type(embedding)}")
    print(f"Vector length: {len(embedding)}")
    print(f"First five values: {embedding[:5]}")


if __name__ == "__main__":
    main()