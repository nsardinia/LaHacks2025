import asyncio
import websockets
import numpy as np
import cv2
import whisper
import tempfile
import os
import re
from gemini import PaddleProcessWords
import time
from typing import List
from moviepy.editor import VideoFileClip
from google import genai
import gemini
import csv
from key import TOKEN

# Load environment variables (API key for Gemini)
# from dotenv import load_dotenv
# load_dotenv()
api_key = TOKEN


# Initialize models
whisper_model = whisper.load_model("small")
client = genai.Client(api_key=api_key)
ai = gemini(api_key)

class StreamProcessor:
    def __init__(self, clip_duration=10, fps=30):
        """
        Initialize a stream processor for handling websocket video frames.
        
        Parameters:
            - clip_duration: Duration of each clip in seconds
            - fps: Frames per second of incoming video
        """
        self.clip_duration = clip_duration
        self.fps = fps
        self.frames_per_clip = clip_duration * fps
        self.current_frames = []
        self.clips = []
        self.start_time = time.time()  # Track when we started receiving frames
        self.frame_count = 0
        self.frame_counter = 0
        
    async def process_frame(self, frame_data):
        """
        Process an incoming frame from the websocket.
        
        Parameters:
            - frame_data: Binary data of the frame
        """
        # Convert binary data to OpenCV frame
        nparr = np.frombuffer(frame_data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Add frame to current buffer
        self.current_frames.append(frame)
        self.frame_count += 1
        self.frame_counter += 1

        # collect a single frame for processing 
        if frame_counter >= 100: 
            print("PROCESSING A FRAME")
            # this one processes the frame, 1/100 frames. not sure how long it takes
            ai.process(PaddleProcessWords(frame_data))
            frame_counter = 0
        
        # If we've collected enough frames for a clip, process it
        if len(self.current_frames) >= self.frames_per_clip:
            await self.process_clip()
            
    async def process_clip(self):
        """Process the current buffer of frames as a complete clip"""
        if not self.current_frames:
            return
            
        # Calculate timestamps for this clip
        clip_start_time = self.start_time + ((self.frame_count - len(self.current_frames)) / self.fps)
        clip_end_time = clip_start_time + self.clip_duration
        
        # Create a temporary video file from frames
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp_video:
            video_path = tmp_video.name
            
            # Create a VideoWriter object
            height, width = self.current_frames[0].shape[:2]
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            video_writer = cv2.VideoWriter(video_path, fourcc, self.fps, (width, height))
            
            # Write all frames to the video
            for frame in self.current_frames:
                video_writer.write(frame)
                
            video_writer.release()
        
        # Extract audio from the temporary video
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_audio:
            audio_path = tmp_audio.name
            
            # Extract audio using moviepy
            video = VideoFileClip(video_path)
            if video.audio is not None:  # Check if video has audio
                video.audio.write_audiofile(audio_path, codec='pcm_s16le', verbose=False)
                
                # Transcribe audio
                transcription = transcribe_audio_whisper(audio_path)
            else:
                transcription = ""  # No audio to transcribe
                
            # Create clip object
            clip = {
                'video_path': video_path,
                'start_time': clip_start_time,
                'end_time': clip_end_time,
                'transcription': transcription,
                'tags': []
            }
            
            self.clips.append(clip)
            
            # Clean up
            os.unlink(audio_path)
            
        # Reset frame buffer
        self.current_frames = []
        
        # If we have accumulated enough clips, send them for tagging
        if len(self.clips) >= 3:  # Arbitrary number, adjust as needed
            await self.tag_clips()
            
    async def tag_clips(self):
        """Send accumulated clips for tagging"""
        if not self.clips:
            return
            
        # Step 1: Prepare transcriptions for tagging
        transcriptions = [
            {
                'start_time': clip['start_time'], 
                'end_time': clip['end_time'], 
                'transcription': clip['transcription']
            } 
            for clip in self.clips
        ]
        
        # Step 2: Send to Gemini for tagging
        gemini_response_text = send_to_gemini_for_tagging(transcriptions)
        
        # Step 3: Parse Gemini's tags and update clips
        self.clips = parse_gemini_tags(gemini_response_text, self.clips)
        
        # Process the tagged clips (e.g., save to database, notify client, etc.)
        for clip in self.clips:
            print(f"Processed clip: {clip['start_time']:.2f}s - {clip['end_time']:.2f}s")
            print(f"Transcription: {clip['transcription']}")
            print(f"Tags: {clip['tags']}")
            print("---")
        
        # Clear buffer after processing
        self.clips = []
        
    async def finish(self):
        """Process any remaining frames and return all clips"""
        if self.current_frames:
            await self.process_clip()
        
        if self.clips:
            await self.tag_clips()

        all_process()
            
        return self.clips

def transcribe_audio_whisper(audio_file):
    """
    Transcribe the audio using Whisper model.
    """
    result = whisper_model.transcribe(audio_file)
    return result["text"]

def send_to_gemini_for_tagging(transcriptions):
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
        prompt += f"Segment {idx+1} ({t['start_time']:.2f}s - {t['end_time']:.2f}s): {t['transcription']}\n\n"

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    return response.text

def parse_gemini_tags(response_text, clips):
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

async def video_receiver(websocket):
    """
    Receive video frames from a websocket and process them.
    """
    print("Client connected")
    processor = StreamProcessor(clip_duration=10, fps=30)
    
    try:
        while True:
            # Receive frame data from websocket
            data = await websocket.recv()  # Binary JPEG image
            
            # Process the frame
            await processor.process_frame(data)
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Process any remaining frames
        final_clips = await processor.finish()
        print(f"Processed a total of {processor.frame_count} frames")


def all_process():
    #now we have the summary response
    ai.refine()
    #we have a refined array of strings
    a = len(ai.content)
    header= []
    for i in range(a):
        header.append((i+1, i*10, (i+1)*10))
    data = [header, ai.get_keywords(), ai.content]
    with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)