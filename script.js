const chatBox = document.getElementById("chat-box");
const input = document.getElementById("user-input");

function addMessage(text, sender, isTyping = false) {
    const msg = document.createElement("div");
    msg.className = `message ${sender}`;
    if (isTyping) msg.id = "typing-indicator"; 
    msg.innerText = text;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
    const message = input.value.trim();
    if (!message) return;

    addMessage("You: " + message, "user");
    input.value = "";
    addMessage("AI is typing...", "ai", true);

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message })
        });

        const data = await response.json();
        data.reply = undefined;
        
        // Remove the specific typing indicator by ID
        const indicator = document.getElementById("typing-indicator");
        if (indicator) indicator.remove();

        addMessage("AI: " + data.reply, "ai");
    } catch (error) {
        const indicator = document.getElementById("typing-indicator");
        if (indicator) indicator.remove();
        addMessage("Error: Could not reach AI.", "ai");
    }
}
