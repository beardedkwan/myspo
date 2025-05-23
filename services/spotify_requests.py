import os
import http.client
import urllib.parse
import json
import base64
from .spotify_auth import refresh_access_token
import time
from utils import debug
from utils.env import load_env_file
from utils.env import get_env_path
from dotenv import get_key

load_env_file()

def check_auth(func):
    def wrapper(*args, **kwargs):
        now = time.time()
        token_expires_str = get_key(get_env_path(), "SPOTIFY_ACCESS_TOKEN_EXPIRES")
        if token_expires_str:
            token_expires_str = token_expires_str.strip("\"'")

        try:
            token_expires = float(token_expires_str) if token_expires_str is not None else 0.0
        except ValueError:
            token_expires = 0.0

        debug.log({"now": now, "expires": float(token_expires)})

        if (now > float(token_expires)):
            debug.log("Refreshing access token...")
            refresh_access_token()

        return func(*args, **kwargs)

    return wrapper

@check_auth
def get_playlists():
    host = "api.spotify.com"
    endpoint = "/v1/me/playlists"

    token = get_key(get_env_path(), "SPOTIFY_ACCESS_TOKEN")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    conn = http.client.HTTPSConnection(host)

    conn.request("GET", endpoint, headers=headers)

    resp = conn.getresponse()

    code = resp.status
    data = {}

    if (code == 200):
        data = json.loads(resp.read())
    else:
        debug.log(resp.read())

    conn.close()

    return data
