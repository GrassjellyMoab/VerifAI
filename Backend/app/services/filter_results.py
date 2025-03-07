from urllib.parse import urlparse
from check_domain import is_credible
def extract_domain(url: str) -> str:
    parsed = urlparse(url)
    return parsed.netloc.lower()

def filter_search_results(serp_results: list) -> list:
    chosen_links = []
    for item in serp_results:
        link = item.get("link", "")
        domain = extract_domain(link)
        if is_credible(domain):
            chosen_links.append(link)
    return chosen_links
