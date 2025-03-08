
import requests
import os
import pytesseract as te
from PIL import Image
import telebot
from dotenv import load_dotenv

verify_url = "http://localhost:5000/verify"
scrape_url = "http://localhost:5000/scrape"
scrape_content_url = "http://localhost:5000/scrape_content"
embedding_url = "http://localhost:5000/embedding"


def reliability_model(message, user_text, bot,
                      redundancy_threshold=15,  # tf - idf parameter
                      max_search_count=20, min_source_count=25,
                      keyword_query_percentage=0.6, max_sites_in_query=4,
                      is_singapore_sources=True  # scraper parameters
                      ):

    global keywords, reply_data, results, score, return_data
    payload = {"text": user_text,
               "redundancy_threshold": redundancy_threshold
               # how many keywords are required to simplify keyword searches; default 15
               }
    try:
        response = requests.post(verify_url, json=payload)
        if response.status_code == 200:
            data = response.json()
            keywords = data.get("keywords", " ")
            reply_msg = f"Extracting Key Words:\n\nKeywords: {keywords}"
        else:
            reply_msg = "Error verifying. Server responded with an error."
    except Exception as e:
        reply_msg = f"Error: {e}"
    # WORKS TILL HERE
    bot.send_message(message.chat.id, reply_msg)
    """
    till this point was doing tf-idf
    """

    """
    scraper 
    {"results": list of data in json format}
    is the json format 
    """

    bot.send_message(message.chat.id, "Finding Sources...")
    payload2 = {"keywords": keywords,
                "max_search_count": max_search_count,
                "min_source_count": min_source_count,
                "keyword_query_percentage": keyword_query_percentage,
                "max_sites_in_query": max_sites_in_query,
                "is_singapore_sources": is_singapore_sources
                }
    import re
    pattern_extension = re.compile(r"(\.com(?:/|$)|\.html?(?:/|$))", re.IGNORECASE)

    try:
        response = requests.post(scrape_url, json=payload2)

        if response.status_code == 200:
            data = response.json()

            results = data.get("results", "N/A")
            print(f"here:: {results}")
            return_data = ""
            for result in results:
                if len(return_data) < 3000:
                    title = result.get("title", "")
                    url = result.get("url", "")
                    if pattern_extension.search(url):
                        return_data += f"{title}\nlink: {url}\n\n\n"

        else:
            reply_msg = "Error verifying. Server responded with an error."
    except Exception as e:
        reply_data = f"Error: {e}"

    bot.send_message(message.chat.id, return_data)
    bot.send_message(message.chat.id, "extracting content of sources...")
    # WORKS TILL HERE

    """
    content Scraper
    """

    payload3 = {"results": results}
    try:
        response = requests.post(scrape_content_url, json=payload3)
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", "N/A")


        else:
            reply_msg = "Error scraping. Server responded with an error."
    except Exception as e:
        reply_data = f"Error: {e}"

    bot.send_message(message.chat.id, "finished extracting articles content...")

    """
    works till here
    now embedding:

    """
    bot.send_message(message.chat.id, "analysing content...")
    payload4 = {"input_text": user_text,
                "article_info": results}
    try:
        response = requests.post(embedding_url, json=payload4)

        data = response.json()
        results = data.get("results", "N/A")  # all articles info
        input_vector = data.get("input_vector", "N/A")
        score = data.get("score", "N/A")
        """
        list of {"url": url,
                        "reliability": reliability,
                        "article_content": article_content,
                       "similarity": sim,
                       "vector": article_vec}
        """

        bot.send_message(message.chat.id, f"score is: {score}")

    except Exception as e:
        reply_data = f"Error: {e}"
