🧠 Local RAG System with FastAPI, LangChain & Ollama

This project is a fully local Retrieval-Augmented Generation (RAG) system built using FastAPI, LangChain, Chroma, and Ollama.
It allows you to ask questions about codebases and PDFs, and get grounded answers with source references, all running locally on your machine.

No cloud APIs. No data leaves your system.

🚀 Features

✅ Local LLM inference using Ollama

✅ RAG pipeline with LangChain

✅ Persistent vector storage using Chroma

✅ Supports code files and PDF documents

✅ Source-grounded answers with citations

✅ FastAPI backend with clean modular structure

✅ Works fully offline after setup

🏗️ Architecture Overview
User Question
     │
     ▼
FastAPI (/ai/ask)
     │
     ▼
LangChain RAG Pipeline
     │
     ├─► Chroma Vector DB (retrieval)
     │       └─ Embeddings via Ollama (nomic-embed-text)
     │
     └─► Local LLM via Ollama (qwen2.5:3b)
              │
              ▼
        Grounded Answer + Sources

🧩 Tech Stack
Component	Technology
Backend API	FastAPI
LLM Runtime	Ollama
Chat Model	qwen2.5:3b
Embeddings	nomic-embed-text
RAG Framework	LangChain
Vector Store	Chroma
Document Types	Code files, PDFs
Language	Python 3.11
📁 Project Structure
backend/
├── app/
│   ├── main.py              # FastAPI app entrypoint
│   ├── config.py            # Central configuration
│   ├── api/
│   │   └── ai.py             # API routes (/ask, /reindex)
│   └── ai/
│       ├── llm.py            # Ollama LLM wrapper
│       ├── embeddings.py     # Ollama embeddings
│       ├── vectorstore.py    # Chroma setup
│       ├── prompts.py        # System & RAG prompts
│       └── rag.py            # RAG orchestration logic
│
├── knowledge/
│   ├── code/                # Source code to index
│   └── pdfs/                # PDF documents to index
│
├── chroma_db/               # Persistent vector store (gitignored)
├── requirements.txt
└── README.md

⚙️ Prerequisites

Python 3.10+

Ollama installed and running

Git

🔧 Setup Instructions
1️⃣ Clone the repository
git clone https://github.com/sharathmorthala/LLM-integrations.git
cd backend

2️⃣ Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

🧠 Setup Ollama Models
Start Ollama
ollama serve

Pull required models
ollama pull qwen2.5:3b
ollama pull nomic-embed-text


Verify:

ollama list

▶️ Run the Backend
uvicorn app.main:app --reload


Server will start at:

http://127.0.0.1:8000

📚 Index Knowledge (Required)

Before asking questions, index your documents:

curl -X POST http://127.0.0.1:8000/ai/reindex


This:

Loads code + PDFs

Splits into chunks

Generates embeddings

Stores them in Chroma

❓ Ask Questions

Example:

curl -X POST http://127.0.0.1:8000/ai/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"What does the main service do? Provide file references."}'

Sample Response
{
  "question": "...",
  "answer": "...",
  "sources": [
    {
      "source": "knowledge/code/main_service.py",
      "snippet": "Main Service Entry Point..."
    }
  ],
  "retrieved_chunks": 4,
  "llm_model": "qwen2.5:3b",
  "embed_model": "nomic-embed-text"
}

⏱️ Performance Notes

Runs fully on CPU by default

Large responses may take time (local inference)

Streaming support planned for better UX

Context size and model choice strongly affect latency

🔒 Privacy & Security

100% local execution

No external API calls

No data sent to third parties

Ideal for private codebases and documents

🛣️ Roadmap

 Streaming responses (SSE)

 Frontend chat UI

 Agent tools (code navigation, file search)

 Model switching (fast vs accurate)

 GPU acceleration support

 Evaluation & metrics

🎯 Why This Project Matters

This project demonstrates:

Real-world RAG architecture

Local LLM deployment

LangChain production patterns

Backend API design

Vector search fundamentals

It’s designed as a learning platform, portfolio project, and foundation for AI products.

📌 Author

Built by Sharath Chandra
Exploring local AI systems, RAG architectures, and applied LLM engineering.