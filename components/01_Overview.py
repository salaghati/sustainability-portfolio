"""
Overview page - KPIs and general insights.
"""
import streamlit as st
import pandas as pd
from utils import load_data_with_uploader, calculate_kpis, apply_data_filters
from charts import create_timeseries_chart, create_platform_chart, create_sentiment_chart


# Page config is handled by main app.py

st.title("📊 Tổng quan Dashboard")
st.caption("KPI chính và xu hướng tương tác mạng xã hội về sustainability")

# Load data
@st.cache_data(show_spinner=False)
def load_cached_data():
    return load_data_with_uploader()

try:
    df = load_cached_data()
except Exception as e:
    st.error(f"Lỗi khi tải dữ liệu: {e}")
    st.stop()

# Sidebar filters
with st.sidebar:
    st.header("🔍 Bộ lọc dữ liệu")
    
    # Platform filter
    if "platform" in df.columns:
        platforms = sorted(df["platform"].dropna().unique())
        platform_sel = st.multiselect(
            "Nền tảng",
            options=platforms,
            default=platforms,
            help="Chọn nền tảng để phân tích"
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
            help="Chọn cảm xúc bài đăng"
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
            max_value=max_date,
            help="Chọn khoảng thời gian phân tích"
        )
    else:
        date_range = None
    
    # Hashtag filter
    hashtag_filter = st.text_input(
        "Tìm hashtag chứa...",
        value="",
        help="Lọc theo hashtag (không phân biệt hoa thường)"
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
st.info(f"Hiển thị {len(filtered_df):,} bài đăng từ tổng số {len(df):,} bài (sau khi lọc)")

# KPIs section
st.subheader("📈 Chỉ số chính (KPI)")

kpis = calculate_kpis(filtered_df)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(
        "Tổng số bài", 
        f"{kpis['total_posts']:,}",
        help="Tổng số bài đăng trong dataset"
    )
with col2:
    avg_er = kpis['avg_engagement_rate']
    st.metric(
        "Engagement Rate TB", 
        f"{avg_er:.2%}" if not pd.isna(avg_er) else "N/A",
        help="Engagement rate trung bình = (likes+shares+comments)/followers"
    )
with col3:
    st.metric(
        "Tổng Engagement", 
        f"{kpis['total_engagement']:,}",
        help="Tổng số likes + shares + comments"
    )

st.markdown("---")

# Charts section
col1, col2 = st.columns(2)

with col1:
    st.subheader("📅 Xu hướng theo thời gian")
    
    chart = create_timeseries_chart(filtered_df)
    if chart:
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("Không có dữ liệu thời gian để hiển thị")
    
    with st.expander("ℹ️ Giải thích"):
        st.markdown("""
        - **Trục X**: Ngày đăng bài
        - **Trục Y**: Tổng engagement (likes + shares + comments)
        - **Mục đích**: Xem xu hướng tương tác theo thời gian, phát hiện peak/drop
        """)

with col2:
    st.subheader("🏗️ Hiệu suất theo nền tảng")
    
    chart = create_platform_chart(filtered_df)
    if chart:
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("Không có dữ liệu nền tảng để hiển thị")
    
    with st.expander("ℹ️ Giải thích"):
        st.markdown("""
        - **Trục X**: Nền tảng mạng xã hội
        - **Trục Y**: Engagement rate trung bình
        - **Mục đích**: So sánh hiệu quả các nền tảng để tối ưu strategy
        """)

st.markdown("---")

# Sentiment analysis
st.subheader("🎭 Phân tích Sentiment")

col1, col2 = st.columns([2, 1])

with col1:
    chart = create_sentiment_chart(filtered_df)
    if chart:
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("Không có dữ liệu sentiment để hiển thị")

with col2:
    st.markdown("### Insights")
    if "post_sentiment" in filtered_df.columns:
        sentiment_counts = filtered_df["post_sentiment"].value_counts()
        st.markdown("**Phân bố Sentiment:**")
        for sentiment, count in sentiment_counts.items():
            percentage = count / len(filtered_df) * 100
            st.markdown(f"- **{sentiment}**: {count:,} bài ({percentage:.1f}%)")
    else:
        st.info("Không có dữ liệu sentiment")

with st.expander("ℹ️ Giải thích Sentiment"):
    st.markdown("""
    - **Positive**: Bài đăng tích cực, lạc quan
    - **Neutral**: Bài đăng trung tính, thông tin
    - **Negative**: Bài đăng tiêu cực, báo động
    - **Phân tích**: Giúp hiểu tone messaging và adjust content strategy
    """)

# Data table
st.markdown("---")
st.subheader("📋 Dữ liệu chi tiết")

with st.expander("Xem bảng dữ liệu"):
    st.dataframe(
        filtered_df[["post_date", "platform", "post_sentiment", "hashtag", 
                    "engagement_total", "engagement_rate", "user_followers"]].head(100),
        use_container_width=True
    )
    
    # Download button
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Tải CSV đã lọc",
        data=csv,
        file_name="sustainability_posts_filtered.csv",
        mime="text/csv"
    )
