from flask import Flask
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
from os import getenv
from flask_bcrypt import Bcrypt
from .externals import db, login_manager, bcrypt
from .views import views
from .models.users import Users
from .models.movie import Movie


def app_startup():
    """Creates the flask app, as well as the database tables"""

    load_dotenv()

    # Flask initialization
    app = Flask(__name__)
    app.config["SECRET_KEY"] = getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")

    app.register_blueprint(views)

    # Enable CSRF protection in FlaskForm by default
    csrf = CSRFProtect(app)

    # Initializes Bcrypt for the flask app
    # Two parameters unlike in the documentation?
    bcrypt_app = Bcrypt.init_app(bcrypt, app)

    # Initializes LoginManager for the flask app
    login_manager.init_app(app)

    # Default view for unauthorized access
    login_manager.login_view = "views.login"

    # Needed by flask_login
    @login_manager.user_loader
    def load_user(uid):
        return Users.query.get(int(uid))

    # Initializes SQLAlchemy for the flask app
    db.init_app(app)

    # DB table creation
    with app.app_context():
        db.create_all()

    return app
