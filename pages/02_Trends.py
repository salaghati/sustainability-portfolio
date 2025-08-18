"""
Trends page - Advanced analytics and deeper insights.
"""
import streamlit as st
import pandas as pd
from utils import load_data_with_uploader, apply_data_filters
from charts import (
    create_hashtag_chart, create_topic_chart, 
    create_time_heatmap, create_cta_chart
)


# Page config is handled by main app.py

st.title("Trends Analysis")
st.caption("Hashtag performance, topic insights, optimal posting times and CTA analysis")

# Load data
@st.cache_data(show_spinner=False)
def load_cached_data():
    return load_data_with_uploader()

try:
    df = load_cached_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Sidebar filters (same as Overview page)
with st.sidebar:
    st.header("Data Filters")
    
    # Platform filter
    if "platform" in df.columns:
        platforms = sorted(df["platform"].dropna().unique())
        platform_sel = st.multiselect(
            "Platforms",
            options=platforms,
            default=platforms
        )
    else:
        platform_sel = []
    
    # Sentiment filter
    if "post_sentiment" in df.columns:
        sentiments = sorted(df["post_sentiment"].dropna().unique())
        sentiment_sel = st.multiselect(
            "Sentiment",
            options=sentiments,
            default=sentiments
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
            max_value=max_date
        )
    else:
        date_range = None
    
    # Hashtag filter
    hashtag_filter = st.text_input(
        "Search hashtags containing...",
        value=""
    )

# Apply filters
filtered_df = apply_data_filters(
    df, 
    platforms=platform_sel,
    sentiments=sentiment_sel,
    date_range=date_range,
    hashtag_filter=hashtag_filter
)

st.info(f"Analyzing {len(filtered_df):,} posts from total {len(df):,} posts")

# Hashtag Analysis
st.subheader("Top Hashtag Performance")

col1, col2 = st.columns([3, 1])

with col1:
    chart = create_hashtag_chart(filtered_df)
    if chart:
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("No hashtag data available to display")

with col2:
    st.markdown("### Hashtag Insights")
    if "hashtag" in filtered_df.columns:
        top_hashtags = (
            filtered_df.groupby("hashtag")
            .agg(posts=("post_id", "count"), avg_er=("engagement_rate", "mean"))
            .sort_values(["posts", "avg_er"], ascending=[False, False])
            .head(5)
        )
        
        st.markdown("**Top 5 Hashtags:**")
        for hashtag, row in top_hashtags.iterrows():
            st.markdown(f"- **{hashtag}**: {row['posts']} posts (ER: {row['avg_er']:.2%})")
    else:
        st.info("No hashtag data available")

with st.expander("Hashtag Analytics Explanation"):
    st.markdown("""
    - **X-axis**: Number of posts using the hashtag
    - **Color**: Average engagement rate
    - **Purpose**: Find effective hashtags for content strategy
    - **Note**: Balance between volume and engagement quality
    """)

st.markdown("---")

# Climate Topics
st.subheader("Sustainability Topics")

col1, col2 = st.columns([3, 1])

with col1:
    chart = create_topic_chart(filtered_df)
    if chart:
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("No topic data available to display")

with col2:
    st.markdown("### Topic Insights")
    if "climate_topic" in filtered_df.columns:
        top_topics = (
            filtered_df.groupby("climate_topic")
            .agg(posts=("post_id", "count"), avg_er=("engagement_rate", "mean"))
            .sort_values(["posts", "avg_er"], ascending=[False, False])
            .head(5)
        )
        
        st.markdown("**Top 5 Topics:**")
        for topic, row in top_topics.iterrows():
            st.markdown(f"- **{topic}**: {row['posts']} posts (ER: {row['avg_er']:.2%})")
    else:
        st.info("No topic data available")

with st.expander("Climate Topics Explanation"):
    st.markdown("""
    - **Classification**: Sustainability topics like Waste Reduction, Energy Storage, etc.
    - **Metrics**: Number of posts and average engagement rate
    - **Strategy**: Focus on topics with high ER and appropriate volume
    - **Trend**: Track shifts in public interest
    """)

