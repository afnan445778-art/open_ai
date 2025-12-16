from flask import Flask, request, jsonify, send_from_directory
import openai
import os

app = Flask(__name__)

chat_history = []

# Read API key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/chat", methods=["POST"])
def chat():
    global chat_history
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "No message provided"}), 400

    user_message = data["message"]

    if not openai.api_key:
        return jsonify({"error": "API key not set"}), 500

    chat_history.append({"role": "user", "content": user_message})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "system",
                "content": "You are a highly intelligent, helpful AI assistant. Always give detailed, accurate, and clear answers with examples if needed."
            }] + chat_history
        )

        reply_text = response.choices[0].message.content
        chat_history.append({"role": "assistant", "content": reply_text})

        if len(chat_history) > 20:
            chat_history = chat_history[-20:]

        return jsonify({"reply": reply_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)



