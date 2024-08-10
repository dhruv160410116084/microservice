-- Create user_db and users table
CREATE DATABASE user_db;
\connect user_db;
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

-- Create product_db and products table
CREATE DATABASE product_db;
\connect product_db;
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    price DECIMAL(10, 2)
);

-- Create order_db and orders table
CREATE DATABASE order_db;
\connect order_db;
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INT,
    product_id INT,
    quantity INT
);
