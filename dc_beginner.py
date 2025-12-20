import pandas as pd

sales_data = pd.read_csv('sales.csv')

sales_clean = sales_data.drop_duplicates()
sales_clean.columns = sales_clean.columns.str.lower()
sales_clean.fillna('0', inplace=True)

sales_clean.to_csv('cleaned_sales.csv', index=False)
