from flask import Flask, send_from_directory
import os

app = Flask(__name__)

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/chat", methods=["POST"])
def chat():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return 'jsonify({"error": "API key not set"}), 500'

    client = 'OpenAI(api_key=api_key)'

    user_message = 'request.json.get("message")'

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a smart AI assistant."},
            {"role": "user", "content": user_message}
        ]
    )

    return 'jsonify({"reply": response.choices[0].message.content})'

    # noinspection PyUnreachableCode
    return jsonify({
        "reply": response.output_text
    })

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))  # Render provides the PORT variable
    app.run(host="0.0.0.0", port=port, debug=True)

