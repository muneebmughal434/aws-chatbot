import logging
from flask import Flask, render_template, request, jsonify

logging.basicConfig(filename='chat_log.txt', level=logging.INFO,
                    format='%(asctime)s %(message)s')

app = Flask(__name__)
history = []

@app.route("/")
def home():
    return render_template("index.html", history=history)

@app.route("/ask", methods=["POST"])
def ask():
    q = request.form.get("question", "").strip()
    if not q:
        return jsonify({"answer": "Please type a question."})
    answer = f"(demo) You said: {q}"  # <-- no AI model, just echo
    history.append({"user": q, "bot": answer})
    logging.info(f"User: {q} | Bot: {answer}")
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
