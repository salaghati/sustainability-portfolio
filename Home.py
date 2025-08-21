"""
Main Streamlit app - Portfolio landing page and About Me section.
"""
import streamlit as st
import base64
import os

st.set_page_config(
    page_title="Trinh Anh Tu - Portfolio",
    page_icon="👨‍💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Main Portfolio Page ---
st.title("Trinh Anh Tu - Data Analyst Portfolio")
st.markdown("""
Welcome! This application showcases my data analysis projects. Each project demonstrates a complete workflow from data fetching and cleaning to interactive visualization and insight generation. 
**Please use the sidebar to navigate through the projects.**
""")
st.markdown("---")

st.header("Projects")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Sustainability Social Media Analysis")
    st.markdown("""
        This project analyzes over 3,000 social media posts related to sustainability to uncover engagement patterns.
        - **Objective:** Identify key topics, effective hashtags, and optimal posting strategies.
        - **Analysis includes:**
            - KPI Dashboard (Engagement Rate, Total Interactions).
            - Platform Performance Comparison.
            - In-depth Hashtag and Sentiment Analysis.
        - **Navigate:** Use the `Social_Media_Overview` and `Social_Media_Analysis` pages in the sidebar.
    """)

with col2:
    st.subheader("🚌 NYC Green Taxi Trip Insights")
    st.markdown("""
        An interactive dashboard exploring NYC Green Taxi trip data from January 2020 to identify operational patterns.
        - **Objective:** Analyze trip characteristics to understand service usage and operational efficiency.
        - **Analysis includes:**
            - Key Metrics (Revenue, Trip Duration, Passenger Count).
            - Trip Distance & Duration Distributions.
            - Peak Hour Analysis with a Timing Heatmap.
        - **Navigate:** Use the `Transport_Overview` and `Transport_Timing` pages in the sidebar.
    """)

st.markdown("---")
st.header("About Me & CV")
st.write("Specializing in social media data analysis, dashboard development, and A/B testing.")

CV_PATH = "[CV]-[Data Analyst]-[Trinh Anh Tu].pdf"
if os.path.exists(CV_PATH):
    with open(CV_PATH, "rb") as f:
        pdf_bytes = f.read()
    st.download_button(
        "Download Resume (PDF)",
        data=pdf_bytes,
        file_name="Resume_Trinh_Anh_Tu_Data_Analyst.pdf",
        mime="application/pdf"
    )