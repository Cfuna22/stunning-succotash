import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config.spotify_config import SpotifyConfig
import logging

logger = logging.getLogger(__name__)

def get_spotify_client():
    """
    Create and return an authentication Spotify client
    This will open  browser window for first-time authentication
    After that, tokens are cached in .cache file
    """
    try:
        # Define the scopes (permissions) we need
        scope = [
            'user-read-private',
            'user-read-email',
            'user-top-read', # Read user's top tracks/artists
            'user-read-private', # Read private playlists
            'user-library-read' #Read saved tracks
        ]

        # Create Spotify OAuth object
        sp_oauth = SpotifyOAuth(
            client_id=SpotifyConfig.CLIENT_ID,
            client_secret=SpotifyConfig.CLIENT_SECRET,
            redirect_uri=SpotifyConfig.REDIRECT_URL,
            scope=' '.join(scope),
            cache_path='.spotify_cache' #Save token for reuse
        )

        # Get access token (opens browser if needed)
        token_info = sp_oauth.get_access_token(as_dict=True)

        if not token_info:
            logger.error('Failed to get access token')
            return None

            # Create Spotify client
            sp = spotipy.Spotify(auth=token_info['access_token'])

            # Test the connection
            user = sp.current_user()
            logger.info(f' Successfully connected to Spotify as: {user['display_name']}')

            return sp

    except Exception as e:
        logger.error(f' authentication failed: {e}')
        return None
