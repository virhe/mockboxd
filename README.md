# mockboxd
## Course project for "Databases and Web Programming" - University of Helsinki

This project aims to work as a social media for movie fans, similar to Letterboxd.
- Users will be able to add, remove, or edit reviews for movies and see other people's reviews.
- Users will be able to see information about movies.
- Users will be able follow other users.
- Users will be able to see a feed of activities from accounts they follow.
- An admin account can add or remove movies and moderate users and their activities (removing accounts, comments, etc.).

## Current state

- User signup and login are securely implemented (password hashing, CSRF protection, no SQL injection, no duplicates).
- Index lists top 10 rated and top 10 latest movies.
- Movies lists all movies in the database and has a search bar.
- Movie names are clickable and bring the user to the movie's info page.
- Info pages contain the movie's name, description, year, genre, average rating, as well as user comments.
- Usernames are clickable in the comments and bring the current user to the user's profile page.
- Profile pages contain the user's watchlist (movies the user has rated).
- Admin account login with username "admin" and password "admin"
- The admin account has access to an admin panel with the ability to add and delete movies.

## TODO

- Page with list of users
- Feed of activities from followed accounts
- Admin removal of accounts and comments
- UI improvements

## Usage

1. Create a postgresql database with the following command:
```SQL
CREATE DATABASE mockboxd;
```

2. Clone the repository to your local device:
```
git clone git@github.com:virhe/mockboxd.git
```

3. Cd into the folder and install dependencies with poetry
```
cd mockboxd
poetry install --without dev
```

4. Create database tables by importing schema.sql into the database called "mockboxd"
```
psql -U [USERNAME] mockboxd < schema.sql
```

5. Create a .env file in src/website/ with the following variables:
```
SECRET_KEY="[INSERT KEY HERE]"
DATABASE_URL=postgresql://[USERNAME]:[PASSWORD]@localhost:[PORT]/mockboxd
```

6. Start the app by running the following command within the mockboxd folder:
```
poetry run python src/app.py
```

7. Access website with this url:
```
127.0.0.1:5000
```

8. Admin panel can be accessed with
username
```admin```
password
```admin```