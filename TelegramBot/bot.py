# bot.py
import os
import requests
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
BACKEND_URL = "http://localhost:5000/verify"

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello! Send me a piece of text or a link, and I'll check reliability.")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    user_text = message.text
    # 5) Send text to your backend /verify endpoint
    payload = {"text": user_text}
    try:
        response = requests.post(BACKEND_URL, json=payload)
        if response.status_code == 200:
            data = response.json()
            score = data.get("score", "N/A")
            summary = data.get("summary", "No summary")
            reply_msg = f"Reliability: {score}%\n\nSummary: {summary}"
        else:
            reply_msg = "Error verifying. Server responded with an error."
    except Exception as e:
        reply_msg = f"Error: {e}"

    bot.reply_to(message, reply_msg)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    # 6) Download the photo file, run OCR (if needed),
    #    then call the backend the same way
    bot.reply_to(message, "Photo received. (OCR step not yet implemented!)")

# 7) Start polling
if __name__ == "__main__":
    print("Bot is polling...")
    bot.polling()
