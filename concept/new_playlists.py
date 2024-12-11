
import json
import requests
from login2 import login
from utils.user import get_current_user_id
from utils.headers import get_headers
from dotenv import load_dotenv
import os

load_dotenv()
URL = os.getenv("SPOTIFY_URL")
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# Steps:
# 1. Read the songs_by_lang file.
# 2. Filter the songs by desired language.
# 3. Create a new playlist using the Spotify API.
# 4. Add the songs to the new playlist.

# Let's start by reading the songs_by_lang file.

with open("songs_by_lang.json", "r") as file:
    songs_by_lang = json.load(file)


def create_playlist_with_songs_in_language(songs_by_lang, language):
    # Filter the songs by the desired language
    songs = songs_by_lang.get(language, [])

    # Create a new playlist
    playlist_name = f"{language.capitalize()} Songs"
    playlist_description = f"Playlist with songs in {language}"

    token = login()
    user_id = get_current_user_id(token)

    headers = get_headers(token)
    payload = {
        "name": playlist_name,
        "description": playlist_description,
        "public": False
    }
    response = requests.post(f"{URL}/users/{user_id}/playlists", headers=headers, json=payload)
    response = response.json()
    print(json.dumps(response, indent=4))
    playlist_id = response["id"]
    print(f"Playlist created with id: {playlist_id}")

    # Add the songs to the new playlist
    uris = [song["uri"] for song in songs]
    # Split the uris into chunks of 80, as the API only allows 100 uris per request
    uris_chunks = [uris[i:i + 80] for i in range(0, len(uris), 80)]

    for uris_chunk in uris_chunks:
        payload = {
            "uris": uris_chunk
        }
        response = requests.post(f"{URL}/playlists/{playlist_id}/tracks", headers=headers, json=payload)
        print(response.json())


create_playlist_with_songs_in_language(songs_by_lang, "en")
