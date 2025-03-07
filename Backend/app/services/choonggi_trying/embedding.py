import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import time

import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from urllib.parse import urlparse
from flask import Blueprint, request, jsonify
from check_domain import is_credible # your is_credible function

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
    total_score = 0.0
    return_vec = []
    for article in _:
        url = article.get("url")
        reliability = article.get("reliability")
        article_content = article.get("article_content")

        if not article_content:
            continue

        article_vec = embed_text(article_content)
        sim = compute_similarity(input_vec, article_vec)
        return_vec.append({"url": url,
                            "reliability": reliability,
                            "article_content": article_content,
                           "similarity": sim,
                           "vector": article_vec})

        # 4) Weight by reliability
        if reliability == 1:
            weighted_score = sim * 1.0
        else:
            weighted_score = sim * -1.0

        total_score = max(weighted_score,total_score)


    print(total_score)

    # 5) Final credibility score (interpret as you wish)
    return jsonify({"score":total_score})# TODO


# ------------------------------------------
# EXAMPLE USAGE
# ------------------------------------------