st.markdown("---")

# Time Heatmap Analysis
st.subheader("Optimal Posting Time Analysis")

# Platform selector for heatmap
if "platform" in filtered_df.columns:
    platform_focus = st.selectbox(
        "Select platform for heatmap analysis (or leave blank to view all)",
        options=[None] + sorted(filtered_df["platform"].dropna().unique()),
        index=0,
        format_func=lambda x: "All platforms" if x is None else x
    )
else:
    platform_focus = None

chart = create_time_heatmap(filtered_df, platform_focus)
if chart:
    st.altair_chart(chart, use_container_width=True)
else:
    st.info("No time data available to display heatmap")

with st.expander("Time Heatmap Explanation"):
    st.markdown("""
    - **X-axis**: Hour of day (0-23)
    - **Y-axis**: Day of week
    - **Color**: Average engagement rate (darker = higher)
    - **Usage**: Find optimal times to post content
    - **Platform**: May vary between different platforms
    """)

st.markdown("---")

# CTA Analysis
st.subheader("Call-to-Action Performance")

chart = create_cta_chart(filtered_df)
if chart:
    st.altair_chart(chart, use_container_width=True)
    
    with st.expander("CTA Analytics Explanation"):
        st.markdown("""
        - **X-axis**: Average shares + comments (interaction proxy)
        - **Y-axis**: Call-to-action types
        - **Color**: Average engagement rate
        - **Purpose**: Find most effective CTAs to drive action
        - **Strategy**: Optimize messaging based on performance data
        """)
else:
    st.info("Insufficient CTA data for analysis (requires call_to_action, engagement_shares, engagement_comments columns)")

st.markdown("---")

# Advanced Metrics
st.subheader("Advanced Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Content Quality")
    if "engagement_rate" in filtered_df.columns:
        high_er_posts = len(filtered_df[filtered_df["engagement_rate"] > filtered_df["engagement_rate"].quantile(0.8)])
        total_posts = len(filtered_df)
        quality_rate = high_er_posts / total_posts if total_posts > 0 else 0
        
        st.metric("High-ER Posts", f"{high_er_posts:,}", f"{quality_rate:.1%} of total")
        st.caption("Posts with ER > 80th percentile")
    else:
        st.info("Requires engagement_rate data")

with col2:
    st.markdown("### Platform Diversity")
    if "platform" in filtered_df.columns:
        platform_count = filtered_df["platform"].nunique()
        most_used = filtered_df["platform"].mode().iloc[0] if len(filtered_df) > 0 else "N/A"
        
        st.metric("Platforms", platform_count)
        st.caption(f"Most used: {most_used}")
    else:
        st.info("Requires platform data")

with col3:
    st.markdown("### Posting Frequency")
    if "post_date" in filtered_df.columns:
        date_range_days = (filtered_df["post_date"].max() - filtered_df["post_date"].min()).days
        posts_per_day = len(filtered_df) / date_range_days if date_range_days > 0 else 0
        
        st.metric("Posts per day", f"{posts_per_day:.1f}")
        st.caption(f"Over {date_range_days} days")
    else:
        st.info("Requires post_date data")

# Data export
st.markdown("---")
st.subheader("Export Data")

export_col1, export_col2 = st.columns(2)

with export_col1:
    # Full filtered data
    csv_full = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download full filtered data",
        data=csv_full,
        file_name="sustainability_trends_analysis.csv",
        mime="text/csv"
    )

with export_col2:
    # Summary statistics
    if "engagement_rate" in filtered_df.columns and "platform" in filtered_df.columns:
        summary = (
            filtered_df.groupby("platform")
            .agg({
                "engagement_rate": ["mean", "median", "std"],
                "post_id": "count",
                "engagement_total": "sum"
            })
            .round(4)
        )
        summary_csv = summary.to_csv().encode("utf-8")
        st.download_button(
            "Download summary statistics",
            data=summary_csv,
            file_name="platform_summary_stats.csv",
            mime="text/csv"
        )