import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseConfig:
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME =('DB_NAME', 'spotify_data')
    DB_USER = ('DB_USER', 'postgres')
    DB_PASSWORD=('DB_PASSWORD', 'postgres')

    @classmethod
    def get_connection_string(cls):
        return f"postgresql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"
