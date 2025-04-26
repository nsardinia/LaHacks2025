import streamlit as st

backend_text = "Here is some AI generated summaries in-context"


def show_sidebar():
    # Using "with" notation
    with st.sidebar:
        add_summary = st.markdown(
        f"""
            <p>{backend_text}</p>
        """, unsafe_allow_html=True)

    # Custom box style using Markdown and HTML
    

        
        