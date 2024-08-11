from flask import Flask, jsonify, request, render_template
import psycopg2
import os
import requests
import time

app = Flask(__name__)

# PostgreSQL configurations from environment variables
DATABASE_HOST = os.getenv('DATABASE_HOST', 'postgres')
DATABASE_PORT = os.getenv('DATABASE_PORT', 5432)
DATABASE_USER = os.getenv('DATABASE_USER', 'user')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', 'password')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'user_db')

# Service URLs
PRODUCT_SERVICE_URL = os.getenv('PRODUCT_SERVICE_URL', 'http://product_service:5002/products')
ORDER_SERVICE_URL = os.getenv('ORDER_SERVICE_URL', 'http://order_service:5003/orders')

def connect_to_db(retries=5, delay=5):
    while retries > 0:
        try:
            conn = psycopg2.connect(
                host=DATABASE_HOST,
                port=DATABASE_PORT,
                user=DATABASE_USER,
                password=DATABASE_PASSWORD,
                dbname=DATABASE_NAME
            )
            print("Connected to the database")
            return conn
        except psycopg2.OperationalError as e:
            print(f"Database connection failed: {e}")
            retries -= 1
            time.sleep(delay)
    raise Exception("Failed to connect to the database after several attempts.")

conn = connect_to_db()

@app.route('/')
def index():
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    cur.close()
    return render_template('index.html', users=users)

@app.route('/create_user', methods=['POST'])
def create_user():
    user = request.form
    cur = conn.cursor()
    cur.execute("INSERT INTO users (id, name) VALUES (%s, %s)", (user['id'], user['name']))
    conn.commit()
    cur.close()
    return jsonify({"status": "User created"}), 201

@app.route('/products')
def list_products():
    response = requests.get(PRODUCT_SERVICE_URL)
    products = response.json()
    return render_template('products.html', products=products)

@app.route('/orders')
def list_orders():
    response = requests.get(ORDER_SERVICE_URL)
    orders = response.json()
    return render_template('orders.html', orders=orders)

@app.route('/add_product', methods=['POST'])
def add_product():
    product = request.form
    response = requests.post(PRODUCT_SERVICE_URL, json={
        'id': product['id'],
        'name': product['name'],
        'price': product['price'],

    })
    return jsonify({"status": response.json().get("status")}), response.status_code

@app.route('/add_order', methods=['POST'])
def add_order():
    order = request.form
    response = requests.post(ORDER_SERVICE_URL, json={
        'id': order['id'],
        'product_id': order['product_id'],
        'quantity': order['quantity']
    })
    return jsonify({"status": response.json().get("status")}), response.status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
