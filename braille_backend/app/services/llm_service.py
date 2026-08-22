from langchain_ollama import ChatOllama
from app.core.config import OLLAMA_MODEL, OLLAMA_BASE_URL


def get_llm():
    return ChatOllama(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=0.1,
        reasoning=False,
        num_predict=256,
        num_ctx=2048,
    )


def ask_llm(prompt: str) -> str:
    response = get_llm().invoke(prompt)
    return response.content
