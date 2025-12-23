import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SpotifyConfig:
    # Get credentials from environment variables
    CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
    CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
    REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')

    # API endpoints
    AUTH_URL = 'https://accounts.spotify.com/authorize'
    TOKEN_URL = 'https://accounts.spotify.com/token'
    API_BASE_URL = 'https://api.spotify.com/v1'
