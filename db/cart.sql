CREATE TABLE cart
(
    id         INTEGER,
    product_id INT(11) NOT NULL REFERENCES products(id),
    user_id    INTEGER NOT NULL REFERENCES user (id),
    quantity   INT(11) NOT NULL,
    PRIMARY KEY(id,product_id)
);
