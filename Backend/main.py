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
    app = create_app()
    # Run on port 5000 by default
    app.run(debug=True, host="0.0.0.0", port=5000)

