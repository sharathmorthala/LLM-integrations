from pydantic import BaseModel
import os


class Settings(BaseModel):
    # Ollama server URL (ollama serve)
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")

    # Your local chat model
    LLM_MODEL: str = os.getenv("LLM_MODEL", "qwen2.5:3b")

    # Embeddings model (must be pulled: `ollama pull nomic-embed-text`)
    EMBED_MODEL: str = os.getenv("EMBED_MODEL", "nomic-embed-text")

    # Chroma persistent directory
    CHROMA_DIR: str = os.getenv("CHROMA_DIR", "./chroma_db")

    # Knowledge roots
    CODE_ROOT: str = os.getenv("CODE_ROOT", "./knowledge/code")
    PDF_ROOT: str = os.getenv("PDF_ROOT", "./knowledge/pdfs")

    # Retrieval tuning
    TOP_K: int = int(os.getenv("TOP_K", "4"))
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "1200"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "200"))


settings = Settings()
