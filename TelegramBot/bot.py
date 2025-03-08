# bot.py


import requests
import os
import pytesseract as te
from PIL import Image
import telebot
from dotenv import load_dotenv
from app.controllers.model import reliability_model

# 1) Load .env if you have it in the project root or telegram_bot folder
load_dotenv()  # Adjust path as needed if .env is at a different level

# 2) Get the bot token from environment
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# 3) Initialize TeleBot
bot = telebot.TeleBot(BOT_TOKEN)

"""
GLOBAL PARAMETERS FOR MODEL
"""


redundancy_threshold = 15
max_search_count = 20
min_source_count = 25
keyword_query_percentage = 0.6
max_sites_in_query = 4
is_singapore_sources = True


def call_model(message, user_text):
    reliability_model(message, user_text,bot,
                      redundancy_threshold=redundancy_threshold,
                      max_search_count=max_search_count,
                      min_source_count=min_source_count,
                      max_sites_in_query=max_sites_in_query,
                      keyword_query_percentage=keyword_query_percentage,
                      is_singapore_sources=is_singapore_sources)




# Helper function to send usage instructions
def send_usage(message, command, usage):
    bot.reply_to(message, f"Usage: /{command} {usage}")

# Command to set redundancy_threshold (integer)
@bot.message_handler(commands=['set_redundancy_threshold'])
def set_redundancy_threshold(message):
    global redundancy_threshold
    parts = message.text.split()
    if len(parts) != 2:
        send_usage(message, "set_redundancy_threshold", "<integer>")
        return
    try:
        value = int(parts[1])
        redundancy_threshold = value
        bot.reply_to(message, f"redundancy_threshold set to {value}.")
    except ValueError:
        bot.reply_to(message, "Please provide a valid integer.")

# Command to set max_search_count (integer)
@bot.message_handler(commands=['set_max_search_count'])
def set_max_search_count(message):
    global max_search_count
    parts = message.text.split()
    if len(parts) != 2:
        send_usage(message, "set_max_search_count", "<integer>")
        return
    try:
        value = int(parts[1])
        max_search_count = value
        bot.reply_to(message, f"max_search_count set to {value}.")
    except ValueError:
        bot.reply_to(message, "Please provide a valid integer.")

# Command to set min_source_count (integer)
@bot.message_handler(commands=['set_min_source_count'])
def set_min_source_count(message):
    global min_source_count
    parts = message.text.split()
    if len(parts) != 2:
        send_usage(message, "set_min_source_count", "<integer>")
        return
    try:
        value = int(parts[1])
        min_source_count = value
        bot.reply_to(message, f"min_source_count set to {value}.")
    except ValueError:
        bot.reply_to(message, "Please provide a valid integer.")

# Command to set keyword_query_percentage (float between 0 and 1)
@bot.message_handler(commands=['set_keyword_query_percentage'])
def set_keyword_query_percentage(message):
    global keyword_query_percentage
    parts = message.text.split()
    if len(parts) != 2:
        send_usage(message, "set_keyword_query_percentage", "<float between 0 and 1>")
        return
    try:
        value = float(parts[1])
        if value < 0 or value > 1:
            bot.reply_to(message, "Value must be between 0 and 1.")
            return
        keyword_query_percentage = value
        bot.reply_to(message, f"keyword_query_percentage set to {value}.")
    except ValueError:
        bot.reply_to(message, "Please provide a valid float between 0 and 1.")

# Command to set max_sites_in_query (integer)
@bot.message_handler(commands=['set_max_sites_in_query'])
def set_max_sites_in_query(message):
    global max_sites_in_query
    parts = message.text.split()
    if len(parts) != 2:
        send_usage(message, "set_max_sites_in_query", "<integer>")
        return
    try:
        value = int(parts[1])
        max_sites_in_query = value
        bot.reply_to(message, f"max_sites_in_query set to {value}.")
    except ValueError:
        bot.reply_to(message, "Please provide a valid integer.")

# Command to set is_singapore_sources (boolean)
@bot.message_handler(commands=['set_is_singapore_sources'])
def set_is_singapore_sources(message):
    global is_singapore_sources
    parts = message.text.split()
    if len(parts) != 2:
        send_usage(message, "set_is_singapore_sources", "<true/false>")
        return
    value_str = parts[1].lower()
    if value_str in ["true", "1", "yes"]:
        is_singapore_sources = True
        bot.reply_to(message, "is_singapore_sources set to True.")
    elif value_str in ["false", "0", "no"]:
        is_singapore_sources = False
        bot.reply_to(message, "is_singapore_sources set to False.")
    else:
        bot.reply_to(message, "Please provide a valid boolean value: true or false.")

@bot.message_handler(commands=['view_parameters'])
def view_parameters(message):
      reply = f"redundancy_threshold     : {redundancy_threshold}  \n"\
              f"max_search_count         :  {max_search_count} \n"\
              f" min_source_count        :  {min_source_count}\n"\
              f"max_sites_in_query       : {max_sites_in_query}\n"\
              f"keyword_query_percentage : {keyword_query_percentage}\n"\
              f"max_sites_in_query       : {max_sites_in_query}\n"

      bot.reply_to(message, reply)


@bot.message_handler(commands=['reset_parameters'])
def reset_parameters(message):
    global redundancy_threshold, max_search_count, min_source_count, max_sites_in_query, keyword_query_percentage, is_singapore_sources
    redundancy_threshold = 15
    max_search_count = 20
    min_source_count = 25
    keyword_query_percentage = 0.6
    max_sites_in_query = 4
    is_singapore_sources = True
    bot.reply_to(message, "resetting parameters...")
    view_parameters(message)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "Hello! I'm your reliability bot.\n"
        "You can set parameters with the following commands:\n"
        "/set_redundancy_threshold <integer>\n"
        "/set_max_search_count <integer>\n"
        "/set_min_source_count <integer>\n"
        "/set_keyword_query_percentage <float between 0 and 1>\n"
        "/set_max_sites_in_query <integer>\n"
        "/set_is_singapore_sources <true/false>\n"
        "/reset_parameters\n"
        "/view_parameters\n\n"
        "Send me a piece of text or a link, and I'll check reliability."
    )
    bot.reply_to(message, welcome_text)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    user_text = message.text
    # 5) Send text to your backend /verify endpoint
    call_model(message, user_text)


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
        call_model(message, user_text)




def start_bot():
    print("Bot is polling...")
    bot.polling()


