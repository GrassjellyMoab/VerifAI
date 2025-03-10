from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from flask import Blueprint, request, jsonify


embedding_blueprint = Blueprint("embedding_blueprint", __name__)


model1 = SentenceTransformer("all-MiniLM-L12-v2")
model2 = SentenceTransformer("all-mpnet-base-v2")
model3 = SentenceTransformer("paraphrase-mpnet-base-v2")
model4 = SentenceTransformer("multi-qa-mpnet-base-dot-v1")

def embed_text(text,model):
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

    claim_vec1 = embed_text(input_text,model1)
    claim_vec2 = embed_text(input_text,model2)
    claim_vec3 = embed_text(input_text, model3)
    claim_vec4 = embed_text(input_text, model4)
    total_score = 0
    highest_score = -1
    min_score = 1
    average_score = 0
    supporting_article = "None"
    challenging_article = "None"

    if not _:
        return jsonify({"credibility_score": total_score})

    similarities = []  # store tuples of (similarity, url)

    for article in _:
        url = article.get("url")
        article_content = article.get("article_content", "")

        if not article_content:
            continue

        article_vec1 = embed_text(article_content,model1)
        article_vec2 = embed_text(article_content,model2)
        article_vec3 = embed_text(article_content,model3)
        article_vec4 = embed_text(article_content,model4)
        sim1 = compute_similarity(claim_vec1, article_vec1)
        sim2 = compute_similarity(claim_vec2, article_vec2)
        sim3 = compute_similarity(claim_vec3, article_vec3)
        sim4 = compute_similarity(claim_vec4, article_vec4)

        medium_sim = sorted([sim1, sim2, sim3])[1]
        mean_sim = min(sim1, sim2, sim3, sim4)
        if mean_sim > 0.6:
            mean_sim += 0.08
        elif mean_sim < 0.4:
            mean_sim -= 0.10
        elif mean_sim < 0.6:
            mean_sim -= 0.15

        similarities.append((mean_sim, url))

    if not similarities:
        return jsonify({
            "average_score": 0,
            "highest_score": 0,
            "lowest_score": 0,
            "supporting_article": None,
            "challenging_article": None,
            "top_articles": [],
            "message": "No valid articles with content."
        })

    # Sort articles by similarity descending (highest first)
    similarities.sort(key=lambda x: x[0], reverse=True)

    # Calculate average, highest and lowest scores
    scores_only = [s[0] for s in similarities]
    highest_score = max(scores_only)
    lowest_score = min(scores_only)
    average_score = sum(scores_only) / len(scores_only)

    # Get the top 2 articles (or fewer if less than 2)
    top_2 = similarities[:2]

    # The best supporting article is the one with the highest similarity
    supporting_article = similarities[0][1]
    # The most "challenging" article is the one with the lowest similarity
    challenging_article = similarities[-1][1]

    response_data = {
        "average_score": average_score,
        "highest_score": highest_score,
        "lowest_score": lowest_score,
        "supporting_article": supporting_article,
        "challenging_article": challenging_article,
        "top_articles": [
            {"similarity": sim, "url": url} for sim, url in top_2
        ]
    }

    return jsonify(response_data)


