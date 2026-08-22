from app.rag.embeddings import AzureEmbeddingService


def main() -> None:
    service = AzureEmbeddingService()

    print(
        "Embedding deployment:",
        repr(service.deployment_name),
    )

    texts = [
        "Employees are entitled to annual leave.",
        "Annual leave requests require manager approval.",
    ]

    print(f"Number of texts: {len(texts)}")
    print("Sending batch embedding request...")

    embeddings = service.create_embeddings(texts)

    print("Batch embedding request succeeded.")
    print(f"Number of embeddings: {len(embeddings)}")
    print(f"Vector length: {len(embeddings[0])}")


if __name__ == "__main__":
    main()