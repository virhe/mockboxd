# mockboxd
## Course project for "Databases and Web Programming" - University of Helsinki

This project aims to work as a social media for movie fans, similar to Letterboxd.
- Users will be able to add, remove, or edit reviews for movies and see other people's reviews.
- Users will be able to see information about movies.
- Users will be able to add friends.
- Users will be able to see a feed of their friends' activities.
- An admin account can add or remove movies and moderate users and their activities (removing accounts, comments, etc.).

## Current state

- User signup and login are securely implemented (password hashing, CSRF protection, no SQL injection, no duplicates).
- Only users who are logged in can access /profile.
- Index lists all movies in the database.
- Index has testing functions for adding and removing example movies; these update both the website and the database.

## Usage

1. Create a postgresql database with the following command:
```SQL
CREATE TABLE mockboxd;
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

4. Create a .env file in src/website/ with the following variables:
```
SECRET_KEY="[INSERT KEY HERE]"
DATABASE_URL=postgresql://[USERNAME]:[PASSWORD]@localhost:[PORT]/mockboxd
```

An example of the file contents:
```
SECRET_KEY="VerySecretKey"
DATABASE_URL=postgresql://user123:password123@localhost:5432/mockboxd
```

5. Start the app by running the following command within the mockboxd folder:
```
poetry run python src/app.py
```

6. Access website with this url:
```
localhost:5000
```