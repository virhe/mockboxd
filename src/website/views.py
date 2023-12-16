"""This module handles all the application views and their logic"""

from flask import Blueprint, render_template, redirect, flash, url_for, abort
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import text
from sqlalchemy.sql import func

from .externals import bcrypt
from .externals import db

from .forms.comment_form import CommentForm
from .forms.login_form import LoginForm
from .forms.signup_form import SignupForm
from .forms.rating_form import RatingForm
from .forms.add_movie_form import AddMovieForm
from .forms.search_movie_form import SearchMovieForm
from .forms.search_user_form import SearchUserForm
from .forms.follow_form import FollowForm
from .forms.unfollow_form import UnfollowForm

from .models.comment import Comment
from .models.movie import Movie
from .models.rating import Rating
from .models.users import Users
from .models.watchlist import Watchlist
from .models.follower import Follower

views = Blueprint("views", __name__)


@views.route("/")
def index():
    """Handles logic related to the index/home page"""
    recently_added = db.session.execute(
        text("SELECT * FROM movie ORDER BY date_added DESC LIMIT 10")
    ).fetchall()

    sql = text(
        """
        SELECT movie.id,
                movie.name,
                AVG(rating.rating) as average_ratings
        FROM movie
        JOIN rating ON movie.id = rating.movie_id
        GROUP BY movie.id, movie.name
        ORDER BY average_ratings DESC
        LIMIT 10
    """
    )

    top_rated = db.session.execute(sql).fetchall()

    return render_template(
        "index.html", title="Home", top=top_rated, recent=recently_added
    )


# MAIN SECTION


@views.route("/movies", methods=["GET", "POST"])
def movies():
    """Handles logic related to listing all movies"""
    all_movies = Movie.query.all()

    form = SearchMovieForm()

    if form.validate_on_submit():
        sql = text("SELECT * FROM movie WHERE name ILIKE :search")
        all_movies = db.session.execute(
            sql, {"search": f"%{form.name.data}%"}
        ).fetchall()

    return render_template(
        "movies.html",
        form=form,
        movies=all_movies,
        title="Movies",
    )


@views.route("/users", methods=["GET", "POST"])
def users():
    """Handles logic related to listing all users"""
    all_users = Users.query.all()

    form = SearchUserForm()

    if form.validate_on_submit():
        sql = text("SELECT * FROM users WHERE username ILIKE :search")
        all_users = db.session.execute(
            sql, {"search": f"%{form.name.data}%"}
        ).fetchall()

    return render_template(
        "users.html",
        form=form,
        users=all_users,
        title="Users",
    )


@views.route("/profile/", defaults={"user_id": None})
@views.route("/profile/<int:user_id>")
def profile(user_id):
    """Handles logic related to the user's profile page"""
    if user_id is None:
        user_id = current_user.id
        return redirect(url_for("views.profile", user_id=user_id))

    user = Users.query.get_or_404(user_id)
    follow_form = FollowForm() if current_user.is_authenticated else None
    unfollow_form = UnfollowForm() if current_user.is_authenticated else None

    # Check if current_user is already following the other user
    if current_user.is_authenticated:
        sql = text(
            "SELECT * FROM follower WHERE follower_id = :follower_id AND followed_id = :followed_id"
        )
        already_following = db.session.execute(
            sql, {"follower_id": current_user.id, "followed_id": user_id}
        ).first()
    else:
        already_following = None

    # This query is ChatGPT generated
    watchlist = (
        db.session.query(Movie, Rating.rating)
        .outerjoin(Rating, (Rating.movie_id == Movie.id) & (Rating.user_id == user_id))
        .join(
            Watchlist, (Watchlist.movie_id == Movie.id) & (Watchlist.user_id == user_id)
        )
        .all()
    )

    return render_template(
        "profile.html",
        title="Profile",
        user=user,
        watchlist=watchlist,
        follow_form=follow_form,
        unfollow_form=unfollow_form,
        following=already_following,
    )


@views.route("/follow/<int:user_id>", methods=["GET", "POST"])
def follow_user(user_id):
    """Handles logic related to following a user"""
    if not current_user.is_authenticated:
        return redirect(url_for("views.index"))

    if user_id == current_user.id:
        return redirect(url_for("views.profile", user_id=user_id))

    # Check if current_user is already following the other user
    if current_user.is_authenticated:
        sql = text(
            "SELECT * FROM follower WHERE follower_id = :follower_id AND followed_id = :followed_id"
        )
        if db.session.execute(
            sql, {"follower_id": current_user.id, "followed_id": user_id}
        ).first():
            return redirect(url_for("views.profile", user_id=user_id))

    follow = Follower(follower_id=current_user.id, followed_id=user_id)
    db.session.add(follow)
    db.session.commit()

    return redirect(url_for("views.profile", user_id=user_id))


