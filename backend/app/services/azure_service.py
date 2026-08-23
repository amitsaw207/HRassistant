from openai import OpenAI

from app.core.config import settings


class AzureChatService:
    def __init__(self) -> None:
        self.client = OpenAI(
            base_url=settings.azure_openai_endpoint,
            api_key=settings.azure_openai_api_key,
        )

        self.deployment_name = (
            settings.azure_openai_chat_deployment
        )

    def generate_answer(
        self,
        question: str,
        context: str,
    ) -> str:
        prompt = f"""
You are an HR policy assistant.

Answer the employee question using only the policy context provided.

If the answer is not available in the context, respond exactly with:
I could not find this information in the uploaded HR policies.

Do not invent policy rules.
Do not provide legal advice.
Do not use general knowledge to answer the question.
Be clear and concise.
Mention the policy source when it is available.

Policy context:
{context}

Employee question:
{question}
"""

        response = self.client.responses.create(
            model=self.deployment_name,
            input=prompt,
        )

        if not response.output_text:
            return "I could not generate an answer."

        return response.output_text.strip()