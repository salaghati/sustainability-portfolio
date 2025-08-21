import streamlit as st
import pandas as pd
from modules.transport.utils import load_and_clean_transport_data
from modules.transport.charts import kpi_card, trend_chart, top_n_chart, distribution_chart, pie_chart

st.title("📊 Transport Insights - Enhanced Overview")
st.markdown("An in-depth look at NYC Green Taxi trips, focusing on key metrics and operational insights.")

df = load_and_clean_transport_data()

if df.empty:
    st.warning("Could not load transport data. Please check the data source or run the app again.")
    st.stop()

# --- Sidebar Filters ---
st.sidebar.header("Transport Filters")
min_date = df['pickup_date'].min()
max_date = df['pickup_date'].max()
start_date, end_date = st.sidebar.date_input("Date range", [min_date, max_date], min_value=min_date, max_value=max_date, key="transport_date")

filtered_df = df[(df['pickup_datetime'].dt.date >= start_date) & (df['pickup_datetime'].dt.date <= end_date)]

if filtered_df.empty:
    st.warning("No data available for the selected date range.")
    st.stop()

# --- KPI Section ---
st.header("Key Performance Indicators")
kpi_cols = st.columns(4)
with kpi_cols[0]:
    kpi_card("Total Trips", f"{filtered_df.shape[0]:,}", "Total number of trips in the selected period.")
with kpi_cols[1]:
    total_revenue = filtered_df['total_amount'].sum()
    kpi_card("Total Revenue ($)", f"${total_revenue:,.2f}", "Total revenue from fares and tips.")
with kpi_cols[2]:
    avg_fare = filtered_df['total_amount'].mean()
    kpi_card("Avg. Fare ($)", f"{avg_fare:.2f}", "Average total amount paid per trip.")
with kpi_cols[3]:
    avg_duration = filtered_df['trip_duration_mins'].mean()
    kpi_card("Avg. Duration (min)", f"{avg_duration:.2f}", "Average trip duration in minutes.")

st.info("""
**💡 Insight:** The key metrics provide a high-level snapshot of the taxi service's performance. A high trip count and revenue indicate strong demand, while average fare and duration offer insights into typical trip characteristics.
""", icon="✅")
st.markdown("---")

# --- Trip Characteristics Analysis ---
st.header("Trip Characteristics")
dist_cols = st.columns(2)
with dist_cols[0]:
    st.altair_chart(distribution_chart(filtered_df, 'trip_distance', 'Trip Distance Distribution', 'Distance (miles)'), use_container_width=True)
with dist_cols[1]:
    st.altair_chart(distribution_chart(filtered_df, 'trip_duration_mins', 'Trip Duration Distribution', 'Duration (minutes)'), use_container_width=True)

st.info("""
**💡 Insight:** The distribution charts reveal that the vast majority of taxi trips are short-distance (under 3 miles) and brief (under 15 minutes). 
This suggests the service primarily caters to short, quick urban journeys rather than long-distance travel.
""", icon="✅")
st.markdown("---")

# --- Operational Analysis ---
st.header("Operational Analysis")
op_cols = st.columns(2)
with op_cols[0]:
    st.altair_chart(pie_chart(filtered_df, 'payment_type_name', 'Payment Type Distribution'), use_container_width=True)
with op_cols[1]:
    st.altair_chart(top_n_chart(filtered_df, 'passengers', n=6), use_container_width=True)

st.info("""
**💡 Insight & Conclusion:**
- **Payment:** Credit card is the dominant payment method, highlighting the importance of reliable electronic payment systems.
- **Passengers:** The most common trips are for a single passenger. This could inform marketing strategies or vehicle size considerations for the fleet.
""", icon="✅")
st.markdown("---")


# --- Trend & Route Analysis ---
st.header("Trend and Route Analysis")
st.altair_chart(trend_chart(filtered_df), use_container_width=True)
st.altair_chart(top_n_chart(filtered_df, 'route', 10), use_container_width=True)
st.info("""
**💡 Insight:**
- **Trend:** The daily trip trend chart helps identify weekly patterns, such as potential dips on weekends or peaks during weekdays.
- **Routes:** The top routes highlight the most critical high-traffic corridors. This information is valuable for driver allocation, understanding demand hotspots, and city planning.
""", icon="✅")
