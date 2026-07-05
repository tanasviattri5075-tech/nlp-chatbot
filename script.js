const chatWindow = document.getElementById("chat-window");
const composer = document.getElementById("composer");
const input = document.getElementById("user-input");

function scrollToBottom() {
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

function addMessage(text, sender) {
  const msg = document.createElement("div");
  msg.className = `msg ${sender}`;

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;
  msg.appendChild(bubble);

  chatWindow.appendChild(msg);
  scrollToBottom();
  return msg;
}

function addMeta(msgEl, tag, confidence) {
  const meta = document.createElement("div");
  meta.className = "meta";
  meta.innerHTML = `intent: <span class="tag">${tag}</span> &middot; confidence: ${confidence}`;
  msgEl.appendChild(meta);
}

function addTypingIndicator() {
  const msg = document.createElement("div");
  msg.className = "msg bot";
  msg.id = "typing-indicator";
  msg.innerHTML = `<div class="bubble typing"><span></span><span></span><span></span></div>`;
  chatWindow.appendChild(msg);
  scrollToBottom();
}

function removeTypingIndicator() {
  const el = document.getElementById("typing-indicator");
  if (el) el.remove();
}

composer.addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if (!text) return;

  addMessage(text, "user");
  input.value = "";
  addTypingIndicator();

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text }),
    });
    const data = await res.json();

    removeTypingIndicator();
    const botMsg = addMessage(data.response, "bot");
    addMeta(botMsg, data.intent, data.confidence);
  } catch (err) {
    removeTypingIndicator();
    addMessage("Something went wrong reaching the server.", "bot");
  }
});

input.focus();