@views.route("/unfollow/<int:user_id>", methods=["GET", "POST"])
def unfollow_user(user_id):
    """Handles logic related to unfollowing a user"""
    if not current_user.is_authenticated:
        return redirect(url_for("views.index"))

    if user_id == current_user.id:
        return redirect(url_for("views.profile", user_id=user_id))

    follow = Follower.query.filter_by(
        follower_id=current_user.id, followed_id=user_id
    ).first()

    # If current_user isn't following the user, return to profile page
    if not follow:
        return redirect(url_for("views.profile", user_id=user_id))

    db.session.delete(follow)
    db.session.commit()

    return redirect(url_for("views.profile", user_id=user_id))


@views.route("/movie/<int:movie_id>", methods=["GET", "POST"])
def movie_info(movie_id):
    """Handles logic related to each movie's info page"""
    movie = Movie.query.get_or_404(movie_id)
    comments = (
        db.session.query(Comment, Users)
        .join(Users, Comment.user_id == Users.id)
        .filter(Comment.movie_id == movie.id)
        .order_by(Comment.date_added.desc())
        .all()
    )

    rating_form = RatingForm()
    comment_form = CommentForm()

    # RATING SECTION

    # Calculates average rating for the movie rounded to two decimal places
    try:
        rating_avg = round(
            db.session.query(func.avg(Rating.rating))
            .filter(Rating.movie_id == movie_id)
            .scalar(),
            2,
        )
    except TypeError:
        rating_avg = "No ratings in database"

    if rating_form.validate_on_submit():
        old_rating = Rating.query.filter_by(
            user_id=current_user.id, movie_id=movie_id
        ).first()
        if old_rating:
            # Changes old review instead of making a new one
            old_rating.rating = rating_form.rating.data
        else:
            rating = Rating(
                user_id=current_user.id,
                movie_id=movie_id,
                rating=rating_form.rating.data,
            )
            db.session.add(rating)

            # Add to watchlist if it's not already on the list
            if not Watchlist.query.filter_by(
                    user_id=current_user.id, movie_id=movie_id
            ).first():
                entry = Watchlist(user_id=current_user.id, movie_id=movie_id)
                db.session.add(entry)

        db.session.commit()

        return redirect(
            url_for("views.movie_info", movie_id=movie_id, title=movie.name)
        )

    # COMMENTING SECTION

    if comment_form.validate_on_submit():
        comment = Comment(
            user_id=current_user.id,
            movie_id=movie_id,
            comment=comment_form.comment.data,
        )
        db.session.add(comment)
        db.session.commit()

        return redirect(
            url_for("views.movie_info", movie_id=movie_id, title=movie.name)
        )

    return render_template(
        "movie_info.html",
        movie=movie,
        rating=rating_avg,
        comments=comments,
        rating_form=rating_form,
        comment_form=comment_form,
        title=movie.name,
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


# ADMIN SECTION


@views.route("/admin")
@login_required
def admin():
    """Handles logic related to admin control panel"""
    if not current_user.admin:
        abort(403)

    return render_template("admin/admin_panel.html", title="Admin Panel")


@views.route("/admin/add-movie", methods=["GET", "POST"])
@login_required
def add_movie():
    """Handles logic related to adding a movie to the database"""
    if not current_user.admin:
        abort(403)

    add_movie_form = AddMovieForm()
    if add_movie_form.validate_on_submit():
        movie = Movie(
            name=add_movie_form.name.data.capitalize(),
            year=add_movie_form.year.data,
            description=add_movie_form.description.data,
            genre=add_movie_form.genre.data,
        )
        db.session.add(movie)
        db.session.commit()
        flash(f"{add_movie_form.name.data} added to the database.")
        return redirect(url_for("views.add_movie"))

    return render_template(
        "admin/add_movie.html", form=add_movie_form, title="Add Movie"
    )


@views.route("/admin/search-movies", methods=["GET", "POST"])
@login_required
def search_movie():
    """Handles logic related to searching for a movie by name"""
    if not current_user.admin:
        abort(403)

    search_movie_form = SearchMovieForm()
    matching_names = []

    if search_movie_form.validate_on_submit():
        matching_names = Movie.query.filter(
            Movie.name.ilike(f"%{search_movie_form.name.data}%")
        ).all()

    return render_template(
        "admin/search_movie.html",
        form=search_movie_form,
        movies=matching_names,
        title="Delete Movie",
    )


@views.route("/admin/delete-movie/<int:movie_id>", methods=["GET", "POST"])
@login_required
def delete_movie(movie_id):
    """Handles logic related to deleting a movie from the database"""
    if not current_user.admin:
        abort(403)

    movie = Movie.query.get_or_404(movie_id)
    Watchlist.query.filter_by(movie_id=movie_id).delete()
    Rating.query.filter_by(movie_id=movie.id).delete()
    Comment.query.filter_by(movie_id=movie.id).delete()
    db.session.delete(movie)
    db.session.commit()

    flash(f"{movie.name} deleted from the database.")
    return redirect(url_for("views.search_movie"))
