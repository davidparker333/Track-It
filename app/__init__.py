from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app)
    login.init_app(app)

    login.login_view = 'auth.login'
    login.login_message_category = 'danger'

    with app.app_context():
        from app.blueprints.home import bp as home
        app.register_blueprint(home)

        from app.blueprints.auth import bp as auth
        app.register_blueprint(auth)

    return app