CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT NOT NULL
);

INSERT INTO messages (message) VALUES ("Welcome to your DevOps Flask app!<br>Project was done by Tobi & Believe</br>");