from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    db.init_app(app)
    login_manager.init_app(app)

    from .views import main
    app.register_blueprint(main)

    login_manager.login_view = 'main.login'

    with app.app_context():
        db.create_all()
    
    return app