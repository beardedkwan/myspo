import http.client
import urllib.parse
import json

def get_spotify_token(secret):
    host = "accounts.spotify.com"
    endpoint = "/api/token"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = urllib.parse.urlencode({
        "grant_type": "client_credentials",
        "client_id": "ca6300b771ea4ddd8a3d1406f9b76f68",
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
