drop table if exists users;

CREATE TABLE if not exists users (
    id integer PRIMARY KEY,
    tea integer,
    coffee integer,
    thanks integer,
    thanks_at integer
);
