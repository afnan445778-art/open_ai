import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "You are a smart, friendly, professional AI assistant. Keep answers clear and helpful."
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    )

    return jsonify({
        "reply": response.output_text
    })

if __name__ == "__main__":
    app.run(debug=True)
