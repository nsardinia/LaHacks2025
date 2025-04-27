import whisper
import streamlit as st
import tempfile
import os
import json
import re
from moviepy.editor import VideoFileClip
# from dotenv import load_dotenv
from google import genai
from key import TOKEN

# Load environment variables
# load_dotenv()
api_key = TOKEN

# Initialize models
model = whisper.load_model("small")
client = genai.Client(api_key=api_key)

def extract_audio_segment(video_file, start_time, end_time, audio_file):
    video = VideoFileClip(video_file).subclip(start_time, end_time)
    audio = video.audio
    audio.write_audiofile(audio_file, codec='pcm_s16le')

def transcribe_audio_whisper(audio_file):
    result = model.transcribe(audio_file)
    return result["text"]

def process_video(input_video, clip_duration=10):
    video = VideoFileClip(input_video)
    video_duration = int(video.duration)
    transcriptions = []

    for start_time in range(0, video_duration, clip_duration):
        end_time = min(start_time + clip_duration, video_duration)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_audio:
            extract_audio_segment(input_video, start_time, end_time, tmp_audio.name)
            transcription = transcribe_audio_whisper(tmp_audio.name)
            transcriptions.append({
                'start_time': start_time,
                'end_time': end_time,
                'transcription': transcription
            })
            os.unlink(tmp_audio.name)
    return transcriptions

def send_to_gemini_for_tagging(transcriptions):
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

def parse_gemini_tags(response_text):
    tag_mapping = {}
    current_segment = None

    for line in response_text.strip().splitlines():
        segment_match = re.match(r"Segment\s*(\d+):", line)
        tag_match = re.match(r"-\s*tag:\s*'(.*?)',\s*score:\s*(\d+(?:\.\d+)?)", line)

        if segment_match:
            current_segment = int(segment_match.group(1)) - 1
            tag_mapping[current_segment] = []

        elif tag_match and current_segment is not None:
            tag = tag_match.group(1)
            score = float(tag_match.group(2))
            tag_mapping[current_segment].append({
                "tag": tag,
                "score": score
            })
    return tag_mapping

# Streamlit app
st.title("Video Auto-Tagging App 🌐")

uploaded_video = st.file_uploader("Upload a lecture or tutorial video", type=["mp4", "mov", "avi"])
clip_duration = st.slider("Clip duration (seconds)", min_value=5, max_value=60, value=10, step=5)

if uploaded_video:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_video:
        tmp_video.write(uploaded_video.read())
        tmp_video_path = tmp_video.name

    with st.spinner("Processing video and extracting audio clips..."):
        transcriptions = process_video(tmp_video_path, clip_duration)

    with st.spinner("Sending transcriptions to Gemini for tagging..."):
        gemini_response_text = send_to_gemini_for_tagging(transcriptions)
        tag_mapping = parse_gemini_tags(gemini_response_text)

    # Merge and display
    output = []
    for idx, t in enumerate(transcriptions):
        output.append({
            "video_path": tmp_video_path,
            "start_time": t["start_time"],
            "end_time": t["end_time"],
            "transcription": t["transcription"],
            "tags": tag_mapping.get(idx, [])
        })

    st.success("✅ Processing complete!")

    for segment in output:
        st.subheader(f"{segment['start_time']}s - {segment['end_time']}s")
        st.text(segment['transcription'])
        for tag in segment['tags']:
            st.write(f"**Tag:** {tag['tag']} | **Score:** {tag['score']}")

    # Save button
    if st.button("Save results as JSON"):
        with open("output_segments.json", "w") as f:
            json.dump(output, f, indent=4)
        st.success("Saved as output_segments.json")

    # --- New Search Feature ---
    st.header("🔎 Search for a Tag")
    search_query = st.text_input("Enter a tag to search for:")

    if search_query:
        matching_segments = []

        for segment in output:
            for tag in segment['tags']:
                if search_query.lower() in tag['tag'].lower():
                    matching_segments.append((segment, tag['score']))

        if matching_segments:
            # Sort matches by tag relevance score (descending)
            matching_segments.sort(key=lambda x: x[1], reverse=True)
            best_match = matching_segments[0][0]

            st.success(f"Found a matching segment from {best_match['start_time']}s to {best_match['end_time']}s!")
            
            st.video(best_match["video_path"], start_time=best_match["start_time"])
            st.text(best_match["transcription"])
            st.write(f"**Tags:** {[t['tag'] for t in best_match['tags']]}")
        else:
            st.warning("No matching tag found.")
