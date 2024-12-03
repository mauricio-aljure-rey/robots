# Time machine project.
# - Scrap: Get the list of most heard songs of a particular year.
# - Spotify: add them to a new playlist of spotify.
# - The user id, user secret must be set as environment variables
# SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET
# 

import tkinter
from tkinter import simpledialog
import requests
import bs4
import json
import spotipy
import os


def scrap_list(date_of_interest):
    # TODO: Write a function to scrap from the webpage with the year nuber given.
    link = "https://www.billboard.com/charts/hot-100/" + date_of_interest + "/"
    response = requests.get(link)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    playlist = soup.select('[class*="c-title a-no-trucate a-font-primary-bold-s"]')
    songs = [item.getText().strip() for item in playlist]
    print(songs)
    return songs


# Asking the user for year of interest
ROOT = tkinter.Tk()
ROOT.withdraw()
date_hits = tkinter.simpledialog.askstring(title="Hit songs search machine",
                                           prompt="Type the date you are interest at in YYYY-MM-DD format:")

# TODO: check the validity of the input given by the user. It most be a number with specific limits.
# Limit 1: lower than actual day.
# Limit 2: larger than the minimum allowed by the webpage.

# Getting the list of hits for that year.
hits_list = scrap_list(date_hits)

# ------------- Creating and populating the playlist --------------------#

user_id = os.environ.get("SPOTIPY_CLIENT_ID")
user_secret = os.environ.get("SPOTIPY_CLIENT_SECRET")

sp = spotipy.Spotify(
    auth_manager=spotipy.oauth2.SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=user_id,
        client_secret=user_secret,
        show_dialog=True,
        cache_path="token.txt"
    )
)
current_user = sp.current_user()["id"]
playlist = sp.user_playlist_create(user=current_user,
                                   name=f'Hits {date_hits}',
                                   public=False,
                                   collaborative=False
                                   )
tracks_uri = []
n = 0
for song_name in hits_list:
    song_data = sp.search(q=f"track: {song_name}", limit=1, type="track")
    if song_data["tracks"]["items"]:
        drilling = song_data["tracks"]["items"][0]
        tracks_uri.append(song_data["tracks"]["items"][0]["uri"])

sp.playlist_add_items(playlist_id=playlist["id"], items=tracks_uri)
