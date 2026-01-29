from langchain_community.vectorstores import Chroma
from app.ai.embeddings import get_embeddings
from app.config import settings

COLLECTION_NAME = "personal_rag"


def get_vectorstore() -> Chroma:
    embeddings = get_embeddings()
    return Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=settings.CHROMA_DIR,
        embedding_function=embeddings,
    )
