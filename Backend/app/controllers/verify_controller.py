# verify_controller.py
from flask import Blueprint, request, jsonify
from app.services.web_search import perform_web_search 

verify_blueprint = Blueprint("verify_blueprint", __name__)

@verify_blueprint.route("/", methods=["POST"])
def verify_claim():
    data = request.get_json()
    user_text = data.get("text", "")

    # Then do your search:
    search_results = perform_web_search(user_text)
    print(search_results)
    
    # ...some logic to parse results, compute reliability, etc...

    return jsonify({"score": 80, "summary": "Found multiple supporting articles."})
