# verify_controller.py
from flask import Blueprint, request, jsonify
from app.services.web_search import perform_web_search


verify_blueprint = Blueprint("verify_blueprint", __name__)



@verify_blueprint.route("/", methods=["POST"])
def verify_claim():
    data = request.get_json()
    user_text = data.get("text", "")
    # find term keywords using TF - IDF then do the search
    keywords = tf_idf_keywords(user_text)

    # Then do your search:
    # search_results = perform_web_search(user_text)
    # print(search_results)




    return jsonify({
        "score": 80,
        "summary": "not implemented"  # Convert set to list for JSON response
    })