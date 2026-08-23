from pathlib import Path

from app.rag.pipeline import HRRAGPipeline


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    policy_path = (
        project_root
        / "data"
        / "uploads"
        / "leave-policy.pdf"
    )

    pipeline = HRRAGPipeline()

    number_of_chunks = pipeline.index_document(
        file_path=policy_path,
    )

    print(
        f"Successfully indexed {number_of_chunks} chunks "
        f"from {policy_path.name}"
    )

    print(
        f"Total chunks in vector database: "
        f"{pipeline.vector_store.count()}"
    )


if __name__ == "__main__":
    main()