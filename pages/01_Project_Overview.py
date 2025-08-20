"""
Overview page - KPIs and general insights with enhanced UI.
"""
import streamlit as st
import pandas as pd
from utils import load_data_with_uploader, calculate_kpis, apply_data_filters
from charts import create_timeseries_chart, create_platform_chart, create_sentiment_chart

# Enhanced CSS for professional cards and metrics
st.markdown("""
<style>
    /* KPI Cards */
    .kpi-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    
    .kpi-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2d3748;
        margin: 0.5rem 0;
    }
    
    .kpi-label {
        font-size: 0.9rem;
        color: #4a5568;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .kpi-icon {
        font-size: 1.5rem;
        opacity: 0.7;
    }
    
    /* Insight cards */
    .insight-card {
        background: linear-gradient(135deg, #f7fafc, #edf2f7);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 3px solid #667eea;
    }
    
    /* Chart containers */
    .chart-container {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Page header with better hierarchy
st.title("📊 Dashboard Overview")
st.markdown("### Key Performance Indicators & Engagement Analysis")

# Quick usage guide
st.info("💡 **Quick Start:** Use the sidebar filters to customize your analysis. Start with platform selection to compare performance across social media channels.")

# Load data with caching
@st.cache_data(show_spinner=False)
def load_cached_data():
    return load_data_with_uploader()

try:
    df = load_cached_data()
except Exception as e:
    st.error(f"❌ Error loading data: {e}")
    st.stop()

# Enhanced sidebar filters with better organization
with st.sidebar:
    st.header("🔍 Analysis Filters")
    st.markdown("*Customize your data view below*")
    
    # Platform filter with help text
    if "platform" in df.columns:
        platforms = sorted(df["platform"].dropna().unique())
        platform_sel = st.multiselect(
            "📱 Social Media Platforms",
            options=platforms,
            default=platforms,
            help="Select one or more platforms to compare their performance metrics"
        )
    else:
        platform_sel = []
    
    # Sentiment filter
    if "post_sentiment" in df.columns:
        sentiments = sorted(df["post_sentiment"].dropna().unique())
        sentiment_sel = st.multiselect(
            "😊 Post Sentiment",
            options=sentiments,
            default=sentiments,
            help="Filter by emotional tone: Positive (encouraging), Neutral (informational), Negative (concerning)"
        )
    else:
        sentiment_sel = []
    
    # Date range with better UX
    if "post_date" in df.columns:
        min_date = df["post_date"].min().date()
        max_date = df["post_date"].max().date()
        
        st.markdown("📅 **Date Range**")

        # Date presets
        preset_col1, preset_col2 = st.columns(2)
        if preset_col1.button("Last 7 Days", use_container_width=True):
            st.session_state.date_range = (max_date - pd.Timedelta(days=7), max_date)
        if preset_col2.button("Last 30 Days", use_container_width=True):
            st.session_state.date_range = (max_date - pd.Timedelta(days=30), max_date)

        if 'date_range' not in st.session_state:
            st.session_state.date_range = (min_date, max_date)
            
        date_range = st.date_input(
            "Select time period",
            value=st.session_state.date_range,
            min_value=min_date,
            max_value=max_date,
            help=f"Filter posts from {min_date} to {max_date}",
            key="date_range_selector"
        )
        st.session_state.date_range = date_range

    else:
        date_range = None
    
    # Hashtag search with multiselect
    if "hashtag" in df.columns:
        hashtags = sorted(df["hashtag"].dropna().unique())
        hashtag_sel = st.multiselect(
            "🏷️ Hashtag Search",
            options=hashtags,
            default=[],
            help="Select one or more hashtags to focus the analysis"
        )
    else:
        hashtag_sel = []
    
    # Filter summary
    with st.expander("📋 Active Filters Summary"):
        st.write(f"**Platforms:** {len(platform_sel) if platform_sel else 'All'}")
        st.write(f"**Sentiments:** {len(sentiment_sel) if sentiment_sel else 'All'}")
        st.write(f"**Hashtags:** {len(hashtag_sel) if hashtag_sel else 'All'}")

# Apply filters
filtered_df = apply_data_filters(
    df, 
    platforms=platform_sel,
    sentiments=sentiment_sel,
    date_range=date_range,
    hashtags=hashtag_sel
)

# Handle empty data case
if filtered_df.empty:
    st.warning("Không có dữ liệu phù hợp với bộ lọc đã chọn. Vui lòng thử lại.")
    st.stop()

# Results summary with better styling
filter_col1, filter_col2 = st.columns([3, 1])
with filter_col1:
    st.success(f"📊 **Showing {len(filtered_df):,} posts** from total {len(df):,} posts (after filtering)")
with filter_col2:
    if len(filtered_df) < len(df):
        reduction_pct = (1 - len(filtered_df)/len(df)) * 100
        st.metric("Data Reduction", f"{reduction_pct:.1f}%")

st.markdown("---")

# Enhanced KPI section with cards
st.subheader("📈 Key Performance Indicators")

kpis = calculate_kpis(filtered_df)

# Create 3 columns for KPI cards
kpi_col1, kpi_col2, kpi_col3 = st.columns(3)

with kpi_col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">📝</div>
        <div class="kpi-number">{kpis['total_posts']:,}</div>
        <div class="kpi-label">Total Posts</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col2:
    avg_er = kpis['avg_engagement_rate']
    er_display = f"{avg_er:.2%}" if not pd.isna(avg_er) else "N/A"
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">💫</div>
        <div class="kpi-number">{er_display}</div>
        <div class="kpi-label">Avg Engagement Rate</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">❤️</div>
        <div class="kpi-number">{kpis['total_engagement']:,}</div>
        <div class="kpi-label">Total Engagement</div>
    </div>
    """, unsafe_allow_html=True)

