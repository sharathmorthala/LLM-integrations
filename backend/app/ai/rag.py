import os
from typing import List, Dict, Any, Tuple

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    DirectoryLoader,
)

from app.ai.vectorstore import get_vectorstore, COLLECTION_NAME
from app.ai.llm import get_llm
from app.ai.prompts import SYSTEM_PROMPT, build_rag_user_prompt
from app.config import settings


def _split_documents(docs: List[Document]) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
    )
    return splitter.split_documents(docs)


def load_code_documents(code_root: str) -> List[Document]:
    """
    Loads code/text files from a folder.
    Excludes common junk folders.
    """
    if not os.path.isdir(code_root):
        return []

    exclude_dirs = {
        "node_modules",
        ".git",
        ".venv",
        "dist",
        "build",
        "target",
        ".idea",
        ".gradle",
    }
    patterns = [
        "**/*.py",
        "**/*.ts",
        "**/*.tsx",
        "**/*.js",
        "**/*.jsx",
        "**/*.kt",
        "**/*.java",
        "**/*.md",
        "**/*.txt",
        "**/*.yml",
        "**/*.yaml",
        "**/*.json",
        "**/*.xml",
        "**/*.gradle",
        "**/*.properties",
    ]

    docs: List[Document] = []
    for pattern in patterns:
        loader = DirectoryLoader(
            code_root,
            glob=pattern,
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"},
            show_progress=False,
            use_multithreading=True,
            silent_errors=True,  # skip unreadable files instead of crashing
        )
        loaded = loader.load()

        # Filter out excluded dirs by source path
        for d in loaded:
            src = str(d.metadata.get("source", ""))
            if any(f"/{ex}/" in src or src.endswith(f"/{ex}") for ex in exclude_dirs):
                continue
            docs.append(d)

    return docs


def load_pdf_documents(pdf_root: str) -> List[Document]:
    if not os.path.isdir(pdf_root):
        return []

    docs: List[Document] = []
    for name in os.listdir(pdf_root):
        if name.lower().endswith(".pdf"):
            path = os.path.join(pdf_root, name)
            loader = PyPDFLoader(path)
            docs.extend(loader.load())
    return docs


def reindex_all() -> Dict[str, Any]:
    """
    Rebuild the vector DB collection from scratch.
    """
    vs = get_vectorstore()

    # Clear the collection safely
    try:
        vs.delete_collection()
    except Exception:
        pass

    # Recreate a fresh collection instance
    vs = get_vectorstore()

    code_docs = load_code_documents(settings.CODE_ROOT)
    pdf_docs = load_pdf_documents(settings.PDF_ROOT)

    all_docs = code_docs + pdf_docs
    chunks = _split_documents(all_docs)

    if chunks:
        vs.add_documents(chunks)

    return {
        "code_docs": len(code_docs),
        "pdf_docs": len(pdf_docs),
        "total_docs": len(all_docs),
        "chunks_indexed": len(chunks),
        "chroma_dir": settings.CHROMA_DIR,
        "collection": COLLECTION_NAME,
        "embed_model": settings.EMBED_MODEL,
        "llm_model": settings.LLM_MODEL,
    }


def _format_context(
    docs: List[Document], max_chars: int = 8000
) -> Tuple[str, List[Dict[str, str]]]:
    sources: List[Dict[str, str]] = []
    parts: List[str] = []
    total = 0

    for d in docs:
        src = d.metadata.get("source", "unknown")
        text = (d.page_content or "").strip()
        if not text:
            continue

        snippet = text.replace("\n", " ")
        snippet_short = snippet[:300] + ("..." if len(snippet) > 300 else "")

        sources.append({"source": str(src), "snippet": snippet_short})

        block = f"[SOURCE: {src}]\n{text}\n"
        if total + len(block) > max_chars:
            break
        parts.append(block)
        total += len(block)

    return "\n---\n".join(parts), sources


def ask(question: str) -> Dict[str, Any]:
    vs = get_vectorstore()
    retriever = vs.as_retriever(search_kwargs={"k": settings.TOP_K})

    docs = retriever.invoke(question)
    context, sources = _format_context(docs)

    llm = get_llm()
    user_prompt = build_rag_user_prompt(question, context)

    resp = llm.invoke(
        [
            ("system", SYSTEM_PROMPT),
            ("user", user_prompt),
        ]
    )

    answer_text = getattr(resp, "content", str(resp))

    return {
        "question": question,
        "answer": answer_text,
        "sources": sources,
        "retrieved_chunks": len(docs),
        "llm_model": settings.LLM_MODEL,
        "embed_model": settings.EMBED_MODEL,
    }
