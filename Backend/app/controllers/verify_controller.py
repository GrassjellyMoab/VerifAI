# app/controllers/verify_controller.py

from flask import Blueprint, request, jsonify

# Define a Flask Blueprint
verify_blueprint = Blueprint("verify_blueprint", __name__)

@verify_blueprint.route("/", methods=["POST"])
def verify_claim():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "No text provided"}), 400

    text_to_verify = data["text"]
    
    # Call your pipeline (search, scrape, embed, stance detect, etc.)
    # For hackathon demonstration, let's do a dummy response:
    # reliability_score = run_fact_check(text_to_verify)

    return jsonify({
        "score": 75.5,
        "summary": "Dummy explanation. Found some sources supporting, some refuting."
    })
