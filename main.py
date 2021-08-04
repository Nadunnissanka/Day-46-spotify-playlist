from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

APP_CLIENT_ID = "ba79e1e44d534dfab38a61b8f4fa169a"
APP_CLIENT_SECRET = "df1b416b3ef1405185e9d8cda409500d"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=APP_CLIENT_ID,
        client_secret=APP_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)

date = input("Enter year month and day like to listen (Format: YYYY-MM-DD):- ")

response = requests.get(url=f"https://www.billboard.com/charts/hot-100/{date}")
billboard_web_page = response.text

soup = BeautifulSoup(billboard_web_page, "html.parser")

top_hundred_songs = soup.find_all(name="span", class_="chart-element__information__song")

user_id = sp.current_user()["id"]
top_hundred_songs_list = [song.getText() for song in top_hundred_songs]

song_uris = []
year = date.split("-")[0]
for song in top_hundred_songs_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
# print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)