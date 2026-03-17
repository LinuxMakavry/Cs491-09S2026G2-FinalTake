from flask import Flask
from flask_cors import CORS
from .config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Allow requests from the Vite dev server
    CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5173", "http://localhost:3000"]}})

    from .api_routes import bp
    app.register_blueprint(bp)

    return app
