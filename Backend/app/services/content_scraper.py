import requests
from bs4 import BeautifulSoup
from flask import Blueprint, request, jsonify

scrape_content_blueprint = Blueprint("scrape_content_blueprint", __name__)


def extract_main_content(url, headers=None):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an error for bad responses (e.g. 404, 500)
        content_type = response.headers.get('Content-Type', '')

        # Process based on content type
        if 'html' in content_type.lower():
            try:
                soup = BeautifulSoup(response.text, "html.parser")
            except Exception as e:
                # If default parser fails, try a different parser
                soup = BeautifulSoup(response.text, "lxml")

            # Try extracting common content elements from news sites
            content_selectors = [
                "article",  # Many sites wrap content in <article> tags
                "div.story-body", "div.post-content",  # BBC, blogs, medium, etc.
                "div.entry-content", "div.article-content", "div.main-content",
                "section.article-body", "div.content__article-body",  # Common structures
                "p"  # Last fallback: Grab all paragraphs
            ]

            for selector in content_selectors:
                elements = soup.select(selector)
                if elements:
                    # Concatenate text from all found elements
                    print("Content scrap successful (HTML)")
                    extracted_text = " ".join([el.get_text(strip=True) for el in elements])
                    if extracted_text:
                        return extracted_text

            return "Main content not found in HTML."

        elif 'xml' in content_type.lower():
            # Process XML content
            soup = BeautifulSoup(response.text, "xml")
            # Depending on the XML structure, you may customize extraction.
            # Here, we extract all text content from the XML.
            extracted_text = soup.get_text(strip=True)
            if extracted_text:
                print("Content scrap successful (XML)")
                return extracted_text
            else:
                return "Main content not found in XML."

        else:
            # Return a message if the content is neither HTML nor XML
            return f"Content is neither HTML nor XML. Detected content type: {content_type}"

    except requests.exceptions.RequestException as e:
        return f"Error retrieving content: {str(e)}"
    except Exception as e:
        return f"Error processing content: {str(e)}"


@scrape_content_blueprint.route("/", methods=["POST"])
def scrape_content():
    """Fetches and extracts the main body of an article from a given URL."""
    data = request.get_json()
    urls = data.get("results")  # list of dicts: {title: title, url: url, reliability: r}
    return_data = []

    for item in urls:
        url = item.get("url")
        reliability = item.get("reliability")

        if not url:
            return jsonify({"error": "URL is required"}), 400

        article_content = extract_main_content(url)
        return_data.append({
            "url": url,
            "reliability": reliability,
            "article_content": article_content
        })

    return jsonify({"results": return_data})
