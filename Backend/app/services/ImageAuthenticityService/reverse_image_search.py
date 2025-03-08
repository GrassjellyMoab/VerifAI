import http.client
import json
import urllib.parse

import os
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")  # e.g., "e37dd7ffa7msh..."

def reverse_image_search(image_url: str):
    """
    Calls the RapidAPI reverse image search endpoint using the given image_url.
    Returns a dict containing the raw JSON results and a simplified 'similar_found' flag, etc.
    """
    # Quote/encode the image_url so it can be used in a URL parameter
    encoded_url = urllib.parse.quote_plus(image_url)

    # Build the endpoint with any query params you want (limit=10, safe_search=off, etc.)
    endpoint = f"/reverse-image-search?url={encoded_url}&limit=10&safe_search=off"

    conn = http.client.HTTPSConnection("reverse-image-search1.p.rapidapi.com")

    # Prepare the headers with your RapidAPI credentials
    headers = {
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': "reverse-image-search1.p.rapidapi.com"
    }

    # Make the GET request
    conn.request("GET", endpoint, headers=headers)
    res = conn.getresponse()
    data = res.read()

    # Parse the JSON response
    try:
        results = json.loads(data.decode("utf-8"))
    except json.JSONDecodeError:
        return {
            "similar_found": False,
            "source_link": None,
            "raw_response": None,
            "error": "Failed to parse JSON from API"
        }

    # Here, you need to inspect `results` to see how the API returns matches.
    # The example below *guesses* there's a key like 'results' or 'data' with matches.
    # Adjust based on the actual structure you get from print(results).

    # For demonstration, let's say if there's a 'results' key with a list, we assume we found something.
    matches = results.get("results", [])  # (You must confirm actual structure in the JSON)

    # Build a simple dictionary to unify your detection approach
    if matches:
        # Let's just take the first match as 'source_link'
        first_match = matches[0]
        source_link = first_match.get("url")  # or however the link is provided

        return {
            "similar_found": True,
            "source_link": source_link,
            "raw_response": results,
            "error": None
        }
    else:
        return {
            "similar_found": False,
            "source_link": None,
            "raw_response": results,
            "error": None
        }


def analyze_reverse_search(search_result: dict):
    """
    Takes the result of reverse_image_search() and returns a scoring dictionary
    as in your existing logic.
    """
    if search_result["similar_found"]:
        return {
            "reverse_search_score": 0.5,
            "reason": f"Image found online at {search_result['source_link']}"
        }
    else:
        return {
            "reverse_search_score": 1.0,
            "reason": "No matches found"
        }


if __name__ == "__main__":
    # Just a test call
    test_url = "https://i.imgur.com/HBrB8p0.png"
    result = reverse_image_search(test_url)
    print("Raw reverse image search result:", result)

    analysis = analyze_reverse_search(result)
    print("Analysis:", analysis)
