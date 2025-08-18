"""
Overview page - KPIs and general insights.
"""
import streamlit as st
import pandas as pd
from utils import load_data_with_uploader, calculate_kpis, apply_data_filters
from charts import create_timeseries_chart, create_platform_chart, create_sentiment_chart


# Page config is handled by main app.py

st.title("Dashboard Overview")
st.caption("Key performance indicators and social media engagement trends for sustainability")

# Load data
@st.cache_data(show_spinner=False)
def load_cached_data():
    return load_data_with_uploader()

try:
    df = load_cached_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Sidebar filters
with st.sidebar:
    st.header("Data Filters")
    
    # Platform filter
    if "platform" in df.columns:
        platforms = sorted(df["platform"].dropna().unique())
        platform_sel = st.multiselect(
            "Platforms",
            options=platforms,
            default=platforms,
            help="Select platforms to analyze"
        )
    else:
        platform_sel = []
    
    # Sentiment filter
    if "post_sentiment" in df.columns:
        sentiments = sorted(df["post_sentiment"].dropna().unique())
        sentiment_sel = st.multiselect(
            "Sentiment",
            options=sentiments,
            default=sentiments,
            help="Select post sentiment"
        )
    else:
        sentiment_sel = []
    
    # Date range filter
    if "post_date" in df.columns:
        min_date = df["post_date"].min().date()
        max_date = df["post_date"].max().date()
        date_range = st.date_input(
            "Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            help="Select analysis time period"
        )
    else:
        date_range = None
    
    # Hashtag filter
    hashtag_filter = st.text_input(
        "Search hashtags containing...",
        value="",
        help="Filter by hashtag (case insensitive)"
    )

# Apply filters
filtered_df = apply_data_filters(
    df, 
    platforms=platform_sel,
    sentiments=sentiment_sel,
    date_range=date_range,
    hashtag_filter=hashtag_filter
)

# Show filter results
st.info(f"Showing {len(filtered_df):,} posts from total {len(df):,} posts (after filtering)")

# KPIs section
st.subheader("Key Performance Indicators (KPIs)")

kpis = calculate_kpis(filtered_df)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(
        "Total Posts", 
        f"{kpis['total_posts']:,}",
        help="Total number of posts in dataset"
    )
with col2:
    avg_er = kpis['avg_engagement_rate']
    st.metric(
        "Avg Engagement Rate", 
        f"{avg_er:.2%}" if not pd.isna(avg_er) else "N/A",
        help="Average engagement rate = (likes+shares+comments)/followers"
    )
with col3:
    st.metric(
        "Total Engagement", 
        f"{kpis['total_engagement']:,}",
        help="Total likes + shares + comments"
    )

st.markdown("---")

# Charts section
col1, col2 = st.columns(2)

with col1:
    st.subheader("Time Trend")
    
    chart = create_timeseries_chart(filtered_df)
    if chart:
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("No time data available to display")
    
    with st.expander("Explanation"):
        st.markdown("""
        - **X-axis**: Post date
        - **Y-axis**: Total engagement (likes + shares + comments)
        - **Purpose**: View engagement trends over time, detect peaks/drops
        """)

with col2:
    st.subheader("Platform Performance")
    
    chart = create_platform_chart(filtered_df)
    if chart:
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("No platform data available to display")
    
    with st.expander("Explanation"):
        st.markdown("""
        - **X-axis**: Social media platform
        - **Y-axis**: Average engagement rate
        - **Purpose**: Compare platform effectiveness to optimize strategy
        """)

st.markdown("---")

# Sentiment analysis
st.subheader("Sentiment Analysis")

col1, col2 = st.columns([2, 1])

with col1:
    chart = create_sentiment_chart(filtered_df)
    if chart:
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("No sentiment data available to display")

with col2:
    st.markdown("### Insights")
    if "post_sentiment" in filtered_df.columns:
        sentiment_counts = filtered_df["post_sentiment"].value_counts()
        st.markdown("**Sentiment Distribution:**")
        for sentiment, count in sentiment_counts.items():
            percentage = count / len(filtered_df) * 100
            st.markdown(f"- **{sentiment}**: {count:,} posts ({percentage:.1f}%)")
    else:
        st.info("No sentiment data available")

with st.expander("Sentiment Explanation"):
    st.markdown("""
    - **Positive**: Optimistic, encouraging posts
    - **Neutral**: Informational, factual posts
    - **Negative**: Concerning, alarming posts
    - **Analysis**: Helps understand messaging tone and adjust content strategy
    """)

# Data table
st.markdown("---")
st.subheader("Data Details")

with st.expander("View data table"):
    st.dataframe(
        filtered_df[["post_date", "platform", "post_sentiment", "hashtag", 
                    "engagement_total", "engagement_rate", "user_followers"]].head(100),
        use_container_width=True
    )
    
    # Download button
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download filtered CSV",
        data=csv,
        file_name="sustainability_posts_filtered.csv",
        mime="text/csv"
    )