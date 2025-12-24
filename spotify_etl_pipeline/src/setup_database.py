import psycopg2
from config.database_config import DatabaseConfig
import logging

logger = logging.getLogger(__name__)

class DatabaseSetup:
    def __init__(self):
        self.connection = psycopg2.connect(
            host=DatabaseConfig.DB_HOST,
            port=DatabaseConfig.DB_PORT,
            database=DatabaseConfig.DB_NAME,
            user=DatabaseConfig.DB_USER,
            password=DatabaseConfig.DB_PASSWORD
        )
        self.cursor = self.connection.cursor()
        logger.info('Connected to PostgreSQL database')

    def create_tables(self):
        """Create all tables for Spotify ETL"""
        try:
            # Users table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id VARCHAR(255) PRIMARY KEY,
                    display_name VARCHAR(255),
                    email VARCHAR(255),
                    country VARCHAR(10),
                    followers INTEGER,
                    account_type VARCHAR(50),
                    etl_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(user_id)
                )
            """)
            
            # Artists table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS artists (
                    artist_id VARCHAR(255) PRIMARY KEY,
                    artist_name VARCHAR(255) NOT NULL,
                    etl_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(artist_id)
                )
            """)
            
            # Tracks table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS tracks (
                    track_id VARCHAR(255) PRIMARY KEY,
                    track_name VARCHAR(255) NOT NULL,
                    artist_id VARCHAR(255) REFERENCES artists(artist_id),
                    duration_ms INTEGER,
                    explicit BOOLEAN,
                    popularity INTEGER,
                    preview_url TEXT,
                    spotify_url TEXT,
                    etl_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(track_id)
                )
            """)
            
            # Listening history table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS listening_history (
                    history_id SERIAL PRIMARY KEY,
                    user_id VARCHAR(255),
                    track_id VARCHAR(255) REFERENCES tracks(track_id),
                    played_at TIMESTAMP NOT NULL,
                    context_type VARCHAR(100),
                    context_name VARCHAR(255),
                    etl_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Audio features table (for later when we add audio analysis)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS audio_features (
                    track_id VARCHAR(255) PRIMARY KEY REFERENCES tracks(track_id),
                    danceability DECIMAL(4,3),
                    energy DECIMAL(4,3),
                    key INTEGER,
                    loudness DECIMAL(5,3),
                    mode INTEGER,
                    speechiness DECIMAL(4,3),
                    acousticness DECIMAL(6,5),
                    instrumentalness DECIMAL(6,5),
                    liveness DECIMAL(4,3),
                    valence DECIMAL(4,3),
                    tempo DECIMAL(6,3),
                    duration_ms INTEGER,
                    time_signature INTEGER,
                    etl_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create indexes for better performance
            self.cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_listening_history_played_at 
                ON listening_history(played_at DESC)
            """)
            
            self.cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_listening_history_user_id 
                ON listening_history(user_id)
            """)
            
            self.connection.commit()
            logger.info(" All database tables created successfully!")
            
            # Show what we created
            self.cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """)
            tables = self.cursor.fetchall()
            print("\n Created Tables:")
            for table in tables:
                print(f"   • {table[0]}")

        except Exception as e:
            logger.error(f' Failed to create tables: {e}')
            self.connection.rollback()
            raise

    def close(self):
        """Close db connection"""
        self.cursor.close()
        self.connection.close()

def setup_database():
    """Main function to setup db"""
    print(' Setting up Spotify PostgreSQL Db...')
    print('=' * 50)

    try:
        db_setup = DatabaseSetup()
        db_setup.create_tables()
        db_setup.close()
        print('=' * 50)
        print(' Db setup completed successfully!')
        print('\nNext Steps:')
        print("1. Play some music on Spotify")
        print("2. Run: python -m src.extract_spotify")
        print("3. Load data: python src/setup_database.py")

    except Exception as e:
        print(f" Database setup failed: {e}")
        print("\nTroubleshooting:")
        print("• Is Docker running? (docker ps)")
        print("• Is PostgreSQL container started? (docker start spotify-postgres)")
        print("• Check .env file for correct credentials")

if __name__ == '__main__':
    setup_database()
