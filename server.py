import os
from flask import Flask, request, jsonify, send_from_directory
from openai import OpenAI, APIError  # Import the modern OpenAI class and exception

# --- Application Initialization ---

app = Flask(__name__)

# IMPORTANT: Initialize the OpenAI Client
# The modern client automatically reads the OPENAI_API_KEY from os.environ.
# We initialize this client outside of the chat function so it's ready for every request.
try:
    client = OpenAI()
    print("OpenAI client initialized successfully.")

except Exception as e:
    # If the key is not found on startup, the client initialization will fail.
    # This ensures the app doesn't start without the necessary key.
    print("-" * 50)
    print("FATAL ERROR: Failed to initialize OpenAI client. Key not found.")
    print("ACTION: Please ensure the OPENAI_API_KEY environment variable is set in your Render dashboard.")
    print("-" * 50)
    # Raising the error will halt the application start, making the problem clear in the logs.
    raise e

# --- Global State Management (Chat History) ---
# NOTE: This chat history is session-wide and not user-specific.
# It will reset when the server restarts.
chat_history = []


# --- Routes ---

@app.route("/")
def home():
    """Serves the index.html file from the current directory."""
    # Ensure your index.html file is in the same directory as this Python script.
    return send_from_directory(".", "index.html")


@app.route("/chat", methods=["POST"])
def chat():
    """Handles the user's chat request."""
    global chat_history

    # 1. Input Validation
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "No message provided"}), 400

    user_message = data["message"]

    # 2. Add user message to history
    chat_history.append({"role": "user", "content": user_message})

    # 3. Construct message list for the API (including system prompt)
    system_message = {
        "role": "system",
        "content": "You are a highly intelligent, helpful AI assistant. Always give detailed, accurate, and clear answers with examples if needed."
    }

    messages_to_send = [system_message] + chat_history

    # 4. API Call and Error Handling
    try:
        # Call the OpenAI API using the initialized client
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages_to_send,
        )

        reply_text = response.choices[0].message.content

        # 5. Update history and clean up
        chat_history.append({"role": "assistant", "content": reply_text})

        # Keep history manageable (e.g., last 20 messages)
        if len(chat_history) > 20:
            chat_history = chat_history[-20:]

        return jsonify({"reply": reply_text})

    except APIError as api_error:
        # This catches errors like invalid key (rejected by OpenAI), billing issues, model not found.
        print(f"OpenAI API Error: {api_error}")
        # The error will be specific (e.g., status code 401 for invalid key)
        return jsonify(
            {"error": f"API Call Failed: Check your key validity/billing. Error: {api_error.status_code}"}), 500

    except Exception as e:
        # Catch all other exceptions (network, server issues)
        print(f"General Server Error: {e}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


# --- App Runner ---
if __name__ == "__main__":
    # Use the PORT environment variable if Render provides one, otherwise default to 5000.
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)


