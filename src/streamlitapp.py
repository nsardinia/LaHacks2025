# main.py

import streamlit as st
import numpy as np
import tempfile
import pandas as pd
import os
from database import save_clips_to_db, get_all_tag_names, generate_cards
from google import genai
from key import TOKEN
# Import the sidebar from the other file
from sidebar import show_sidebar
from video_file import VideoFileProcessor

upload_dir = "videos"
os.makedirs(upload_dir, exist_ok = True)
VideoProcessor = VideoFileProcessor(10)

api_key = TOKEN

client = genai.Client(api_key=api_key)
def getBestTagFromGemini(userPrompt, tags):
        print("test")
        prompt = (
            "You are given a list of tags and a user query.\n"
            f"list of tags: {tags}, user query: {userPrompt}\n"
            "Return the tag that most closely aligns with the user query\n"
            "return the chosen tag name only for example: tag\n"
            
            "...\n\n"
        )

        print("test2")
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        print(response.text)
        return response.text   
def main():
    st.set_page_config(layout="wide")  # Wide layout

    # Layout: Left main content + Right sidebar
    col1, col2 = st.columns([4, 1], gap="large")

    with col1:
        videoslot = st.empty()
        uploaded_video = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi", "mkv"])

        # Display video player above upload button if video is uploaded
        if uploaded_video is not None:
            # Save the uploaded video temporarily
            vid = os.path.join(upload_dir, uploaded_video.name)
            with open(vid, 'wb') as f:
                f.write(uploaded_video.read())


            # Display the video above the upload button
            videoslot.video(vid)

            #processing the vide
            clips = VideoProcessor.process_video(vid)
            save_clips_to_db(clips)

            videoslot.empty()


        # Use a text_input to get the keywords to filter the dataframe
        text_search = st.text_input("Search videos by title or speaker", value="")
            
        # mock the video dataframe

        # List of lists (rows)
        dataVids = generate_cards()

        # Create DataFrame from list of lists
        df = pd.DataFrame(dataVids, columns=['id', 'video_path', 'start_time', 'end_time', 'transcription', 'notes',
                                              'tags'])
        
        # Filter the dataframe using masks
        if (text_search == ""):
            m2 = df["tags"].str.contains("")
        else:
            m2 = df["tags"].str.contains(str(getBestTagFromGemini(text_search, get_all_tag_names())).strip())
        df_search = df[m2]

        N_cards_per_row = 3

        for n_row, row in df_search.reset_index().iterrows():
            i = n_row%N_cards_per_row
            if i==0:
                st.write("---")
                cols = st.columns(N_cards_per_row, gap="large")
            # draw the card
            with cols[n_row%N_cards_per_row]:
                st.markdown(f"**{str(row['id']).strip()}**")
                st.markdown(f"*{row['tags'].strip()}*")
                st.markdown(f"**{str(row['start_time'])}**")




    with col2:
        show_sidebar()  # Sidebar imported from sidebar.py

if __name__ == "__main__":
    main()
