"""
Minimal test app for debugging Streamlit Cloud
"""
import streamlit as st

st.set_page_config(page_title="Test App", layout="wide")

st.title("🧪 Minimal Test App")
st.write("If you see this, the app is working!")

st.subheader("Environment Info")
import sys
st.write(f"Python version: {sys.version}")

import pandas as pd
st.write(f"Pandas version: {pd.__version__}")

import altair as alt  
st.write(f"Altair version: {alt.__version__}")

st.write(f"Streamlit version: {st.__version__}")

st.success("✅ All imports working!")

# Test basic functionality
if st.button("Test Button"):
    st.balloons()
    st.write("Button works!")

# Test file operations
import os
st.write(f"Current directory: {os.getcwd()}")
st.write(f"Files in directory: {os.listdir('.')}")
