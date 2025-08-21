import streamlit as st
from modules.transport.utils import load_and_clean_transport_data
from modules.transport.charts import timing_heatmap

st.title("⏱️ Transport Insights - Timing Analysis")

df = load_and_clean_transport_data()

if not df.empty:
    st.altair_chart(timing_heatmap(df), use_container_width=True)
else:
    st.warning("Could not load transport data.")
