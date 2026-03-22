from flask import Flask
from flask_cors import CORS
from .config import Config
from .models import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize database
    db.init_app(app)

    # Allow requests from the Vite dev server
    CORS(app, resources={
        r"/api/*": {"origins": ["http://localhost:5173", "http://localhost:3000"]},
        r"/auth/*": {"origins": ["http://localhost:5173", "http://localhost:3000"]}
    })

    from .api_routes import bp
    app.register_blueprint(bp)

    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app
