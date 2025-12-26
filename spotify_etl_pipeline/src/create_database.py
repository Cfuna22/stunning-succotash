import psycopg2
from config.database_config import DatabaseConfig
import logging

logger = logging.getLogger(__name__)

def create_tables():
    """Create all necessary tables for Spotify data"""

    connection = None
    try:
        # Connect to Postgres
        connection = psycopg2.connect(
            host=DatabaseConfig.DB_HOST,
            port=DatabaseConfig.DB_PORT,
            database=DatabaseConfig.DB_NAME,
            user=DatabaseConfig.DB_USER,
            password=DatabaseConfig.DB_PASSWORD
        )
        cursor = connection.cursor()

        # 1. Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user (
                user_id VARCHAR(255),
                email VARCHAR(255),
                country VARCHAR(20),
                followers INTEGER,
                account_type VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 2. Artists table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS artists (
                artists_id VARCHAR(255) PRIMARY KEY,
                artists_name VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 3. Albums table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS albums (
                album_id VARCHAR(255) PRIMARY KEY,
                album_name VARCHAR(255),
                artists_id VARCHAR(255) REFERENCES artists(artists_id),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 4. Tracks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tracks (
                track_id VARCHAR(255) PRIMARY KEY,
                track_name VARCHAR(255),
                artist_id VARCHAR(255) REFERENCES artists(artist_id),
                album_id VARCHAR(255) REFERENCES albums(album_id),
                popularity INTEGER,
                duration_ms INTEGER,
                explicit BOOLEAN,
                track_number INTEGER,
                preview_url TEXT,
                spotify_url TEXT,
                album_image_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 5. Listening history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS listening_history (
                id SERIAL PRIMARY KEY,
                user_id VARCHAR(255),
                track_id VARCHAR(255) REFERENCES tracks(track_id),
                played_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 6. Top tracks table (aggregated data)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS top_tracks (
                id SERIAL PRIMARY KEY,
                user_id VARCHAR(255),
                track_id VARCHAR(255) REFERENCES tracks(track_id),
                time_range VARCHAR(50),
                rank_position INTEGER,
                retrieved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        connection.commit()
        logger.info(' All tables created successfully!')

    except Exception as e:
        logger.error(f' Failed to create tables: {e}')
        if connection:
            connection.rollback()
    finally:
        if connection:
            cursor.close()
            connection.close()

if __name__ == '__main__':
    create_tables()
