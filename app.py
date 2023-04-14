from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/api/chat", methods=["POST"])
def chat_completion():
    data = request.json
    prompt = data.get("prompt")

    chatgpt_payload = {
        "model": "text-davinci-003",
        "prompt": prompt,
        "max_tokens": 150,
        "n": 1,
        "stop": None,
        "temperature": 0.8
    }

    try:
        chatgpt_response = openai.Completion.create(**chatgpt_payload)
        response_text = chatgpt_response.choices[0].text.strip()
        print(response_text)
        return jsonify({"text": response_text})
    except Exception as e:
        print(e)
        return jsonify({"error": f"Error communicating with ChatGPT API: {str(e)}"}), 500


if __name__ == "__main__":
    app.run()
