import pandas as pd
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleETL:
    def __init__(self):
        logger.info('ETL started')

    def extract(self,file_path):
        """Extract data from file"""
        try:
            logger.info(f'Extract from {file_path}')
            return pd.read_csv(file_path)
        except FileNotFoundError:
            logger.error(f'File not found: {file_path}')
            return pd.DataFrame()

    def transform(self, df):
        """Clean the data"""
        if df.empty:
            logger.warning('No data to transform!')
            return df

            df_clean = df.copy()
            df_clean.columns = [col.lower().replace(' ', '_') for col in df_clean.columns]
            df_clean = df_clean.fillna('Unknown')

            logger.info(f'Transformed {len(df_clean)} records')
            return df_clean

    def load(self, df, output_path):
        """Save cleaned data"""
        if not df.empty:
            df.to_csv(output_path, index=False)
            logger.info(f'Saved to {output_path}')
        else:
            logger.warning('No data to save!')

# Usage
etl = SimpleETL()
data = etl.extract('data.csv')
cleaned = etl.transform('data')
etl.load(cleaned, 'output.csv')
