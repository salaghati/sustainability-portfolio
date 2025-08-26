import streamlit as st
import pandas as pd
from modules.transport.utils import load_and_clean_transport_data
from modules.transport.charts import kpi_card, trend_chart, top_n_chart, distribution_chart, pie_chart

st.title("📊 Transport Insights - Enhanced Overview")

with st.expander("📖 Project Background & Objectives", expanded=True):
    st.markdown("""
        **Bối cảnh:** Dữ liệu di chuyển trong đô thị là một nguồn thông tin quý giá để hiểu về hành vi đi lại, nhu cầu và các điểm nóng giao thông. Dự án này tập trung vào dữ liệu của các chuyến taxi Xanh tại New York.
        
        **Mục tiêu:**
        - **Phân tích Đặc điểm Chuyến đi:** Hiểu các đặc điểm vận hành chính như quãng đường, thời gian, và chi phí trung bình của một chuyến đi.
        - **Xác định Xu hướng:** Tìm ra các mẫu hình về thời gian (giờ cao điểm, ngày trong tuần) và các tuyến đường phổ biến.
        - **Đưa ra Quyết định:** Cung cấp các insight dựa trên dữ liệu để hỗ trợ việc ra quyết định trong vận hành, như phân bổ tài xế hoặc tối ưu hóa giá cả.
        
        **Dataset:** Phân tích dựa trên bộ dữ liệu `NYC Green Taxi trips` cho tháng 1 năm 2020.
    """)

st.markdown("An in-depth look at NYC Green Taxi trips, focusing on key metrics and operational patterns.")

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

st.markdown("---")

# --- Trip Characteristics Analysis ---
st.header("Trip Characteristics")
dist_cols = st.columns(2)
with dist_cols[0]:
    st.altair_chart(distribution_chart(filtered_df, 'trip_distance', 'Trip Distance Distribution', 'Distance (miles)'), use_container_width=True)
    st.caption("Distribution of trip distances, showing the frequency of short vs. long trips.")
with dist_cols[1]:
    st.altair_chart(distribution_chart(filtered_df, 'trip_duration_mins', 'Trip Duration Distribution', 'Duration (minutes)'), use_container_width=True)
    st.caption("Distribution of trip durations, showing how long trips typically last.")
st.markdown("---")

# --- Operational Analysis ---
st.header("Operational Analysis")
op_cols = st.columns(2)
with op_cols[0]:
    st.altair_chart(pie_chart(filtered_df, 'payment_type_name', 'Payment Type Distribution'), use_container_width=True)
    st.caption("Breakdown of payment methods used by passengers.")
with op_cols[1]:
    st.altair_chart(top_n_chart(filtered_df, 'passengers', n=6), use_container_width=True)
    st.caption("Frequency of trips based on the number of passengers.")
st.markdown("---")

# --- Trend & Route Analysis ---
st.header("Trend and Route Analysis")
st.altair_chart(trend_chart(filtered_df), use_container_width=True)
st.caption("Daily trip volumes over the selected date range.")
st.altair_chart(top_n_chart(filtered_df, 'route', 10), use_container_width=True)
st.caption("Top 10 most frequent trip routes (Pickup ID -> Dropoff ID).")
