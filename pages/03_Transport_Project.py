"""
Transport Project - Complete Analysis (Overview + Timing Analysis)
"""
import streamlit as st
import pandas as pd
from modules.transport.utils import load_and_clean_transport_data
from modules.transport.charts import kpi_card, trend_chart, top_n_chart, distribution_chart, pie_chart, timing_heatmap

st.title("🚌 Transport Project")
st.markdown("### Complete Analysis: NYC Green Taxi Operations & Insights")

with st.expander("📖 Project Background & Objectives", expanded=True):
    st.markdown("""
        **Context:** Urban mobility data is a valuable source for understanding travel behavior, demand, and traffic hotspots. This project focuses on data from NYC Green Taxis.
        
        **Objectives:**
        - **Trip Characteristic Analysis:** Understand key operational metrics like average trip distance, duration, and cost.
        - **Trend Identification:** Uncover patterns related to timing (peak hours, days of the week) and popular routes.
        - **Decision Support:** Provide data-driven insights to support operational decisions, such as driver allocation or price optimization.
        
        **Dataset:** The analysis is based on the `NYC Green Taxi trips` dataset for January 2020.
    """)

st.markdown("An in-depth look at NYC Green Taxi trips, focusing on key metrics, operational patterns, and optimal timing analysis.")

df = load_and_clean_transport_data()

if df.empty:
    st.warning("Could not load transport data. Please check the data source or run the app again.")
    st.stop()

# --- Sidebar Filters ---
with st.sidebar:
    st.header("🚌 Transport Filters")
    st.markdown("*Customize your trip analysis*")
    
    # Date range filter
    min_date = df['pickup_date'].min()
    max_date = df['pickup_date'].max()
    
    st.markdown("📅 **Analysis Period**")
    start_date, end_date = st.date_input(
        "Select date range", 
        [min_date, max_date], 
        min_value=min_date, 
        max_value=max_date, 
        key="transport_date",
        help="Filter trips within this date range"
    )
    
    # Additional filters could be added here in the future
    st.markdown("---")
    st.markdown("### 📊 Analysis Scope")
    
    analysis_focus = st.radio(
        "Choose analysis focus",
        ["All Trips", "High-Value Trips", "Peak Hours Only"],
        help="Select the scope of your analysis"
    )

# Apply date filter
filtered_df = df[(df['pickup_datetime'].dt.date >= start_date) & (df['pickup_datetime'].dt.date <= end_date)]

if filtered_df.empty:
    st.warning("No data available for the selected date range.")
    st.stop()

# Apply analysis focus
if analysis_focus == "High-Value Trips":
    threshold = filtered_df['total_amount'].quantile(0.75)
    filtered_df = filtered_df[filtered_df['total_amount'] >= threshold]
elif analysis_focus == "Peak Hours Only":
    # Define peak hours as 7-9 AM and 5-7 PM
    filtered_df = filtered_df[
        (filtered_df['pickup_datetime'].dt.hour.between(7, 9)) |
        (filtered_df['pickup_datetime'].dt.hour.between(17, 19))
    ]

# Results summary
st.success(f"🚌 **Analyzing {len(filtered_df):,} trips** from total {len(df):,} trips")

st.markdown("---")

# =============================================================================
# SECTION 1: KEY PERFORMANCE INDICATORS
# =============================================================================

st.header("📊 Key Performance Indicators")

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

# =============================================================================
# SECTION 2: TRIP CHARACTERISTICS ANALYSIS  
# =============================================================================

st.header("🚗 Trip Characteristics Analysis")

# Trip characteristics in tabs
char_tab1, char_tab2, char_tab3 = st.tabs(["📏 Distance & Duration", "💳 Payment & Passengers", "📈 Trends & Routes"])

with char_tab1:
    st.subheader("Distance and Duration Distributions")
    
    dist_cols = st.columns(2)
    
    with dist_cols[0]:
        st.altair_chart(
            distribution_chart(filtered_df, 'trip_distance', 'Trip Distance Distribution', 'Distance (miles)'), 
            use_container_width=True
        )
        st.caption("📊 Distribution of trip distances, showing the frequency of short vs. long trips.")
    
    with dist_cols[1]:
        st.altair_chart(
            distribution_chart(filtered_df, 'trip_duration_mins', 'Trip Duration Distribution', 'Duration (minutes)'), 
            use_container_width=True
        )
        st.caption("⏱️ Distribution of trip durations, showing how long trips typically last.")

