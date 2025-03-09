import requests
import os
import re
import pytesseract as te
from PIL import Image
import telebot
from dotenv import load_dotenv
from app.services.explanation import generate_reasoning_summary

load_dotenv()

Openai_API_KEY = os.getenv("OPENAI_API_KEY")

verify_url = "http://localhost:5050/verify"
scrape_url = "http://localhost:5050/scrape"
scrape_content_url = "http://localhost:5050/scrape_content"
embedding_url = "http://localhost:5050/embedding"

def reliability_check(min_score, max_score, min_article, max_article):
    if min_score < -0.5:
        return f"Highly Unreliable. Sources suggest opposite of the claim. \n\n source URL: {min_article}"

    if max_score < 0.55:
        return "Unreliable. No credible sources back the claim up."

    if max_score > 0.5 and max_score < 0.60:
        return f"It is ambiguous whether the claim is reliable. \n Some credible sources support it slightly, but doesnt support it directly. \n\n source URL: {max_article}"

    if max_score > 0.60:
        return f"There is strong evidence that the claim is reliable. The source: backs it up. \n\n source URL: {max_article}"

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

    bot.send_message(message.chat.id, reply_msg)

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
                    if url.endswith(".xml"):
                        continue
                    return_data += f"{title}\nlink: {url}\n\n\n"

        else:
            return_data = "Error verifying. Server responded with an error."
    except Exception as e:
        reply_data = f"Error: {e}"
    if return_data == "":
        bot.send_message(message.chat.id, "No relevant credible Sources could be found. This is likely a fake news.")
        return None
    bot.send_message(message.chat.id, return_data)
    bot.send_message(message.chat.id, "extracting content of sources...")

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
        average_score = data.get("average_score", "N/A")
        max_score = data.get("highest_score", "N/A")
        min_score = data.get("lowest_score", "N/A")

        # Get best/worst article URLs
        max_article = data.get("supporting_article", "N/A")
        min_article = data.get("challenging_article", "N/A")

        top_articles = data.get("top_articles", [])

        bot.send_message(message.chat.id, f"average score is: {average_score}\nhighest score is: {max_score}\nlowest score is: {min_score}")

        bot.reply_to(message, reliability_check(min_score, max_score,min_article,max_article))

    except Exception as e:
        bot.send_message(message.chat.id, f"Error during embedding analysis: {e}")
        return

    try:
        print("NOW TRYING TO GIVE REASONING")
        supporting_texts = []
        for article in results:
            article_url = article.get("url", "")
            # Check if this article's URL is in the top_articles list (supporting articles)
            if any(article_url == ta.get("url") for ta in top_articles):
                content = article.get("article_content", "")
                if content:
                    supporting_texts.append(f"Source ({article_url}):\n{content}\n")

        # Also get challenging article content (if available)
        challenging_text = ""
        for article in results:
            if article.get("url", "") == min_article:
                challenging_text = article.get("article_content", "")
                break

        reasoning_summary = generate_reasoning_summary(user_text, supporting_texts, challenging_text)
        bot.send_message(message.chat.id, f"Reasoning Summary:\n\n{reasoning_summary}")
    except Exception as e:
        return f"Error generating reasoning summary: {e}"
