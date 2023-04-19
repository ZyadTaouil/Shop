CREATE TABLE products
(
    id          INT(11) NOT NULL PRIMARY KEY,
    title       VARCHAR(255)   NOT NULL,
    price       DECIMAL(10, 2) NOT NULL,
    description TEXT,
    image VARCHAR(255)
);