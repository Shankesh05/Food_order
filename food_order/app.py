from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database Initialization
def init_db():
    with sqlite3.connect('food_ordering.db') as conn:
        cur = conn.cursor()

        # Users Table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                name TEXT NOT NULL,
                address TEXT,
                phone TEXT,
                is_admin INTEGER DEFAULT 0
            )
        ''')

        # Insert Sample Users
        cur.execute("INSERT OR IGNORE INTO users (username, password, name, address, phone, is_admin) VALUES ('admin', 'admin123', 'Admin User', '123 Admin St', '9876543210', 1)")
        cur.execute("INSERT OR IGNORE INTO users (username, password, name, address, phone) VALUES ('user1', 'password1', 'John Doe', '456 Main St', '1234567890')")

        # Food Items Table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS food (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                rating REAL,
                image_url TEXT,
                stock INTEGER DEFAULT 10
            )
        ''')

        # Insert Sample Food Items
        food_items = [
            ('Paneer Butter Masala', 'Rich paneer curry in butter sauce', 250.00, 4.5, '/static/images/paneer.jpg', 20),
            ('Chicken Biryani', 'Spicy biryani with chicken', 300.00, 4.8, '/static/images/biryani.jpg', 15),
            ('Masala Dosa', 'Crispy dosa with spiced potato filling', 150.00, 4.6, '/static/images/dosa.jpg', 30),
            ('Rajma Chawal', 'Kidney beans curry with rice', 180.00, 4.3, '/static/images/rajma.jpg', 25),
            ('Chole Bhature', 'Spicy chickpeas with fried bread', 200.00, 4.7, '/static/images/chole.jpg', 18),
            ('Pav Bhaji', 'Spicy mashed vegetables with bread rolls', 170.00, 4.5, '/static/images/pav_bhaji.jpg', 22),
            ('Butter Chicken', 'Creamy chicken curry with spices', 320.00, 4.9, '/static/images/butter_chicken.jpg', 12),
            ('Dal Makhani', 'Slow-cooked black lentils in butter', 220.00, 4.4, '/static/images/dal_makhani.jpg', 20),
            ('Hyderabadi Dum Biryani', 'Fragrant rice with marinated meat', 350.00, 4.9, '/static/images/hyderabadi_biryani.jpg', 14),
            ('Veg Thali', 'Assorted Indian vegetarian meal', 280.00, 4.6, '/static/images/veg_thali.jpg', 19),
            ('Aloo Paratha', 'Stuffed flatbread with spiced potatoes', 120.00, 4.5, '/static/images/aloo_paratha.jpg', 25),
            ('Tandoori Chicken', 'Char-grilled marinated chicken', 340.00, 4.7, '/static/images/tandoori.jpg', 10),
            ('Gulab Jamun', 'Soft milk dumplings in sugar syrup', 90.00, 4.9, '/static/images/gulab_jamun.jpg', 30),
            ('Samosa', 'Crispy pastry filled with spiced potatoes', 50.00, 4.6, '/static/images/samosa.jpg', 40),
            ('Rasgulla', 'Spongy dessert soaked in syrup', 100.00, 4.8, '/static/images/rasgulla.jpg', 35),
            ('Fish Curry', 'Spiced fish cooked in a tangy sauce', 330.00, 4.7, '/static/images/fish_curry.jpg', 12),
            ('Mango Lassi', 'Refreshing mango yogurt drink', 130.00, 4.8, '/static/images/mango_lassi.jpg', 25),
            ('Chocolate Cake', 'Rich and moist chocolate cake', 250.00, 4.9, '/static/images/choco_cake.jpg', 15),
            ('Pizza Margherita', 'Classic cheese and tomato pizza', 400.00, 4.8, '/static/images/pizza.jpg', 12),
            ('Burger', 'Grilled burger with crispy fries', 230.00, 4.7, '/static/images/burger.jpg', 20),
            ('Pasta Alfredo', 'Creamy white sauce pasta', 290.00, 4.5, '/static/images/pasta.jpg', 18),
            ('Caesar Salad', 'Fresh greens with Caesar dressing', 180.00, 4.3, '/static/images/salad.jpg', 25),
            ('Momos', 'Steamed dumplings with spicy sauce', 120.00, 4.6, '/static/images/momos.jpg', 28),
            ('Falooda', 'Indian dessert with ice cream & vermicelli', 160.00, 4.8, '/static/images/falooda.jpg', 22),
        ]
        
        # Insert Data if Not Exists
        # Insert Data if Not Exists
        for food in food_items:
            cur.execute('''
                INSERT OR IGNORE INTO food (name, description, price, rating, image_url, stock)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', food)


        conn.commit()
        print("Food table created and sample data inserted successfully!")


        # Orders Table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                food_id INTEGER,
                address TEXT,
                phone TEXT,
                order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'Pending',
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (food_id) REFERENCES food(id)
            )
        ''')

        conn.commit()

