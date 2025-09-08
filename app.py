import logging
from flask import Flask, render_template, request, jsonify
import re

# --- Logging setup ---
logging.basicConfig(
    filename="chat_log.txt",
    level=logging.INFO,
    format="%(asctime)s %(message)s"
)

app = Flask(__name__)

# Simple in-memory history (per process)
conversation_history = []

@app.route("/")
def home():
    return render_template("index.html", history=conversation_history)

@app.route("/ask", methods=["POST"])
def ask():
    try:
        user_input = request.form.get("question", "").strip()

        # --- Validation ---
        if not user_input:
            return jsonify({"answer": "Please type a question."}), 400
        if len(user_input) > 500:
            return jsonify({"answer": "Message too long (max 500 chars)."}), 413
        if not re.search(r"[A-Za-z0-9]", user_input):
            return jsonify({"answer": "Please include some letters or numbers."}), 400

        # --- Demo reply (no AI) ---
        answer = f"(demo) You said: {user_input}"

        # Save conversation + log
        conversation_history.append({"user": user_input, "bot": answer})
        logging.info(f"User: {user_input} | Bot: {answer}")

        return jsonify({"answer": answer}), 200

    except Exception:
        logging.exception("Unhandled error in /ask")
        return jsonify({"answer": "Sorry, something went wrong on the server."}), 500

if __name__ == "__main__":
    # Port 80 so you can open the public IP directly
    app.run(host="0.0.0.0", port=80)

