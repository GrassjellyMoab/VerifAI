import os
import time
from random import random

import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from urllib.parse import urlparse
from flask import Blueprint, request, jsonify

from check_domain import is_credible # your is_credible function
from googlesearch import search
from dotenv import load_dotenv
load_dotenv()
scrape_blueprint = Blueprint("scrape_blueprint", __name__)

CREDIBLE_DOMAINS = [
    # --- TLD patterns (handle via partial checks in code) ---
    ".gov",  # covers cdc.gov, nih.gov, etc.
    ".edu",  # US educational institutions
    ".ac.",  # academic subdomains in some countries (e.g. .ac.uk)
    ".gov.",  # e.g. .gov.uk, .gov.sg

    # --- International orgs and agencies ---
    "who.int",  # World Health Organization
    "un.org",  # United Nations
    "europa.eu",  # European Union websites
    "imf.org",  # International Monetary Fund
    "worldbank.org",  # World Bank
    "oecd.org",  # Organisation for Economic Co-operation and Development

    # -- Singapore Government & TLD Patterns --
    ".gov.sg",  # covers moh.gov.sg, mom.gov.sg, etc.
    "gov.sg",  # top-level domain
    ".edu.sg",  # e.g., nus.edu.sg, ntu.edu.sg
    ".ac.sg",  # some academic subdomains

    # -- Singapore News Outlets --
    "straitstimes.com",
    "channelnewsasia.com",
    "todayonline.com",
    "zaobao.com.sg",
    "businesstimes.com.sg",

    # --- Major news outlets / media (English-speaking examples) ---
    "bbc.com",
    "bbc.co.uk",
    "reuters.com",
    "apnews.com",
    "theguardian.com",
    "nytimes.com",
    "washingtonpost.com",
    "cnn.com",
    "npr.org",  # US public radio
    "wsj.com",  # Wall Street Journal
    "bloomberg.com",
    "abcnews.go.com",
    "cbsnews.com",
    "nbcnews.com",
    "latimes.com",

    # --- Fact-checking / watchdog sites ---
    "snopes.com",
    "factcheck.org",
    "politifact.com",
    "fullfact.org",  # UK-based fact-check
    "truthout.org",  # independent, though check editorial stance

    # --- Popular tech/science journals or magazines (examples) ---
    "sciencedirect.com",
    "nature.com",
    "sciencemag.org",
    "nationalgeographic.com",
    "newscientist.com",

    # --- Security/antivirus references (for scam detection, e.g. scanning) ---
    "malwarebytes.com",
    "kaspersky.com",
    "mcafee.com",

    "snopes.com", "factcheck.org", "politifact.com", "reuters.com", "bbc.com",
    "apnews.com", "npr.org", "theguardian.com", "forbes.com", "bloomberg.com"

    # --- Additional TLD patterns or country-specific G/NGOs may follow ---
]


def get_domain(url: str) -> str:
    """Extracts the domain from a given URL."""
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.lower()
        if domain.startswith("www."):
            domain = domain[4:]
        return domain
    except Exception:
        return ""

def duckduckgo_search(query, num_results=15):
    """Search DuckDuckGo for the given query and return top results."""
    results = []

    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=num_results):
                results.append({"title": r["title"], "url": r["href"]})

    except Exception:
        print("Exception occurred" + str(len(results)))
    return results


def google_custom_search(query, num_results=10):
    """
    Search Google using the Custom Search API and return top results.
    You'll need to replace YOUR_GOOGLE_API_KEY and YOUR_GOOGLE_CSE_ID with your credentials.
    """
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # Replace with your API key
    GOOGLE_CSE_ID = "50fd98dbe1984411d"  # Replace with your Custom Search Engine ID
    search_url = "https://www.googleapis.com/customsearch/v1"
    final_query = f"{query} (site:.com OR site:.org OR site:.sg)"

    params = {
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_CSE_ID,
        "q": final_query,
        "num": 10,
    }

    response = requests.get(search_url, params=params)
    response.raise_for_status()
    data = response.json()

    results = []
    if "items" in data:
        for item in data["items"]:
            results.append({
                "title": item.get("title", "No Title"),
                "url": item.get("link", "")
            })
    return results


