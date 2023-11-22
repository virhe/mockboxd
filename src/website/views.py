from flask import Blueprint, render_template, redirect, session, flash
from flask_login import login_user, logout_user, login_required, current_user
from .externals import bcrypt
from .forms.signup_form import SignupForm
from .forms.login_form import LoginForm
from .externals import db
from .models.users import Users
from .models.movie import Movie

views = Blueprint("views", __name__)


@views.route("/")
def index():
    """Handles logic related to the index/home page"""
    movies = Movie.query.all()
    return render_template("index.html", title="Home", movies=movies)


# AUTH SECTION


@views.route("/signup", methods=["GET", "POST"])
def signup():
    """Handles logic related to signing users up"""
    signup_form = SignupForm()
    if signup_form.validate_on_submit():
        # Check if username already exists
        if Users.query.filter((Users.username == signup_form.username.data)).first():
            flash("Username taken!")
            return redirect("/signup")

        hashed_password = bcrypt.generate_password_hash(
            signup_form.password.data
        ).decode("utf-8")
        # Add user to DB
        user = Users(username=signup_form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        return redirect("/login")

    return render_template("signup.html", title="Sign Up", form=signup_form)


@views.route("/login", methods=["GET", "POST"])
def login():
    """Handles logic related to logging users in"""
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = Users.query.filter((Users.username == login_form.username.data)).first()

        # Check for wrong login information
        if not user or not bcrypt.check_password_hash(
            user.password, login_form.password.data
        ):
            flash("Wrong username or password.")
            return redirect("/login")

        login_user(user)

        return redirect("/profile")

    return render_template("login.html", title="Log In", form=login_form)


@views.route("/logout")
def logout():
    """Handles logic related to logging users out"""
    logout_user()
    return redirect("/")


# MAIN SECTION


@views.route("/profile")
@login_required
def profile():
    """Handles logic related to the user's profile page"""
    return render_template("profile.html", title="Profile")


# TEST SECTION


@views.route("/create_movies")
def create_movies():
    """Temporary view for creating example movies"""
    test1 = Movie(name="Test1", year=1962, score=4)
    test2 = Movie(name="Test2", year=1999, score=2)
    test3 = Movie(name="Test3", year=2012, score=5)

    db.session.add(test1)
    db.session.add(test2)
    db.session.add(test3)
    db.session.commit()

    return redirect("/")


@views.route("/delete_movies")
def delete_movies():
    """Temporary view for deleting example movies"""
    db.session.query(Movie).delete()
    db.session.commit()

    return redirect("/")
