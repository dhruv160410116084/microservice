from flask import Flask, jsonify, request
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
DATABASE_NAME = os.getenv('DATABASE_NAME', 'order_db')

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

@app.route('/orders', methods=['GET'])
def get_orders():
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders")
    orders = cur.fetchall()
    cur.close()
    return jsonify(orders)

@app.route('/orders', methods=['POST'])
def create_order():
    order = request.json
    user = requests.get(f'http://user_service:5001/users/{order["user_id"]}').json()
    product = requests.get(f'http://product_service:5002/products/{order["product_id"]}').json()
    if user and product:
        cur = conn.cursor()
        cur.execute("INSERT INTO orders (user_id, product_id, quantity) VALUES (%s, %s, %s)", (order['user_id'], order['product_id'], order['quantity']))
        conn.commit()
        cur.close()
        return jsonify(order), 201
    return jsonify({"error": "Invalid user or product"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
