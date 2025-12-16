from flask import Flask, request, jsonify, send_from_directory
import os
import openai  # Make sure you installed it: pip install openai

app = Flask(__name__)

# Serve your index.html
@app.route("/")
def home():
    return send_from_directory(".", "index.html")


# Chat endpoint
@app.route("/chat", methods=["POST"])
def chat():
    # Get API key from environment variable
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return jsonify({"error": "API key not set"}), 500

    openai.api_key = api_key

    # Get user message from POST JSON
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "No message provided"}), 400

    user_message = data["message"]

    try:
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a smart AI assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        reply_text = response.choices[0].message.content

        return jsonify({"reply": reply_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use environment PORT or 5000
    app.run(host="0.0.0.0", port=port, debug=True)

