import sqlite3
from utils import Tag, Clip 

# Create a connection (makes a file "clips.db")
conn = sqlite3.connect('clips.db')
c = conn.cursor()

# Create a table
c.execute('''
        CREATE TABLE IF NOT EXISTS clips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_path TEXT NOT NULL,
            start_time INTEGER NOT NULL,
            end_time INTEGER NOT NULL,
            transcription TEXT,
            tags TEXT,
            UNIQUE(video_path, start_time, end_time)
        )
''')

conn.commit()
conn.close()

# Save a clip to the database

def save_clips_to_db(clips: list[Clip]) -> None:
    conn = sqlite3.connect('clips.db')
    c = conn.cursor()

    for clip in clips:
        tags_text = ",".join([t['tag'] for t in clip['tags']])
        c.execute('''
            INSERT INTO clips (video_path, start_time, end_time, transcription, tags)
            VALUES (?, ?, ?, ?, ?)
        ''', (clip['video_path'], clip['start_time'], clip['end_time'], clip['transcription'], tags_text))

    conn.commit()
    conn.close()

def search_by_tag(tag_query):
    conn = sqlite3.connect('clips.db')
    c = conn.cursor()

    c.execute('''
        SELECT video_path, start_time, end_time, transcription, tags
        FROM clips
        WHERE tags LIKE ?
    ''', ('%' + tag_query + '%',))

    results = c.fetchall()
    conn.close()

    return results
