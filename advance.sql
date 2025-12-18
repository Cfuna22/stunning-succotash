-- 🚀 SQL & PYTHON DATA CENTRALIZATION BOOTCAMP: From Basic to Advanced
-- PART 1: SETTING UP OUR PRACTICE ENVIRONMENT
-- First, Let's Create a REAL Practice Database

-- -- 1. CREATE DATABASE (if you haven't already)
CREATE DATABASE centralization_practice;
\c centralization_practice; --Connect to it (PostgreSQL)

-- 2. Create our SOURCE tables (scattered data)
-- These represent data in different systems

-- SOURCE 1: Sales from MySQL (simulating)
CREATE TABLE source_sales_mysql (
    sale_id SERIAL PRIMARY KEY,
    sale_date TIMESTAMP,
    cust_id INT,
    prod_code VARCHAR(20),
    qty INT,
    unit_price DECIMAL(10, 2),
    disc DECIMAL(10, 2),
    disc DECIMAL(10, 2) DEFAULT 0,
    day_type VARCHAR(50),
    order_src VARCHAR(100)
);

-- SOURCE 2: Products from Excel (simulating)
CREATE TABLE source_products_excel (
    prod_code VARCHAR(20),
    prod_name VARCHAR(200),
    cat VARCHAR(50),
    subcat VARCHAR(50),
    cost DECIMAL(10, 2),
    supplier VARCHAR(100)
);

-- SOURCE 3: Customers from CRM (simulating)
CREATE TABLE source_customers_crm (
    cust_id INT PRIMARY KEY,
    cust_name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    city VARCHAR(50),
    signup_date DATE,
    status VARCHAR(20)
);


-- Insert into sales (MySQL source)
INSERT INTO source_sales_mysql (sale_date, cust_id, prod_code, qty, unit_price, disc, pay_type, order_src) VALUES
('2024-03-01 10:30:00', 101, 'LAP-001', 1, 1200.00, 50.00, 'CC', 'website'),
('2024-03-01 14:15:00', 102, 'PHN-002', 2, 800.00, 0.00, 'PAYPAL', 'mobile-app'),
('2024-03-02 09:45:00', 103, 'LAP-001', 1, 1200.00, 100.00, 'CREDIT_CARD', 'store'),
('2024-03-02 16:20:00', 101, 'PHN-002', 1, 800.00, 0.00, 'CC', 'website'),
('2024-03-03 11:10:00', 104, 'TAB-003', 3, 400.00, 60.00, 'DEBIT', 'web-portal'),
('2024-03-03 13:25:00', 105, 'LAP-001', 2, 1200.00, 200.00, NULL, 'mobile'),
('2024-03-04 15:40:00', 102, 'ACC-004', 5, 50.00, 25.00, 'CC', 'website'),
(NULL, 103, 'TAB-003', 1, 400.00, 0.00, 'PAYPAL', 'store');  -- NULL sale_date to test

-- Insert into products (Excel source)
INSERT INTO source_products_excel VALUES
('LAP-001', 'Laptop Pro', 'Electronics', 'Computers', 900.00, 'TechSupplier Inc.'),
('PHN-002', 'SmartPhone X', 'Electronics', 'Mobile', 600.00, 'PhoneCo'),
('TAB-003', 'Tablet Lite', 'Electronics', 'Tablets', 300.00, 'GadgetWorld'),
('ACC-004', 'Wireless Mouse', 'Electronics', 'Accessories', 30.00, 'AccessoryHub'),
('DESK-005', 'Office Desk', 'Furniture', 'Office', 200.00, 'FurnitureCo'),
('CHAIR-006', 'Ergonomic Chair', 'Furniture', 'Office', 150.00, 'ComfySeats');

-- Insert into customers (CRM source)
INSERT INTO source_customers_crm VALUES
(101, 'John Smith', 'john@email.com', '555-0101', 'New York', '2024-01-15', 'Active'),
(102, 'Maria Garcia', 'maria@email.com', '555-0102', 'Los Angeles', '2024-02-01', 'Active'),
(103, 'David Lee', 'david@email.com', NULL, 'Chicago', '2024-01-20', 'Active'),
(104, 'Sarah Johnson', 'sarah@email.com', '555-0104', 'Miami', '2024-02-10', 'Inactive'),
(105, 'Robert Chen', 'robert@email.com', '555-0105', 'Seattle', '2024-03-01', 'Active'),
(106, 'Lisa Wong', 'lisa@email.com', '555-0106', 'Boston', '2024-02-15', 'Active');


-- DIM_DATE: Time dimension (CRITICAL for all analysis!)
CREATE TABLE dim_date (
    date_id DATE PRIMARY KEY,
    year INT NOT NULL,
    quarter INT NOT NULL,
    month INT NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    day_of_month INT NOT NULL,
    day_of_week INT NOT NULL,
    day_name VARCHAR(20) NOT NULL,
    is_weekend BOOLEAN NOT NULL,
    is_holiday BOOLEAN DEFAULT FALSE,
    fiscal_year INT NOT NULL,
    fiscal_quarter INT NOT NULL
);

-- DIM_CUSTOMERS: All customer information
CREATE TABLE dim_customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20),
    city VARCHAR(50),
    status VARCHAR(20),
    signup_date DATE,
    total_orders INT DEFAULT 0,
    total_spent DECIMAL(12, 2) DEFAULT 0,
    last_order_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- DIM_PRODUCTS: All product information
CREATE TABLE dim_products (
    product_id SERIAL PRIMARY KEY,
    product_code VARCHAR(20) UNIQUE NOT NULL,
    product_name VARCHAR(200) NOT NULL,
    category VARCHAR(50) NOT NULL,
    subcategory VARCHAR(50),
    cost_price DECIMAL(10, 2) NOT NULL,
    retail_price DECIMAL(10, 2),
    supplier VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
);

-- DIM_CHANNELS: Where sales come from
CREATE TABLE dim_channels (
    channel_id SERIAL PRIMARY KEY,
    channel_name VARCHAR(50) UNIQUE NOT NULL,
    channel_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
);

-- DIM_PAYMENT_METHODS: How customers pay
CREATE TABLE dim_payment_methods (
    payment_id SERIAL PRIMARY KEY,
    payment_name VARCHAR(50) UNIQUE NOT NULL,
    payment_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Step 2: Create Fact Tables (The "What Happened")


-- FACT_SALES: The MAIN fact table
CREATE TABLE fact_sales (
    sale_id INT PRIMARY KEY,
    date_id DATE REFERENCES dim_date(date_id),
    customer_id INT REFERENCES dim_customers(customer_id),
    product_id INT REFERENCES dim_products(product_id),
    channel_id INT REFERENCES dim_channels(channel_id),
    payment_id INT REFERENCES dim_payment_methods(payment_id),
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    discount_amount DECIMAL(10, 2) DEFAULT 0,
    net_amount DECIMAL(10, 2) NOT NULL,
    cost_amount DECIMAL(10, 2) NOT NULL,
    profit_amount DECIMAL(10, 2) GENERATED ALWAYS AS (net_amount - cost_amount) STORED,
    created_by TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX idx_fact_sales_date ON fact_sales(date_id);
CREATE INDEX idx_fact_sales_customer ON fact_sales(customer_id);
CREATE INDEX idx_fact_sales_product ON fact_sales(product_id);

-- PART 3: COMPLEX SQL - Building the ETL Pipeline
-- Procedure 1: Populate Date Dimension (Smart Way)
-- sql
