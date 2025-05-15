from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import datetime
import requests
from knowledge_index import get_top_matches

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class Message(BaseModel):
    message: str

UNKNOWN_LOG_FILE = "unknown_questions.json"
conversation_history = []  # for contextual memory during session

def log_unknown(user_input: str):
    try:
        with open(UNKNOWN_LOG_FILE, "r", encoding="utf-8") as f:
            logs = json.load(f)
    except FileNotFoundError:
        logs = []
    logs.append({
        "message": user_input,
        "timestamp": datetime.datetime.now().isoformat()
    })
    with open(UNKNOWN_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2)

@app.post("/chat")
async def chat(msg: Message):
    user_input = msg.message.strip()
    conversation_history.append(f"User: {user_input}")

    # Limit history to last 10 turns
    if len(conversation_history) > 10:
        conversation_history[:] = conversation_history[-10:]

    # Try semantic matching first
    matches, confidence = get_top_matches(user_input)

    if confidence > 0.6:
        knowledge = "\n".join([f"Q: {m['question']}\nA: {m['answer']}" for m in matches])
        prompt = f"""You are a helpful and intelligent banking assistant. Use the knowledge below to assist the user.

{knowledge}

"""
    else:
        log_unknown(user_input)
        prompt = "You are a helpful and intelligent banking assistant. Continue the conversation naturally.\n"

    # Add chat history
    prompt += "\n".join(conversation_history) + "\nAssistant:"

    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        })
        if response.ok:
            result = response.json()
            reply = result["response"].strip()
            conversation_history.append(f"Assistant: {reply}")
            return {"reply": reply}
    except Exception as e:
        print("Ollama Error:", e)

    fallback = matches[0]["answer"] if matches else "I'm still learning and couldn't understand that. Could you rephrase or ask something else?"
    conversation_history.append(f"Assistant: {fallback}")
    return {"reply": fallback}  # final fallback
