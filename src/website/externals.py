from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Create objects that can be accessed in other modules
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
