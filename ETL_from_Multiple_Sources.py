import pandas as pd
import requests
import json

class MultiSourceETL:
    def extract_from_csv(self, path):
        return pd.read_csv(path)

    def extract_from_excel(self, path):
        return pd.read_excel(path)

    def extract_from_api(self, url):
        response = requests.get(url)
        data = response.json()
        return pd.DataFrame(data)

    def transform_all(self, dataframes):
        """Combine and transform multiple dataframes"""
        # Combine
        combined = pd.concat(dataframes, ignore_index=True)

        # Standardize column names
        combined.columns = combined.columns.lower().str.replace(' ', '_')

        # Add sources tracking
        combined['etl_timestamp'] = pd.Timestamp.now()
        return combined

    def load_to_csv(self, df, path):
        df.to_csv(path, index=False)
        print(f'saved {len(df)} records to {path}')

etl = MultiSourceETL()
csv_data = etl.extract_from_csv('sale.csv')
excel_data = etl.extract_from_excel('sales.xlsx')
api_data = etl.extract_from_api('https://api.example.com/products')

all_data = etl.transform_all([csv_data, excel_data, api_data])
etl.load_to_csv(all_data, 'central_data.csv')
