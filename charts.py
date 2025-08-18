"""
Chart creation functions using Altair.
"""
from typing import Optional
import pandas as pd
import altair as alt
import streamlit as st


def create_timeseries_chart(df: pd.DataFrame) -> Optional[alt.Chart]:
    """
    Create time series chart showing engagement over time.
    
    Args:
        df: DataFrame with post_date and engagement_total columns
        
    Returns:
        Altair chart or None if insufficient data
    """
    if "post_date" not in df.columns:
        return None
        
    ts = (
        df.dropna(subset=["post_date"]).copy()
        .assign(post_day=lambda d: d["post_date"].dt.date)
        .groupby("post_day", as_index=False)["engagement_total"].sum()
    )
    
    if ts.empty:
        return None
        
    chart = (
        alt.Chart(ts)
        .mark_line(point=True)
        .encode(
            x=alt.X("post_day:T", title="Ngày"),
            y=alt.Y("engagement_total:Q", title="Tổng engagement"),
            tooltip=["post_day:T", "engagement_total:Q"],
        )
        .properties(height=300)
    )
    return chart


def create_platform_chart(df: pd.DataFrame) -> Optional[alt.Chart]:
    """
    Create platform performance chart.
    
    Args:
        df: DataFrame with platform and engagement metrics
        
    Returns:
        Altair chart or None if insufficient data
    """
    if "platform" not in df.columns:
        return None
        
    plat = (
        df.groupby("platform", as_index=False)
        .agg(engagement_rate=("engagement_rate", "mean"), posts=("post_id", "count"))
        .sort_values("engagement_rate", ascending=False)
    )
    
    if plat.empty:
        return None
        
    chart = (
        alt.Chart(plat)
        .mark_bar()
        .encode(
            x=alt.X("platform:N", title="Nền tảng", sort="-y"),
            y=alt.Y("engagement_rate:Q", title="Engagement rate TB", axis=alt.Axis(format="%")),
            tooltip=[
                "platform", 
                alt.Tooltip("posts:Q", title="Số bài"), 
                alt.Tooltip("engagement_rate:Q", title="ER TB", format=".2%")
            ],
            color="platform:N",
        )
        .properties(height=300)
    )
    return chart


def create_sentiment_chart(df: pd.DataFrame) -> Optional[alt.Chart]:
    """
    Create sentiment distribution chart.
    
    Args:
        df: DataFrame with post_sentiment column
        
    Returns:
        Altair chart or None if insufficient data
    """
    if "post_sentiment" not in df.columns:
        return None
        
    sent = df["post_sentiment"].value_counts().reset_index()
    sent.columns = ["post_sentiment", "count"]
    
    if sent.empty:
        return None
        
    chart = (
        alt.Chart(sent)
        .mark_bar()
        .encode(
            x=alt.X("post_sentiment:N", title="Sentiment"),
            y=alt.Y("count:Q", title="Số bài"),
            tooltip=["post_sentiment", "count"],
            color="post_sentiment:N",
        )
        .properties(height=300)
    )
    return chart


def create_hashtag_chart(df: pd.DataFrame) -> Optional[alt.Chart]:
    """
    Create top hashtags chart.
    
    Args:
        df: DataFrame with hashtag and engagement metrics
        
    Returns:
        Altair chart or None if insufficient data
    """
    if "hashtag" not in df.columns:
        return None
        
    top = (
        df.groupby("hashtag", as_index=False)
        .agg(posts=("post_id", "count"), er=("engagement_rate", "mean"))
        .sort_values(["posts", "er"], ascending=[False, False])
        .head(15)
    )
    
    if top.empty:
        return None
        
    chart = (
        alt.Chart(top)
        .mark_bar()
        .encode(
            x=alt.X("posts:Q", title="Số bài"),
            y=alt.Y("hashtag:N", sort="-x", title="Hashtag"),
            tooltip=[
                "hashtag", 
                "posts", 
                alt.Tooltip("er:Q", title="ER TB", format=".2%")
            ],
            color=alt.Color("er:Q", title="ER TB", scale=alt.Scale(scheme="blues")),
        )
        .properties(height=400)
    )
    return chart


