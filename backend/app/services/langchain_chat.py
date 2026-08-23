from langchain_openai import ChatOpenAI

from app.core.config import settings


class LangChainChatService:
    def __init__(self) -> None:
        self.model = ChatOpenAI(
            model=settings.azure_openai_chat_deployment,
            base_url=settings.azure_openai_endpoint,
            api_key=settings.azure_openai_api_key,
            temperature=0,
            max_tokens=500,
        )

    def generate_answer(
        self,
        question: str,
        context: str,
    ) -> str:
        prompt = f"""
You are an HR policy assistant.

Answer the employee question using only the policy context below.

If the answer is not available in the context, respond exactly with:
I could not find this information in the uploaded HR policies.

Do not invent policy rules.
Do not provide legal advice.
Do not use general knowledge.
Be clear and concise.

Policy context:
{context}

Employee question:
{question}
"""

        response = self.model.invoke(prompt)

        content = response.content

        if isinstance(content, str):
            return content.strip()

        return str(content).strip()