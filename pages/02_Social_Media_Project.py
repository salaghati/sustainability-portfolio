"""
Social Media Project - Complete Analysis (Overview + Advanced Trends)
"""
import streamlit as st
import pandas as pd
from utils import load_data_with_uploader, calculate_kpis, apply_data_filters
from charts import (
    create_timeseries_chart, create_platform_chart, create_sentiment_chart,
    create_hashtag_chart, create_topic_chart, create_time_heatmap, create_cta_chart
)

# Enhanced CSS for complete project
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
    
    /* Insight cards */
    .insight-card {
        background: linear-gradient(135deg, #f7fafc, #edf2f7);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 3px solid #667eea;
        color: #2d3748;
    }
    
    .insight-card strong {
        color: #434190;
    }
    
    /* Trend cards */
    .trend-card {
        background: linear-gradient(135deg, #ffffff, #f8fafc);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border-left: 4px solid #8b5cf6;
        color: #2d3748;
    }
    
    .trend-card strong {
        color: #4c51bf;
    }

    /* Metric badges */
    .metric-badge {
        display: inline-block;
        background: linear-gradient(135deg, #8b5cf6, #ec4899);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        margin: 0.2rem;
    }
    
    /* Insight panels */
    .insight-panel {
        background: linear-gradient(135deg, #fef3c7, #fde68a);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 3px solid #f59e0b;
        color: #713f12;
    }

    /* Time heatmap legend */
    .heatmap-legend {
        background: #f7fafc;
        border-radius: 8px;
        padding: 0.8rem;
        margin: 0.5rem 0;
        font-size: 0.9rem;
        color: #2d3748;
    }
</style>
""", unsafe_allow_html=True)

st.title("Social Media Project")
st.markdown("### Complete Analysis: Sustainability Content Performance & Strategy")

with st.expander("📖 Project Background & Objectives", expanded=True):
    st.markdown("""
        **Context:** As sustainability issues gain prominence, brands and organizations need to better understand how the public engages with related content on social media.
        
        **Objectives:**
        - **Performance Analysis:** Evaluate engagement levels across different platforms (Facebook, Instagram, etc.).
        - **Insight Discovery:** Identify which topics, hashtags, and content types generate the highest interaction.
        - **Strategy Recommendations:** Provide data-driven suggestions for content strategy and optimal posting times.
        
        **Dataset:** The analysis is based on the `sustainability_social_media_posts.csv` dataset, containing over 3,000 posts.
    """)

# Load data with caching
@st.cache_data(show_spinner=False)
def load_cached_data():
    return load_data_with_uploader()

try:
    df = load_cached_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Enhanced sidebar filters
with st.sidebar:
    st.header("Analysis Filters")
    st.markdown("*Customize your data view below*")
    
    # Platform filter
    if "platform" in df.columns:
        platforms = sorted(df["platform"].dropna().unique())
        platform_sel = st.multiselect(
            "Social Media Platforms",
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
    
    # Date range
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
    
    # Hashtag search
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
    
    # Analysis type
    st.markdown("---")
    st.markdown("### Analysis Scope")
    
    analysis_type = st.radio(
        "Choose focus",
        ["All Content", "High-Engagement Only", "Recent Posts Only"],
        help="Adjust analysis scope based on your needs"
    )

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
    st.warning("No data matches the selected filters. Please try again.")
    st.stop()

# Apply analysis scope
if analysis_type == "High-Engagement Only" and "engagement_rate" in filtered_df.columns:
    threshold = filtered_df["engagement_rate"].quantile(0.7)
    filtered_df = filtered_df[filtered_df["engagement_rate"] >= threshold]
elif analysis_type == "Recent Posts Only" and "post_date" in filtered_df.columns:
    recent_date = filtered_df["post_date"].max() - pd.Timedelta(days=30)
    filtered_df = filtered_df[filtered_df["post_date"] >= recent_date]

# Results summary
st.success(f"**Showing {len(filtered_df):,} posts** from total {len(df):,} posts")

st.markdown("---")

# =============================================================================
# SECTION 1: OVERVIEW & KPIs
# =============================================================================

st.header("Performance Overview")

# KPI Section
kpis = calculate_kpis(filtered_df)

kpi_col1, kpi_col2, kpi_col3 = st.columns(3)

with kpi_col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div style="font-size: 1.5rem;"></div>
        <div class="kpi-number">{kpis['total_posts']:,}</div>
        <div class="kpi-label">Total Posts</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col2:
    avg_er = kpis['avg_engagement_rate']
    er_display = f"{avg_er:.2%}" if not pd.isna(avg_er) else "N/A"
    st.markdown(f"""
    <div class="kpi-card">
        <div style="font-size: 1.5rem;">💫</div>
        <div class="kpi-number">{er_display}</div>
        <div class="kpi-label">Avg Engagement Rate</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div style="font-size: 1.5rem;">❤️</div>
        <div class="kpi-number">{kpis['total_engagement']:,}</div>
        <div class="kpi-label">Total Engagement</div>
    </div>
    """, unsafe_allow_html=True)

# Charts section
st.subheader("Performance Visualizations")

# Tabs for better organization
tab1, tab2, tab3 = st.tabs(["Time Trends", "Platform Comparison", "Sentiment Analysis"])

with tab1:
    chart = create_timeseries_chart(filtered_df)
    if chart:
        st.altair_chart(chart, use_container_width=True)
        st.markdown("""
        **How to Read This Chart:**
        - **X-axis**: Days when posts were published
        - **Y-axis**: Total engagement (likes + shares + comments)
        - **Insight**: Look for patterns to optimize posting schedule
        """)
    else:
        st.warning("⚠️ No time data available to display trends")

with tab2:
    chart = create_platform_chart(filtered_df)
    if chart:
        st.altair_chart(chart, use_container_width=True)
        st.markdown("""
        **Platform Analysis Guide:**
        - **Height**: Average engagement rate per platform
        - **Strategy**: Focus content efforts on top-performing platforms
        """)
    else:
        st.warning("⚠️ No platform data available")

with tab3:
    sent_col1, sent_col2 = st.columns([2, 1])

    with sent_col1:
        chart = create_sentiment_chart(filtered_df)
        if chart:
            st.altair_chart(chart, use_container_width=True)
        else:
            st.warning("⚠️ No sentiment data available")

    with sent_col2:
        st.markdown("#### 💭 Sentiment Distribution")
        
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

st.markdown("---")

# =============================================================================
# SECTION 2: ADVANCED TRENDS ANALYSIS  
# =============================================================================

st.header("🔬 Advanced Trends Analysis")

# Advanced metrics
metrics_col1, metrics_col2, metrics_col3 = st.columns(3)

with metrics_col1:
    if "engagement_rate" in filtered_df.columns and len(filtered_df) > 0:
        high_quality_posts = len(filtered_df[filtered_df["engagement_rate"] > filtered_df["engagement_rate"].quantile(0.8)])
        total_posts = len(filtered_df)
        quality_score = (high_quality_posts / total_posts * 100) if total_posts > 0 else 0
        
        st.metric("🏆 Content Quality Score", f"{quality_score:.1f}%", 
                 help=f"{high_quality_posts:,} high-quality posts")
    else:
        st.metric("🏆 Content Quality Score", "N/A")

with metrics_col2:
    if "platform" in filtered_df.columns and len(filtered_df) > 0:
        platform_count = filtered_df["platform"].nunique()
        most_used = filtered_df["platform"].mode().iloc[0] if len(filtered_df) > 0 else "N/A"
        
        st.metric("Platform Diversity", f"{platform_count} platforms", 
                 help=f"Most used: {most_used}")
    else:
        st.metric("Platform Diversity", "N/A")

with metrics_col3:
    if "post_date" in filtered_df.columns and len(filtered_df) > 0:
        date_range_days = (filtered_df["post_date"].max() - filtered_df["post_date"].min()).days
        posts_per_day = len(filtered_df) / date_range_days if date_range_days > 0 else 0
        
        st.metric("⚡ Content Velocity", f"{posts_per_day:.1f} posts/day", 
                 help=f"Over {date_range_days:,} days")
    else:
        st.metric("Content Velocity", "N/A")

# Advanced analysis tabs
adv_tab1, adv_tab2, adv_tab3, adv_tab4 = st.tabs([
    "Hashtag Intelligence", 
    "Topic Insights", 
    "Optimal Timing", 
    "CTA Analysis"
])

with adv_tab1:
    hashtag_col1, hashtag_col2 = st.columns([3, 1])
    
    with hashtag_col1:
        chart = create_hashtag_chart(filtered_df)
        if chart:
            st.altair_chart(chart, use_container_width=True)
        else:
            st.warning("No hashtag data available in current selection")
    
    with hashtag_col2:
        st.markdown("#### Top Performers")
        
        if "hashtag" in filtered_df.columns:
            top_hashtags = (
                filtered_df.groupby("hashtag")
                .agg(posts=("post_id", "count"), avg_er=("engagement_rate", "mean"))
                .sort_values(["posts", "avg_er"], ascending=[False, False])
                .head(5)
            )
            
            for hashtag, row in top_hashtags.iterrows():
                st.markdown(f"""
                <div class="trend-card">
                    <strong>#{hashtag}</strong><br>
                    <span class="metric-badge">{row['posts']} posts</span>
                    <span class="metric-badge">{row['avg_er']:.2%} ER</span>
                </div>
                """, unsafe_allow_html=True)

with adv_tab2:
    topic_col1, topic_col2 = st.columns([3, 1])
    
    with topic_col1:
        chart = create_topic_chart(filtered_df)
        if chart:
            st.altair_chart(chart, use_container_width=True)
        else:
            st.warning("⚠️ No topic data available")
    
    with topic_col2:
        st.markdown("#### 🌟 Trending Topics")
        
        if "climate_topic" in filtered_df.columns:
            top_topics = (
                filtered_df.groupby("climate_topic")
                .agg(posts=("post_id", "count"), avg_er=("engagement_rate", "mean"))
                .sort_values(["posts", "avg_er"], ascending=[False, False])
                .head(5)
            )
            
            for topic, row in top_topics.iterrows():
                priority = "🔥" if row['avg_er'] > 0.03 and row['posts'] > 50 else "⭐" if row['avg_er'] > 0.02 else "📌"
                
                st.markdown(f"""
                <div class="insight-panel">
                    {priority} <strong>{topic}</strong><br>
                    {row['posts']} posts | {row['avg_er']:.2%} engagement
                </div>
                """, unsafe_allow_html=True)

with adv_tab3:
    time_col1, time_col2 = st.columns([3, 1])
    
    with time_col1:
        if "platform" in filtered_df.columns:
            platform_focus = st.selectbox(
                "Focus Platform for Time Analysis",
                options=[None] + sorted(filtered_df["platform"].dropna().unique()),
                index=0,
                format_func=lambda x: "All Platforms" if x is None else f"{x}",
                help="Select specific platform for detailed timing insights"
            )
        else:
            platform_focus = None
        
        chart = create_time_heatmap(filtered_df, platform_focus)
        if chart:
            st.altair_chart(chart, use_container_width=True)
        else:
            st.warning("⚠️ Insufficient time data for heatmap")
    
    with time_col2:
        st.markdown("#### Timing Guide")
        
        st.markdown("""
        <div class="heatmap-legend">
            <strong>Reading the Heatmap:</strong><br>
            Lower engagement (blue)<br>
            Moderate engagement (yellow)<br>  
            High engagement (red)<br><br>
            <strong>Look for:</strong><br>
            • Dark spots = Prime time<br>
            • Patterns = Audience habits<br>
            • Platform differences
        </div>
        """, unsafe_allow_html=True)

with adv_tab4:
    cta_chart = create_cta_chart(filtered_df)
    if cta_chart:
        st.altair_chart(cta_chart, use_container_width=True)
        
        st.markdown("""
        **CTA Optimization Guide:**
        - High-performing CTAs should be used more frequently.
        - Test different phrasings to see what resonates with your audience.
        """)
    else:
        st.info("💡 **CTA Analysis**: Requires relevant data columns for detailed analysis.")

st.markdown("---")

# =============================================================================
# EXPORT & INSIGHTS SUMMARY
# =============================================================================

st.subheader("💾 Export Analysis Results")

export_col1, export_col2, export_col3 = st.columns(3)

with export_col1:
    csv_data = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        f"📥 Download Complete Data ({len(filtered_df)} rows)",
        data=csv_data,
        file_name="social_media_complete_analysis.csv",
        mime="text/csv",
        help="Full filtered dataset with all metrics",
        use_container_width=True,
        type="primary"
    )

with export_col2:
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
            f"Platform Summary ({len(summary)} platforms)",
            data=summary_csv,
            file_name="platform_performance_summary.csv",
            mime="text/csv",
            help="Aggregated performance metrics by platform",
            use_container_width=True
        )

with export_col3:
    st.markdown("""
    **Analysis Complete:**  
    Performance metrics analyzed  
    Trends & patterns identified  
    Optimization insights generated  
    Ready for implementation  
    """)

# Final insights
st.markdown("---")
st.subheader("Key Strategic Insights")

insights_col1, insights_col2 = st.columns(2)

with insights_col1:
    st.success("""
    **Content Strategy:**
    - Focus on high-performing platforms for maximum reach
    - Balance sentiment mix: 60% positive, 30% neutral, 10% negative
    - Use trending hashtags but combine with niche ones
    - Post during identified peak engagement times
    """)

with insights_col2:
    st.info("""
    **Performance Optimization:**
    - Monitor quality score monthly (target: >20%)
    - Maintain consistent posting velocity
    - Test different CTAs and measure results
    - Adapt strategy based on topic performance
    """)

st.success("""
🚀 **Next Steps for Implementation:**
1. **Schedule Content:** Use optimal timing insights for content calendar
2. **Hashtag Strategy:** Implement top-performing hashtags in upcoming posts  
3. **A/B Test CTAs:** Test different call-to-action approaches
4. **Monthly Review:** Return to this analysis to track performance changes
""")