def google_search(query, num_results=10):
    """
    Performs a free Google search by scraping results.

    Warning: This is an unofficial method and may lead to CAPTCHAs or rate limiting.
    """
    results = []
    # The 'pause' parameter adds a delay between requests to help avoid rate limiting.
    for url in search(query):
        results.append(url)
    return results

def generate_credible_filter(credible_domains, max_sites=5):
    """
    Generates a query string filter using the 'site:' operator
    from the first max_sites credible domains.
    """
    # Use only domains that don't start with a dot (full domains)
    import random
    sites = []
    for i in range(8):
        sites.append(CREDIBLE_DOMAINS[random.randrange(len(CREDIBLE_DOMAINS))])


    return " OR ".join([f"site:{site}" for site in sites])

@scrape_blueprint.route("/", methods=["POST"])
def verify_keywords_with_sources():
    data = request.get_json()
    keywords = data.get("keywords", "")
    if not keywords:
        return jsonify({"error": "No keywords provided"}), 400

    # Combine keywords into a base search query


    # Generate a credible filter from a subset of credible domains

    # Append the filter to the query so only results from those domains are returned


    verified_results = []
    allowed_tlds = [".com", ".sg", ".org"]
    import re

    pattern = r"(who\.int|who\.org|un\.org|europa\.eu|imf\.org|worldbank\.org|oecd\.org|edu\.sg|ac\.sg|moh\.gov\.sg|mom\.gov\.sg|mas\.gov\.sg|mha\.gov\.sg|nea\.gov\.sg|ica\.gov\.sg|singstat\.gov\.sg|police\.gov\.sg|straitstimes\.com|channelnewsasia\.com|todayonline\.com|zaobao\.com\.sg|businesstimes\.com\.sg|cdc\.gov|nih\.gov|fda\.gov|epa\.gov|ftc\.gov|consumer\.ftc\.gov|usa\.gov|bbc\.com|bbc\.co\.uk|reuters\.com|apnews\.com|theguardian\.com|nytimes\.com|washingtonpost\.com|cnn\.com|npr\.org|wsj\.com|bloomberg\.com|abcnews\.go\.com|cbsnews\.com|nbcnews\.com|latimes\.com|snopes\.com|factcheck\.org|politifact\.com|fullfact\.org|truthout\.org|sciencedirect\.com|nature\.com|sciencemag\.org|nationalgeographic\.com|newscientist\.com|malwarebytes\.com|kaspersky\.com|mcafee\.com|forbes\.com)"
    url = "https://www.who.int/news/world-xyz"

    counter = 0
    while (len({item['url'] for item in verified_results}) < 20):
        time.sleep(2)
        if counter >= 15:
            break

        counter += 1
        print(counter)
        try:
            import random

            random_keys = random.sample(keywords, 3*(len(keywords)-1) // 4 )
            base_query = " ".join(random_keys)
            credible_filter = generate_credible_filter(CREDIBLE_DOMAINS, max_sites=15)
            search_query = f"{base_query} ({credible_filter})"
            search_results = google_custom_search(search_query)
            print(search_results, counter)
            for result in search_results:
                url = result.get("url")
                domain = get_domain(url)
                match = re.search(pattern, url)
                if match:
                    if is_credible(domain) == 1:
                        verified_results.append({
                            "title": result.get("title", "No Title Found"),
                            "url": url,
                            "reliability": 1
                        })
                    else:
                        verified_results.append({
                            "title": result.get("title", "No Title Found"),
                            "url": url,
                            "reliability": -1
                        })
        finally:
            pass

    # Now perform the search


    return jsonify({"results": verified_results})
