import http.client
import urllib.parse

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
    #print(resp.status, resp.reason)
    #print(resp.read().decode())

    access_token = resp.read().decode()

    conn.close()

    return access_token
