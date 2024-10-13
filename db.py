from main import sqlite3, json, time

# Setup SQLite database
def setup_database(db_name='songs.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY,
            song_name TEXT,
            artist_name TEXT,
            album_name TEXT,
            cover_image TEXT,
            UNIQUE(song_name, artist_name)
        )
    ''')
    conn.commit()
    conn.close()

# Load data from JSON
def load_json_data(filename='recently_played_songs.json'):
    with open(filename, 'r') as json_file:
        return json.load(json_file)

# Insert new songs into SQLite database
def insert_new_songs(data, db_name='songs.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    for song in data:
        try:
            cursor.execute('''
                INSERT INTO songs (song_name, artist_name, album_name, cover_image)
                VALUES (?, ?, ?, ?)
            ''', (song['song_name'], song['artist_name'], song['album_name'], song['cover_image']))
        except sqlite3.IntegrityError:
            continue  # Skip if the song already exists

    conn.commit()
    conn.close()

# Check for new entries every minute
def check_for_new_entries():
    setup_database()
    
    while True:
        songs_data = load_json_data()
        insert_new_songs(songs_data)
        print("Checked for new entries and updated the database.")
        time.sleep(3)

if __name__ == '__main__':
    # setup_database()
    check_for_new_entries()