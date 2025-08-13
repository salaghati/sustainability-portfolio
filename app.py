import os
import inspect
import base64
import pandas as pd
import numpy as np
import altair as alt
import streamlit as st


DEFAULT_CSV_ABS_PATH = \
    "/Users/macm1/Documents/Practice DA/Social Media Data/sustainability_social_media_posts.csv"
CV_ABS_PATH = \
    "/Users/macm1/Documents/Practice DA/Social Media Data/[CV]-[Data Analyst]-[Trinh Anh Tu].pdf"
PROFILE_IMG_ABS_PATH = \
    "/Users/macm1/Documents/Practice DA/Social Media Data/profile.jpg"

# For Streamlit Cloud deployment - use relative paths
if not os.path.exists(CV_ABS_PATH):
    CV_ABS_PATH = "[CV]-[Data Analyst]-[Trinh Anh Tu].pdf"
if not os.path.exists(DEFAULT_CSV_ABS_PATH):
    DEFAULT_CSV_ABS_PATH = "sustainability_social_media_posts.csv"
if not os.path.exists(PROFILE_IMG_ABS_PATH):
    PROFILE_IMG_ABS_PATH = "profile.jpg"


@st.cache_data(show_spinner=False)
def load_data(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(
        csv_path,
        parse_dates=["post_date"],
        encoding="utf-8"
    )
    # Chuẩn hoá cột
    numeric_cols = [
        "engagement_likes",
        "engagement_shares",
        "engagement_comments",
        "user_followers",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Tạo chỉ số
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

    # Tạo trường ngày chuẩn hoá
    if "post_date" in df.columns:
        df["post_date"] = pd.to_datetime(df["post_date"], errors="coerce")
        df["post_month"] = df["post_date"].dt.to_period("M").dt.to_timestamp()

    # Chuẩn hashtag (loại bỏ null, xuống lowercase)
    if "hashtag" in df.columns:
        df["hashtag"] = df["hashtag"].astype(str).str.strip().str.lower()

    # Chuẩn sentiment/topic
    for c in ["post_sentiment", "climate_topic", "platform"]:
        if c in df.columns:
            df[c] = df[c].astype(str)

    return df


def kpi_section(df: pd.DataFrame) -> None:
    total_posts = int(len(df))
    avg_eng_rate = float(df["engagement_rate"].mean(skipna=True)) if "engagement_rate" in df else float("nan")
    total_eng = int(df["engagement_total"].sum()) if "engagement_total" in df else 0

    c1, c2, c3 = st.columns(3)
    c1.metric("Số bài", f"{total_posts:,}")
    c2.metric("Engagement rate TB", f"{avg_eng_rate:.2%}" if not np.isnan(avg_eng_rate) else "N/A")
    c3.metric("Tổng engagement", f"{total_eng:,}")


def chart_timeseries(df: pd.DataFrame) -> None:
    if "post_date" not in df.columns:
        return
    ts = (
        df.dropna(subset=["post_date"]).copy()
        .assign(post_day=lambda d: d["post_date"].dt.date)
        .groupby("post_day", as_index=False)["engagement_total"].sum()
    )
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
    st.altair_chart(chart, use_container_width=True)


def chart_platform(df: pd.DataFrame) -> None:
    if "platform" not in df.columns:
        return
    plat = (
        df.groupby("platform", as_index=False)
        .agg(engagement_rate=("engagement_rate", "mean"), posts=("post_id", "count"))
        .sort_values("engagement_rate", ascending=False)
    )
    chart = (
        alt.Chart(plat)
        .mark_bar()
        .encode(
            x=alt.X("platform:N", title="Nền tảng", sort="-y"),
            y=alt.Y("engagement_rate:Q", title="Engagement rate TB", axis=alt.Axis(format="%")),
            tooltip=["platform", alt.Tooltip("posts:Q", title="Số bài"), alt.Tooltip("engagement_rate:Q", title="ER TB", format=".2%")],
            color="platform:N",
        )
        .properties(height=300)
    )
    st.altair_chart(chart, use_container_width=True)


def chart_sentiment(df: pd.DataFrame) -> None:
    if "post_sentiment" not in df.columns:
        return
    sent = df["post_sentiment"].value_counts().reset_index()
    sent.columns = ["post_sentiment", "count"]
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
    st.altair_chart(chart, use_container_width=True)


def chart_hashtag(df: pd.DataFrame) -> None:
    if "hashtag" not in df.columns:
        return
    top = (
        df.groupby("hashtag", as_index=False)
        .agg(posts=("post_id", "count"), er=("engagement_rate", "mean"))
        .sort_values(["posts", "er"], ascending=[False, False])
        .head(15)
    )
    chart = (
        alt.Chart(top)
        .mark_bar()
        .encode(
            x=alt.X("posts:Q", title="Số bài"),
            y=alt.Y("hashtag:N", sort="-x", title="Hashtag"),
            tooltip=["hashtag", "posts", alt.Tooltip("er:Q", title="ER TB", format=".2%")],
            color=alt.Color("er:Q", title="ER TB", scale=alt.Scale(scheme="blues")),
        )
        .properties(height=400)
    )
    st.altair_chart(chart, use_container_width=True)


def _render_pdf_inline(pdf_path, height: int = 900) -> None:
    try:
        if isinstance(pdf_path, str) and os.path.exists(pdf_path):
            # File path
            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()
        else:
            # Uploaded file object
            pdf_bytes = pdf_path.read()
        
        b64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
        html = f'<iframe src="data:application/pdf;base64,{b64_pdf}" width="100%" height="{height}" type="application/pdf"></iframe>'
        st.components.v1.html(html, height=height, scrolling=True)
    except Exception as e:
        st.error(f"Could not display PDF: {e}")
        st.info("Your browser may block PDF display. Try downloading the file instead.")


def about_me_tab() -> None:
    st.subheader("About Me")
    st.markdown(
        """
        <style>
        .hero {background: linear-gradient(90deg,#0ea5e9,#22c55e); padding: 24px; border-radius: 12px; color: white;}
        .chips {display:flex; flex-wrap:wrap; gap:8px; margin-top:8px}
        .chip {background:#f1f5f9; color:#0f172a; padding:6px 10px; border-radius:999px; font-size:12px; border:1px solid #e2e8f0}
        .card {background:#ffffff; border:1px solid #e5e7eb; border-radius:12px; padding:16px; color:#0f172a}
        .avatar-round {width:180px; height:180px; border-radius:50%; object-fit:cover; border:4px solid #e5e7eb}
        </style>
        <div class="hero">
            <div style="font-size:24px; font-weight:700;">Trịnh Anh Tú · Data Analyst</div>
            <div style="opacity:0.9; margin-top:4px;">Data Analyst Portfolio</div>
            <div class="chips">
                <span class="chip">Python</span>
                <span class="chip">Pandas</span>
                <span class="chip">SQL</span>
                <span class="chip">Visualization</span>
                <span class="chip">Experimentation</span>
                <span class="chip">Streamlit</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("\n")
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown("<div class='card'><b>Summary</b><br/>Data Analyst focusing on analytical storytelling, dashboarding, and experimentation. Skilled in Python (pandas), SQL, and data visualization for decision support.</div>", unsafe_allow_html=True)
        st.markdown("\n")
        st.markdown("<div class='card'><b>Contacts</b><br/>📧 Email: trinhanhtu01@gmail.com<br/>💼 LinkedIn: linkedin.com/tú-trịnh<br/>💻 GitHub: github.com/salaghati</div>", unsafe_allow_html=True)
    with c2:
        # avatar
        if os.path.exists(PROFILE_IMG_ABS_PATH):
            with open(PROFILE_IMG_ABS_PATH, "rb") as f:
                b64_img = base64.b64encode(f.read()).decode("utf-8")
            st.markdown(f"<img class='avatar-round' src='data:image/*;base64,{b64_img}' alt='avatar' />", unsafe_allow_html=True)
            st.markdown("\n")
        st.markdown("<div class='card'><b>Resume (PDF)</b></div>", unsafe_allow_html=True)
        
        # Always show CV inline by default
        if os.path.exists(CV_ABS_PATH):
            _render_pdf_inline(CV_ABS_PATH, height=600)
            st.markdown("\n")
            with open(CV_ABS_PATH, "rb") as f:
                st.download_button(
                    label="📄 Download Resume (PDF)",
                    data=f.read(),
                    file_name=os.path.basename(CV_ABS_PATH),
                    mime="application/pdf",
                    key="download_cv_main",
                )
        else:
            st.warning("Resume file not found. Please add your CV file to the project directory.")
            uploaded_cv = st.file_uploader("Upload your Resume (PDF)", type=["pdf"], key="cv_upload_main")
            if uploaded_cv is not None:
                _render_pdf_inline(uploaded_cv, height=600)


def _about_me_sidebar_section() -> None:
    # Styles cho sidebar card
    st.markdown(
        """
        <style>
        .hero-side {background: linear-gradient(135deg,#0ea5e9,#22c55e); padding: 14px; border-radius: 12px; color: #e6f6ff; border: 1px solid rgba(255,255,255,0.15);}
        .name {font-size:18px; font-weight:800; margin-bottom:2px;}
        .role {font-size:12px; opacity:0.95; color:#f2fbff;}
        .chips {display:flex; flex-wrap:wrap; gap:6px; margin-top:8px}
        .chip {background: rgba(255,255,255,0.94); color:#0f172a; padding:4px 8px; border-radius:999px; font-size:11px; border:1px solid rgba(15,23,42,0.1)}
        .avatar-wrap {display:flex; align-items:center; gap:10px; margin-bottom:8px}
        .avatar {width:48px; height:48px; border-radius:50%; border:2px solid rgba(255,255,255,0.9); object-fit:cover}
        .card-side {background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.15); border-radius:12px; padding:10px; color:#e9f6ff}
        .cv-link a {color:#a7f3d0; font-weight:700; text-decoration:none}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Ảnh đại diện
    avatar_html = ""
    if os.path.exists(PROFILE_IMG_ABS_PATH):
        with open(PROFILE_IMG_ABS_PATH, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        avatar_html = f'<img class="avatar" src="data:image/*;base64,{b64}" alt="avatar" />'
    else:
        avatar_html = '<div class="avatar" style="display:flex;align-items:center;justify-content:center;background:#0ea5e955;color:#fff;font-weight:700;">TA</div>'

    st.markdown(
        f"""
        <div class="hero-side">
            <div class="avatar-wrap">{avatar_html}
                <div>
                    <div class="name">Trịnh Anh Tú</div>
                    <div class="role">Data Analyst · Social Sustainability</div>
                </div>
            </div>
            <div class="chips">
                <span class="chip">Python</span>
                <span class="chip">Pandas</span>
                <span class="chip">SQL</span>
                <span class="chip">Visualization</span>
                <span class="chip">Experimentation</span>
                <span class="chip">Streamlit</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Resume link: open new tab via data URI + download button
    if os.path.exists(CV_ABS_PATH):
        with open(CV_ABS_PATH, "rb") as f:
            pdf_bytes = f.read()
        b64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
        st.markdown(
            f"<div class='card-side cv-link'>📄 <a href='data:application/pdf;base64,{b64_pdf}' target='_blank'>Open Resume (new tab)</a></div>",
            unsafe_allow_html=True,
        )
        st.download_button("Download Resume (PDF)", data=pdf_bytes, file_name=os.path.basename(CV_ABS_PATH), mime="application/pdf", key="download_cv_sidebar")
    else:
        st.info("Resume not found. You can upload below to show the link.")
        up = st.file_uploader("Upload Resume (PDF)", type=["pdf"], key="cv_upload_sidebar")
        if up is not None:
            b64_pdf = base64.b64encode(up.read()).decode("utf-8")
            st.markdown(
                f"<div class='card-side cv-link'>📄 <a href='data:application/pdf;base64,{b64_pdf}' target='_blank'>Open Resume (new tab)</a></div>",
                unsafe_allow_html=True,
            )


def chart_topic(df: pd.DataFrame) -> None:
    if "climate_topic" not in df.columns:
        return
    topic = (
        df.groupby("climate_topic", as_index=False)
        .agg(posts=("post_id", "count"), er=("engagement_rate", "mean"))
        .sort_values(["posts", "er"], ascending=[False, False])
        .head(20)
    )
    chart = (
        alt.Chart(topic)
        .mark_bar()
        .encode(
            x=alt.X("posts:Q", title="Số bài"),
            y=alt.Y("climate_topic:N", sort="-x", title="Chủ đề"),
            tooltip=["climate_topic", "posts", alt.Tooltip("er:Q", title="ER TB", format=".2%")],
            color=alt.Color("er:Q", title="ER TB", scale=alt.Scale(scheme="greens")),
        )
        .properties(height=400)
    )
    st.altair_chart(chart, use_container_width=True)


def chart_time_heatmap(df: pd.DataFrame, platform_focus: str | None = None) -> None:
    if "post_date" not in df.columns:
        return
    data = df.copy()
    if platform_focus and "platform" in data.columns:
        data = data[data["platform"] == platform_focus]
    data = data.dropna(subset=["post_date"]).assign(
        dow=lambda d: d["post_date"].dt.day_name(),
        hod=lambda d: d["post_date"].dt.hour,
    )
    heat = (
        data.groupby(["dow", "hod"], as_index=False)
        .agg(er=("engagement_rate", "mean"), n=("post_id", "count"))
    )
    # Thứ theo thứ tự thông dụng
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
            tooltip=["dow", "hod", alt.Tooltip("er:Q", title="ER TB", format=".2%"), alt.Tooltip("n:Q", title="Số bài")],
        )
        .properties(height=280)
    )
    st.altair_chart(chart, use_container_width=True)


def apply_filters(df: pd.DataFrame, enabled: bool) -> pd.DataFrame:
    # Sidebar
    with st.sidebar:
        # Khu vực About Me mini ở sidebar
        _about_me_sidebar_section()

        st.header("Bộ lọc")
        st.caption("Điều chỉnh nguồn dữ liệu và tiêu chí để cập nhật biểu đồ & KPI.")
        file_path = st.text_input(
            "CSV path",
            value=DEFAULT_CSV_ABS_PATH,
            help="Đường dẫn tuyệt đối tới file CSV dữ liệu. Có thể thay đổi để nạp dataset khác.",
            disabled=not enabled,
        )
        if enabled and file_path and os.path.abspath(file_path) != os.path.abspath(DEFAULT_CSV_ABS_PATH):
            # Cho phép nạp file khác nếu người dùng đổi
            try:
                new_df = load_data(file_path)
                df = new_df
                st.success("Đã nạp dữ liệu từ đường dẫn mới")
            except Exception as e:
                st.error(f"Không thể nạp file mới: {e}")

        platforms = sorted(df["platform"].dropna().unique().tolist()) if "platform" in df.columns else []
        platform_sel = st.multiselect(
            "Nền tảng",
            options=platforms,
            default=platforms,
            help="Chọn một hoặc nhiều nền tảng để lọc các biểu đồ và bảng.",
            disabled=not enabled,
        )

        sentiments = sorted(df["post_sentiment"].dropna().unique().tolist()) if "post_sentiment" in df.columns else []
        sentiment_sel = st.multiselect(
            "Sentiment",
            options=sentiments,
            default=sentiments,
            help="Chọn cảm xúc (Positive/Neutral/Negative) của bài đăng.",
            disabled=not enabled,
        )

        min_date = df["post_date"].min() if "post_date" in df.columns else None
        max_date = df["post_date"].max() if "post_date" in df.columns else None
        if min_date is not None and max_date is not None:
            date_range = st.date_input(
                "Khoảng thời gian",
                value=(min_date.date(), max_date.date()),
                help="Giới hạn thời gian các bài đăng được hiển thị.",
                disabled=not enabled,
            )
        else:
            date_range = None

        hashtag_q = st.text_input(
            "Tìm hashtag chứa...",
            value="",
            help="Lọc những bài có hashtag chứa cụm từ nhập vào (không phân biệt hoa thường).",
            disabled=not enabled,
        )

        with st.expander("Giải thích các bộ lọc"):
            st.markdown("- CSV path: nguồn dữ liệu.\n- Nền tảng: lọc theo platform để so sánh công bằng.\n- Sentiment: chọn cảm xúc của bài.\n- Khoảng thời gian: thu hẹp khoảng phân tích.\n- Tìm hashtag: tìm theo chuỗi con trong hashtag.")

    # Áp dụng lọc
    filtered = df.copy()
    if platform_sel and "platform" in filtered.columns:
        filtered = filtered[filtered["platform"].isin(platform_sel)]
    if sentiment_sel and "post_sentiment" in filtered.columns:
        filtered = filtered[filtered["post_sentiment"].isin(sentiment_sel)]
    if date_range and "post_date" in filtered.columns:
        start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
        mask = (filtered["post_date"] >= start) & (filtered["post_date"] <= end)
        filtered = filtered[mask]
    if hashtag_q and "hashtag" in filtered.columns:
        filtered = filtered[filtered["hashtag"].str.contains(hashtag_q.strip().lower(), na=False)]

    return filtered


def main() -> None:
    st.set_page_config(page_title="Sustainability Social Media", layout="wide")
    # Layout giống ví dụ: sidebar chọn section, main hiển thị nội dung
    with st.sidebar:
        st.markdown("## My Page")
        section = st.radio(
            "Choose what you want to know",
            options=["About Me", "Projects"],
            index=0,
            key="portfolio_section",
        )

    # Khu vực About Me riêng trên cùng
    if section == "About Me":
        st.title("My Portfolio")
        st.caption("Personal profile, skills and resume.")
        about_me_tab()
        st.markdown("<hr style='opacity:0.2' />", unsafe_allow_html=True)
        st.stop()

    # Nếu chọn project, bật toàn bộ dashboard phân tích
    view_project = section == "Projects"
    # Tiêu đề chỉ hiện cho Project
    st.title("Sustainability Social Media Dashboard")
    st.caption("Khám phá dữ liệu bài đăng mạng xã hội về sustainability để làm portfolio DA. Dùng các tab bên dưới để xem KPI, thời gian, nền tảng, sentiment/topic, hashtag, CTA và bảng dữ liệu.")

    # Chỉ nạp dữ liệu khi vào Projects
    df = load_data(DEFAULT_CSV_ABS_PATH)
    df = apply_filters(df, enabled=view_project)

    overview_tab, plat_time_tab, sent_topic_tab, hashtag_tab, cta_tab, data_tab, docs_tab = st.tabs([
        "Overview", "Platform & Time", "Sentiment & Topic", "Hashtag", "CTA", "Data", "Docs"
    ])

    with overview_tab:
        if not view_project:
            st.info("Select 'Projects' from the sidebar to view the dashboard.")
            st.stop()
        st.subheader("KPI tổng quan")
        with st.expander("Giải thích"):
            st.markdown("- Số bài: tổng số dòng (post).\n- Engagement rate (ER) = (likes+shares+comments)/followers.\n- Tổng engagement: tổng likes+shares+comments.")
        kpi_section(df)
        st.subheader("Xu hướng tương tác theo thời gian")
        with st.expander("Giải thích"):
            st.markdown("Đường thời gian cộng gộp tổng engagement theo ngày để nhìn biến động và mùa vụ.")
        chart_timeseries(df)

    with plat_time_tab:
        if not view_project:
            st.info("Select 'Projects' from the sidebar to view the dashboard.")
            st.stop()
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Hiệu suất theo nền tảng")
            with st.expander("Giải thích"):
                st.markdown("Cột hiển thị ER trung bình và số bài theo platform, giúp quyết định nơi ưu tiên nội dung.")
            chart_platform(df)
        with c2:
            st.subheader("Heatmap thời gian (ER theo thứ/giờ)")
            platform_focus = None
            if "platform" in df.columns:
                platform_focus = st.selectbox("Chọn platform để xem heatmap", options=[None] + sorted(df["platform"].dropna().unique().tolist()), index=0)
            with st.expander("Giải thích"):
                st.markdown("Heatmap ER trung bình theo thứ và giờ đăng, hỗ trợ chọn khung thời gian tối ưu.")
            chart_time_heatmap(df, platform_focus)

    with sent_topic_tab:
        if not view_project:
            st.info("Select 'Projects' from the sidebar to view the dashboard.")
            st.stop()
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Phân bố sentiment")
            with st.expander("Giải thích"):
                st.markdown("Đếm số bài theo sentiment để hiểu tone nội dung.")
            chart_sentiment(df)
        with c2:
            st.subheader("Chủ đề nổi bật (Topic)")
            with st.expander("Giải thích"):
                st.markdown("Top chủ đề theo số bài và ER trung bình để ưu tiên nội dung bền vững.")
            chart_topic(df)

    with hashtag_tab:
        if not view_project:
            st.info("Select 'Projects' from the sidebar to view the dashboard.")
            st.stop()
        st.subheader("Top hashtag theo số bài & ER TB")
        with st.expander("Giải thích"):
            st.markdown("Top 15 hashtag được dùng nhiều và hiệu quả (ER) tốt.")
        chart_hashtag(df)

    with cta_tab:
        if not view_project:
            st.info("Select 'Projects' from the sidebar to view the dashboard.")
            st.stop()
        st.subheader("CTA và tương tác")
        if {"engagement_shares", "engagement_comments", "call_to_action"}.issubset(df.columns):
            tmp = df.copy()
            tmp["interaction_proxy"] = tmp["engagement_shares"].fillna(0) + tmp["engagement_comments"].fillna(0)
            cta = (
                tmp.groupby("call_to_action", as_index=False)
                .agg(posts=("post_id", "count"), er=("engagement_rate", "mean"), proxy=("interaction_proxy", "mean"))
                .sort_values(["posts", "proxy", "er"], ascending=[False, False, False])
                .head(20)
            )
            chart = (
                alt.Chart(cta)
                .mark_bar()
                .encode(
                    x=alt.X("proxy:Q", title="Shares + Comments (TB)"),
                    y=alt.Y("call_to_action:N", sort="-x", title="CTA"),
                    tooltip=["call_to_action", alt.Tooltip("posts:Q", title="Số bài"), alt.Tooltip("er:Q", title="ER TB", format=".2%"), alt.Tooltip("proxy:Q", title="S+C TB")],
                    color=alt.Color("er:Q", title="ER TB", scale=alt.Scale(scheme="oranges")),
                )
                .properties(height=500)
            )
            with st.expander("Giải thích"):
                st.markdown("CTA được xếp theo số bài và tương tác bình luận+chia sẻ (proxy), kèm ER trung bình.")
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("Thiếu cột cần thiết để phân tích CTA.")

    with data_tab:
        if not view_project:
            st.info("Select 'Projects' from the sidebar to view the dashboard.")
            st.stop()
        st.subheader("Bảng dữ liệu (đã lọc)")
        st.dataframe(df, use_container_width=True, hide_index=True)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Tải CSV đã lọc", data=csv, file_name="filtered_posts.csv", mime="text/csv")

    with docs_tab:
        st.subheader("Hướng dẫn & giải thích thành phần")
        st.markdown(
            """
            - Entity/Grain: mỗi dòng là 1 Post; dùng các chiều như platform, sentiment, topic, hashtag để nhóm.
            - Chỉ số chính: engagement_total = likes+shares+comments; ER = engagement_total / followers.
            - Bộ lọc: dùng để giới hạn dữ liệu trước khi tính KPI/biểu đồ.
            - Biểu đồ:
              - Timeseries: tổng engagement theo ngày.
              - Platform: ER trung bình theo nền tảng và số bài.
              - Heatmap thời gian: ER theo thứ và giờ đăng.
              - Sentiment: số bài theo cảm xúc.
              - Topic: top chủ đề theo số bài và ER.
              - Hashtag: top hashtag theo số bài và ER.
              - CTA: proxy tương tác (shares+comments) và ER theo CTA.
            - Gợi ý đọc số liệu: ưu tiên khác biệt ổn định (n lớn, CI hẹp), tránh kết luận từ nhóm quá nhỏ.
            """
        )
        with st.expander("Mã nguồn: load_data()"):
            st.code(inspect.getsource(load_data), language="python")
            st.markdown("""
            - Đọc CSV và ép kiểu ngày cho `post_date`.
            - Chuyển cột số về numeric (coerce) để xử lý giá trị lỗi.
            - Tạo `engagement_total` và `engagement_rate` (ER).
            - Sinh `post_month`, chuẩn hoá `hashtag`, và đảm bảo kiểu chuỗi cho `platform/sentiment/topic`.
            - Trả về DataFrame đã chuẩn hoá.
            """)
        with st.expander("Mã nguồn: apply_filters()"):
            st.code(inspect.getsource(apply_filters), language="python")
            st.markdown("""
            - Sidebar: chọn file CSV, platform, sentiment, khoảng thời gian, và tìm hashtag.
            - Áp dụng lọc tuần tự để tạo `filtered`.
            - Trả về DataFrame đã lọc, dùng cho mọi KPI/biểu đồ.
            """)
        with st.expander("Mã nguồn: KPI & biểu đồ chính"):
            st.code(inspect.getsource(kpi_section), language="python")
            st.code(inspect.getsource(chart_timeseries), language="python")
            st.code(inspect.getsource(chart_platform), language="python")
            st.code(inspect.getsource(chart_sentiment), language="python")
            st.code(inspect.getsource(chart_hashtag), language="python")
            st.code(inspect.getsource(chart_topic), language="python")
            st.code(inspect.getsource(chart_time_heatmap), language="python")
            st.markdown("""
            - KPI: số bài, ER trung bình, tổng engagement.
            - Timeseries: tổng engagement theo ngày.
            - Platform: ER TB và số bài theo nền tảng.
            - Sentiment/Hashtag/Topic: phân phối và hiệu suất nội dung.
            - Heatmap: ER theo thứ/giờ.
            """)
        with st.expander("Mã nguồn: main()"):
            st.code(inspect.getsource(main), language="python")
            st.markdown("""
            - Thiết lập trang, nạp dữ liệu, áp dụng lọc.
            - Bố cục theo tab: Overview, Platform & Time, Sentiment & Topic, Hashtag, CTA, Data, Docs.
            - Mỗi tab có phần giải thích ngắn (expander) giúp đọc hiểu đúng.
            """)


if __name__ == "__main__":
    main()