with char_tab2:
    st.subheader("Operational Characteristics")
    
    op_cols = st.columns(2)
    
    with op_cols[0]:
        st.altair_chart(
            pie_chart(filtered_df, 'payment_type_name', 'Payment Type Distribution'), 
            use_container_width=True
        )
        st.caption("💳 Breakdown of payment methods used by passengers.")
    
    with op_cols[1]:
        st.altair_chart(
            top_n_chart(filtered_df, 'passengers', n=6), 
            use_container_width=True
        )
        st.caption("👥 Frequency of trips based on the number of passengers.")

with char_tab3:
    st.subheader("Trends and Popular Routes")
    
    st.altair_chart(trend_chart(filtered_df), use_container_width=True)
    st.caption("📈 Daily trip volumes over the selected date range.")
    
    st.altair_chart(top_n_chart(filtered_df, 'route', 10), use_container_width=True)
    st.caption("🗺️ Top 10 most frequent trip routes (Pickup ID → Dropoff ID).")

st.markdown("---")

# =============================================================================
# SECTION 3: TIMING ANALYSIS
# =============================================================================

st.header("⏰ Timing Analysis & Optimization")

timing_tab1, timing_tab2 = st.tabs(["🔥 Peak Hours Heatmap", "📊 Timing Insights"])

with timing_tab1:
    st.subheader("Trip Volume by Hour and Day of Week")
    
    # Display the timing heatmap
    heatmap_chart = timing_heatmap(filtered_df)
    if heatmap_chart:
        st.altair_chart(heatmap_chart, use_container_width=True)
        
        st.markdown("""
        **How to Read This Heatmap:**
        - **X-axis**: Hours of the day (0-23)
        - **Y-axis**: Days of the week
        - **Color Intensity**: Number of trips (darker = more trips)
        - **Peak Patterns**: Look for dark spots indicating high-demand periods
        """)
    else:
        st.warning("⚠️ Could not generate timing heatmap from current data.")

with timing_tab2:
    st.subheader("Operational Insights from Timing Patterns")
    
    insights_col1, insights_col2 = st.columns(2)
    
    with insights_col1:
        st.markdown("#### 🚀 Peak Hours Analysis")
        
        if 'pickup_datetime' in filtered_df.columns:
            # Calculate peak hours
            hourly_trips = filtered_df.groupby(filtered_df['pickup_datetime'].dt.hour).size()
            peak_hour = hourly_trips.idxmax()
            peak_count = hourly_trips.max()
            
            st.success(f"""
            **🔥 Peak Hour: {peak_hour}:00**
            - {peak_count:,} trips during this hour
            - {(peak_count/len(filtered_df)*100):.1f}% of daily volume
            """)
            
            # Day of week analysis
            dow_trips = filtered_df.groupby(filtered_df['pickup_datetime'].dt.day_name()).size()
            peak_day = dow_trips.idxmax()
            
            st.info(f"""
            **📅 Busiest Day: {peak_day}**
            - {dow_trips.max():,} trips on this day
            - {(dow_trips.max()/len(filtered_df)*100):.1f}% of weekly volume
            """)
    
    with insights_col2:
        st.markdown("#### 💡 Business Recommendations")
        
        st.markdown("""
        **🚗 Driver Allocation:**
        - Deploy more drivers during identified peak hours
        - Consider surge pricing during high-demand periods
        - Optimize vehicle maintenance during low-demand hours
        
        **📊 Revenue Optimization:**
        - Implement dynamic pricing based on demand patterns
        - Focus marketing efforts on low-demand periods
        - Plan special promotions during off-peak hours
        """)

st.markdown("---")

# =============================================================================
# SECTION 4: PERFORMANCE METRICS & INSIGHTS
# =============================================================================

st.header("📈 Advanced Performance Metrics")

