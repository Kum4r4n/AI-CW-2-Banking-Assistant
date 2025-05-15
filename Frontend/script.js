const chatBox = document.getElementById("chat-box");
const input = document.getElementById("user-input");

function appendMessage(content, type) {
    const msg = document.createElement("div");
    msg.classList.add("message", type); // 'user' or 'bot'
    msg.textContent = content;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
  }
  


async function sendMessage() {
  const message = input.value.trim();
  if (!message) return;

  appendMessage(message, "user");
  input.value = "";

  const res = await fetch("http://localhost:8000/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ message })
  });

  const data = await res.json();
  appendMessage(data.reply, "bot");
}
