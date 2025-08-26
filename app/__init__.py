# app/__init__.py (Final Version)
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from project_config import Config
from flask_migrate import Migrate 

migrate = Migrate()

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth_bp.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # ADD THIS USER LOADER vvvv
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    with app.app_context():
        from .auth import routes as auth_routes
        app.register_blueprint(auth_routes.auth_bp)

    return app