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
    matches, confidence = get_top_matches(user_input)

    print("Top match:", matches[0]["question"])
    print("Matched answer:", matches[0]["answer"])
    print("Confidence:", confidence)

    if confidence > 0.6:
        knowledge = "\n".join([f"Q: {m['question']}\nA: {m['answer']}" for m in matches])
        prompt = f"""You are a helpful and intelligent banking assistant. Use the knowledge below to assist the user.

{knowledge}

User: {user_input}
Assistant:"""

        try:
            
            response = requests.post("http://localhost:11434/api/generate", json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            })
            
            if response.ok:
                print("Ollama response:", response.text)
                result = response.json()
                return {"reply": result["response"].strip()}
        except:
            print("Ollama error:0000")
            pass  # Fallback

        return {"reply": matches[0]["answer"]}
    else:
        log_unknown(user_input)
        return {"reply": "I'm still learning and couldn't understand that. Could you rephrase or ask something else?"}
