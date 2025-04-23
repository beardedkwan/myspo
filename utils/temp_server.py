import http.server
import socketserver
import urllib.parse

PORT = 8888

class SpotifyAuthHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        code = params.get("code", [None])[0]

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<h1>Authorization complete. You can return to the terminal.</h1>")

        print(f"\nGot Spotify authorization code:\n{code}")
        self.server.auth_code = code

def get_spotify_auth_code():
    with socketserver.TCPServer(("localhost", PORT), SpotifyAuthHandler) as httpd:
        print(f"Listening at http://localhost:{PORT}/callback")
        print("Waiting for Spotify redirect...")
        httpd.handle_request()  # only handle ONE request
        return httpd.auth_code

# Usage:
auth_code = get_spotify_auth_code()
print(f"Authorization Code: {auth_code}")