init_db()

# Home Page: Display Food Items
@app.route('/')
def home():
    with sqlite3.connect('food_ordering.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM food')
        foods = cur.fetchall()
    return render_template('home.html', foods=foods)

@app.route('/check_duplicates')
def check_duplicates():
    with sqlite3.connect('food_ordering.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM food')
        foods = cur.fetchall()
        print(foods)  # Print food items in the console
    return "Check your console for duplicate entries."

@app.route('/check_food')
def check_food():
    with sqlite3.connect('food_ordering.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM food')
        foods = cur.fetchall()
    return f"Total Food Items: {len(foods)}<br>{foods}"



@app.route('/remove_duplicates')
def remove_duplicates():
    with sqlite3.connect('food_ordering.db') as conn:
        cur = conn.cursor()

        # Delete duplicate food records while keeping the first occurrence
        cur.execute('''
            DELETE FROM food
            WHERE id NOT IN (
                SELECT MIN(id)
                FROM food
                GROUP BY name, description, price, rating, image_url
            )
        ''')
        conn.commit()
    return "Duplicates removed successfully!"



# Signup Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        address = request.form['address']
        phone = request.form['phone']

        try:
            with sqlite3.connect('food_ordering.db') as conn:
                cur = conn.cursor()
                cur.execute('INSERT INTO users (username, password, name, address, phone) VALUES (?, ?, ?, ?, ?)', 
                            (username, password, name, address, phone))
                conn.commit()
                flash('Signup successful! Please log in.', 'success')
                return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists. Try again.', 'danger')
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with sqlite3.connect('food_ordering.db') as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
            user = cur.fetchone()

            if user:
                session['user_id'] = user[0]
                session['is_admin'] = user[6]

                flash('Login Successful!', 'success')

                # Redirect based on role (admin or user)
                if user[6] == 1:  # Admin role (assuming 1 means admin)
                    return redirect(url_for('admin_dashboard'))
                else:  # Regular user role
                    return redirect(url_for('food_details'))
            else:
                flash('Invalid Credentials!', 'danger')

    return render_template('login.html')

@app.route('/add_food', methods=['POST'])
def add_food():
    if not session.get('is_admin'):
        flash('Unauthorized Access!', 'danger')
        return redirect(url_for('login'))

    try:
        name = request.form['name']
        price = request.form['price']
        stock = request.form['stock']
        image_url = request.form['image_url']

        with sqlite3.connect('food_ordering.db') as conn:
            cur = conn.cursor()
            cur.execute('INSERT INTO foods (name, price, stock, image_url) VALUES (?, ?, ?, ?)',
                        (name, price, stock, image_url))
            conn.commit()

        flash('Food item added successfully!', 'success')
    except Exception as e:
        flash(f'Error: {e}', 'danger')

    # Redirect to admin dashboard
    return redirect(url_for('admin_dashboard'))


@app.route('/update_food/<int:food_id>', methods=['POST'])
def update_food(food_id):
    if not session.get('is_admin'):
        flash('Unauthorized Access!', 'danger')
        return redirect(url_for('login'))

    try:
        price = request.form['price']
        stock = request.form['stock']

        with sqlite3.connect('food_ordering.db') as conn:
            cur = conn.cursor()
            cur.execute('UPDATE foods SET price = ?, stock = ? WHERE id = ?', (price, stock, food_id))
            conn.commit()

        flash('Food item updated successfully!', 'success')
    except Exception as e:
        flash(f'Error: {e}', 'danger')

    return redirect(url_for('admin_dashboard'))


@app.route('/remove_food/<int:food_id>')
def remove_food(food_id):
    if not session.get('is_admin'):
        flash('Unauthorized Access!', 'danger')
        return redirect(url_for('login'))

    try:
        with sqlite3.connect('food_ordering.db') as conn:
            cur = conn.cursor()
            cur.execute('DELETE FROM foods WHERE id = ?', (food_id,))
            conn.commit()

        flash('Food item removed successfully!', 'success')
    except Exception as e:
        flash(f'Error: {e}', 'danger')

    return redirect(url_for('admin_dashboard'))


# Logout Route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('is_admin', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('home'))

# Initialize Cart in Session
@app.before_request
def initialize_cart():
    if 'cart' not in session:
        session['cart'] = []

