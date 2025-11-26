CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL UNIQUE,
    hash TEXT NOT NULL,
    );


CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER NOT NULL,
    objectID INTEGER NOT NULL,
    objectName TEXT,
    title TEXT,
    artistName TEXT,
    primaryImage TEXT,
    impressions TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

