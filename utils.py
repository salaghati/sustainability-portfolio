"""
Utilities for data processing and loading.
"""
import os
from typing import Optional
import pandas as pd
import numpy as np
import streamlit as st


@st.cache_data(show_spinner=False)
def load_data(csv_path: str) -> pd.DataFrame:
    """
    Load and preprocess social media data from CSV.
    
    Args:
        csv_path: Path to the CSV file
        
    Returns:
        Processed DataFrame with engagement metrics and normalized columns
    """
    df = pd.read_csv(
        csv_path,
        parse_dates=["post_date"],
        encoding="utf-8"
    )
    
    # Normalize numeric columns
    numeric_cols = [
        "engagement_likes",
        "engagement_shares", 
        "engagement_comments",
        "user_followers",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Create engagement metrics
    df["engagement_total"] = (
        df.get("engagement_likes", 0).fillna(0)
        + df.get("engagement_shares", 0).fillna(0)
        + df.get("engagement_comments", 0).fillna(0)
    )
    df["engagement_rate"] = np.where(
        df.get("user_followers", 0).fillna(0) > 0,
        df["engagement_total"] / df["user_followers"],
        np.nan,
    )

    # Create normalized date fields
    if "post_date" in df.columns:
        df["post_date"] = pd.to_datetime(df["post_date"], errors="coerce")
        df["post_month"] = df["post_date"].dt.to_period("M").dt.to_timestamp()

    # Normalize hashtag (remove nulls, lowercase)
    if "hashtag" in df.columns:
        df["hashtag"] = df["hashtag"].astype(str).str.strip().str.lower()

    # Normalize categorical columns
    for c in ["post_sentiment", "climate_topic", "platform"]:
        if c in df.columns:
            df[c] = df[c].astype(str)

    return df


def get_default_csv_path() -> str:
    """Get the default CSV path, preferring relative path for deployment."""
    relative_path = "sustainability_social_media_posts.csv"
    if os.path.exists(relative_path):
        return relative_path
    # Fallback to absolute path for local development
    return "/Users/macm1/Documents/Practice DA/Social Media Data/sustainability_social_media_posts.csv"


def load_data_with_uploader(default_path: Optional[str] = None) -> pd.DataFrame:
    """
    Load data with file uploader fallback.
    
    Args:
        default_path: Default CSV path to try first
        
    Returns:
        Processed DataFrame
    """
    if default_path is None:
        default_path = get_default_csv_path()
        
    # Try to load default file
    if os.path.exists(default_path):
        try:
            return load_data(default_path)
        except Exception as e:
            st.error(f"Không thể đọc file mặc định: {e}")
    
    # Show file uploader if default fails
    st.warning("File dữ liệu mặc định không tìm thấy. Vui lòng upload file CSV:")
    uploaded_file = st.file_uploader(
        "Chọn file CSV dữ liệu mạng xã hội", 
        type=["csv"],
        help="File CSV cần có các cột: post_id, platform, engagement_likes, etc."
    )
    
    if uploaded_file is not None:
        try:
            return load_data(uploaded_file)
        except Exception as e:
            st.error(f"Lỗi khi đọc file upload: {e}")
            st.stop()
    else:
        st.info("Hãy upload file CSV để tiếp tục")
        st.stop()


def calculate_kpis(df: pd.DataFrame) -> dict:
    """
    Calculate key performance indicators from the dataset.
    
    Args:
        df: Input DataFrame
        
    Returns:
        Dictionary with KPI values
    """
    total_posts = int(len(df))
    avg_eng_rate = float(df["engagement_rate"].mean(skipna=True)) if "engagement_rate" in df else float("nan")
    total_eng = int(df["engagement_total"].sum()) if "engagement_total" in df else 0
    
    return {
        "total_posts": total_posts,
        "avg_engagement_rate": avg_eng_rate,
        "total_engagement": total_eng
    }


def apply_data_filters(df: pd.DataFrame, 
                      platforms: list = None,
                      sentiments: list = None, 
                      date_range: tuple = None,
                      hashtag_filter: str = "") -> pd.DataFrame:
    """
    Apply filters to the dataset.
    
    Args:
        df: Input DataFrame
        platforms: List of platforms to filter
        sentiments: List of sentiments to filter
        date_range: Tuple of (start_date, end_date)
        hashtag_filter: String to search in hashtags
        
    Returns:
        Filtered DataFrame
    """
    filtered = df.copy()
    
    if platforms and "platform" in filtered.columns:
        filtered = filtered[filtered["platform"].isin(platforms)]
        
    if sentiments and "post_sentiment" in filtered.columns:
        filtered = filtered[filtered["post_sentiment"].isin(sentiments)]
        
    if date_range and "post_date" in filtered.columns:
        start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
        mask = (filtered["post_date"] >= start) & (filtered["post_date"] <= end)
        filtered = filtered[mask]
        
    if hashtag_filter and "hashtag" in filtered.columns:
        filtered = filtered[filtered["hashtag"].str.contains(hashtag_filter.strip().lower(), na=False)]
    
    return filtered
