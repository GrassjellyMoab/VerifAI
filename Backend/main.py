# main.py
from flask import Flask
from app.controllers.verify_controller import verify_blueprint
from app.services.web_search import perform_web_search

def create_app():
    app = Flask(__name__)
    
    # Register your blueprint for the /verify endpoint
    app.register_blueprint(verify_blueprint, url_prefix="/verify")

    # (Optional) configure app settings, load env, etc.
    return app


if __name__ == "__main__":
    app = create_app()
    # Run on port 5000 by default
    app.run(debug=True, host="0.0.0.0", port=5001)    

