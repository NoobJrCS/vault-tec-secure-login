# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from project_config import Config

# Create the database extension instance, but don't attach it to an app yet
db = SQLAlchemy()

def create_app(config_class=Config):
    """
    Creates and configures the Flask application.
    This is the App Factory.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize the database with the app
    db.init_app(app)

    # Import and register blueprints INSIDE the factory function
    with app.app_context():
        from .auth import routes as auth_routes
        app.register_blueprint(auth_routes.auth_bp)

    return app