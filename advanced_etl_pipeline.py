import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text
import numpy as np
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s -%(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AdvancedETLPipeline:
    """Advanced ETL pipeline for data centralization"""

    def __init__(self, db_url: str):
        """
        Initialize the ETL pipeline

        Args:
            db_url: Database connection string
                    Example: 'postgresql://user:pass@localhost:5432/database'
        """
        self.db_url = db_url
        self.engine = create_engine()
        self.conn = self.engine.connect()
        logger.info("ETL Pipeline initialized")

    def extract_from_api(self, api_url: str, params: Optional[Dict] = None) -> pd.DataFrame:
        """
        Extract data from REST API

        Args:
            api_url: API endpoint URL
            params: Query parameters
            
        Returns:
            DataFrame with API data
        """
        try:
            import requests
            logger.info(f"Extract data from API: {api_url}")
            response = requests.get(api_url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()

            # Convert to DataFrame
            if 'data' in data:
                df = pd.DataFrame(data['data'])
            elif 'results' in data:
                df = pd.DataFrame(data['results'])
            else:
                df = pd.DataFrame(data)

            logger.info(f"Extracted {len(df)} records from API")
            return df

        except Exception as e:
            logger.error(f"API extraction failed: {e} raise")
            raise

        def extract_from_excel(self, file_path: str, sheet_name: str = None) -> pd.DataFrame:
            """
        Extract data from Excel with advanced error handling
        
        Args:
            file_path: Path to Excel file
            sheet_name: Specific sheet to read (None = all sheets)
            
        Returns:
            DataFrame with Excel data
        """
        try:
            logger.info(f"Extracting data from Excel: {file_path}")

            if sheet_name:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
            else:
                # Read all sheets and concatenate
                xls = pd.ExcelFile(file_path)
                sheet_data = []

                for sheet in xls.sheet_names:
                    sheet_df = pd.read_excel(file_path, sheet_name=sheet)
                    sheet_df['source_sheet'] = sheet
                    sheets_data.append(sheet_data, ignore_index=True)
                    logger.info(f"Extracted {len(df)} records from Excel")
                    return df
        except Exception as e:
            logger.error(f"Excel extraction failed: {e}")
            raise

        def transform_data(self, df: pd.DataFrame, rules: Dict) -> pd.DataFrame:
            """
            Transform data based on business rules
        
            Args:
                df: Raw DataFrame
                rules: Transformation rules dictionary

            Returns:
                Transformed DataFrame
            """
            logger.info("Starting data transformation")

            df_clean = df.copy()

            # 1. Standardize column names
            if 'column_mapping' in rules:
                df_clean.rename(columns=rules['column_mapping'], inplace=True)
                
