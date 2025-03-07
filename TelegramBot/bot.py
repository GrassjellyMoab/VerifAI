# bot.py


import requests
import os
import pytesseract as te
from PIL import Image
import telebot
from dotenv import load_dotenv

# 1) Load .env if you have it in the project root or telegram_bot folder
load_dotenv()  # Adjust path as needed if .env is at a different level

# 2) Get the bot token from environment
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# 3) Initialize TeleBot
bot = telebot.TeleBot(BOT_TOKEN)

# 4) The URL where your Flask backend runs
#    If you run Flask locally: e.g. "http://localhost:5000/verify"
verify_url = "http://localhost:5000/verify"
scrape_url = "http://localhost:5000/scrape"
scrape_content_url = "http://localhost:5000/scrape_content"
embedding_url = "http://localhost:5000/embedding"

def reliability_calculator(message, user_text):
    global keywords, reply_data, results, score
    payload = {"text": user_text}
    try:
        response = requests.post(verify_url, json=payload)
        if response.status_code == 200:
            data = response.json()
            score = data.get("score", "N/A")
            keywords = data.get("keywords", " ")
            reply_msg = f"Reliability: {score}%\n\nKeywords: {keywords}"
        else:
            reply_msg = "Error verifying. Server responded with an error."
    except Exception as e:
        reply_msg = f"Error: {e}"
    #WORKS TILL HERE
    bot.reply_to(message, reply_msg)
    """
    till this point was doing tf-idf
    """


    """
    scraper 
    {"results": list of data in json format}
    is the json format 
    """
    payload2 = {"keywords": keywords}
    try:
        response = requests.post(scrape_url, json=payload2)

        if response.status_code == 200:
            data = response.json()

            results = data.get("results", "N/A")

            reply_data = f"results: {results}"
        else:
            reply_msg = "Error verifying. Server responded with an error."
    except Exception as e:
        reply_data = f"Error: {e}"


    bot.reply_to(message, reply_data)

    #WORKS TILL HERE

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

    bot.reply_to(message, "Success")


    """
    works till here
    now embedding:
    
    """
    payload4 = {"input_text": user_text,
                "article_info": results}
    try:
        response = requests.post(embedding_url, json=payload4)
        if response.status_code == 200:
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

            bot.reply_to(message, f"score is: {score}")
        else:
            reply_data = "Error in embedding. Server responded with an error."
    except Exception as e:
        reply_data = f"Error: {e}"




@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello! Send me a piece of text or a link, and I'll check reliability.")


@bot.message_handler(content_types=['text'])
def handle_text(message):
    user_text = message.text
    # 5) Send text to your backend /verify endpoint
    reliability_calculator(message, user_text)


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    """
    downloads image from telegram bot, processes content words and returns text
    """
    image_folder = "images"
    # 6) Download the photo file, run OCR (if needed),
    #    then call the backend the same way
    file_id = message.photo[-1].file_id  # last element has the highest resolution

    if file_id is None:
        bot.reply_to(message, "photo was not correctly received!")
        raise ValueError("file was not correctly received backend in bot.py file")

    else:
        bot.reply_to(message, "Photo received. Processing it right now")

    # image downloading
    file_info = bot.get_file(file_id)
    file_path = file_info.file_path

    #construction of download url of image to process
    file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

    # Get the image
    response = requests.get(file_url)
    if response.status_code == 200:
        file_data = response.content
        file_name = file_info.file_path.split("/")[-1]  # Extracts "image.jpg"

        os.makedirs(image_folder, exist_ok=True)
        file_name = os.path.join(image_folder, file_name)

        with open(file_name, "wb") as f:
            f.write(file_data)

        # bot.reply_to(message, f"Photo saved as {file_name}")
        # with open(file_name, "rb") as photo:
        #     bot.send_photo(message.chat.id, photo, caption=f"how to send back image")

        # now process image for words
        user_text = te.image_to_string(Image.open(file_name))


        # send to backend
        reliability_calculator(message, user_text)

# 7) Start polling
if __name__ == "__main__":
    print("Bot is polling...")
    bot.polling()
    from flask import Flask
    from app.controllers.verify_controller import verify_blueprint
    from app.services.choonggi_trying.scraper import scrape_blueprint



    def create_app():
        app = Flask(__name__)

        # Register your blueprint for the /verify endpoint
        app.register_blueprint(verify_blueprint, url_prefix="/verify")
        app.register_blueprint(scrape_blueprint, url_prefix="/scrape")
        # (Optional) configure app settings, load env, etc.
        return app


    if __name__ == "__main__":
        app = create_app()
        # Run on port 5000 by default
        app.run(debug=True, host="0.0.0.0", port=5000)


