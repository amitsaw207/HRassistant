from pathlib import Path

from app.rag.langchain_pipeline import LangChainHRPipeline


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]

    policy_path = (
        project_root
        / "data"
        / "uploads"
        / "leave-policy.pdf"
    )

    pipeline = LangChainHRPipeline()

    number_of_documents = pipeline.index_document(
        file_path=policy_path,
    )

    print(
        f"Successfully indexed "
        f"{number_of_documents} LangChain documents."
    )

    print(
        "Stored documents:",
        pipeline.vector_store.count(),
    )


if __name__ == "__main__":
    main()