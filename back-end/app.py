import logging
import os

from flask import Flask
from flask_cors import CORS

from extensions.services import pipa


def create_app():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    app = Flask(__name__)
    app.config["PIPA_DATA_DIR"] = os.environ.get("PIPA_DATA_DIR", "./data")
    app.config["MAX_CONTENT_LENGTH"] = 500 * 1024 * 1024  # 500 MB max upload
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")

    CORS(app)

    # Register services
    pipa.init_app(app)

    # Register blueprints
    from blueprints.view import bp as view_bp
    from blueprints.api import api_bp

    app.register_blueprint(view_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
