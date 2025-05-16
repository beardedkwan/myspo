import os
import http.client
import urllib.parse
import json
import base64
import time
from utils import debug
from dotenv import set_key
from utils.env import load_env_file

load_env_file()

def generate_auth_url():
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    redirect_uri = "http://localhost:8888/callback"
    scope = "playlist-read-private user-library-read user-read-playback-state user-modify-playback-state"

    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": scope,
        "show_dialog": "true"
    }

    auth_url = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode(params)
    print(auth_url)

def get_access_token():
    host = "accounts.spotify.com"
    endpoint = "/api/token"

    data = urllib.parse.urlencode({
        "grant_type": "authorization_code",
        "code": "AQAEKqEmzLo3LlNDy1e6J7AFVuiHwZ7qnQfNnaGIBcN9oTjRz5oxrV2Ce4zl_NENSoc4VnY3MIpOkz-kwe14wHs_E8NpYXdsfP2yIxIQRry1CrJAYEiyKz3PJe9CR4Bcymchr4aWCUOukpuA8VmTJjg5HUDTi7FkTbyqqRwwP42TUsohvFSa1FzcLRVnHHeUucjaVNJnS2E_fKbKjTTAU8j0oxtV-Gm78qSeMk4fOA0YTV9zdSohbmf5xIVc63ii4-5IrWBoU6ykkZBIBn68OzV9wCIHxrIhYkXa5RAUsH03lQ",
        "redirect_uri": "http://localhost:8888/callback",
    })

    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    auth_string = f"{client_id}:{client_secret}"
    auth_b64 = base64.b64encode(auth_string.encode("utf-8")).decode("utf-8")

    headers = {
        "Authorization": f"Basic {auth_b64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    conn = http.client.HTTPSConnection(host)

    conn.request("POST", endpoint, body=data, headers=headers)

    resp = conn.getresponse()

    token_dict = json.loads(resp.read().decode())

    conn.close()

    return token_dict

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

def refresh_access_token():
    host = "accounts.spotify.com"
    endpoint = "/api/token"

    data = urllib.parse.urlencode({
        "grant_type": "refresh_token",
        "refresh_token": os.getenv("SPOTIFY_REFRESH_TOKEN")
    })

    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    auth_string = f"{client_id}:{client_secret}"
    auth_b64 = base64.b64encode(auth_string.encode("utf-8")).decode("utf-8")

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {auth_b64}"
    }

    conn = http.client.HTTPSConnection(host)

    conn.request("POST", endpoint, body=data, headers=headers)

    resp = conn.getresponse()

    resp_body = resp.read()
    resp_code = resp.status
    resp_dict = {}

    debug.log(resp_code)
    debug.log(resp_body)

    if (resp_code == 200):
        resp_dict = json.loads(resp_body)

    conn.close()

    if resp_dict:
        set_key(".env", "SPOTIFY_ACCESS_TOKEN", resp_dict["access_token"])

        BUFFER = 5
        expires_in = float(resp_dict["expires_in"]) - BUFFER
        expire_date = time.time() + expires_in
        set_key(".env", "SPOTIFY_ACCESS_TOKEN_EXPIRES", str(expire_date))

        # left off here - expire date is not persisting in the .env file, resulting in refreshing the access token every call.
