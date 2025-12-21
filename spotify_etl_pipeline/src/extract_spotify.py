import logging
from src.auth_spotify import *
import pandas as pd

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SpotifyExtractor:
    def __init__(self):
        self.sp = get_spotify_client()
        if not self.sp:
            raise ConnectionError('Failed to connect to Spotify API')

        def get_user_profile(self):
            """Get current user's profile info"""
            logger.info('Fetching user profile...')
            try:
                user = self.sp.current_user()
                profile_data = {
                    'user_id': user['id'],
                    'display_name': user['']
                }
