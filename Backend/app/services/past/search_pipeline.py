# search_pipeline.py

from web_search import perform_web_search
from past.filter_results import filter_search_results
# Optional: if you want to scrape each credible link,
# you could also import a scraping function here.
# from app.services.scraping import scrape_articles

def retrieve_and_filter_links(query: str):
    """
    1) Use SerpAPI to get search results for 'query'.
    2) Filter them by domain credibility.
    3) Return a list of credible links.
    """
    # Step 1: Retrieve results
    serp_results = perform_web_search(query)
    
    # Step 2: Filter them by credibility
    chosen_links = filter_search_results(serp_results)
    
    scraped_data = scrape_articles(chosen_links)
    
    return scraped_data

if __name__ == "__main__":
    # Quick local test
    test_query = "Latest scam. Turned off your outside tap, no water. Then put scan QR code for you to scan. All your bank accounts & money gone! BN. AEB IRARINEAYZK Ww, 27K. AM LAH ZE TS TERIA. PRP AAYERTT MP MEER T "
    links = retrieve_and_filter_links(test_query)
    print("Credible Links:", links)
    # If you want to see the full results, print them out or debug.
