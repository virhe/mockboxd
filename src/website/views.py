from flask import Blueprint

views = Blueprint("views", __name__)


@views.route("/")
def index():
    return "Hei"


@views.route("/sign-up")
def signup():
    return "Signup"


@views.route("/login")
def login():
    return "Login"
