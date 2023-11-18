from flask import Blueprint, render_template, redirect, session

views = Blueprint("views", __name__)


@views.route("/")
def index():
    return render_template("index.html", title="Home")

# AUTH SECTION

@views.route("/signup")
def signup():
    return render_template("signup.html", title="Sign Up")


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