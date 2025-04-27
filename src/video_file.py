
import os
import re
import tempfile
from typing import List
import whisper
from moviepy.editor import VideoFileClip
from google import genai
import gemini
from gemini import PaddleProcessWords

# Load environment variables (API key for Gemini)
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("API_KEY")

# Initialize models
whisper_model = whisper.load_model("small")
client = genai.Client(api_key=api_key)
ai = gemini(api_key)

class VideoFileProcessor:
    def __init__(self, clip_duration=10):
        """
        Initialize a processor for handling complete video files.
        
        Parameters:
            - clip_duration: Duration of each clip in seconds
        """
        self.clip_duration = clip_duration
        
    def extract_audio_segment(self, video_file, start_time, end_time, audio_file):
        """
        Extracts an audio segment from a video file.
        """
        video = VideoFileClip(video_file).subclip(start_time, end_time)
        audio = video.audio
        if audio is not None:
            audio.write_audiofile(audio_file, codec='pcm_s16le', verbose=False)
            return True
        return False

    def process_video(self, video_path):
        """
        Process a complete video file by breaking it into clips and transcribing each one.
        
        Parameters:
            - video_path: Path to the video file
            
        Returns:
            - A list of clips with transcriptions and tags
        """
        clips = []
        
        try:
            # Get video duration
            video = VideoFileClip(video_path)
            video_duration = int(video.duration)
            
            # Process video in clips
            for start_time in range(0, video_duration, self.clip_duration):
                end_time = min(start_time + self.clip_duration, video_duration)
                
                # Extract audio segment
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_audio:
                    audio_path = tmp_audio.name
                    
                    # Extract audio
                    has_audio = self.extract_audio_segment(video_path, start_time, end_time, audio_path)
                    
                    if has_audio:
                        # Transcribe audio
                        transcription = self.transcribe_audio(audio_path)
                    else:
                        transcription = ""  # No audio to transcribe

                    frame = video.get_frame(end_time)
                    
        
                        
                    # Create clip object
                    clip = {
                        'video_path': video_path,
                        'start_time': start_time,
                        'end_time': end_time,
                        'transcription': transcription,
                        'notes': ai.process(PaddleProcessWords(frame)),
                        'tags': []
                    }
                    
                    clips.append(clip)
                    
                    # Clean up audio file
                    os.unlink(audio_path)
            
            # Get tags for all clips
            if clips:
                clips = self.tag_clips(clips)
                
            return clips
            
        except Exception as e:
            print(f"Error processing video: {e}")
            return []
        finally:
            # Make sure to close the video file
            if 'video' in locals():
                video.close()

    def transcribe_audio(self, audio_file):
        """
        Transcribe the audio using Whisper model.
        """
        result = whisper_model.transcribe(audio_file)
        return result["text"]

    def tag_clips(self, clips):
        """
        Send clips for tagging and update with the results.
        """
        # Step 1: Prepare transcriptions for tagging
        transcriptions = [
            {
                'start_time': clip['start_time'], 
                'end_time': clip['end_time'], 
                'transcription': clip['transcription']
            } 
            for clip in clips
        ]
        
        # Step 2: Send to Gemini for tagging
        gemini_response_text = self.send_to_gemini_for_tagging(transcriptions)
        
        # Step 3: Parse Gemini's tags and update clips
        clips = self.parse_gemini_tags(gemini_response_text, clips)
        
        return clips

    def send_to_gemini_for_tagging(self, transcriptions):
        """
        Send transcriptions to Gemini for tagging.
        """
        prompt = (
            "You are helping analyze segments of a lecture video.\n"
            "Each segment has a transcription.\n"
            "For each segment, suggest 1-3 SHORT tags that describe the main concepts.\n"
            "For each tag, assign a relevance score between 0.0 and 1.0.\n"
            "Format exactly like:\n"
            "Segment 1:\n"
            "- tag: 'example', score: 0.95\n"
            "...\n\n"
        )

        for idx, t in enumerate(transcriptions):
            prompt += f"Segment {idx+1} ({t['start_time']}s - {t['end_time']}s): {t['transcription']}\n\n"

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return response.text

    def parse_gemini_tags(self, response_text, clips):
        """
        Parse the response from Gemini for tags and update clips.
        """
        current_segment = None

        for line in response_text.strip().splitlines():
            segment_match = re.match(r"Segment\s*(\d+):", line)
            tag_match = re.match(r"-\s*tag:\s*'(.*?)',\s*score:\s*(\d+(?:\.\d+)?)", line)

            if segment_match:
                current_segment = int(segment_match.group(1)) - 1

            elif tag_match and current_segment is not None and current_segment < len(clips):
                tag = tag_match.group(1)
                score = float(tag_match.group(2))
                clips[current_segment]['tags'].append({
                    'tag': tag,
                    'score': score
                })

        return clips
    

