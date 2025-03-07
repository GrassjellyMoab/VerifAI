import requests
from bs4 import BeautifulSoup
from flask import Blueprint, request, jsonify

scrape_content_blueprint = Blueprint("scrape_content_blueprint", __name__)

def extract_main_content(url):
    """Extracts the main content from an article page using BeautifulSoup."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an error for bad responses (404, 500)

        soup = BeautifulSoup(response.text, "html.parser")

        # Try extracting common content elements from news sites
        content_selectors = [
            "article",  # Many sites wrap content in <article> tags
            "div.story-body", "div.post-content",  # BBC, blogs, medium, etc.
            "div.entry-content", "div.article-content", "div.main-content",
            "section.article-body", "div.content__article-body",  # Common structures
            "p"  # Last fallback: Grab all paragraphs
        ]

        for selector in content_selectors:
            content = soup.select(selector)
            if content:
                return " ".join([p.get_text(strip=True) for p in content])

        return "Main content not found."

    except requests.exceptions.RequestException as e:
        return f"Error retrieving content: {str(e)}"

@scrape_content_blueprint.route("/", methods=["POST"])
def scrape_content():
    """Fetches and extracts the main body of an article from a given URL."""
    data = request.get_json()
    urls = data.get("results")  # list of {title : title, url:url, reliability: r}
    return_data = []
    for _ in urls:
        url = _.get("url")
        reliability = _.get("reliability")

        if not url:
            return jsonify({"error": "URL is required"}), 400

        article_content = extract_main_content(url)
        return_data.append({"url": url,
                            "reliability": reliability,
                            "article_content": article_content})

    return jsonify({"results": return_data})
