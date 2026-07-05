from flask import Flask, request, jsonify, render_template
from chatbot import Chatbot

app = Flask(__name__)
bot = Chatbot()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    user_message = (data.get("message") or "").strip()

    if not user_message:
        return jsonify({"response": "Please type something!"})

    reply, tag, score = bot.get_response(user_message, with_meta=True)
    return jsonify({"response": reply, "intent": tag, "confidence": round(score, 2)})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
