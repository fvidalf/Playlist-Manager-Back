import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
import webbrowser
from urllib.parse import urlparse, parse_qs, urlencode, quote
import json


CLIENT_ID = "7ca6331c457a4891b197b09102a54843"
CLIENT_SECRET = "bb70f18a24104bd4b59d0203b06a9770"
REDIRECT_URI = "http://localhost:3000"
SCOPE = "playlist-read-private playlist-modify-private"
AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"

# Global variable to store the access token
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
    access_token = response.json().get('access_token')


def login():
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE
    }
    url = requests.Request('GET', AUTH_URL, params=params).prepare().url
    webbrowser.open(url)
    start_server()
    return access_token


if __name__ == "__main__":
    token = login()
    print(token)
