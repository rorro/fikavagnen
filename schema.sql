CREATE TABLE if not exists users (
    id integer PRIMARY KEY,
    tea integer,
    coffee integer,
    thanks integer,
    thanks_at integer,
    no_thanks integer
);

CREATE TABLE if not exists usernames (
    id integer PRIMARY KEY,
    username varchar(100)
);
