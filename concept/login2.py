import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
import webbrowser
from urllib.parse import urlparse, parse_qs, urlencode, quote
from dotenv import load_dotenv
import os
import json

load_dotenv()
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:3000"
SCOPE = "playlist-read-private playlist-modify-private"
AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"

access_token = None


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global access_token
        self.send_response(200)
        self.end_headers()
        query = urlparse(self.path).query
        code = parse_qs(query).get('code', None)
        if code:
            self.wfile.write(b"Login successful. You can close this window.")
            exchange_code_for_token(code[0])
        else:
            self.wfile.write(b"Failed to login.")


def start_server():
    server_address = ('', 3000)
    httpd = HTTPServer(server_address, RequestHandler)
    httpd.handle_request()


def exchange_code_for_token(code):
    global access_token
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    response = requests.post(TOKEN_URL, data=payload)
    print(json.dumps(response.json(), indent=4))
    access_token = response.json().get('access_token')


def login():
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE
    }
    # Ensure the scope parameter is correctly encoded to handle spaces
    encoded_params = urlencode(params, quote_via=quote)
    url = f"{AUTH_URL}?{encoded_params}"
    print(f"Opening {url} in your browser")
    webbrowser.open(url)
    start_server()
    return access_token


if __name__ == "__main__":
    token = login()
    print(token)
