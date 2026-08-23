from app.rag.langchain_pipeline import LangChainHRPipeline


def main() -> None:
    pipeline = LangChainHRPipeline()

    collection = pipeline.vector_store.vector_store._collection

    result = collection.get(
        include=[],
    )

    ids = result.get("ids", [])

    print(f"Vectors found: {len(ids)}")

    if ids:
        collection.delete(ids=ids)

    print("All LangChain chunks and vectors deleted.")
    print(
        "Remaining vectors:",
        pipeline.vector_store.count(),
    )


if __name__ == "__main__":
    main()