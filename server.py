from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


client = 'OpenAI( api_key=os.environ.get("OPENAI_API_KEY")'

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
    import os
    port = int(os.environ.get("PORT", 5000))  # Render provides the PORT variable
    app.run(host="0.0.0.0", port=port, debug=True)

