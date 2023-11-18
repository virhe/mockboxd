import sqlite3
from flask import Flask
from .views import views


def create_db() -> None:
    """Creates needed database tables"""

    connection = sqlite3.connect("mockboxd.db")
    cursor = connection.cursor()

    users = """ CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username VARCHAR(30) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL
                ); """

    cursor.execute(users)

    movies = """ CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                year INTEGER NOT NULL,
                SCORE INTEGER
                ); """

    cursor.execute(movies)

    print("DB tables are ready")

    connection.commit()
    connection.close()


def create_flask_app():
    """Creates flask app"""

    app = Flask(__name__)
    print(type(app))

    app.register_blueprint(views)

    return app
