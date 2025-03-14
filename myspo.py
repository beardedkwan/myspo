from services import spotify_requests as sr

spotify_client_secret = input("Client Secret: ")

token = sr.get_spotify_token(spotify_client_secret)
print(token)