# Add to Cart Route
@app.route('/add_to_cart/<int:food_id>', methods=['POST'])
def add_to_cart(food_id):
    try:
        with sqlite3.connect('food_ordering.db') as conn:
            cur = conn.cursor()
            cur.execute('SELECT id, name, price, stock, image_url FROM food WHERE id = ?', (food_id,))
            food = cur.fetchone()

        if not food:
            flash('Food item not found!', 'danger')
            return redirect(url_for('home'))

        cart = session.get('cart', [])

        # Check if item already exists in cart, update quantity
        for item in cart:
            if item['id'] == food_id:
                item['quantity'] += 1
                break
        else:
            if food[3] < 1:
                flash('Item is out of stock!', 'warning')
                return redirect(url_for('home'))

            cart.append({
                'id': food[0],
                'product_name': food[1],
                'price': food[2],
                'image_url': food[4],
                'quantity': 1
            })

        session['cart'] = cart
        session.modified = True
        flash('Item added to cart!', 'success')
    except Exception as e:
        flash(f'Error: {e}', 'danger')
    return redirect(url_for('home'))

# Cart Route
@app.route('/cart')
def cart():
    cart = session.get('cart', [])
    total_price = sum(item['price'] * item['quantity'] for item in cart)

    return render_template('cart.html', cart_items=cart, total_price=total_price)

# Update Cart Quantity
@app.route('/update_cart/<int:food_id>', methods=['POST'])
def update_cart(food_id):
    try:
        new_quantity = int(request.form.get('quantity', 1))
        if new_quantity < 1:
            new_quantity = 1

        cart = session.get('cart', [])

        for item in cart:
            if item['id'] == food_id:
                item['quantity'] = new_quantity
                break

        session['cart'] = cart
        session.modified = True
        flash('Cart updated successfully!', 'info')
    except Exception as e:
        flash(f'Error: {e}', 'danger')
    return redirect(url_for('cart'))

# Remove Item from Cart
@app.route('/remove_from_cart/<int:food_id>')
def remove_from_cart(food_id):
    try:
        cart = [item for item in session.get('cart', []) if item['id'] != food_id]
        session['cart'] = cart
        session.modified = True
        flash('Item removed from cart.', 'warning')
    except Exception as e:
        flash(f'Error: {e}', 'danger')
    return redirect(url_for('cart'))

# Checkout Route
# Checkout Route
@app.route('/checkout', methods=['POST', 'GET'])
def checkout():
    cart_items = session.get('cart', [])
    if not cart_items:
        return redirect(url_for('cart'))

    if request.method == 'POST':
        address = request.form.get('address')
        phone = request.form.get('phone')
        payment_mode = request.form.get('payment_mode')

        # Clear cart after successful order
        session.pop('cart', None)

        return render_template('order_success.html', address=address, phone=phone, payment_mode=payment_mode)

    return render_template('checkout.html', cart_items=cart_items)

# Order Success Route
@app.route('/order_success')
def order_success():
    return render_template('order_success.html')

@app.route('/products')
def products():
    return render_template('food_item.html')

# Food Detail and Order with Transaction
@app.route('/food/<int:food_id>', methods=['GET', 'POST'])
def food_detail(food_id):
    with sqlite3.connect('food_ordering.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM food WHERE id = ?', (food_id,))
        food = cur.fetchone()

        if request.method == 'POST':
            if 'user_id' not in session:
                flash('Please log in to place an order.', 'warning')
                return redirect(url_for('login'))

            user_id = session['user_id']
            address = request.form['address']
            phone = request.form['phone']

            # Transaction: Check Stock & Place Order
            try:
                conn.execute('BEGIN')
                cur.execute('SELECT stock FROM food WHERE id = ?', (food_id,))
                stock = cur.fetchone()[0]

                if stock > 0:
                    cur.execute('INSERT INTO orders (user_id, food_id, address, phone) VALUES (?, ?, ?, ?)',
                                (user_id, food_id, address, phone))
                    cur.execute('UPDATE food SET stock = stock - 1 WHERE id = ?', (food_id,))
                    conn.commit()
                    flash('Order placed successfully!', 'success')
                    return redirect(url_for('home'))
                else:
                    flash('Item is out of stock!', 'danger')
                    conn.rollback()
            except Exception as e:
                conn.rollback()
                flash('Error placing order. Try again.', 'danger')

    return render_template('food_detail.html', food=food)


@app.route('/routes')
def list_routes():
    output = []
    for rule in app.url_map.iter_rules():
        output.append(f"{rule.endpoint} -> {rule}")
    return "<br>".join(output)


# Admin Dashboard
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user_id' not in session or session.get('is_admin') != 1:
        flash('Access Denied. Admin only.', 'danger')
        return redirect(url_for('login'))

    with sqlite3.connect('food_ordering.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM users')
        users = cur.fetchall()

        cur.execute('SELECT * FROM food')
        foods = cur.fetchall()

        cur.execute('''
            SELECT orders.id, users.name, food.name, orders.address, orders.phone, orders.status
            FROM orders
            JOIN users ON orders.user_id = users.id
            JOIN food ON orders.food_id = food.id
        ''')
        orders = cur.fetchall()

    return render_template('admin_dashboard.html', users=users, foods=foods, orders=orders)

if __name__ == '__main__':
    app.run(debug=True)
