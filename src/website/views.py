from flask import Blueprint, render_template, redirect, flash, url_for
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.sql import func

from .externals import bcrypt
from .externals import db
from .forms.comment_form import CommentForm
from .forms.login_form import LoginForm
from .forms.signup_form import SignupForm
from .models.comment import Comment
from .models.movie import Movie
from .models.rating import Rating
from .models.users import Users

views = Blueprint("views", __name__)


@views.route("/")
def index():
    """Handles logic related to the index/home page"""
    recently_added = Movie.query.order_by(Movie.date_added).limit(10).all()

    # If no movies have reviews, show recently added instead
    if Rating.query.first() is not None:
        top_rated = (
            Movie.query.join(Rating)
            .group_by(Movie.id)
            .order_by(func.avg(Rating.rating))
            .limit(10)
            .all()
        )
    else:
        top_rated = recently_added

    return render_template(
        "index.html", title="Home", top=top_rated, recent=recently_added
    )


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

        return redirect(url_for("views.login"))

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
            return redirect(url_for("views.login"))

        login_user(user)

        return redirect(url_for("views.profile"))

    return render_template("login.html", title="Log In", form=login_form)


@views.route("/logout")
def logout():
    """Handles logic related to logging users out"""
    logout_user()
    return redirect(url_for("views.index"))


# MAIN SECTION


@views.route("/profile")
@login_required
def profile():
    """Handles logic related to the user's profile page"""
    return render_template("profile.html", title="Profile")


@views.route("/movie/<int:movie_id>", methods=["GET", "POST"])
def movie_info(movie_id):
    movie = Movie.query.get(movie_id)
    comments = Comment.query.filter_by(movie_id=movie_id).all()

    comment_form = CommentForm()

    if comment_form.validate_on_submit():
        comment = Comment(
            user_id=current_user.id,
            movie_id=movie_id,
            comment=comment_form.comment.data,
        )
        db.session.add(comment)
        db.session.commit()

        return redirect(url_for("views.movie_info", movie_id=movie_id))

    return render_template(
        "movie_info.html", movie=movie, comments=comments, form=comment_form
    )


# TEST SECTION


@views.route("/create_movies")
def create_movies():
    """Temporary view for creating example movies"""
    test1 = Movie(name="Test1", year=1962)
    test2 = Movie(name="Test2", year=1999)
    test3 = Movie(name="Test3", year=2012)

    rating = Rating(user_id=1, movie_id=4, rating=8)

    db.session.add(test1)
    db.session.add(test2)
    db.session.add(test3)
    # db.session.add(rating)
    db.session.commit()

    return redirect(url_for("views.index"))


@views.route("/delete_movies")
def delete_movies():
    """Temporary view for deleting example movies"""
    movies = Movie.query.all()
    for movie in movies:
        Rating.query.filter_by(movie_id=movie.id).delete()
        Comment.query.filter_by(movie_id=movie.id).delete()
        db.session.delete(movie)
    db.session.commit()

    return redirect(url_for("views.index"))
