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
        "api_key": SERP_API_KEY
    }
    
    
    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results["organic_results"]
    
    return organic_results