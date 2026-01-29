from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.ai.rag import ask, reindex_all
from app.config import settings

router = APIRouter(prefix="/ai", tags=["ai"])


class AskRequest(BaseModel):
    question: str


@router.get("/models")
def models():
    return {
        "ollama_base_url": settings.OLLAMA_BASE_URL,
        "llm_model": settings.LLM_MODEL,
        "embed_model": settings.EMBED_MODEL,
    }


@router.post("/ask")
def ask_endpoint(req: AskRequest):
    q = (req.question or "").strip()
    if not q:
        raise HTTPException(status_code=400, detail="question is required")
    return ask(q)


@router.post("/reindex")
def reindex_endpoint():
    return reindex_all()
