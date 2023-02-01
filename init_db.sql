PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- 表：keys
DROP TABLE IF EXISTS keys;

CREATE TABLE keys (
    id       INTEGER      NOT NULL,
    code     VARCHAR (20) NOT NULL,
    status   BOOLEAN,
    createDt DATETIME,
    activeDt DATETIME,
    PRIMARY KEY (
        id
    ),
    UNIQUE (
        code
    )
);


-- 表：students
DROP TABLE IF EXISTS students;

CREATE TABLE students (
    id       INTEGER      NOT NULL,
    name     VARCHAR (32) NOT NULL,
    password VARCHAR (32) NOT NULL,
    age      INTEGER,
    funds    FLOAT,
    addr     VARCHAR (32),
    honor    VARCHAR (32),
    PRIMARY KEY (
        id
    )
);


-- 表：users
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id       INTEGER      NOT NULL,
    username VARCHAR (32) NOT NULL,
    password VARCHAR (32) NOT NULL,
    PRIMARY KEY (
        id
    )
);

-- INSERT INTO users (id, username, password) VALUES (1, 'admin', 'pbkdf2:sha256:260000$QATHZPi94J4AGJ0b$84f963e7a846260b41c5b7f84744286a34689bfb7df950f8a4854d4219d9826f');

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
