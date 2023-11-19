from flask import Blueprint, render_template, redirect, session, flash
from flask_login import login_user, logout_user, login_required, current_user
from .externals import bcrypt
from .forms.signup_form import SignupForm
from .forms.login_form import LoginForm
from .externals import db
from .models.users import User

views = Blueprint("views", __name__)


@views.route("/")
def index():
    return render_template("index.html", title="Home")


# AUTH SECTION


@views.route("/signup", methods=["GET", "POST"])
def signup():
    signup_form = SignupForm()
    if signup_form.validate_on_submit():
        if User.query.filter((User.username == signup_form.username.data)).first():
            flash("Username taken!")
            return redirect("/signup")

        hashed_password = bcrypt.generate_password_hash(signup_form.password.data).decode("utf-8")
        user = User(username=signup_form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        return redirect("/login")

    return render_template("signup.html", title="Sign Up", form=signup_form)


@views.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter((User.username == login_form.username.data)).first()

        if not user or not bcrypt.check_password_hash(user.password, login_form.password.data):
            flash("Wrong username or password.")
            return redirect("/login")

        login_user(user)

        return redirect("/profile")
    
    return render_template("login.html", title="Log In", form=login_form)


@views.route("/logout")
def logout():
    logout_user()
    return redirect("/")


# MAIN SECTION


@views.route("/profile")
@login_required
def profile():
    return render_template("profile.html", title="Profile")
