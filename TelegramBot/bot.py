import requests
import os
import pytesseract as te
from PIL import Image
import telebot
from dotenv import load_dotenv

from Backend.app.controllers.model import reliability_model
from Backend.app.controllers.AICheckModel import aiChecker_model
from Backend.app.controllers.heatmap_model import heatmap_creator

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# GLOBAL PARAMETERS FOR MODEL
redundancy_threshold = 10
max_search_count = 35
min_source_count = 40
keyword_query_percentage = 0.4
max_sites_in_query = 4
is_singapore_sources = True
from tensorflow.keras.models import load_model
model = load_model('MobileNetV2_finetuned_model(0.95 loss 0.11).keras')

# This dictionary will store each user's current "mode"
# e.g. user_mode[chat_id] = "reliability" or "ai" or None
user_mode = {}


def call_model(message, user_text, isReliability=True):
    """
    Wrapper function to call either the reliability_model or aiChecker_model
    depending on the isReliability flag.
    """
    if isReliability:
        reliability_model(
            message, user_text, bot,
            redundancy_threshold=redundancy_threshold,
            max_search_count=max_search_count,
            min_source_count=min_source_count,
            max_sites_in_query=max_sites_in_query,
            keyword_query_percentage=keyword_query_percentage,
            is_singapore_sources=is_singapore_sources
        )
    else:
        aiChecker_model(message, user_text, bot)
        if os.path.isfile(user_text):
            try:
                processing_msg = bot.send_message(message.chat.id, "Generating heatmap visualization... Please wait.")

                heatmap_path = heatmap_creator(user_text,model) #heatmap generation

                with open(heatmap_path, 'rb') as heatmap_img:
                    bot.send_photo(message.chat.id, heatmap_img,
                                   caption="Heatmap visualization showing AI detection regions")

                bot.delete_message(message.chat.id, processing_msg.message_id)

            except Exception as e:
                bot.send_message(message.chat.id, f"Error generating heatmap: {str(e)}")


def send_usage(message, command, usage):
    bot.reply_to(message, f"Usage: /{command} {usage}")


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


@bot.message_handler(commands=['set_max_search_count'])
def set_max_search_count_cmd(message):
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


@bot.message_handler(commands=['set_min_source_count'])
def set_min_source_count_cmd(message):
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


@bot.message_handler(commands=['set_keyword_query_percentage'])
def set_keyword_query_percentage_cmd(message):
    global keyword_query_percentage
    parts = message.text.split()
    if len(parts) != 2:
        send_usage(message, "set_keyword_query_percentage", "<float between 0 and 1>")
        return
    try:
        value = float(parts[1])
        if not 0 <= value <= 1:
            bot.reply_to(message, "Value must be between 0 and 1.")
            return
        keyword_query_percentage = value
        bot.reply_to(message, f"keyword_query_percentage set to {value}.")
    except ValueError:
        bot.reply_to(message, "Please provide a valid float between 0 and 1.")


@bot.message_handler(commands=['set_max_sites_in_query'])
def set_max_sites_in_query_cmd(message):
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


@bot.message_handler(commands=['set_is_singapore_sources'])
def set_is_singapore_sources_cmd(message):
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
def view_parameters_cmd(message):
    reply = (
        f"redundancy_threshold     : {redundancy_threshold}\n"
        f"max_search_count         : {max_search_count}\n"
        f"min_source_count         : {min_source_count}\n"
        f"max_sites_in_query       : {max_sites_in_query}\n"
        f"keyword_query_percentage : {keyword_query_percentage}\n"
        f"is_singapore_sources     : {is_singapore_sources}\n"
    )
    bot.reply_to(message, reply)


@bot.message_handler(commands=['reset_parameters'])
def reset_parameters_cmd(message):
    global redundancy_threshold, max_search_count, min_source_count, max_sites_in_query, keyword_query_percentage, is_singapore_sources
    redundancy_threshold = 10
    max_search_count = 35
    min_source_count = 40
    keyword_query_percentage = 0.4
    max_sites_in_query = 4
    is_singapore_sources = True
    bot.reply_to(message, "Resetting parameters to defaults...")
    view_parameters_cmd(message)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    """
    Sends a welcome message and presents a custom keyboard with 3 buttons:
      - Check Text Reliability
      - Detect AI Image
      - End Conversation
    """
    welcome_text = (
        "Hello, I'm VerifAI!\n\n"
        "I can verify reliability of texts or check if an image is AI-generated. 🕵️ \n\n"
        "Choose one of the options below or set my parameters of the bot with the /help command!\n\n"
        "Type /start to see this message again! 😁"
    )

    # Create a custom reply keyboard
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    reliability_btn = telebot.types.KeyboardButton("Check Text Reliability")
    ai_btn = telebot.types.KeyboardButton("Detect AI Image")
    end_btn = telebot.types.KeyboardButton("End Conversation")
    keyboard.row(reliability_btn, ai_btn)
    keyboard.row(end_btn)

    bot.send_message(message.chat.id, welcome_text, reply_markup=keyboard)
    # Initialize user mode to None
    user_mode[message.chat.id] = None

