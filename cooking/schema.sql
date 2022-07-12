-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS participant;
DROP TABLE IF EXISTS command;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE command(
id INTEGER PRIMARY KEY AUTOINCREMENT,
restaurant TEXT NOT NULL,
menu  TEXT NOT NULL,
command_day DATE  NOT NULL,
command_hour time  NOT NULL
);

CREATE TABLE participant(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
mail TEXT NOT NULL,
command_details TEXT NOT NULL,
command_id INTEGER NOT NULL,
 FOREIGN KEY (command_id) REFERENCES command (id)
);




