import sqlite3


class Database:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('db/database.db')
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    # Orders

    def create_order(self, name, email, phone, address, notes, user_id):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO orders "
                       "(name, email, phone, address, notes, user_id)"
                       " VALUES (?, ?, ?, ?, ?, ?)",
                       (name, email, phone, address, notes, user_id))
        connection.commit()
        cursor.close()

        return True

    def get_orders(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM orders")
        orders = cursor.fetchall()
        cursor.close()

        return orders

    # Cart

    def add_to_cart(self, product_id, user_id, quantity):
        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute("INSERT INTO cart (id, product_id, user_id, quantity) "
                       "VALUES (?, ?, ?, ?)",
                       (user_id, product_id, user_id, quantity,))
        connection.commit()
        cursor.close()

        return True

    def update_cart(self, cart_id, product_id, quantity):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE cart SET quantity=? WHERE id=? AND product_id=?",
            (quantity, cart_id, product_id))
        connection.commit()
        cursor.close()

        return True

    def remove_from_cart(self, product_id):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM cart WHERE product_id = ?",
                       (product_id,))
        connection.commit()
        cursor.close()

        return True

    def clear_cart(self, user_id):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM cart WHERE user_id=?", (user_id,))
        connection.commit()
        cursor.close()

        return True

    def get_cart_from_product(self, product_id):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM cart WHERE product_id=?", (product_id,))
        product = cursor.fetchone()
        cursor.close()

        return product

    def get_cart_items(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM cart")
        cart_items = cursor.fetchall()
        cursor.close()

        return cart_items

    # Products

    def get_products(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        cursor.close()

        return products

    def get_product(self, product_id):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM products WHERE id=?", (product_id,))
        product = cursor.fetchone()
        cursor.close()

        return product

    def get_product_price(self, product_id):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT price FROM products WHERE id=?", (product_id,))
        product = cursor.fetchone()
        cursor.close()

        return product

    # User

    def add_user(self, username, salt, password):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO user (username, salt, hashed_password) "
            "VALUES (?, ?, ?)",
            (username, salt, password))

        self.connection.commit()
        cursor.close()

    def get_user(self, username):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM user WHERE username = ?",
            (username,))
        user = cursor.fetchone()
        cursor.close()
        return user

    def check_username(self, username):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT username FROM user WHERE username = ? LIMIT 1",
            (username,))
        user = cursor.fetchone()
        cursor.close()
        return user

    def get_password(self, password):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT hashed_password FROM user WHERE hashed_password = ?",
            (password,))
        user = cursor.fetchone()
        cursor.close()
        return user

    def get_password_by_username(self, username):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT hashed_password FROM user WHERE username = ?",
            (username,))
        user = cursor.fetchone()
        cursor.close()
        return user

    # Sessions

    def save_session(self, id_session, username):
        connection = self.get_connection()
        connection.execute(("insert into sessions(id_session, user) "
                            "values(?, ?)"), (id_session, username))
        connection.commit()

    def delete_session(self, id_session):
        connection = self.get_connection()
        connection.execute(("delete from sessions where id_session=?"),
                           (id_session,))
        connection.commit()

    def get_session(self, id_session):
        cursor = self.get_connection().cursor()
        cursor.execute(("select user from sessions where id_session=?"),
                       (id_session,))
        data = cursor.fetchone()
        cursor.close()
        if data is None:
            return None
        else:
            return data[0]

    def close_connection(self):
        self.conn.close()
