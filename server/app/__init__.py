from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev-secret-change-in-prod"
    CORS(app)

    from app.api_routes import bp
    app.register_blueprint(bp)

    return app


"""
SOURCES / REFERENCES:
- Flask application factory pattern documentation
  https://flask.palletsprojects.com/en/3.0.x/patterns/appfactories/
- Flask Blueprint registration docs
  https://flask.palletsprojects.com/en/3.0.x/blueprints/
- flask-cors documentation
  https://flask-cors.readthedocs.io/en/latest/
"""