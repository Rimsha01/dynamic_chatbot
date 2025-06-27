#  Dynamic Chatbotwith RAG Capabilities

A  Full-stack FastAPI-based chatbot that processes uploaded documents and answers questions using Retrieval-Augmented Generation (RAG) with Ollama and HuggingFace embeddings.

## Features

- 📄 Document upload (CSV/TXT) with automatic chunking
- 🔍 Semantic search using HuggingFace embeddings
- 💬 Real-time question answering via WebSocket
- 🧠 Context-aware responses using Ollama LLM
- 🗃️ PostgreSQL database for document storage

## Prerequisites

- Python 3.9+
- PostgreSQL
- Ollama (with at least one LLM model installed)
- Reactjs 

## Installation

1. Clone the repository:
   git clone https://github.com/Rimsha01/dynamic_chatbot.git

2. Create and activate virtual environment:

   python -m venv env
   source env/bin/activate  # Linux/Mac
   # OR
   env\Scripts\activate    # Windows

4. Install dependencies :
   pip install -r requirements.txt
