import os
import http.client
import urllib.parse
import json

def generate_auth_url():
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    redirect_uri = "http://localhost:8888/callback"
    scope = "playlist-read-private user-library-read user-read-playback-state user-modify-playback-state"

    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": scope
    }

    auth_url = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode(params)
    print(auth_url)

def get_spotify_client_token(secret):
    host = "accounts.spotify.com"
    endpoint = "/api/token"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = urllib.parse.urlencode({
        "grant_type": "client_credentials",
        "client_id": "",
        "client_secret": secret
    })

    conn = http.client.HTTPSConnection(host)

    conn.request("POST", endpoint, body=data, headers=headers)

    resp = conn.getresponse()

    token_dict = json.loads(resp.read().decode())

    conn.close()

    return token_dict

def get_playlists(token):
    print(f"Access token: {token}")

    host = "api.spotify.com"
    endpoint = "/v1/me/playlists"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    conn = http.client.HTTPSConnection(host)

    conn.request("GET", endpoint, headers=headers)

    resp = conn.getresponse()
    print(resp.read().decode())
