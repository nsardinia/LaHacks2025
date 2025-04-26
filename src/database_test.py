# test_database.py
import unittest
from database import save_clips_to_db, search_by_tag
from utils import Clip  # Assuming the Clip class is defined in utils.py

class TestDatabaseFunctions(unittest.TestCase):

    def setUp(self):
        """Set up the database and clear it before each test."""
        # Optionally, clear the database before each test to avoid leftover data
        self.clear_database()

    def tearDown(self):
        """Clear the database after each test to maintain isolation."""
        self.clear_database()

    def clear_database(self):
        """Helper method to clear the clips table."""
        import sqlite3
        conn = sqlite3.connect('clips.db')
        c = conn.cursor()
        c.execute('DELETE FROM clips')  # Clear the clips table
        conn.commit()
        conn.close()

    def test_save_clips_to_db(self):
        """Test the functionality of saving clips to the database."""
        clip1 = Clip(
            video_path="video1.mp4",
            start_time=10,
            end_time=20,
            transcription="This is a test transcription.",
            tags=[{"tag": "test"}, {"tag": "clip"}]
        )

        clip2 = Clip(
            video_path="video2.mp4",
            start_time=30,
            end_time=40,
            transcription="Another test transcription.",
            tags=[{"tag": "demo"}, {"tag": "clip"}]
        )

        save_clips_to_db([clip1, clip2])

        # Check that the clips are in the database
        results = search_by_tag("clip")
        print("Results for 'clip' tag:")
        for result in results:
            print(result)
        self.assertGreater(len(results), 0, "No clips found with the tag 'clip'.")

    def test_search_by_tag(self):
        """Test the functionality of searching clips by tag."""
        clip1 = Clip(
            video_path="video1.mp4",
            start_time=10,
            end_time=20,
            transcription="This is a test transcription.",
            tags=[{"tag": "funny"}, {"tag": "clip"}]
        )

        clip2 = Clip(
            video_path="video2.mp4",
            start_time=30,
            end_time=40,
            transcription="Another test transcription.",
            tags=[{"tag": "serious"}, {"tag": "clip"}]
        )

        save_clips_to_db([clip1, clip2])

        # Search for a clip with the tag 'funny'
        results = search_by_tag("funny")
        print("Results for 'funny' tag:")
        for result in results:
            print(result)
        self.assertEqual(len(results), 1, "Failed to find the clip with the tag 'funny'.")

        # Search for a clip with a non-existent tag 'comedy'
        results = search_by_tag("comedy")
        print("Results for 'comedy' tag (should be empty):")
        for result in results:
            print(result)
        self.assertEqual(len(results), 0, "Should not find any clips with the tag 'comedy'.")

if __name__ == '__main__':
    unittest.main()
