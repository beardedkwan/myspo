import os
from utils.env import load_env_file
from services import spotify_requests as sr
from services import spotify_auth as auth

load_env_file()

sr.get_playlists()
