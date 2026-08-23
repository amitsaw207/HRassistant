from app.rag.langchain_pipeline import LangChainHRPipeline


def main() -> None:
    pipeline = LangChainHRPipeline()

    print("LangChain HR Policy Assistant")
    print("Type 'exit' to stop.")

    while True:
        question = input("\nEmployee question: ").strip()

        if question.lower() == "exit":
            print("Goodbye.")
            break

        if not question:
            print("Please enter a question.")
            continue

        try:
            result = pipeline.ask(question)

            print("\nAnswer:")
            print(result["answer"])

            print("\nSources:")

            if not result["sources"]:
                print("No sources found.")
                continue

            for source in result["sources"]:
                print(
                    f"- {source['source']}, "
                    f"page {source['page']}"
                )

        except Exception as error:
            print(f"\nError: {error}")


if __name__ == "__main__":
    main()