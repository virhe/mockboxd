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

-- SAMPLE DATA
INSERT INTO movie (name, year, description, genre) VALUES ('The Shawshank Redemption', 1994, 'Over the course of several years, two convicts form a friendship, seeking consolation and, eventually, redemption through basic compassion.', 'Drama');
INSERT INTO movie (name, year, description, genre) VALUES ('Avatar: The Way of Water', 2022, 'Jake Sully lives with his newfound family formed on the extrasolar moon Pandora. Once a familiar threat returns to finish what was previously started, Jake must work with Neytiri and the army of the Na''vi race to protect their home.', 'Action');
INSERT INTO movie (name, year, description, genre) VALUES ('The Godfather Part II', 1974, 'The early life and career of Vito Corleone in 1920s New York City is portrayed, while his son, Michael, expands and tightens his grip on the family crime syndicate.', 'Drama');
INSERT INTO movie (name, year, description, genre) VALUES ('Antz', 1998, 'A rather neurotic ant tries to break from his totalitarian society while trying to win the affection of the princess he loves.', 'Action');
INSERT INTO movie (name, year, description, genre) VALUES ('The Room', 2003, 'In San Francisco, an amiable banker''s seemingly perfect life is turned upside down when his deceitful fiancée embarks on an affair with his best friend.', 'Drama');
INSERT INTO movie (name, year, description, genre) VALUES ('Mr. Bean''s Holiday', 2007, 'Mr. Bean wins a trip to Cannes where he unwittingly separates a young boy from his father and must help the two reunite. On the way he discovers France, bicycling, and true love.', 'Comedy');

-- Admin
INSERT INTO rating (user_id, movie_id, rating) VALUES (1, 1, 5);
INSERT INTO rating (user_id, movie_id, rating) VALUES (1, 2, 3);
INSERT INTO rating (user_id, movie_id, rating) VALUES (1, 3, 4);
INSERT INTO rating (user_id, movie_id, rating) VALUES (1, 4, 2);
INSERT INTO rating (user_id, movie_id, rating) VALUES (1, 5, 5);
INSERT INTO rating (user_id, movie_id, rating) VALUES (1, 6, 4);

INSERT INTO watchlist (user_id, movie_id) VALUES(1, 1);
INSERT INTO watchlist (user_id, movie_id) VALUES(1, 2);
INSERT INTO watchlist (user_id, movie_id) VALUES(1, 3);
INSERT INTO watchlist (user_id, movie_id) VALUES(1, 4);
INSERT INTO watchlist (user_id, movie_id) VALUES(1, 5);
INSERT INTO watchlist (user_id, movie_id) VALUES(1, 6);

INSERT INTO comment (user_id, movie_id, comment) VALUES (1, 1, 'Much better than you would initially expect.');
INSERT INTO comment (user_id, movie_id, comment) VALUES (1, 2, 'Not good, not bad.');
INSERT INTO comment (user_id, movie_id, comment) VALUES (1, 3, 'Excellent but way too long.');
INSERT INTO comment (user_id, movie_id, comment) VALUES (1, 5, 'Simply THE greatest movie ever made.');

-- Users
INSERT INTO users (username, password, admin) VALUES ('bob', '$2b$12$blid7Gw50K3ohaHWTcICIuD2G6KJy9HQBRjXKEjcwznvJsIOgTjbi', FALSE);
INSERT INTO users (username, password, admin) VALUES ('alice', '$2b$12$blid7Gw50K3ohaHWTcICIuD2G6KJy9HQBRjXKEjcwznvJsIOgTjbi', FALSE);
INSERT INTO users (username, password, admin) VALUES ('matti', '$2b$12$blid7Gw50K3ohaHWTcICIuD2G6KJy9HQBRjXKEjcwznvJsIOgTjbi', FALSE);
INSERT INTO users (username, password, admin) VALUES ('teppo', '$2b$12$blid7Gw50K3ohaHWTcICIuD2G6KJy9HQBRjXKEjcwznvJsIOgTjbi', FALSE);

-- Bob
INSERT INTO rating (user_id, movie_id, rating) VALUES (2, 1, 1);
INSERT INTO rating (user_id, movie_id, rating) VALUES (2, 2, 1);
INSERT INTO rating (user_id, movie_id, rating) VALUES (2, 3, 1);

INSERT INTO watchlist (user_id, movie_id) VALUES(2, 1);
INSERT INTO watchlist (user_id, movie_id) VALUES(2, 2);
INSERT INTO watchlist (user_id, movie_id) VALUES(2, 3);

INSERT INTO comment (user_id, movie_id, comment) VALUES (2, 1, 'I hate this!');
INSERT INTO comment (user_id, movie_id, comment) VALUES (2, 2, 'I hate this more!');
INSERT INTO comment (user_id, movie_id, comment) VALUES (2, 3, 'I hate this the most!');

INSERT INTO follower (follower_id, followed_id) VALUES (2, 3);

-- Alice
INSERT INTO rating (user_id, movie_id, rating) VALUES (3, 1, 3);
INSERT INTO rating (user_id, movie_id, rating) VALUES (3, 2, 3);
INSERT INTO rating (user_id, movie_id, rating) VALUES (3, 6, 5);

INSERT INTO watchlist (user_id, movie_id) VALUES(3, 1);
INSERT INTO watchlist (user_id, movie_id) VALUES(3, 2);
INSERT INTO watchlist (user_id, movie_id) VALUES(3, 3);
INSERT INTO watchlist (user_id, movie_id) VALUES(3, 6);

INSERT INTO comment (user_id, movie_id, comment) VALUES (3, 1, 'It was fine.');
INSERT INTO comment (user_id, movie_id, comment) VALUES (3, 6, 'Loved it.');

INSERT INTO follower (follower_id, followed_id) VALUES (3, 2);
INSERT INTO follower (follower_id, followed_id) VALUES (3, 4);

-- Matti
INSERT INTO rating (user_id, movie_id, rating) VALUES (4, 1, 4);
INSERT INTO rating (user_id, movie_id, rating) VALUES (4, 2, 4);
INSERT INTO rating (user_id, movie_id, rating) VALUES (4, 4, 2);

INSERT INTO watchlist (user_id, movie_id) VALUES(4, 1);
INSERT INTO watchlist (user_id, movie_id) VALUES(4, 2);
INSERT INTO watchlist (user_id, movie_id) VALUES(4, 4);

INSERT INTO comment (user_id, movie_id, comment) VALUES (4, 2, 'I slept through the movie, had a nice dream though!');
INSERT INTO comment (user_id, movie_id, comment) VALUES (4, 4, 'Overhyped.');

INSERT INTO follower (follower_id, followed_id) VALUES (4, 2);
INSERT INTO follower (follower_id, followed_id) VALUES (4, 3);
INSERT INTO follower (follower_id, followed_id) VALUES (4, 4);

-- Teppo
INSERT INTO rating (user_id, movie_id, rating) VALUES (5, 2, 1);

INSERT INTO watchlist (user_id, movie_id) VALUES(5, 2);

INSERT INTO comment (user_id, movie_id, comment) VALUES (5, 2, 'BOOORRRRRRRIIIIIIIIIIIIING >:((((((');

INSERT INTO follower (follower_id, followed_id) VALUES (5, 1);
INSERT INTO follower (follower_id, followed_id) VALUES (5, 2);
INSERT INTO follower (follower_id, followed_id) VALUES (5, 4);
