import requests
from flask import Flask, request, jsonify, render_template_string
from pathlib import Path

app = Flask(__name__)

url = "http://localhost:11434/api/generate"


@app.route("/")
def home():

    html_file = Path(__file__).with_name("AI_model_interface.html")

    html = html_file.read_text(encoding="utf-8")

    return render_template_string(html)


@app.route("/ask", methods=["POST"])
def ask_ai():

    user_message = request.json.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "Please enter a message."}), 400

    data = {
        "model": "llama3.2:1b",
        "prompt": user_message,
        "stream": False
    }

    try:

        response = requests.post(
            url,
            json=data,
            timeout=120
        )

        response.raise_for_status()

        result = response.json()

        return jsonify({
            "reply": result.get("response", "Empty response")
        })

    except requests.exceptions.RequestException as e:

        return jsonify({
            "error": "Ollama connection error",
            "details": str(e)
        }), 500


if __name__ == "__main__":

    app.run(debug=True)