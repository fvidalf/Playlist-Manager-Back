
from utils.headers import get_headers
import requests
from dotenv import load_dotenv
import os

load_dotenv()
URL = os.getenv("SPOTIFY_URL")


def get_current_user_id(token):
    headers = get_headers(token)
    response = requests.get(f"{URL}/me", headers=headers)
    return response.json()["id"]
