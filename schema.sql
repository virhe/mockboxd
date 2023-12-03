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