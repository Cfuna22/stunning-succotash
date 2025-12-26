import logging
from .extract_spotify import SpotifyExtractor
from .load_to_database import DatabaseLoader
import schedule
import time

logger = logging.getLogger(__name__)

def run_etl():
    """Run complete ETL pipeline"""
    logger.info('Start Spotify ETL Pipeline...')

    try:
        # EXTRACT
        extractor = SpotifyExtractor()

        # Get user profile
        profile = extractor.get_user_profile()

        resent_tracks = extractor.get_recent_played(limit=50)

        # TRANSFORM & LOAD
        loader = DatabaseLoader()

        if profile:
            loader.load_user_profile(profile)

        if not resent_tracks.empty:
            loader.load_tracks(resent_tracks)
            logger.info(f' Processed {len(recent_tracks)} tracks')
        else:
            logger.info('No recent tracks to process')

            loader.close()
            logger.info('ETL Pipeline completed successfully!')

    except Exception as e:
        logger.error(f'ETL Pipeline failed: {e}')

# Schedule to run daily
if __name__ == '__main__':
    # Run immediately
    run_etl()

    # Schedule to run daily at 2 AM
    schedule.every().day.at('02:00').do(run_etl)

    logger.info(' ETL schedular started (running daily at 2 AM)')

    while True:
        schedule.run_pending()
        time.sleep(60)
