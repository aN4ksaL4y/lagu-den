from main import (
    SPOTIPY_CLIENT_SECRET,
    SPOTIPY_CLIENT_ID,
    spotipy,
    time,
    json
)
from spotipy.oauth2 import SpotifyOAuth
from main import icecream
from icecream import ic
import logging


logging.basicConfig(level=logging.DEBUG)

ic.DEFAULT_PREFIX = 'INI DEBUG |'
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri="http://127.0.0.1:3112",
        scope="user-read-recently-played",
        open_browser=False
    )
)

# Save data to JSON
def save_to_json(data, filename="recently_played_songs.json"):
    with open(filename, "w") as json_file:
        json.dump(data, json_file, indent=4)

# Fetch recently played songs
def get_recently_played(sp):

    ic()
    results = sp.current_user_recently_played(limit=5)  # Adjust limit as needed
    return results["items"]

# Main function
def main():
    while True:
        try:
            recent_songs = get_recently_played(sp)
            songs_data = []

            for item in recent_songs:
                track = item["track"]
                song_info = {
                    "song_name": track["name"],
                    "artist_name": ", ".join(
                        artist["name"] for artist in track["artists"]
                    ),
                    "album_name": track["album"]["name"],
                    "cover_image": (
                        track["album"]["images"][0]["url"]
                        if track["album"]["images"]
                        else None
                    ),
                }
                songs_data.append(song_info)
                print(
                    f"Song: {song_info['song_name']}, Artist: {song_info['artist_name']}, Album: {
                        song_info['album_name']}, Cover Image: {song_info['cover_image']}"
                )

            # Save the collected data to a JSON file
            save_to_json(songs_data)
            print("New entries saved!")

            time.sleep(5)
        except Exception as err:
                ic(err)


if __name__ == "__main__":
    main()
