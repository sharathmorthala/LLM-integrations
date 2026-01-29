from langchain_ollama import ChatOllama
from app.config import settings


def get_llm() -> ChatOllama:
    return ChatOllama(
        model=settings.LLM_MODEL,
        base_url=settings.OLLAMA_BASE_URL,
        temperature=0.2,
    )
