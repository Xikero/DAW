from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config  # Importa la clase Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=Config):  # Pasa la clase Config por defecto
    app = Flask(__name__)
    app.config.from_object(config_class)  # Carga la configuración

    db.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'main.login'

    with app.app_context():
        from .models import User, Incident
        from . import routes
        app.register_blueprint(routes.main)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
