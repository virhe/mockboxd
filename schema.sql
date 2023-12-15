CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(30) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    admin BOOLEAN DEFAULT FALSE NOT NULL
);

CREATE TABLE movie (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    year INTEGER,
    description TEXT NOT NULL,
    genre VARCHAR(255) NOT NULL,
    date_added TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE rating (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    movie_id INTEGER REFERENCES movie(id),
    rating INTEGER NOT NULL,
    date_added TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE comment (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    movie_id INTEGER REFERENCES movie(id),
    comment TEXT NOT NULL,
    date_added TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE watchlist (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    movie_id INTEGER REFERENCES movie(id),
    date_added TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE follower (
    id SERIAL PRIMARY KEY,
    follower_id INTEGER REFERENCES users(id) NOT NULL,
    followed_id INTEGER REFERENCES users(id) NOT NULL
);

INSERT INTO users (username, password, admin) VALUES ('admin', '$2b$12$blid7Gw50K3ohaHWTcICIuD2G6KJy9HQBRjXKEjcwznvJsIOgTjbi', TRUE);

INSERT INTO movie (name, year, description, genre) VALUES ('The Shawshank Redemption', 1994, 'Over the course of several years, two convicts form a friendship, seeking consolation and, eventually, redemption through basic compassion.', 'Drama');
INSERT INTO movie (name, year, description, genre) VALUES ('Avatar: The Way of Water', 2022, 'Jake Sully lives with his newfound family formed on the extrasolar moon Pandora. Once a familiar threat returns to finish what was previously started, Jake must work with Neytiri and the army of the Navi race to protect their home.', 'Action');
INSERT INTO movie (name, year, description, genre) VALUES ('The Godfather Part II', 1974, 'The early life and career of Vito Corleone in 1920s New York City is portrayed, while his son, Michael, expands and tightens his grip on the family crime syndicate.', 'Drama');

INSERT INTO rating (user_id, movie_id, rating) VALUES (1, 1, 5);
INSERT INTO rating (user_id, movie_id, rating) VALUES (1, 2, 3);
INSERT INTO rating (user_id, movie_id, rating) VALUES (1, 3, 4);

INSERT INTO watchlist (user_id, movie_id) VALUES(1, 1);
INSERT INTO watchlist (user_id, movie_id) VALUES(1, 2);
INSERT INTO watchlist (user_id, movie_id) VALUES(1, 3);

INSERT INTO comment (user_id, movie_id, comment) VALUES (1, 1, 'Much better than you would initially expect.');
INSERT INTO comment (user_id, movie_id, comment) VALUES (1, 2, 'Not good, not bad.');
INSERT INTO comment (user_id, movie_id, comment) VALUES (1, 3, 'Excellent but way too long.');