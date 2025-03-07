# app/services/web_search.py
from serpapi import GoogleSearch

import os
from dotenv import load_dotenv

load_dotenv() 
SERP_API_KEY = os.getenv("SERP_API_KEY")


def perform_web_search(query):
    """
    Calls a search API (e.g. SerpAPI, Bing, Google) to find relevant links
    for the given 'query'. Returns a list of URLs or metadata.
    """
    params = {
        "engine": "google",
        "q": query,
        "api_key": SERP_API_KEY,
        "location": "Singapore",       
        "gl": "sg",                   
        "google_domain": "google.com.sg",  
        "hl": "en" 
    }
    
    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results.get("organic_results", [])
    return organic_results

if __name__ == "__main__":
    print("Testing perform_web_search...")
    test_query = "Latest scam. Turned off your outside tap, no water. Then put scan QR code for you to scan. All your bank accounts & money gone! BN. AEB IRARINEAYZK Ww, 27K. AM LAH ZE TS TERIA. PRP AAYERTT MP MEER T "
    search_results = perform_web_search(test_query)
    print(search_results)