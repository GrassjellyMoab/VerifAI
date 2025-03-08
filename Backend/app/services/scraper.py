import os
import time

import requests
from urllib.parse import urlparse
from flask import Blueprint, request, jsonify
import re

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
    "mothership.sg",
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

SINGAPORE_DOMAIN = [
    ".gov.sg",  # covers moh.gov.sg, mom.gov.sg, etc.
    "gov.sg",  # top-level domain
    ".edu.sg",  # e.g., nus.edu.sg, ntu.edu.sg
    ".ac.sg",  # some academic subdomains

    # -- Singapore News Outlets --
    "mothership.sg",
    "straitstimes.com",
    "channelnewsasia.com",
    "todayonline.com",
    "zaobao.com.sg",
    "businesstimes.com.sg",
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



def generate_credible_filter(credible_domains, max_sites=5):
    """
    Generates a query string filter using the 'site:' operator
    from the first max_sites credible domains.
    """
    # Use only domains that don't start with a dot (full domains)
    import random
    sites = []
    for i in range(max_sites):
        sites.append(credible_domains[random.randrange(len(credible_domains))])


    return " OR ".join([f"site:{site}" for site in sites])

@scrape_blueprint.route("/", methods=["POST"])
def verify_keywords_with_sources():
    data = request.get_json()
    keywords = data.get("keywords", "")
    max_search_count = data.get("max_search_count", 20)
    min_source_count = data.get("min_source_count", 25)
    keyword_query_percentage = data.get("keyword_query_percentage", 0.8)
    max_sites_in_query = data.get("max_sites_in_query", 5)
    is_singapore_sources = data.get("is_singapore_sources", False)



    if keyword_query_percentage > 1 or keyword_query_percentage < 0.2:
        keyword_query_percentage = 0.5


    if not keywords:
        return jsonify({"error": "No keywords provided"}), 400

    # Combine keywords into a base search query

    # Generate a credible filter from a subset of credible domains

    # Append the filter to the query so only results from those domains are returned


    verified_results = []
    allowed_tlds = [".com", ".sg", ".org"]

    pattern = r"(mothership\.sg|who\.int|who\.org|un\.org|europa\.eu|imf\.org|worldbank\.org|oecd\.org|edu\.sg|ac\.sg|moh\.gov\.sg|mom\.gov\.sg|mas\.gov\.sg|mha\.gov\.sg|nea\.gov\.sg|ica\.gov\.sg|singstat\.gov\.sg|police\.gov\.sg|straitstimes\.com|channelnewsasia\.com|todayonline\.com|zaobao\.com\.sg|businesstimes\.com\.sg|cdc\.gov|nih\.gov|fda\.gov|epa\.gov|ftc\.gov|consumer\.ftc\.gov|usa\.gov|bbc\.com|bbc\.co\.uk|reuters\.com|apnews\.com|theguardian\.com|nytimes\.com|washingtonpost\.com|cnn\.com|npr\.org|wsj\.com|bloomberg\.com|abcnews\.go\.com|cbsnews\.com|nbcnews\.com|latimes\.com|snopes\.com|factcheck\.org|politifact\.com|fullfact\.org|truthout\.org|sciencedirect\.com|nature\.com|sciencemag\.org|nationalgeographic\.com|newscientist\.com|malwarebytes\.com|kaspersky\.com|mcafee\.com|forbes\.com)"

    counter = 0
    while len({item['url'] for item in verified_results}) < min_source_count:
        time.sleep(1)
        if counter >= max_search_count:
            break

        counter += 1

        try:

            import random


            random_keys = random.sample(keywords, int(keyword_query_percentage*(len(keywords)-1)) )
            base_query = " ".join(random_keys)
            if counter == 1:
                search_query = f"{base_query} (site:mothership.sg)"
                print("here")
            else:
                if is_singapore_sources:
                    credible_filter = generate_credible_filter(SINGAPORE_DOMAIN, max_sites=3)
                else:
                    credible_filter = generate_credible_filter(CREDIBLE_DOMAINS, max_sites=max_sites_in_query)
                search_query = f"{base_query} ({credible_filter} OR {credible_filter})"

            print(f"query: {search_query}")
            search_results = google_custom_search(search_query)
            print(f"search number: {counter}\n"
                  f"{search_results}")

            for result in search_results:
                url = result.get("url")
                domain = get_domain(url)
                match = re.search(pattern, url)
                if url.lower().endswith(".pdf"):
                    continue
                if match:
                    if is_credible(domain) == 1:
                        verified_results.append({
                            "title": result.get("title", "No Title Found"),
                            "url": url,
                            "reliability": 1
                        })

        finally:
            pass

    # Now perform the search


    return jsonify({"results": verified_results})
