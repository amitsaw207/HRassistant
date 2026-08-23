from openai import OpenAI

from app.core.config import settings


def main() -> None:
    print("Creating Azure AI client...")
    print("Endpoint:", settings.azure_openai_endpoint)
    print("Chat deployment:", settings.azure_openai_chat_deployment)

    client = OpenAI(
        base_url=settings.azure_openai_endpoint,
        api_key=settings.azure_openai_api_key,
    )

    print("Sending request...")

    response = client.responses.create(
        model=settings.azure_openai_chat_deployment,
        input="Say hello in one short sentence.",
    )

    print("\nChat request succeeded.")
    print("Response:")
    print(response.output_text)


if __name__ == "__main__":
    main()