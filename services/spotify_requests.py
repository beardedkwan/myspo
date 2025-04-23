import os
import http.client
import urllib.parse
import json
import base64
from .spotify_auth import refresh_access_token

def get_playlists():
    host = "api.spotify.com"
    endpoint = "/v1/me/playlists"

    token = os.getenv("SPOTIFY_ACCESS_TOKEN")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    conn = http.client.HTTPSConnection(host)

    conn.request("GET", endpoint, headers=headers)

    resp = conn.getresponse()
    print(resp.read().decode())
