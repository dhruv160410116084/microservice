from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os
import time

app = Flask(__name__)

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

@app.route('/')
def index():
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    cur.close()
    return render_template('index.html', products=products)

@app.route('/add_product', methods=['POST'])
def add_product():
    product_id = request.form['id']
    name = request.form['name']
    price = request.form['price']
    cur = conn.cursor()
    cur.execute("INSERT INTO products (id, name, price) VALUES (%s, %s, %s)", (product_id, name, price))
    conn.commit()
    cur.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
