import spotipy, sqlite3, json, time, icecream
from spotipy.oauth2 import SpotifyClientCredentials
import os

# Replace these with your Spotify API credentials
SPOTIPY_CLIENT_ID = "2a552506817c47cb8c21b80d88c9d406"
SPOTIPY_CLIENT_SECRET = "09b1459c7a784014923af0de39a138d0"

# Authentication - without user login
auth_manager = SpotifyClientCredentials(
    client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET
)
sp = spotipy.Spotify(auth_manager=auth_manager)


def get_mood_input():
    moods = [
        "happy",
        "sad",
        "energetic",
        "calm",
        "focused",
        "romantic",
        "angry",
        "melancholic",
        "confident",
        "nostalgic",
        "chill",
        "inspired",
        "reflective",
        "lonely",
        "motivated",
        "playful",
        "anxious",
        "hopeful",
        "adventurous",
        "tired",
        "excited",
        "grateful",
        "rebellious",
        "curious",
        "optimistic",
        "celebratory",
        "heartbroken",
        "frustrated",
        "mysterious",
        "serene",
        "free-spirited",
        "silly",
        "disoriented",
    ]

    print("What mood are you in? Choose from the following:")
    i = 0
    for _mood in moods:
        i += 1
        print(i, _mood)

    mood = input("Enter your mood: ").lower()
    # print(mood)

    try:
        if mood in moods:
            return mood

        if mood.isdigit():
            mood_index = int(mood)
            mood = moods[mood_index - 1]

            return mood
    except Exception as err:

        print("Please choose the right number or type the mood.", err)
        # return get_mood_input()


# This function will connect to the Spotify API and get a playlist based on the mood.
def get_playlist_for_mood(mood):
    # Map moods to Spotify categories (you can customize this)

    mood_to_genre = {
        "happy": "pop",  # Upbeat, cheerful tunes with catchy rhythms
        "sad": "acoustic",  # Stripped-back acoustic sounds for emotional reflection
        "energetic": "electronic",  # High-energy, fast-paced beats like EDM or dance
        "calm": "ambient",  # Soothing, atmospheric music to relax
        "focused": "classical",  # Complex but non-intrusive music for concentration
        "romantic": "r&b",  # Smooth, soulful melodies with emotional depth
        "angry": "metal",  # Aggressive, loud, and intense music to channel emotions
        "melancholic": "indie",  # Thought-provoking, often introspective alternative sounds
        "confident": "hip-hop",  # Strong beats and lyrics to boost self-confidence
        "nostalgic": "retro",  # Throwback tunes from earlier decades, e.g., 80s or 90s
        "chill": "lo-fi",  # Relaxed, downtempo beats often used for background music
        "inspired": "indie folk",  # Acoustic-driven with storytelling and emotional depth
        "reflective": "jazz",  # Smooth, improvisational tunes for introspective moments
        "lonely": "blues",  # Deep, emotional music reflecting solitude and longing
        "motivated": "rock",  # Strong, driving rhythms for inspiration and motivation
        "playful": "funk",  # Groovy, lively tunes that are upbeat and fun
        "anxious": "trip-hop",  # A mix of electronic and hip-hop, often dark and moody
        "hopeful": "gospel",  # Uplifting, often spiritual music
        "adventurous": "world",  # Eclectic sounds from different cultures and countries
        "tired": "downtempo",  # Slower, mellow electronic music for unwinding
        "excited": "dance",  # High-energy, rhythmic music to boost excitement
        "lonely": "country",  # Ballads and storytelling tunes reflecting personal struggles
        "grateful": "soul",  # Warm, rich melodies with emotional resonance
        "rebellious": "punk",  # Raw, high-energy music with themes of defiance
        "curious": "experimental",  # Unconventional, avant-garde music for exploration
        "optimistic": "synthwave",  # Retro-futuristic electronic music with hopeful vibes
        "celebratory": "latin",  # Rhythmic, upbeat Latin music perfect for celebrations
        "heartbroken": "folk",  # Emotional and narrative-driven acoustic music
        "frustrated": "industrial",  # Harsh, mechanical sounds to express anger or frustration
        "mysterious": "psychedelic",  # Trippy, mind-bending sounds for deep contemplation
        "serene": "new age",  # Calming, meditative music for peace and serenity
        "free-spirited": "reggae",  # Laid-back, carefree tunes with rhythmic grooves
        "silly": "electro swing",  # Fun, upbeat tunes combining vintage swing with modern beats
        "disoriented": "drone",  # Slow, evolving soundscapes that create a hypnotic atmosphere
    }

    genre = mood_to_genre.get(mood, "pop")

    # Search for playlists related to the genre

    try:
        playlists = sp.search(q=f"genre:{genre}", type="playlist", limit=20)
        return playlists["playlists"]["items"]

    except Exception as er:
        return "Try decreased limit"


def get_playlist_tracks(playlist_link):
    # Extract playlist ID from the link
    playlist_id = playlist_link.split("/")[-1].split("?")[0]

    # Fetch the playlist tracks
    results = sp.playlist_tracks(playlist_id)

    # Iterate through the tracks and print song titles and artist names
    songs = []
    for item in results["items"]:
        try:
            track = item["track"]
            if track:  # Check if the track exists
                song_title = track["name"]
                artist_names = ", ".join(artist["name"] for artist in track["artists"])
                song = {"artist": artist_names, "title": song_title}
                songs.append(song)
        except Exception as e:
            print(e)

    return songs


def get_song_genre(song_name, artist_name=None):
    # Search for the song by name (and optionally by artist)
    query = song_name
    if artist_name:
        query += f" artist:{artist_name}"

    results = sp.search(q=query, type="track", limit=1)

    if results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        artist_id = track["artists"][0]["id"]
        artist_info = sp.artist(artist_id)

        # Get genres associated with the artist
        genres = artist_info.get("genres", [])

        if genres:
            print(
                f"Genres for {track['name']} by {track['artists'][0]['name']}: {', '.join(genres)}"
            )
        else:
            print(f"No genres found for {track['artists'][0]['name']}")
    else:
        print(f"No results found for song: {song_name}")


if __name__ == "__main__":
    # mood = get_mood_input()
    # playlists = get_playlist_for_mood(mood)

    # 'artist': 'James Gavin', 'title': 'All I Can Be'
    # print(f"Here are some playlists for your {mood} mood:\n")
    # for idx, playlist in enumerate(playlists):
    #     # print(playlist)
    #     print(f"{idx+1}. {playlist['name']} - {playlist['external_urls']['spotify']}")

    # r = get_playlist_tracks('https://open.spotify.com/playlist/6cGR8lJ2VPnaM9ePGPdhHI')

    # print(r)

    
    print(get_song_genre('Skinny Love', 'Bon Iver'))