perf_col1, perf_col2, perf_col3 = st.columns(3)

with perf_col1:
    # Revenue per mile
    if len(filtered_df) > 0 and 'total_amount' in filtered_df.columns and 'trip_distance' in filtered_df.columns:
        avg_revenue_per_mile = (filtered_df['total_amount'] / filtered_df['trip_distance']).mean()
        st.metric(
            "💰 Revenue per Mile", 
            f"${avg_revenue_per_mile:.2f}",
            help="Average revenue generated per mile traveled"
        )
    else:
        st.metric("💰 Revenue per Mile", "N/A")

with perf_col2:
    # Trip efficiency (distance/duration)
    if len(filtered_df) > 0 and 'trip_distance' in filtered_df.columns and 'trip_duration_mins' in filtered_df.columns:
        avg_speed = (filtered_df['trip_distance'] / (filtered_df['trip_duration_mins'] / 60)).mean()
        st.metric(
            "⚡ Average Speed", 
            f"{avg_speed:.1f} mph",
            help="Average speed across all trips"
        )
    else:
        st.metric("⚡ Average Speed", "N/A")

with perf_col3:
    # Customer satisfaction proxy (tip percentage)
    if len(filtered_df) > 0 and 'tip_amount' in filtered_df.columns and 'total_amount' in filtered_df.columns:
        avg_tip_pct = (filtered_df['tip_amount'] / filtered_df['total_amount'] * 100).mean()
        st.metric(
            "🎯 Avg Tip %", 
            f"{avg_tip_pct:.1f}%",
            help="Average tip percentage as proxy for customer satisfaction"
        )
    else:
        st.metric("🎯 Avg Tip %", "N/A")

st.markdown("---")

# =============================================================================
# EXPORT & SUMMARY
# =============================================================================

st.subheader("💾 Export Analysis Results")

export_col1, export_col2, export_col3 = st.columns(3)

with export_col1:
    # Export filtered data
    csv_data = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        f"📥 Download Trip Data ({len(filtered_df)} trips)",
        data=csv_data,
        file_name="nyc_taxi_analysis_results.csv",
        mime="text/csv",
        help="Complete filtered dataset",
        use_container_width=True,
        type="primary"
    )

with export_col2:
    # Export summary statistics
    if len(filtered_df) > 0:
        summary_stats = filtered_df.describe().round(2)
        summary_csv = summary_stats.to_csv().encode("utf-8")
        st.download_button(
            f"📊 Summary Statistics",
            data=summary_csv,
            file_name="trip_summary_statistics.csv",
            mime="text/csv",
            help="Descriptive statistics for all metrics",
            use_container_width=True
        )

with export_col3:
    st.markdown("""
    **🚌 Analysis Complete:**  
    ✅ Trip patterns identified  
    ✅ Peak hours analyzed  
    ✅ Revenue insights generated  
    ✅ Operational recommendations ready  
    """)

# Final insights summary
st.markdown("---")
st.subheader("📝 Strategic Insights Summary")

summary_col1, summary_col2 = st.columns(2)

with summary_col1:
    st.success("""
    **🎯 Operational Excellence:**
    - **Peak Hour Management:** Deploy resources during identified high-demand periods
    - **Route Optimization:** Focus on popular routes for maximum efficiency  
    - **Pricing Strategy:** Implement dynamic pricing based on demand patterns
    - **Service Quality:** Monitor tip percentages as satisfaction indicators
    """)

with summary_col2:
    st.info("""
    **📊 Performance Monitoring:**
    - **Revenue per Mile:** Track efficiency of trip monetization
    - **Average Speed:** Monitor traffic conditions and route efficiency
    - **Customer Satisfaction:** Use tip percentages to gauge service quality
    - **Demand Forecasting:** Use timing patterns for resource planning
    """)

st.success("""
🚀 **Implementation Roadmap:**
1. **Resource Allocation:** Use peak hour insights for driver scheduling
2. **Revenue Optimization:** Implement surge pricing during high-demand periods
3. **Route Planning:** Focus on top-performing pickup/dropoff locations
4. **Performance Tracking:** Monitor KPIs monthly and adjust strategies accordingly
""")
