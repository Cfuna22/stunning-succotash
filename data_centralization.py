import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import os

def load_inventory_from_excel():
    """Load inventory data from Abel's excel file"""

    # Connect to central database
    engine = create_engine('postgres:user:pass@localhost/eco_central_warehouse')

    # step 1: Extract from excel
    excel_path = '/path/to/Abel_Inventory.xlsx'
    df = pd.read_excel(excel_path, sheet_name='Current_Stock')

    # step 2: Transform and clean
    df_clean = df.copy()

    # Standardize column names
    df_clean.columns = [col.lower().replace(' ', '_') for col in df_clean.columns]

    # Handle missing values
    df_clean['stock_level'] = df_clean['stock_level'].fillna(0)
    df_clean['reorder_level'] = df_clean['reorder_level'].fillna(10)

    # Add metadata
    df_clean['date_id'] = pd.Timestamp.today().date()
    df_clean['created_at'] = pd.Timestamp.now()

    # Step 3: Load to dimension table (products)
    df_products = df_clean[['product_id', 'product_name', 'category', 'cost_price', 'retail_price', 'supplier_id']].drop_duplicates()
    df_products.to_sql('dim_products', engine, if_exists='append', index=False)

    # Step 4: Load to fact table (inventory)
    df_inventory = df_clean[['date_id', 'product_id', 'stock_level', 'reorder_level', 'created_at']]
    df_inventory.rename(columns={'stock_level': 'ending_stock'}, inplace=True)

    df_inventory.to_sql('fact_inventory', engine, if_exists='append', index=False)

    print(f"Loaded {len(df_clean)} inventory records")





# Scenario 3: Extract from API (Web Analytics)
