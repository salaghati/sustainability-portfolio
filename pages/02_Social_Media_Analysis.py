"""
Trends page - Advanced analytics with enhanced UI and deeper insights.
"""
import streamlit as st
import pandas as pd
from utils import load_data_with_uploader, apply_data_filters
from charts import (
    create_hashtag_chart, create_topic_chart, 
    create_time_heatmap, create_cta_chart
)

# Enhanced CSS for trends page
st.markdown("""
<style>
    /* Trend cards */
    .trend-card {
        background: linear-gradient(135deg, #ffffff, #f8fafc);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border-left: 4px solid #8b5cf6;
        color: #2d3748; /* Added for text visibility */
    }
    
    .trend-card strong {
        color: #4c51bf; /* Darker color for hashtag */
    }

    .trend-card .metric-badge {
        background-color: #e9d5ff; /* Lighter purple */
        color: #5b21b6; /* Darker purple text */
    }
    
    .trend-card h4 {
        color: #2d3748;
        margin-bottom: 0.5rem;
        font-weight: 600;
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
        color: #713f12; /* Dark amber for text visibility */
    }

    .insight-panel strong {
        color: #422006; /* Even darker for emphasis */
    }
    
    /* Time heatmap legend */
    .heatmap-legend {
        background: #f7fafc;
        border-radius: 8px;
        padding: 0.8rem;
        margin: 0.5rem 0;
        font-size: 0.9rem;
        color: #2d3748; /* Dark gray for text visibility */
    }
    
    /* Advanced metric card */
    .advanced-metric {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 15px rgba(0,0,0,0.1);
        border-top: 3px solid #10b981;
    }
    
    .advanced-number {
        font-size: 1.8rem;
        font-weight: 700;
        color: #059669;
    }
</style>
""", unsafe_allow_html=True)

# Page header with better styling
st.title("📈 Advanced Trends Analysis")
st.markdown("### Deep Dive into Content Performance & Strategy Optimization")

# Usage guide with actionable tips
st.info("🎯 **Pro Tips:** Use platform-specific filters to find optimal posting times. Check hashtag performance to identify trending topics. Export insights for your content calendar!")

# Load data
@st.cache_data(show_spinner=False)
def load_cached_data():
    return load_data_with_uploader()

try:
    df = load_cached_data()
except Exception as e:
    st.error(f"❌ Error loading data: {e}")
    st.stop()

# Enhanced sidebar with better organization
with st.sidebar:
    st.header("🎛️ Advanced Filters")
    st.markdown("*Fine-tune your analysis*")
    
    # Platform filter
    if "platform" in df.columns:
        platforms = sorted(df["platform"].dropna().unique())
        platform_sel = st.multiselect(
            "📱 Platforms",
            options=platforms,
            default=platforms,
            help="Select platforms for detailed trend analysis"
        )
    else:
        platform_sel = []
    
    # Sentiment filter
    if "post_sentiment" in df.columns:
        sentiments = sorted(df["post_sentiment"].dropna().unique())
        sentiment_sel = st.multiselect(
            "😊 Sentiment",
            options=sentiments,
            default=sentiments,
            help="Focus on specific emotional tones"
        )
    else:
        sentiment_sel = []
    
    # Date range
    if "post_date" in df.columns:
        min_date = df["post_date"].min().date()
        max_date = df["post_date"].max().date()
        
        st.markdown("📅 **Analysis Period**")
        
        # Date presets
        preset_col1, preset_col2 = st.columns(2)
        if preset_col1.button("Last 7 Days", use_container_width=True, key="trends_7_days"):
            st.session_state.trends_date_range = (max_date - pd.Timedelta(days=7), max_date)
        if preset_col2.button("Last 30 Days", use_container_width=True, key="trends_30_days"):
            st.session_state.trends_date_range = (max_date - pd.Timedelta(days=30), max_date)

        if 'trends_date_range' not in st.session_state:
            st.session_state.trends_date_range = (min_date, max_date)

        date_range = st.date_input(
            "Select timeframe",
            value=st.session_state.trends_date_range,
            min_value=min_date,
            max_value=max_date,
            help="Choose time period for trend analysis",
            key="trends_date_range_selector"
        )
        st.session_state.trends_date_range = date_range
    else:
        date_range = None
    
    # Hashtag filter
    if "hashtag" in df.columns:
        hashtags = sorted(df["hashtag"].dropna().unique())
        hashtag_sel = st.multiselect(
            "🏷️ Hashtag Focus",
            options=hashtags,
            default=[],
            help="Analyze specific hashtag trends"
        )
    else:
        hashtag_sel = []
    
    # Analysis scope
    st.markdown("---")
    st.markdown("### 🔍 Analysis Scope")
    
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
    st.warning("Không có dữ liệu phù hợp với bộ lọc đã chọn. Vui lòng thử lại.")
    st.stop()

