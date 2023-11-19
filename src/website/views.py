from flask import Blueprint, render_template, redirect, session, flash
from .forms.SignupForm import SignupForm
from .db import db
from .models.user import User

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

        user = User(username=signup_form.username.data, password=signup_form.password.data)
        db.session.add(user)
        db.session.commit()
        
        return redirect("/login")

    return render_template("signup.html", title="Sign Up", form=signup_form)


@views.route("/login")
def login():
    session["logged_in"] = True
    return render_template("login.html", title="Log In")


@views.route("/logout")
def logout():
    session["logged_in"] = False
    return redirect("/")


# MAIN SECTION


@views.route("/profile")
def profile():
    return render_template("profile.html", title="Profile")
