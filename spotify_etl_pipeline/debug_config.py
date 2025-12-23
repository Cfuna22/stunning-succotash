import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

try:
    from config.spotify_config import SpotifyConfig
    print("✅ Successfully imported SpotifyConfig")
    print(f"CLIENT_ID length: {len(SpotifyConfig.CLIENT_ID) if SpotifyConfig.CLIENT_ID else 0} chars")
    print(f"CLIENT_SECRET length: {len(SpotifyConfig.CLIENT_SECRET) if SpotifyConfig.CLIENT_SECRET else 0} chars")
    print(f"REDIRECT_URI: {SpotifyConfig.REDIRECT_URI}")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    print("Current directory:", os.getcwd())
    print("Python path:", sys.path)
except Exception as e:
    print(f"❌ Other error: {e}")
