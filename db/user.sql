CREATE TABLE user (
    id INTEGER PRIMARY KEY UNIQUE,
    username TEXT NOT NULL,
    salt VARCHAR(32) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL
);
