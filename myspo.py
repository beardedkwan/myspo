import os
from utils.env import load_env_file
from services import spotify_requests as sr

load_env_file()
#os.getenv("SPOTIFY_CLIENT_ID")

sr.get_playlists()
