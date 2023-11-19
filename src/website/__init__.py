from flask import Flask
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
from os import getenv
from .db import db
from .views import views
from .models.user import User
from .models.movie import Movie


def app_startup():
    """Creates the flask app, as well as the database if it doesn't exist"""

    load_dotenv()

    # Flask initialization
    app = Flask(__name__)
    app.config["SECRET_KEY"] = getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")

    app.register_blueprint(views)
    csrf = CSRFProtect(app)

    # Create database
    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app
