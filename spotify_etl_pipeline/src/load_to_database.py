import psycopg2
from psycopg2.extras import execute_values
from config.database_config import DatabaseConfig
import logging

logger = logging.getLogger(__name__)

class DatabaseLoader:
    def __init__(self):
        self.connect = psycopg2.connect(
            host=DatabaseConfig.DB_HOST,
            port=DatabaseConfig.DB_PORT,
            database=DatabaseConfig.DB_NAME,
            user=DatabaseConfig.DB_USER,
            password=DatabaseConfig.DB_PASSWORD
        )
        self.cursor = self.connect.cursor()

    def load_user_profile(self, profile_data):
        """Load user profile to database"""
        try:
            query = """
                INSERT INTO users (user_id, display_name, email, country, followers, account_type)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (user_id)
                DO NOT UPDATE SET
                    display_name = EXCLUDED.display_name
                    email = EXCLUDED.email,
                    country = EXCLUDED.country,
                    followers = EXCLUDED.followers,
                    account_type = EXCLUDED.account_type,
                    updates_at = CURRENT_TIMESTAMP
            """
            self.cursor.execute(query, (
                profile_data['user_id'],
                profile_data['display_name'],
                profile_data['email'],
                profile_data['country'],
                profile_data['followers'],
                profile_data['account_type']
            ))
            self.connect.commit()
            logger.info(f' Loaded user: {profile_data['display_name']}')
            return True

        except Exception as e:
            logger.error(f' Failed to load user: {e}')
            self.connect.rollback()
            return False

    def load_tracks(self, tracks_df):
        """Load tracks data to database"""
        if tracks_df.empty:
            return 0

        try:
            # First, Load artists
            artists_data = []
            for _, row in tracks_df.iterrows():
                artists_data.append((row['artist_id'], row['artist_name']))

                if artists_data:
                    artists_query = """
                        INSERT INTO artists (artist_id, artist_name)
                        VALUES %s
                        ON CONFLICT (artist_id) DO NOTHING
                    """
                    execute_values(self.cursor, artists_query, artists_data)

                    # Then load tracks
                    tracks_data = []
                    for _, row in tracks_df.iterrows():
                        tracks_data.append((
                            row['track_id'],
                            row['track_name'],
                            row['artist_id'],
                            row['album_id'],
                            row['popularity'],
                            row['duration_ms'],
                            row['explicit'],
                            row['track_number'],
                            row['preview_url'],
                            row['spotify_url'],
                            row['album_image_url']
                        ))

                        tracks_query = """
                            INSERT INTO tracks (track_id, track_name, artist_id, album_id, popularity, duration_ms, explicit, track_number, preview_url, spotify_url, album_image_url)
                            VALUES %s
                            ON CONFLICT (track_id) DO NOTHING
                        """
                        execute_values(self.cursor, tracks_query, tracks_data)

                        self.connect.commit()
                        logger.info(f' Loaded {len(tracks_df)} tracks')
                        return len(tracks_df)

        except Exception as e:
            logger.error(f' Failed to load tracks: {e}')
            self.connect.rollback()
            return 0

    def close(self):
        """Close database connection"""
        self.cursor.close()
        self.connection.close()
