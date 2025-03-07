# app/services/scraping.py

import requests
from bs4 import BeautifulSoup

def scrape_page(url):
    """
    Scrapes the page at 'url' and returns the textual content.
    """
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    # Extract main article text - naive approach:
    return soup.get_text(separator=" ", strip=True)
