import logging
from .auth_spotify import get_spotify_client
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
                    'display_name': user['display_name'],
                    'email': user.get('email', ''),
                    'country': user.get('country', ''),
                    'followers': user['followers']['total'] if 'followers' in user else 0,
                    'account_type': user.get('product', 'free'),
                }
                logger.info(f'Retrieved profile for: {profile_data['display_name']}')
                return profile_data
            except Exception as e:
                logger.error(f'Failed to get user profile: {e}')
                return None

    def get_top_tracks(self, time_range='short_term', limit=20):
        """
        Get user's top tracks
        
        Args:
            time_range: 'short_term' (4 weeks), 'medium_term' (6 months), 'long_term' (all time)
            limit: Number of tracks to fetch (max 50)
        """
        logger.info(f'Fetching top tracks ({time_range})...')
        try:
            top_tracks = self.sp.current_user_top_tracks(
                time_range=time_range,
                limit=limit
            )

            tracks_data = []
            for item in top_tracks['items']:
                track_info = {
                    'track_id': item['id'],
                    'track_name': item['name'],
                    'artist_id': item['artists'][0]['id'],
                    'artist_name': item['artists'][0]['name'],
                    'album_id': item['album']['id'],
                    'album_name': item['album']['name'],
                    'popularity': item['popularity'],
                    'duration_ms': item['duration_ms'],
                    'explicit': item['explicit'],
                    'track_number': item['track_number'],
                    'preview_url': item.get('preview_url', ''),
                    'spotify_url': item['external_urls']['spotify'],
                    'album_image_url': item['album']['images'][0]['url'] if item['album']['images'] else ''
                }
                tracks_data.append(track_info)

            logger.info(f'retrieved {len(tracks_data)} top tracks')
            return pd.DataFrame(tracks_data)
        except Exception as e:
            logger.error(f'Failed to get top tracks: {e}')
            return pd.DataFrame()

    def get_recent_played(self, limit=50):
        """Get recent played tracks"""
        logger.info(f'Fetching {limit} recently played tracks...')
        try:
            recent_tracks = self.sp.current_user_recently_played(limit=limit)

            played_data = []
            for item in recent_tracks['items']:
                track = item['track']
                played_at = item['played_at']

                played_ifo = {
                    'played_at': played_at,
                    'track_id': track['id'],
                    'track_name': track['name'],
                    'artist_id': track['artists'][0]['id'],
                    'artist_name': track['artists'][0]['name'],
                    'album_id': track['album']['id'],
                    'album_name': track['album']['name'],
                    'popularity': track['popularity'],
                    'duration_ms': track['duration_ms']
                }
                played_data.append(played_info)

            logger.info(f'Retrieved {len(played_data)} recently played tracks')
            return pd.DataFrame(played_data)

        except Exception as e:
            logger.error(f'Failed to get recently played tracks: {e}')
            return pd.DataFrame()

def test_extraction():
    """Test the extraction function"""
    print('Testing Spotify ETL Extraction...')
    print('=' * 50)

    try:
        extractor = SpotifyExtractor()

        # Get user profile
        profile = extractor.get_user_profile()
        if profile:
            print(f"👤 User: {profile['display_name']}")
            print(f"📍 Country: {profile['country']}")
            print(f"👥 Followers: {profile['followers']}")
            print(f"💎 Account: {profile['account_type']}")
            print()

        # Get top tracks
        top_tracks = extractor.get_top_tracks(time_range='short_term', limit=5)
        if not top_tracks.empty:
            print(' Your Top 5 Tracks This month:')
            for idx, row in top_tracks.iterrows():
                print(f' {idx+1}. {row['track_name']} - {row['artist_name']} (Popularity: {row['popularity']})')
                print()

                # Get recently played
                recent = extractor.get_recent_played(limit=3)
                if not recent.empty:
                    print(' Recently played:')
                    for idx, row in recent.iterrows():
                        print(f' {row['track_name']} - {row['artist_name']}')
                        print(f' {row['played_at']}')
                    print('=' * 50)
                    print(' Extraction test completed successfully')

    except Exception as e:
        print(f' Text failed: {e}')

if __name__ == '__main__':
    test_extraction()
