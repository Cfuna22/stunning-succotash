CREATE DATABASE eco_central_warehouse;
USE eco_central_warehouse;

-- Enable time travel (for history analysis)
ALTER DATABASE eco_central_warehouse
SET DATA_RETENTION_TIME_IN_DAYS = 90;

-- DIM_CUSTOMERS
CREATE TABLE dim_customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    email VARCHAR(100),
    join_date DATE,
    customer_tier VARCHAR(30),
    city VARCHAR(50)
    country VARCHAR(50),
    total_orders INT DEFAULT 0,
    total_spent DECIMAL(10, 2) DEFAULT 0,
    last_order_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- DIM_PRODUCTS
CREATE TABLE dim_products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(200),
    category VARCHAR(50),
    subcategory VARCHAR(50),
    brand VARCHAR(50),
    cost_price DECIMAL(10, 2),
    retail_price DECIMAL(10, 2),
    supplier_id INT,
    in_stock BOOLEAN DEFAULT TRUE,
    created_by TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- DIM_DATE
CREATE TABLE dim_date (
    date_id DATE PRIMARY KEY,
    year INT,
    quarter INT,
    month INT,
    month_name VARCHAR(20)
    week INT,
    day_of_month INT,
    day_of_week INT,
    day_name VARCHAR(20)
    is_weekend BOOLEAN,
    is_holyday BOOLEAN,
    fiscal_year INT,
    fiscal_quarter INT
);

-- populate dim_date for 5 years
INSERT INTO dim_date
SELECT
    date_id,
    EXTRACT(YEAR FROM date_id) as year,
    EXTRACT(QUARTER FROM date_id) as quarter,
    EXTRACT(MONTH FROM date_id) as month,
    TO_CHAR(date_id, 'Month') as month_name,
    EXTRACT(WEEK FROM date_id) as week,
    EXTRACT(DAY FROM date_id) as day_of_month,
    EXTRACT(DOW FROM date_id) as day_of_week,
    TO_CHAR(date_id, 'Day') as day_name,
    EXTRACT(DOW FROM date_id) in (0, 6)as is_weekend,
    FALSE as is_holyday,
    CASE
        WHEN EXTRACT(MONTH FROM date_id) >= 7
        THEN EXTRACT(YEAR FROM date_id) + 1
        ELSE EXTRACT(YEAR FROM date_id)
    END as fiscal_year,
    CASE
        WHEN EXTRACT(MONTH FROM date_id) BETWEEN 7 AND 9 THEN 1
        WHEN EXTRACT(MONTH FROM date_id) BETWEEN 10 AND 12 THEN 2
        WHEN EXTRACT(MONTH FROM date_id) BETWEEN 1 AND 3 THEN 3
        WHEN EXTRACT(MONTH FROM date_id) BETWEEN 4 AND 6 THEN 4
    END as fiscal_quarter
FROM generate_series(
    '2020-01-01'::date,
    '2025-12-31'::date,
    '1 day'::interval
) AS date_id;

-- FACT_SALES
CREATE TABLE fact_sales (
    sale_id BIGINT PRIMARY KEY,
    date_id DATE REFERENCES dim_date(date_id),
    customer_id INT REFERENCES dim_customers(customer_id),
    product_id INT REFERENCES dim_products(product_id),
    quantity INT,
    unit_price DECIMAL(10, 2),
    total_amount DECIMAL(10, 2),
    discount_amount DECIMAL(10, 2) DEFAULT 0,
    net_amount DECIMAL(10, 2),
    payment_method VARCHAR(50),
    channel VARCHAR(50),
    region VARCHAR(50),
    created_at TIMESTAMP
);

-- fact_inventory
CREATE TABLE fact_inventory (
    inventory_id BIGINT PRIMARY KEY,
    date_id DATE REFERENCES dim_date(date_id),
    product_id DATE REFERENCES dim_products(date_id),
    beginning_stock INT,
    received_stock INT,
    sold_stock INT,
    ending_stock INT,
    stockout_stock INT,
    created_at TIMESTAMP
);

-- fact_web_analytic: Customer behavior
CREATE TABLE fact_web_analytic (
    session_id VARCHAR(100) PRIMARY KEY,
    date_id DATE REFERENCES dim_date(date_id)
    customer_id DATE REFERENCES dim_customers(customer_id)
    page_views INT,
    time_on_site INT,
    products_viewed TEXT[],
    cart_additions INT,
    purchases INT,
    bounce_rate DECIMAL(5, 2),
    device_type VARCHAR(50),
    traffic_source VARCHAR(100)
);

-- PART 4: ETL PROCESS - Bringing Data INTO Central System
-- Scenario 1: Extract from MySQL Sales Database


-- In our central warehouse, create a pipeline
CREATE OR REPLACE PROCEDURE load_sales_from_mysql()
LANGUAGE plpgsql
AS $$
BEGIN
    -- Step 1: Extract from MySQL (using FDW or similar)
    -- For simplicity, let's assume we have access

    -- step 2: Transform and Clean
    WITH cleaned_sales AS (
        SELECT
            s.sale_id,
            s.sale_date::date as date_id,
            s.customer_id,
            s.product_id,
            s.quantity,
            s.unit_price,
            -- Handle NULL discounts
            COALESCE(s.discount, 0) as discount_amount,
            -- Calculate net amount
            (s.quantity * s.unit_price - COALESCE(s.discount, 0)) as net_amount,
            -- Standardize payment methods
            CASE
                WHEN s.payment_type IN ('CC', 'CREDIT_CARD')
                THEN 'Credit Card'
                WHEN s.payment_type = 'PAYPAL'
                THEN 'PayPal'
                ELSE 'Other'
            END as payment_method,
            -- Extract channel from order source
            CASE
                WHEN s.order_source LIKE '%web%' THEN 'Website'
                WHEN s.order_source LIKE '%mobile%' THEN 'Mobile'
                WHEN s.order_source LIKE '%store%' THEN 'Store'
                ELSE 'Unknown'
            END as channel,
            s.created_at
        FROM mysql_sales.Sales s
        WHERE s.sale_date >= (SELECT MAX(date_is) FROM fact_sales)
        OR s.sale_date >= CURRENT_DATE - INTERVAL '7 days'
    )

    -- Step 3: Load into central fact table
    INSERT INTO fact_sales (
        sale_id, date_id, customer_id, product_id, quantity,
        unit_price, discount_amount, net_amount, payment_method,
        channel, created_at
    )
    SELECT * FROM cleaned_sales
    ON CONFLICT (sale_id)
    DO UPDATE SET
        quantity = EXCLUDED.quantity,
        unit_price = EXCLUDED.unit_price,
        discount_amount = EXCLUDED.discount_amount,
        net_amount = EXCLUDED.net_amount,
        updated_at = EXCLUDED.updated_at,

    -- Update customer totals
    UPDATE dim_customers c
    SET
        total_orders = sub.total_orders,
        total_spent = sub.total_spent,
        last_order_date = sub.last_order_date,
        updated_at = CURRENT_TIMESTAMP
    FROM (
        SELECT
        customer_id,
        COUNT(*) as total_orders,
        SUM(net_amount) as total_spent,
        MAX(date_id) as last_order_date
        FROM BY customer_id
    ) sub
    WHERE c.customer_id = sub.customer_id;

    RAISE NOTICE 'Sales data loaded successfully'
END;
$$;
