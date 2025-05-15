import json

with open("unknown_questions.json", "r", encoding="utf-8") as f:
    logs = json.load(f)

print("Unanswered Questions:")
for i, item in enumerate(logs):
    print(f"{i+1}. {item['message']}")

idx = int(input("Enter question number to teach: ")) - 1
answer = input("Enter the correct answer: ")

with open("banking_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

data["intents"].append({
    "tag": f"learned_{len(data['intents'])}",
    "patterns": [logs[idx]["message"]],
    "response": answer
})

with open("banking_data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

del logs[idx]
with open("unknown_questions.json", "w", encoding="utf-8") as f:
    json.dump(logs, f, indent=2)

print("✅ New knowledge saved.")