@bot.message_handler(commands=['help'])
def send_commands(message):
    """
    Sends help information with available commands and their usage
    """
    help_text = (
        "<b>Parameter Settings</b>\n\n"

        "🔧 <b>Basic Parameters:</b>\n"
        "• /set_redundancy_threshold &lt;integer&gt; \n"
        "  Usage: To adjust how many redundant checks to perform\n"
        "  Example: <code>/set_redundancy_threshold 15</code>\n\n"

        "• /set_max_search_count &lt;integer&gt;\n "
        "  Usage: To set the maximum number of search results\n"
        "  Example: <code>/set_max_search_count 40</code>\n\n"

        "• /set_min_source_count &lt;integer&gt;\n "
        "  Usage: To set the minimum sources to consider\n"
        "  Example: <code>/set_min_source_count 30</code>\n\n"

        "🔍 <b>Search Parameters:</b>\n"
        "• /set_keyword_query_percentage &lt;float&gt; "
        "  Usage: Insert a float from 0-1\n"
        "  Example: <code>/set_keyword_query_percentage 0.5</code>\n\n"

        "• /set_max_sites_in_query &lt;integer&gt;\n "
        "  Usage: Set the max websites per query\n"
        "  Example: <code>/set_max_sites_in_query 5</code>\n\n"

        "• /set_is_singapore_sources &lt;true/false&gt;\n "
        "  Usage: To set whether or not to only use Singapore sources\n"
        "  Example: <code>/set_is_singapore_sources true</code>\n\n"

        "⚙️ <b>Management Commands:</b>\n"
        "• /view_parameters - View current settings\n"
        "• /reset_parameters - Reset to defaults\n\n"

        "Type /start to return to main menu"
    )

    bot.send_message(message.chat.id, help_text, parse_mode="HTML")
    # Initialize user mode to None
    user_mode[message.chat.id] = None


@bot.message_handler(content_types=['text'])
def handle_text(message):
    """
    Handle text messages. We check if the user clicked one of the buttons or
    is sending normal text for analysis.
    """
    chat_id = message.chat.id
    text = message.text.strip()

    # Check if the user pressed a button
    if text == "Check Text Reliability":
        user_mode[chat_id] = "reliability"
        bot.reply_to(message, "You selected: Check Text Reliability.\nSend me text or a image to analyse.")
        return
    elif text == "Detect AI Image":
        user_mode[chat_id] = "ai"
        bot.reply_to(message, "You selected: Detect AI Image.\nPlease send me an image (as a file or photo).")
        return
    elif text == "End Conversation":
        user_mode[chat_id] = None
        # Remove the custom keyboard
        remove_kb = telebot.types.ReplyKeyboardRemove()
        bot.send_message(chat_id, "Conversation ended. Type /start to begin again.", reply_markup=remove_kb)
        return

    # If user_mode is reliability, handle it with reliability_model
    if user_mode.get(chat_id) == "reliability":
        call_model(message, text, isReliability=True)
    # If user_mode is ai, we can pass the text to AI checker if it was a link
    elif user_mode.get(chat_id) == "ai":
        # If the user typed a URL to an image, you can handle it here
        # If it’s just text, you might want to inform them to send an image.
        bot.reply_to(message, "Please send an image as a file or photo for AI detection, or a direct image URL.")
    else:
        # No mode selected
        bot.reply_to(message, "Please choose an option from the keyboard or type /start.")


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    """
    Downloads the photo from the user.
    If user is in 'reliability' mode, we OCR the image text and call reliability_model.
    If user is in 'ai' mode, we pass the image path or URL to aiChecker_model.
    """
    chat_id = message.chat.id
    if message.photo is None:
        bot.reply_to(message, "No photo detected.")
        return

    file_id = message.photo[-1].file_id  # the highest resolution
    file_info = bot.get_file(file_id)
    file_path = file_info.file_path
    file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

    # Download the image locally
    image_folder = "images"
    os.makedirs(image_folder, exist_ok=True)
    response = requests.get(file_url)
    if response.status_code != 200:
        bot.reply_to(message, "Error downloading the image.")
        return

    file_data = response.content
    local_filename = file_path.split("/")[-1]
    local_path = os.path.join(image_folder, local_filename)
    with open(local_path, "wb") as f:
        f.write(file_data)

    # Check user mode
    mode = user_mode.get(chat_id)
    if mode == "reliability":
        # OCR the image to get text, then run reliability_model
        extracted_text = te.image_to_string(Image.open(local_path))
        call_model(message, extracted_text, isReliability=True)
    elif mode == "ai":
        # For AI detection, we likely want to pass the *file path* or *URL* to aiChecker_model
        # Depending on how your aiChecker_model is implemented, you can pass the local path or the file_url.
        # Example: passing the local path
        call_model(message, local_path, isReliability=False)
    else:
        bot.reply_to(message, "Please select a mode first by clicking a button or type /start.")


def start_bot():
    print("Bot is polling...")
    bot.polling()
