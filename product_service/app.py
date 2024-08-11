from flask import Flask, jsonify, request
import psycopg2
import os
import time

app = Flask(__name__)

# PostgreSQL configurations from environment variables
DATABASE_HOST = os.getenv('DATABASE_HOST', 'postgres')
DATABASE_PORT = os.getenv('DATABASE_PORT', 5432)
DATABASE_USER = os.getenv('DATABASE_USER', 'user')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', 'password')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'product_db')

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

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cur.fetchone()
    cur.close()
    if product:
        return jsonify({"id": product[0], "name": product[1]}), 200
    else:
        return jsonify({"error": "Product not found"}), 404


@app.route('/products', methods=['GET'])
def get_products():
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    cur.close()
    return jsonify(products)

@app.route('/products', methods=['POST'])
def create_product():
    product = request.json
    cur = conn.cursor()
    cur.execute("INSERT INTO products (id, name, price) VALUES (%s, %s, %s)", (product['id'], product['name'], product['price']))
    conn.commit()
    cur.close()
    return jsonify({'success':'true'}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
