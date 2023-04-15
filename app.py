import uuid
from functools import wraps
from flask import Flask, request, jsonify, session, make_response
from flask_cors import CORS
from flask_session import Session
import openai

app = Flask(__name__)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "supersecretkey"
CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "http://127.0.0.1:3000"}})
Session(app)


def requires_session_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "session_token" not in session:
            session["session_token"] = str(uuid.uuid4())
        return f(*args, **kwargs)

    return decorated_function


@app.route("/api/chat", methods=["POST"])
def chat_completion():
    data = request.json
    prompt = data.get("prompt")

    # Check if 'session_token' exists in the request cookies
    session_token = request.cookies.get("session_token")

    # If not, generate a new session token
    if not session_token:
        session_token = str(uuid.uuid4())

    conversation_key = f"conversation_{session_token}"
    conversation = session.get(conversation_key, [])
    conversation.append({
        "role": "user",
        "content": prompt
    })

    chatgpt_payload = {
        "model": "gpt-3.5-turbo",
        "messages": conversation,
        "max_tokens": 150,
        "n": 1,
        "stop": None,
        "temperature": 0.8
    }

    try:
        chatgpt_response = openai.ChatCompletion.create(**chatgpt_payload)
        response_text = chatgpt_response.choices[0].message["content"].strip()
        conversation.append({
            "role": "assistant",
            "content": response_text
        })
        session[conversation_key] = conversation

        # Prepare the response with the assistant's message
        response = make_response(jsonify({"text": response_text}))

        # Set the 'session_token' cookie if it doesn't exist
        if not request.cookies.get("session_token"):
            response.set_cookie(
                "session_token",
                session_token,
                secure=False,  # Set to True when using HTTPS
                samesite="Lax",
                path="/",
            )

        print(response)

        print(f"Conversation: {conversation}")
        return response

    except Exception as e:
        print(e)
        return jsonify({"error": f"Error communicating with ChatGPT API: {str(e)}"}), 500


if __name__ == "__main__":
    app.run()