# KPI insights
with st.expander("📊 Understanding These Metrics"):
    st.markdown("""
    - **Total Posts**: Number of social media posts in your filtered dataset
    - **Engagement Rate**: Average of (likes + shares + comments) ÷ followers across all posts
    - **Total Engagement**: Sum of all likes, shares, and comments
    
    💡 **Tip**: High engagement rate (>3%) indicates strong audience connection
    """)

st.markdown("---")

# Charts section with better layout
st.subheader("📊 Data Visualizations")

with st.expander("📈 Engagement Trends Over Time", expanded=True):
    chart = create_timeseries_chart(filtered_df)
    if chart:
        st.altair_chart(chart, use_container_width=True)
    else:
        st.warning("⚠️ No time data available to display trends")
    
    st.markdown("""
    **How to Read This Chart:**
    - **X-axis**: Days when posts were published
    - **Y-axis**: Total engagement (likes + shares + comments)
    - **Insight**: Look for patterns to optimize posting schedule
    """)

with st.expander("🏆 Platform Performance Comparison", expanded=True):
    chart = create_platform_chart(filtered_df)
    if chart:
        st.altair_chart(chart, use_container_width=True)
    else:
        st.warning("⚠️ No platform data available")
        
    st.markdown("""
    **Platform Analysis Guide:**
    - **Height**: Average engagement rate per platform
    - **Strategy**: Focus content efforts on top-performing platforms
    """)

st.markdown("---")

# Sentiment analysis with enhanced layout
st.subheader("🎭 Sentiment Analysis")

with st.expander("🎭 Sentiment Distribution", expanded=True):
    sent_col1, sent_col2 = st.columns([2, 1])

    with sent_col1:
        chart = create_sentiment_chart(filtered_df)
        if chart:
            st.altair_chart(chart, use_container_width=True)
        else:
            st.warning("⚠️ No sentiment data available")

    with sent_col2:
        st.markdown("#### 💭 Sentiment Insights")
        
        if "post_sentiment" in filtered_df.columns:
            sentiment_counts = filtered_df["post_sentiment"].value_counts()
            
            for sentiment, count in sentiment_counts.items():
                percentage = count / len(filtered_df) * 100
                color = {"Positive": "#22c55e", "Neutral": "#6b7280", "Negative": "#ef4444"}.get(sentiment, "#667eea")
                
                st.markdown(f"""
                <div class="insight-card">
                    <span style="color: {color}; font-weight: bold;">{sentiment}</span><br>
                    <strong>{count:,} posts</strong> ({percentage:.1f}%)
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("💡 No sentiment data in current selection")

with st.expander("🎭 Sentiment Analysis Guide"):
    st.markdown("""
    **Sentiment Categories:**
    - 🟢 **Positive**: Optimistic, encouraging, solution-focused posts
    - 🟡 **Neutral**: Informational, factual, educational content  
    - 🔴 **Negative**: Concerning, alarming, problem-focused posts
    
    **Content Strategy:**
    - Balance emotional tone based on your audience
    - Positive content drives engagement
    - Neutral content builds trust and authority
    """)

st.markdown("---")
st.subheader("📝 Key Insights Summary")
st.info("""
- **Platform Focus:** Identify which 1-2 platforms deliver the highest engagement rate and concentrate content efforts there.
- **Sentiment Strategy:** Positive and neutral content generally performs best. Use sentiment analysis to guide your content's emotional tone.
- **Engagement Peaks:** Look for recurring peaks in the engagement trend chart to identify the best days of the week to post.
""")

# Data export section
st.markdown("---")
st.subheader("💾 Export & Download")

export_col1, export_col2, export_col3 = st.columns(3)

with export_col1:
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        f"📥 Download Filtered Data ({len(filtered_df)} rows)",
        data=csv,
        file_name="social_media_analysis_filtered.csv",
        mime="text/csv",
        help="Download current filtered dataset as CSV",
        use_container_width=True
    )

with export_col2:
    if st.button("📊 View Raw Data", use_container_width=True):
        st.dataframe(
            filtered_df[["post_date", "platform", "post_sentiment", "hashtag", 
                        "engagement_total", "engagement_rate", "user_followers"]].head(100),
            use_container_width=True
        )

with export_col3:
    st.markdown("""
    **Data Quality:**  
    ✅ {total_posts:,} posts analyzed  
    ✅ Real engagement metrics  
    ✅ Multi-platform coverage  
    """.format(total_posts=len(filtered_df)))

# Footer with next steps
st.markdown("---")
st.info("🚀 **Next Steps:** Visit the **Trends Analysis** page for deeper insights into hashtag performance, optimal posting times, and content strategy recommendations.")