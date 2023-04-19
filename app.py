# Import flask_login and other modules
import hashlib
import uuid
from functools import wraps

from flask import Flask, render_template, request, redirect, flash, url_for, \
    g, session, Response

from database import Database

# Create app instance
app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'



def get_db():
    with app.app_context():
        db = getattr(g, '_database', None)
        if db is None:
            g.database = Database()
        return g.database


def authentication_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_authenticated(session):
            return send_unauthorized()
        return f(*args, **kwargs)

    return decorated


def is_authenticated(session):
    return "id" in session


def send_unauthorized():
    return Response('Could not verify your access level for that URL.\n'
                    'You have to login with proper credentials.', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'})


@app.route('/')
def index():
    # Get all products from database
    products = get_db().get_products()
    # Get id of user
    username = None
    if "id" in session:
        username = get_db().get_session(session["id"])
    # Render homepage template with products
    return render_template('home.html', products=products, username=username)


@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if not is_authenticated(session):
        return redirect("/login")
    else:
        username = get_db().get_session(session["id"])
        # Get the product from database by id
        product = get_db().get_product(product_id)
        if not product:
            return 404
        # Get the quantity from the form input
        quantity = int(request.form.get('quantity'))
        # Check if the quantity is valid
        if quantity < 1:
            # Flash an error message and redirect to homepage
            flash(f'Invalid quantity for {product[1]}', 'danger')
            return redirect('/')
        else:
            # Check if the product is already in cart
            cart_item = get_db().get_cart_from_product(product_id)
            if cart_item:
                # Update the quantity of the existing cart item
                q = cart_item[3] + quantity
                get_db().update_cart(cart_item[0], product_id, q)
            else:
                # Create a new cart item with the product and quantity
                get_db().add_to_cart(product_id, username, quantity)
            # Flash a success message and redirect to cart page
            flash(f'Added {product[1]} x {quantity} to cart', 'success')
            return redirect('/cart')


@app.route('/cart')
def cart():
    if not is_authenticated(session):
        return redirect('/login')
    # Get all cart items from database
    cart_items = get_db().get_cart_items()
    if len(cart_items) > 0:
        products = get_db().get_products()
        # Calculate the total price of the cart items
        total_price = 0
        for item in cart_items:
            product_price = get_db().get_product_price(item[1])
            quantity = item[3]
            total_price += product_price[0] * quantity
        return render_template('cart.html', cart_items=cart_items,
                               products=products, total_price=total_price)
    # Render cart template with cart items, products and total price
    return render_template('cart.html', cart_items=cart_items)



@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    cart_item = get_db().get_cart_from_product(product_id)
    product = get_db().get_product(product_id)
    get_db().remove_from_cart(product_id)
    # Flash a success message and redirect to cart page
    flash(f'Removed {product[1]} x {cart_item[3]} from cart',
          'success')
    return redirect("/cart")


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if not is_authenticated(session):
        return redirect("/login")
    # Check if the request method is POST
    if request.method == 'POST':
        # Get the form data from the request
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        notes = request.form.get('notes')
        # Validate the form data
        if not name or not email or not phone or not address:
            # Flash an error message and redirect to check out page
            flash('All fields except notes are required', 'danger')
            return redirect(url_for('checkout'))
        else:
            # Create a new order with the form data
            user = get_db().get_session(session['id'])
            get_db().create_order\
                (name, email, phone, address, notes, user[0])
            # Clear the cart items from database
            get_db().clear_cart(user[0])
            # Flash a success message and redirect to homepage
            flash('Your order has been placed successfully', 'success')
            return redirect('/')
    else:
        # Render checkout template with form
        return render_template('checkout.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Check if the request method is POST
    if request.method == 'POST':
        # Get the form data from the request
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        # Validate the form data
        if not username or not password or not confirm_password:
            # Flash an error message and redirect to signup page
            flash('Username and password are required', 'danger')
            return redirect(url_for('signup'))
        elif password != confirm_password:
            # Flash an error message and redirect to signup page
            flash('Passwords do not match', 'danger')
            return redirect('/signup')
        else:
            # Check if the username is already taken
            user = get_db().check_username(username)
            if user:
                # Flash an error message and redirect to signup page
                flash('Username already exists', 'danger')
                return redirect('/signup')
            else:
                # Create a new user with the form data and hashed password
                salt = uuid.uuid4().hex
                hashed_password = hashlib.sha512(
                    str(password + salt).encode("utf-8")).hexdigest()

                get_db().add_user(username, salt, hashed_password)
                id_session = uuid.uuid4().hex
                get_db().save_session(id_session, username)
                session["id"] = id_session
                # Flash a success message and redirect to login page
                flash('You have signed up successfully', 'success')
                return redirect('/')
    else:
        # Render signup template with form
        return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Check if the request method is POST
    if request.method == 'POST':
        # Get the form data from the request
        username = request.form.get('username')
        password = request.form.get('password')
        # Validate the form data
        if not username or not password:
            # Flash an error message and redirect to login page
            flash('Username and password are required', 'danger')
            return redirect('/login')
        else:
            # Get the user from database by username
            db_user = get_db().get_user(username)
            db_password = db_user[3]
            db_salt = db_user[2]
            hashed_password = hashlib.sha512\
                (str(password + db_salt).encode("utf-8")).hexdigest()
            # Check if the user exists and the password is correct
            if db_user[1] == username and db_password == hashed_password:
                id_session = uuid.uuid4().hex
                get_db().save_session(id_session, username)
                session["id"] = id_session
                # Flash a success message and redirect to orders page
                flash(f'Welcome back {db_user[1]}', 'success')
                return redirect('/')
            else:
                # Flash an error message and redirect to login page
                flash('Invalid username or password', 'danger')
                return redirect(url_for('login'))
    else:
        # Render login template with form
        return render_template('login.html')


@app.route('/logout')
@authentication_required
def logout():
    id_session = session["id"]
    session.pop('id', None)
    get_db().delete_session(id_session)
    # Flash a success message and redirect to homepage
    flash('You have logged out successfully', 'success')
    return redirect('/')


@app.route('/orders')
def orders():
    if not is_authenticated(session):
        return redirect('/login')
    # Get all orders from database
    orders = get_db().get_orders()
    # Render orders template with orders
    return render_template('orders.html', orders=orders)


# Run app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