def create_topic_chart(df: pd.DataFrame) -> Optional[alt.Chart]:
    """
    Create climate topics chart.
    
    Args:
        df: DataFrame with climate_topic column
        
    Returns:
        Altair chart or None if insufficient data
    """
    if "climate_topic" not in df.columns:
        return None
        
    topic = (
        df.groupby("climate_topic", as_index=False)
        .agg(posts=("post_id", "count"), er=("engagement_rate", "mean"))
        .sort_values(["posts", "er"], ascending=[False, False])
        .head(20)
    )
    
    if topic.empty:
        return None
        
    chart = (
        alt.Chart(topic)
        .mark_bar()
        .encode(
            x=alt.X("posts:Q", title="Số bài"),
            y=alt.Y("climate_topic:N", sort="-x", title="Chủ đề"),
            tooltip=[
                "climate_topic", 
                "posts", 
                alt.Tooltip("er:Q", title="ER TB", format=".2%")
            ],
            color=alt.Color("er:Q", title="ER TB", scale=alt.Scale(scheme="greens")),
        )
        .properties(height=400)
    )
    return chart


def create_time_heatmap(df: pd.DataFrame, platform_focus: Optional[str] = None) -> Optional[alt.Chart]:
    """
    Create time heatmap showing engagement by day of week and hour.
    
    Args:
        df: DataFrame with post_date and engagement metrics
        platform_focus: Optional platform to focus on
        
    Returns:
        Altair chart or None if insufficient data
    """
    if "post_date" not in df.columns:
        return None
        
    data = df.copy()
    if platform_focus and "platform" in data.columns:
        data = data[data["platform"] == platform_focus]
        
    data = data.dropna(subset=["post_date"]).assign(
        dow=lambda d: d["post_date"].dt.day_name(),
        hod=lambda d: d["post_date"].dt.hour,
    )
    
    if data.empty:
        return None
        
    heat = (
        data.groupby(["dow", "hod"], as_index=False)
        .agg(er=("engagement_rate", "mean"), n=("post_id", "count"))
    )
    
    # Day order
    dow_order = [
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
    ]
    
    chart = (
        alt.Chart(heat)
        .mark_rect()
        .encode(
            x=alt.X("hod:O", title="Giờ trong ngày"),
            y=alt.Y("dow:N", title="Thứ", sort=dow_order),
            color=alt.Color("er:Q", title="ER TB", scale=alt.Scale(scheme="magma")),
            tooltip=[
                "dow", 
                "hod", 
                alt.Tooltip("er:Q", title="ER TB", format=".2%"), 
                alt.Tooltip("n:Q", title="Số bài")
            ],
        )
        .properties(height=280)
    )
    return chart


def create_cta_chart(df: pd.DataFrame) -> Optional[alt.Chart]:
    """
    Create Call-to-Action performance chart.
    
    Args:
        df: DataFrame with CTA and engagement metrics
        
    Returns:
        Altair chart or None if insufficient data
    """
    required_cols = {"engagement_shares", "engagement_comments", "call_to_action"}
    if not required_cols.issubset(df.columns):
        return None
        
    tmp = df.copy()
    tmp["interaction_proxy"] = tmp["engagement_shares"].fillna(0) + tmp["engagement_comments"].fillna(0)
    
    cta = (
        tmp.groupby("call_to_action", as_index=False)
        .agg(
            posts=("post_id", "count"), 
            er=("engagement_rate", "mean"), 
            proxy=("interaction_proxy", "mean")
        )
        .sort_values(["posts", "proxy", "er"], ascending=[False, False, False])
        .head(20)
    )
    
    if cta.empty:
        return None
        
    chart = (
        alt.Chart(cta)
        .mark_bar()
        .encode(
            x=alt.X("proxy:Q", title="Shares + Comments (TB)"),
            y=alt.Y("call_to_action:N", sort="-x", title="CTA"),
            tooltip=[
                "call_to_action", 
                alt.Tooltip("posts:Q", title="Số bài"), 
                alt.Tooltip("er:Q", title="ER TB", format=".2%"), 
                alt.Tooltip("proxy:Q", title="S+C TB")
            ],
            color=alt.Color("er:Q", title="ER TB", scale=alt.Scale(scheme="oranges")),
        )
        .properties(height=500)
    )
    return chart
