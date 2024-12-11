import requests
import json
from login import login
from lyricsgenius import Genius
from langdetect import detect
from utils.headers import get_headers
from utils.user import get_current_user_id
from dotenv import load_dotenv
import os

load_dotenv()
URL = os.getenv("SPOTIFY_URL")
GENIUS_TOKEN = os.getenv("GENIUS_TOKEN")

def get_current_user_playlists(token):
    headers = get_headers(token)
    response = requests.get(f"{URL}/me/playlists", headers=headers)
    return response.json()


def get_user_playlists(token, user_id):
    headers = get_headers(token)
    response = requests.get(f"{URL}/users/{user_id}/playlists", headers=headers)
    return response.json()


def get_playlist(token, playlist_id):
    headers = get_headers(token)
    response = requests.get(f"{URL}/playlists/{playlist_id}", headers=headers)
    response = response.json()
    # Keep getting the next page until there is no next page
    # Save current response, and extend the list with the next response
    current_response = response
    next_url = response["tracks"]["next"]

    while next_url:
        response = requests.get(next_url, headers=headers)
        response = response.json()
        current_response["tracks"]["items"].extend(response["items"])
        next_url = response["next"]
    return current_response


token = login()
user_id = get_current_user_id(token)

# This is urban blazing id
playlist_id = "1G0jSl6Jz8McCFJY81bPWn"
playlist = get_playlist(token, playlist_id)
# print(json.dumps(playlist, indent=4))


# Keep only the artists name, track name and uri
def filter_playlist(playlist):
    return [
        {
            "artist": track["track"]["artists"][0]["name"],
            "track": track["track"]["name"],
            "uri": track["track"]["uri"]
        }
        for track in playlist["tracks"]["items"]
    ]


filtered_playlist = filter_playlist(playlist)
# print(json.dumps(filtered_playlist, indent=4))


def get_lyrics(filtered_playlist):

    for track in filtered_playlist:
        try:
            genius = Genius(GENIUS_TOKEN)
            genius.remove_section_headers = True
            song = genius.search_song(track["track"], track["artist"], get_full_info=False)
            track["lyrics"] = song.lyrics
        except Exception as e:
            print(e)
            track["lyrics"] = None

    return filtered_playlist


songs_by_lang = {}
songs_by_lang["unknown"] = []
songs = get_lyrics(filtered_playlist)

for song in songs:
    try:
        detected_lang = detect(song["lyrics"])
        if detected_lang not in songs_by_lang:
            songs_by_lang[detected_lang] = [song]
        else:
            songs_by_lang[detected_lang].append(song)
    except Exception as e:
        print(e)
        songs_by_lang["unknown"].append(song)

# Save songs_by_lang to a file
with open("songs_by_lang.json", "w") as file:
    json.dump(songs_by_lang, file, indent=4)
