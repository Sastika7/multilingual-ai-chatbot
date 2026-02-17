from flask import Flask, request, jsonify
from nlp_pipeline import chat_reply

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()

        if not data or "message" not in data:
            return jsonify({"reply": "No message provided"}), 400

        user_message = data["message"]

        reply = chat_reply(user_message)

        return jsonify({
            "reply": reply,
            "source": "Hybrid (tinyllama + deep-translator)"
        })

    except Exception as e:
        print("🔥 BACKEND ERROR:", repr(e))
        return jsonify({"reply": f"Backend error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