# Apply analysis scope
if analysis_type == "High-Engagement Only" and "engagement_rate" in filtered_df.columns:
    threshold = filtered_df["engagement_rate"].quantile(0.7)
    filtered_df = filtered_df[filtered_df["engagement_rate"] >= threshold]
elif analysis_type == "Recent Posts Only" and "post_date" in filtered_df.columns:
    recent_date = filtered_df["post_date"].max() - pd.Timedelta(days=30)
    filtered_df = filtered_df[filtered_df["post_date"] >= recent_date]

# Results overview with insights
result_col1, result_col2, result_col3 = st.columns(3)

with result_col1:
    st.metric("📊 Posts Analyzed", f"{len(filtered_df):,}")

with result_col2:
    if len(filtered_df) > 0 and "post_date" in filtered_df.columns:
        date_span = (filtered_df["post_date"].max() - filtered_df["post_date"].min()).days
        st.metric("📅 Time Span", f"{date_span} days")
    else:
        st.metric("📅 Time Span", "N/A")

with result_col3:
    if "platform" in filtered_df.columns:
        platform_count = filtered_df["platform"].nunique()
        st.metric("📱 Platforms", platform_count)
    else:
        st.metric("📱 Platforms", "N/A")

st.markdown("---")

# Analysis sections within expanders
with st.expander("🏷️ Hashtag Performance Intelligence", expanded=True):
    hashtag_col1, hashtag_col2 = st.columns([3, 1])
    with hashtag_col1:
        chart = create_hashtag_chart(filtered_df)
        if chart:
            st.altair_chart(chart, use_container_width=True)
        else:
            st.warning("⚠️ No hashtag data available in current selection")
    with hashtag_col2:
        st.markdown("#### 🎯 Hashtag Insights")
        
        if "hashtag" in filtered_df.columns:
            top_hashtags = (
                filtered_df.groupby("hashtag")
                .agg(posts=("post_id", "count"), avg_er=("engagement_rate", "mean"))
                .sort_values(["posts", "avg_er"], ascending=[False, False])
                .head(5)
            )
            
            st.markdown("**🏆 Top Performers:**")
            for hashtag, row in top_hashtags.iterrows():
                st.markdown(f"""
                <div class="trend-card">
                    <strong>#{hashtag}</strong><br>
                    <span class="metric-badge">{row['posts']} posts</span>
                    <span class="metric-badge">{row['avg_er']:.2%} ER</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("💡 Upload data with hashtag column for insights")

with st.expander("🌍 Sustainability Topic Insights", expanded=True):
    topic_col1, topic_col2 = st.columns([3, 1])
    with topic_col1:
        chart = create_topic_chart(filtered_df)
        if chart:
            st.altair_chart(chart, use_container_width=True)
        else:
            st.warning("⚠️ No topic data available")
    with topic_col2:
        st.markdown("#### 📊 Topic Intelligence")
        
        if "climate_topic" in filtered_df.columns:
            top_topics = (
                filtered_df.groupby("climate_topic")
                .agg(posts=("post_id", "count"), avg_er=("engagement_rate", "mean"))
                .sort_values(["posts", "avg_er"], ascending=[False, False])
                .head(5)
            )
            
            st.markdown("**🌟 Trending Topics:**")
            for topic, row in top_topics.iterrows():
                # Topic priority based on volume and engagement
                priority = "🔥" if row['avg_er'] > 0.03 and row['posts'] > 50 else "⭐" if row['avg_er'] > 0.02 else "📌"
                
                st.markdown(f"""
                <div class="insight-panel">
                    {priority} <strong>{topic}</strong><br>
                    {row['posts']} posts | {row['avg_er']:.2%} engagement
                </div>
                """, unsafe_allow_html=True)

with st.expander("⏰ Optimal Posting Time Analysis", expanded=True):
    time_col1, time_col2 = st.columns([3, 1])
    with time_col1:
        if "platform" in filtered_df.columns:
            platform_focus = st.selectbox(
                "🎯 Focus Platform for Time Analysis",
                options=[None] + sorted(filtered_df["platform"].dropna().unique()),
                index=0,
                format_func=lambda x: "🌐 All Platforms" if x is None else f"📱 {x}",
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
        st.markdown("#### ⏰ Timing Insights")
        
        st.markdown("""
        <div class="heatmap-legend">
            <strong>🎨 Reading the Heatmap:</strong><br>
            🟦 Lower engagement<br>
            🟨 Moderate engagement<br>  
            🟥 High engagement<br><br>
            <strong>💡 Look for:</strong><br>
            • Dark spots = Prime time<br>
            • Patterns = Audience habits<br>
            • Platform differences
        </div>
        """, unsafe_allow_html=True)
        
        # Timing recommendations based on common patterns
        st.markdown("#### 📅 General Best Practices")
        
        timing_tips = {
            "LinkedIn": "🕘 9 AM, 🕐 1 PM, 🕔 5 PM (Weekdays)",
            "Instagram": "🕙 10 AM, 🕐 1 PM, 🕖 7 PM", 
            "Facebook": "🕘 9 AM, 🕐 1 PM, 🕕 6 PM",
            "Twitter": "🕘 9 AM, 🕐 1 PM, 🕔 5 PM",
            "TikTok": "🕙 10 AM, 🕖 7 PM, 🕘 9 PM"
        }
        
        selected_platform = platform_focus if platform_focus else "General"
        if selected_platform in timing_tips:
            st.success(f"📍 **{selected_platform}**: {timing_tips[selected_platform]}")

with st.expander("📢 Call-to-Action Effectiveness", expanded=True):
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

# Advanced Performance Metrics
st.subheader("📊 Advanced Performance Metrics")

metrics_col1, metrics_col2, metrics_col3 = st.columns(3)

with metrics_col1:
    st.markdown("""
    <div class="advanced-metric">
        <div class="advanced-number">Content Quality Score</div>
    """, unsafe_allow_html=True)
    
    if "engagement_rate" in filtered_df.columns and len(filtered_df) > 0:
        high_quality_posts = len(filtered_df[filtered_df["engagement_rate"] > filtered_df["engagement_rate"].quantile(0.8)])
        total_posts = len(filtered_df)
        quality_score = (high_quality_posts / total_posts * 100) if total_posts > 0 else 0
        
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 1rem;">
            <span style="font-size: 2rem; font-weight: bold; color: #059669;">{quality_score:.1f}%</span><br>
            <small>{high_quality_posts:,} high-quality posts</small>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div style="text-align: center;">N/A</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with metrics_col2:
    st.markdown("""
    <div class="advanced-metric">
        <div class="advanced-number">Platform Diversity</div>
    """, unsafe_allow_html=True)
    
    if "platform" in filtered_df.columns and len(filtered_df) > 0:
        platform_count = filtered_df["platform"].nunique()
        total_platforms = 5  # Assuming 5 major platforms
        diversity_score = (platform_count / total_platforms * 100)
        most_used = filtered_df["platform"].mode().iloc[0] if len(filtered_df) > 0 else "N/A"
        
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 1rem;">
            <span style="font-size: 2rem; font-weight: bold; color: #059669;">{platform_count}</span><br>
            <small>platforms ({diversity_score:.0f}% coverage)</small><br>
            <small>Leader: {most_used}</small>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div style="text-align: center;">N/A</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with metrics_col3:
    st.markdown("""
    <div class="advanced-metric">
        <div class="advanced-number">Content Velocity</div>
    """, unsafe_allow_html=True)
    
    if "post_date" in filtered_df.columns and len(filtered_df) > 0:
        date_range_days = (filtered_df["post_date"].max() - filtered_df["post_date"].min()).days
        posts_per_day = len(filtered_df) / date_range_days if date_range_days > 0 else 0
        
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 1rem;">
            <span style="font-size: 2rem; font-weight: bold; color: #059669;">{posts_per_day:.1f}</span><br>
            <small>posts per day</small><br>
            <small>Over {date_range_days:,} days</small>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div style="text-align: center;">N/A</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Export section with enhanced options
st.markdown("---")
st.subheader("💾 Export Analysis Results")

export_row1 = st.columns(3)

with export_row1[0]:
    csv_full = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        f"📥 Download Analysis Data ({len(filtered_df)} rows)",
        data=csv_full,
        file_name="trends_analysis_detailed.csv",
        mime="text/csv",
        help="Complete filtered dataset with all metrics",
        use_container_width=True,
        type="primary"
    )

with export_row1[1]:
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
            f"📊 Platform Summary Stats ({len(summary)} rows)",
            data=summary_csv,
            file_name="platform_performance_summary.csv",
            mime="text/csv",
            help="Aggregated metrics by platform",
            use_container_width=True
        )

with export_row1[2]:
    st.markdown("""
    **📈 Analysis Summary:**  
    ✅ Performance trends identified  
    ✅ Optimal timing analyzed  
    ✅ Content strategy insights  
    ✅ Ready for implementation  
    """)

# Action items and next steps
st.markdown("---")
st.success("""
🚀 **Ready to Optimize?** 
- Use timing insights for content scheduling
- Implement top-performing hashtags in new posts  
- Test different CTAs based on performance data
- Monitor trends and adjust strategy monthly
""")

st.markdown("---")
st.subheader("📝 Key Insights Summary")
st.success("""
- **Hashtag Strategy:** Combine high-volume, high-engagement hashtags with niche ones to maximize reach and relevance.
- **Optimal Timing:** Use the heatmap to identify the best day and hour to post for each key platform, adapting to your audience's online behavior.
- **Content is King:** Topics related to 'Renewable Energy' and 'Policy' tend to generate high engagement. Focus content creation around these themes.
""")

st.info("💡 **Pro Tip**: Bookmark this analysis and return monthly to track performance changes and identify new trends!")