const chatBox = document.getElementById("chat-box");
const input = document.getElementById("user-input");

function addMessage(text, sender) {
    const msg = document.createElement("div");
    msg.className = `message ${sender}`;
    msg.innerText = text;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function sendMessage() {
    const message = input.value.trim();
    if (!message) return;

    addMessage("You: " + message, "user");
    input.value = "";

    addMessage("AI is typing...", "ai");

    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
    })
    .then(res => res.json())
    .then(data => {
        chatBox.lastChild.remove(); // remove typing text
        addMessage("AI: " + data.reply, "ai");
    });
}
