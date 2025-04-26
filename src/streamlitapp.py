# main.py

import streamlit as st
import numpy as np
import tempfile
import pandas as pd


# Import the sidebar from the other file
from sidebar import show_sidebar


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
            tfile = tempfile.NamedTemporaryFile(delete=False)
            tfile.write(uploaded_video.read())

            # Display the video above the upload button
            videoslot.video(tfile.name)

        # Use a text_input to get the keywords to filter the dataframe
        text_search = st.text_input("Search videos by title or speaker", value="")
            
        # mock the video dataframe

        # List of lists (rows)
        dataVids = [
            [1, 'Intro', 23],
            [2, 'Kinematics', 30],
            [3, 'Quantam Mechanics', 35],
            [4, 'Thermodynamics', 40],
            [5, 'Electromagnetism', 45],
            [6, 'Fluid Dynamics', 50],
            [7, 'Optics', 55],
            [8, 'Nuclear Physics', 60],
            [9, 'Astrophysics', 65],
            [10, 'Quantum Computing', 70]
        ]

        # Create DataFrame from list of lists
        df = pd.DataFrame(dataVids, columns=['Timestamp', 'Topic', 'Rand'])

        # Filter the dataframe using masks
        m2 = df["Topic"].str.contains(text_search)
        df_search = df[m2]

        N_cards_per_row = 3

        for n_row, row in df_search.reset_index().iterrows():
            i = n_row%N_cards_per_row
            if i==0:
                st.write("---")
                cols = st.columns(N_cards_per_row, gap="large")
            # draw the card
            with cols[n_row%N_cards_per_row]:
                st.markdown(f"**{str(row['Timestamp']).strip()}**")
                st.markdown(f"*{row['Topic'].strip()}*")
                st.markdown(f"**{str(row['Rand'])}**")




    with col2:
        show_sidebar()  # Sidebar imported from sidebar.py

if __name__ == "__main__":
    main()
