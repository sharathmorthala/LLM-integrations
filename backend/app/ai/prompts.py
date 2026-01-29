SYSTEM_PROMPT = """You are a helpful assistant.
You must answer using ONLY the provided context.
If the context does not contain the answer, say: "I don't know based on the provided documents."
Be concise and accurate.
"""


def build_rag_user_prompt(question: str, context: str) -> str:
    return f"""Use the context below to answer the question.

Context:
{context}

Question:
{question}
"""
