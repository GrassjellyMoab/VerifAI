# main.py
from flask import Flask
from app.controllers.verify_controller import verify_blueprint
from app.services.choonggi_trying.scraper import scrape_blueprint

from app.services.choonggi_trying.content_scraper import scrape_content_blueprint
from app.services.choonggi_trying.embedding import embedding_blueprint


def create_app():
    app = Flask(__name__)

    # Register your blueprint for the /verify endpoint
    app.register_blueprint(verify_blueprint, url_prefix="/verify")
    app.register_blueprint(scrape_blueprint, url_prefix="/scrape")
    app.register_blueprint(scrape_content_blueprint, url_prefix="/scrape_content")
    # (Optional) configure app settings, load env, etc.
    app.register_blueprint(embedding_blueprint, url_prefix="/embedding")
    return app


if __name__ == "__main__":
    from TelegramBot.bot import start_bot
    import threading

    app = create_app()

    thread1 = threading.Thread(target=start_bot)
    thread2 = threading.Thread(target=app.run, kwargs={
        "debug": True,
        "host": "0.0.0.0",
        "port": 5000,
        "use_reloader": False
    })

    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
