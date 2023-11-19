from flask import Flask
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
from os import getenv
from flask_bcrypt import Bcrypt
from .externals import db, login_manager
from .views import views
from .models.users import User
from .models.movie import Movie


def app_startup():
    """Creates the flask app, as well as the database tables"""

    load_dotenv()

    # Flask initialization
    app = Flask(__name__)
    app.config["SECRET_KEY"] = getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")

    app.register_blueprint(views)
    csrf = CSRFProtect(app)

    # Two parameters unlike in the documentation?
    bcrypt = Bcrypt.init_app(app, app)

    login_manager.init_app(app)
    login_manager.login_view = "views.login"

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # Create database
    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app
