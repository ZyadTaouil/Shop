CREATE TABLE orders
(
    id      INTEGER      NOT NULL PRIMARY KEY AUTOINCREMENT,
    name    VARCHAR(255) NOT NULL,
    email   VARCHAR(255) NOT NULL,
    phone   VARCHAR(20)  NOT NULL,
    address TEXT         NOT NULL,
    notes   TEXT,
    user_id INTEGER      NOT NULL REFERENCES user (id)
);