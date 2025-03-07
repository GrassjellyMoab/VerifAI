# main.py (Flask example)

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/verify', methods=['POST'])
def verify_claim():
    data = request.get_json()
    text = data.get("text", "")
    # Again, call your pipeline logic or just do a dummy response:
    return jsonify({"score": 75.5, "summary": "Dummy explanation"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
