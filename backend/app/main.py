from fastapi import FastAPI
from app.api.ai import router as ai_router

app = FastAPI(title="Local RAG with LangChain + Ollama")

app.include_router(ai_router)


@app.get("/health")
def health():
    return {"status": "ok"}
