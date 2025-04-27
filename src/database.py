import sqlite3
from utils import Tag, Clip 
from typing import List
import json

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
            notes TEXT,
            tags TEXT,
            UNIQUE(video_path, start_time, end_time)
        )
''')

conn.commit()
conn.close()

# Save a clip to the database
def save_clips_to_db(clips):
    conn = sqlite3.connect('clips.db')
    c = conn.cursor()

    for clip in clips:
        tags_str = json.dumps(clip['tags'])

        # First try UPDATE
        c.execute('''
            UPDATE clips
            SET transcription = ?, notes = ?, tags = ?
            WHERE video_path = ? AND start_time = ? AND end_time = ?
        ''', (clip['transcription'], clip['notes'], tags_str, clip['video_path'], clip['start_time'], clip['end_time']))

        if c.rowcount == 0:
            # No existing row matched -> INSERT
            c.execute('''
                INSERT INTO clips (video_path, start_time, end_time, transcription, notes, tags)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (clip['video_path'], clip['start_time'], clip['end_time'], clip['transcription'], clip['notes'], tags_str))

    conn.commit()
    conn.close()

    print_all_clips()


def search_by_tag(tag_query: str) -> List[str]:
    conn = sqlite3.connect('clips.db')
    c = conn.cursor()

    c.execute('''
        SELECT video_path, tags
        FROM clips
        WHERE tags LIKE ?
    ''', ('%' + tag_query + '%',))

    results = c.fetchall()
    conn.close()

    video_paths = []

    for video_path, tags_str in results:
        # Assuming `tags_str` is a string representation of the list of tags
        try:
            # Convert the tags_str to a list of dictionaries (e.g., [{"tag": "funny", "score": 0.9}])
            tags = eval(tags_str)
        except:
            tags = []

        # Check if any tag matches the query and has a score, if so, add to the list
        if any(tag['tag'] == tag_query for tag in tags):
            # Sort by the highest tag score
            highest_score = max(tag['score'] for tag in tags if 'score' in tag)
            video_paths.append((video_path, highest_score))

    # Sort the video paths by the highest tag score in descending order
    video_paths.sort(key=lambda x: x[1], reverse=True)

    # Return only the video paths, sorted by highest score
    return [video_path for video_path, _ in video_paths]


def print_all_clips():
    conn = sqlite3.connect('clips.db')
    c = conn.cursor()

    # Fetch all rows from the clips table
    c.execute('''
        SELECT id, video_path, start_time, end_time, transcription, notes, tags
        FROM clips
    ''')

    rows = c.fetchall()
    conn.close()

    # Print each row
    for row in rows:
        id, video_path, start_time, end_time, transcription, notes, tags_str = row
        # Convert the tags_str back to a list of tags
        try:
            tags = json.loads(tags_str)
        except json.JSONDecodeError:
            tags = []

        # Print the clip details
        print(f"ID: {id}")
        print(f"Video Path: {video_path}")
        print(f"Start Time: {start_time}")
        print(f"End Time: {end_time}")
        print(f"Transcription: {transcription}")
        print(f"Notes: {notes}")
        print(f"Tags: {tags}")
        print("-" * 50)

def generate_cards():
    conn = sqlite3.connect('clips.db')
    c = conn.cursor()

    # Fetch all rows from the clips table
    c.execute('''
        SELECT id, video_path, start_time, end_time, transcription, notes, tags
        FROM clips
    ''')

    rows = c.fetchall()
    conn.close()

    return rows

def get_all_tag_names() -> List[str]:
    conn = sqlite3.connect('clips.db')
    c = conn.cursor()

    # Fetch all tags from the clips table
    c.execute('''
        SELECT tags
        FROM clips
    ''')

    rows = c.fetchall()
    conn.close()

    tag_names = set()

    for (tags_str,) in rows:
        if tags_str:
            try:
                tags = json.loads(tags_str)
            except json.JSONDecodeError:
                tags = []
            for tag in tags:
                if isinstance(tag, dict) and 'tag' in tag:
                    tag_names.add(tag['tag'])

    return list(tag_names)


#print(get_all_tag_names())

# Call this function to print all clips
print_all_clips()
