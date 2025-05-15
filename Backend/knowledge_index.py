import json
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

def load_knowledge():
    with open("banking_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    knowledge = []
    for intent in data["intents"]:
        for q in intent["patterns"]:
            knowledge.append({"question": q, "answer": intent["response"]})
    return knowledge

def build_index(knowledge):
    embeddings = model.encode([item["question"] for item in knowledge])
    return embeddings, knowledge

knowledge_data = load_knowledge()
embeddings, knowledge = build_index(knowledge_data)

def get_top_matches(user_input, top_n=3):
    query_vec = model.encode([user_input])[0]
    sims = np.dot(embeddings, query_vec)
    top_indices = np.argsort(sims)[-top_n:][::-1]
    return [knowledge[i] for i in top_indices], max(sims)
