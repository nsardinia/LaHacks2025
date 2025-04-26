import whisper
import os
import subprocess
from moviepy.editor import VideoFileClip
from pydub import AudioSegment


model = whisper.load_model("turbo")

def split_video(input_video, output_folder, clip_duration=10):
    video = VideoFileClip(input_video)
    video_duration = int(video.duration)
    os.makedirs(output_folder, exist_ok=True)

    clips = []
    for start_time in range(0, video_duration, clip_duration):
        end_time = min(start_time + clip_duration, video_duration)
        output_clip = os.path.join(output_folder, f"clip_{start_time}-{end_time}.mp4")
        video.subclip(start_time, end_time).write_videofile(output_clip, codec="libx264", audio_codec="aac")
        clips.append(output_clip)

    return clips

def extract_audio_from_video(video_file, audio_file):
    video = AudioSegment.from_file(video_file)
    video.export(audio_file, format="wav")

def transcribe_audio_whisper(audio_file):
    result = model.transcribe(audio_file)
    print(result["text"])
    return result["text"]

def process_video(input_video, output_folder):
    # Step 1: Split video into 30-second clips
    clips = split_video(input_video, output_folder)
    transcriptions = []

    # Step 2: Process each clip
    for clip in clips:
        audio_file = clip.replace(".mp4", ".wav")
        extract_audio_from_video(clip, audio_file)

        # Step 3: Transcribe audio from the clip
        transcription = transcribe_audio_whisper(audio_file)

        transcriptions.append({
            'clip': clip,
            'transcription': transcription
        })

        # Clean up the audio file after transcription
        os.remove(audio_file)

    return transcriptions

# Example usage
input_video = "./data/test_lecture.mp4"
output_folder = "output_clips"

transcriptions = process_video(input_video, output_folder) 

# Print or save transcriptions
for t in transcriptions:
    print(f"Transcription for {t['clip']}:\n{t['transcription']}\n")
