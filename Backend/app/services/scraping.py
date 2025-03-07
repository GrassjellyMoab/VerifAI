# app/services/scraping.py
from newspaper import Article
import requests
from bs4 import BeautifulSoup

MIN_ACCEPTABLE_LENGTH = 500  # Example threshold for "enough text"

def scrape_with_newspaper(url: str) -> str:
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text.strip()
    except Exception as e:
        print(f"Newspaper3k failed for {url}: {e}")
        return ""

def scrape_with_bs4(url: str) -> str:
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        # e.g., gather all <p> tags or find a main article tag
        paragraphs = soup.find_all("p")
        return " ".join(p.get_text(strip=True) for p in paragraphs)
    except Exception as e:
        print(f"BeautifulSoup failed for {url}: {e}")
        return ""

def combined_scrape(url: str) -> str:
    """
    1) Attempt newspaper3k
    2) If result is too short or fails, fallback to BS4
    3) Return whichever content is available
    """
    text_newspaper = scrape_with_newspaper(url)
    if len(text_newspaper) >= MIN_ACCEPTABLE_LENGTH:
        # Seems good enough
        return text_newspaper
    else:
        # Fallback to custom soup scraping
        text_bs4 = scrape_with_bs4(url)
        # Optionally you could even merge the two texts
        return text_bs4
