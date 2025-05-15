# 🏦 Banking Assistant Chatbot

An AI-powered chatbot designed to assist users with common banking queries using NLP-based intent matching and fallback LLM generation via Mistral (Ollama).

---

## 📁 Project Structure

- `main.py` – FastAPI backend logic
- `knowledge_index.py` – Intent matcher using SentenceTransformer
- `unknown_questions.json` – Logs unmatched user queries
- `intents.json` – JSON-based knowledge base
- `frontend/` – Optional UI (React/HTML based)

---

## 🚀 How to Run the Project

### 🔧 Step 1: Install Ollama
To enable AI-generated responses, install Ollama and run the Mistral model.

1. Download Ollama from [https://ollama.com/download](https://ollama.com/download)
2. Open terminal and run:
   ```bash
   ollama run mistral
This will launch a local LLM server at http://localhost:11434.

### Install required Python packages:
pip install fastapi uvicorn sentence-transformers requests


### Run the FastAPI server:
uvicorn main:app --reload
