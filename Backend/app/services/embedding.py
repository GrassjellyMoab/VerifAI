from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from flask import Blueprint, request, jsonify


embedding_blueprint = Blueprint("embedding_blueprint", __name__)

# 1) Load the embedding model (only once at startup)
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_text(text):
    """
    Converts raw text into a dense vector embedding using a SentenceTransformer model.
    """
    return model.encode(text, convert_to_numpy=True)

def compute_similarity(text_vec, article_vec):
    """
    Computes cosine similarity between two vectors.
    """
    return float(cosine_similarity([text_vec], [article_vec])[0][0])


@embedding_blueprint.route("/", methods=["POST"])
def compute_credibility_score():
    """
    Given the input_text and a list of articles (dict: {'content', 'reliability'}),
    returns a final credibility score.

    articles_info = [
       {
          'content': 'Full text of the scraped article...',
          'reliability': 1 or -1
       },
       ...
    ]
    """
    # 1) Embed the input text (user claim)
    data = request.get_json()
    _ = data.get("article_info")  # list of {title : title, url:url, reliability: r}
    input_text = data.get("input_text")

    input_vec = embed_text(input_text)
    total_score = 0
    highest_score = -1
    min_score = 1
    average_score = 0
    supporting_article = "None"
    challenging_article = "None"
    return_vec = []
    if not _:
        return jsonify({"credibility_score": total_score})

    for article in _:
        url = article.get("url")
        reliability = article.get("reliability")
        article_content = article.get("article_content")

        if not article_content:
            continue

        article_vec = embed_text(article_content)
        sim = compute_similarity(input_vec, article_vec)

        if sim > highest_score:
            highest_score = max(sim, highest_score)
            supporting_article = url
        total_score +=sim
        average_score = total_score / len(_)

        if sim < min_score:
            min_score = min(sim,min_score)
            challenging_article = url


    # 5) Final credibility score (interpret as you wish)
    return jsonify({"average_score":average_score,
                    "highest_score": highest_score,
                    "lowest_score" : min_score,
                    "supporting_article": supporting_article,
                    "challenging_article": challenging_article})


# ------------------------------------------
# EXAMPLE USAGE
# ------------------------------------------

