import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseConfig:
    DB_HOST = 'localhost'
    DB_PORT = '5433'
    DB_NAME = 'spotify_data'
    DB_USER = 'postgres'
    DB_PASSWORD = 'postgres'

    @classmethod
    def get_connection_string(cls):
        return f"postgresql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"
