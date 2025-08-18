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


# Page config
st.set_page_config(
    page_title="Trends - Social Media Analytics", 
    layout="wide",
    page_icon="📈"
)

st.title("📈 Phân tích Xu hướng")
st.caption("Hashtag, chủ đề, thời gian đăng và CTA performance")

# Load data
@st.cache_data(show_spinner=False)
def load_cached_data():
    return load_data_with_uploader()

try:
    df = load_cached_data()
except Exception as e:
    st.error(f"Lỗi khi tải dữ liệu: {e}")
    st.stop()

# Sidebar filters (same as Overview page)
with st.sidebar:
    st.header("🔍 Bộ lọc dữ liệu")
    
    # Platform filter
    if "platform" in df.columns:
        platforms = sorted(df["platform"].dropna().unique())
        platform_sel = st.multiselect(
            "Nền tảng",
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
            "Khoảng thời gian",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
    else:
        date_range = None
    
    # Hashtag filter
    hashtag_filter = st.text_input(
        "Tìm hashtag chứa...",
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

st.info(f"Phân tích {len(filtered_df):,} bài đăng từ tổng số {len(df):,} bài")

# Hashtag Analysis
st.subheader("🏷️ Top Hashtag Performance")

col1, col2 = st.columns([3, 1])

with col1:
    chart = create_hashtag_chart(filtered_df)
    if chart:
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("Không có dữ liệu hashtag để hiển thị")

with col2:
    st.markdown("### 📊 Hashtag Insights")
    if "hashtag" in filtered_df.columns:
        top_hashtags = (
            filtered_df.groupby("hashtag")
            .agg(posts=("post_id", "count"), avg_er=("engagement_rate", "mean"))
            .sort_values(["posts", "avg_er"], ascending=[False, False])
            .head(5)
        )
        
        st.markdown("**Top 5 Hashtag:**")
        for hashtag, row in top_hashtags.iterrows():
            st.markdown(f"- **{hashtag}**: {row['posts']} bài (ER: {row['avg_er']:.2%})")
    else:
        st.info("Không có dữ liệu hashtag")

with st.expander("ℹ️ Giải thích Hashtag Analytics"):
    st.markdown("""
    - **Trục X**: Số lượng bài đăng sử dụng hashtag
    - **Màu sắc**: Engagement rate trung bình
    - **Mục đích**: Tìm hashtag hiệu quả cho strategy content
    - **Lưu ý**: Cân bằng giữa volume và engagement quality
    """)

st.markdown("---")

# Climate Topics
st.subheader("🌍 Chủ đề Sustainability")

col1, col2 = st.columns([3, 1])

with col1:
    chart = create_topic_chart(filtered_df)
    if chart:
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("Không có dữ liệu chủ đề để hiển thị")

with col2:
    st.markdown("### 📈 Topic Insights")
    if "climate_topic" in filtered_df.columns:
        top_topics = (
            filtered_df.groupby("climate_topic")
            .agg(posts=("post_id", "count"), avg_er=("engagement_rate", "mean"))
            .sort_values(["posts", "avg_er"], ascending=[False, False])
            .head(5)
        )
        
        st.markdown("**Top 5 Chủ đề:**")
        for topic, row in top_topics.iterrows():
            st.markdown(f"- **{topic}**: {row['posts']} bài (ER: {row['avg_er']:.2%})")
    else:
        st.info("Không có dữ liệu chủ đề")

with st.expander("ℹ️ Giải thích Climate Topics"):
    st.markdown("""
    - **Phân loại**: Các chủ đề sustainability như Waste Reduction, Energy Storage, etc.
    - **Metric**: Số bài và engagement rate trung bình
    - **Strategy**: Focus vào topics có ER cao và volume phù hợp
    - **Trend**: Theo dõi shift của public interest
    """)

st.markdown("---")

# Time Heatmap Analysis
st.subheader("⏰ Phân tích Thời gian Tối ưu")

# Platform selector for heatmap
if "platform" in filtered_df.columns:
    platform_focus = st.selectbox(
        "Chọn nền tảng để phân tích heatmap (hoặc để trống để xem tất cả)",
        options=[None] + sorted(filtered_df["platform"].dropna().unique()),
        index=0,
        format_func=lambda x: "Tất cả nền tảng" if x is None else x
    )
else:
    platform_focus = None

chart = create_time_heatmap(filtered_df, platform_focus)
if chart:
    st.altair_chart(chart, use_container_width=True)
else:
    st.info("Không có dữ liệu thời gian để hiển thị heatmap")

with st.expander("ℹ️ Giải thích Time Heatmap"):
    st.markdown("""
    - **Trục X**: Giờ trong ngày (0-23)
    - **Trục Y**: Thứ trong tuần
    - **Màu sắc**: Engagement rate trung bình (tối hơn = cao hơn)
    - **Sử dụng**: Tìm thời điểm tối ưu để post content
    - **Platform**: Có thể khác nhau giữa các nền tảng
    """)

st.markdown("---")

# CTA Analysis
st.subheader("📢 Call-to-Action Performance")

chart = create_cta_chart(filtered_df)
if chart:
    st.altair_chart(chart, use_container_width=True)
    
    with st.expander("ℹ️ Giải thích CTA Analytics"):
        st.markdown("""
        - **Trục X**: Shares + Comments trung bình (proxy cho interaction)
        - **Trục Y**: Các loại Call-to-Action
        - **Màu sắc**: Engagement rate trung bình
        - **Mục đích**: Tìm CTA hiệu quả nhất để drive action
        - **Strategy**: Optimize messaging dựa trên performance data
        """)
else:
    st.info("Không có đủ dữ liệu CTA để phân tích (cần cột call_to_action, engagement_shares, engagement_comments)")

st.markdown("---")

# Advanced Metrics
st.subheader("📊 Metrics Nâng cao")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 💡 Content Quality")
    if "engagement_rate" in filtered_df.columns:
        high_er_posts = len(filtered_df[filtered_df["engagement_rate"] > filtered_df["engagement_rate"].quantile(0.8)])
        total_posts = len(filtered_df)
        quality_rate = high_er_posts / total_posts if total_posts > 0 else 0
        
        st.metric("High-ER Posts", f"{high_er_posts:,}", f"{quality_rate:.1%} of total")
        st.caption("Bài có ER > percentile 80")
    else:
        st.info("Cần dữ liệu engagement_rate")

with col2:
    st.markdown("### 📱 Platform Diversity")
    if "platform" in filtered_df.columns:
        platform_count = filtered_df["platform"].nunique()
        most_used = filtered_df["platform"].mode().iloc[0] if len(filtered_df) > 0 else "N/A"
        
        st.metric("Số nền tảng", platform_count)
        st.caption(f"Chủ yếu: {most_used}")
    else:
        st.info("Cần dữ liệu platform")

with col3:
    st.markdown("### 🗓️ Posting Frequency")
    if "post_date" in filtered_df.columns:
        date_range_days = (filtered_df["post_date"].max() - filtered_df["post_date"].min()).days
        posts_per_day = len(filtered_df) / date_range_days if date_range_days > 0 else 0
        
        st.metric("Bài/ngày TB", f"{posts_per_day:.1f}")
        st.caption(f"Trong {date_range_days} ngày")
    else:
        st.info("Cần dữ liệu post_date")

# Data export
st.markdown("---")
st.subheader("💾 Export Dữ liệu")

export_col1, export_col2 = st.columns(2)

with export_col1:
    # Full filtered data
    csv_full = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Tải toàn bộ dữ liệu đã lọc",
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
            "📊 Tải summary thống kê",
            data=summary_csv,
            file_name="platform_summary_stats.csv",
            mime="text/csv"
        )
