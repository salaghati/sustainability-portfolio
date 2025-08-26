"""
Main Streamlit app - Portfolio landing page and About Me section.
"""
import streamlit as st
import base64
import os

st.set_page_config(
    page_title="Trinh Anh Tu - My Portfolio",
    page_icon="👨‍💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Main Portfolio Page ---
st.title("Trinh Anh Tu - My Portfolio")
st.markdown("Welcome! This application showcases my data analysis projects, demonstrating a complete workflow from data processing to insight generation. **Please use the sidebar to navigate.**")
st.markdown("---")

# --- About Me Section ---
st.header("About Me")
st.markdown("""
    Chào mừng bạn đến với portfolio của tôi! Tôi là một sinh viên vừa tốt nghiệp ngành Hệ thống Thông tin tại trường Đại học Công nghệ Thông tin - ĐHQG TP.HCM. 
    Với tư duy ham học hỏi và thái độ cầu tiến, tôi đặc biệt quan tâm đến việc phân tích dữ liệu để giải quyết các vấn đề thực tế và hỗ trợ ra quyết định thông minh.
""")

# --- Work Experience & Education ---
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.subheader("🎓 Education")
    st.markdown("""
        **University of Information Technology (UIT)**
        - **B.E. in Information Systems** (2020 - 2024)
        - GPA: 7.0
    """)

with col2:
    st.subheader("💼 Work Experience")
    st.markdown("""
        **RioTech .,JSC**
        - **Data Analyst Intern** (Sep 2023 - Dec 2023)
        - *Phát triển dashboard, phân tích dữ liệu bán hàng để tìm ra xu hướng và hỗ trợ làm sạch, chuyển đổi dữ liệu.*
    """)

st.markdown("---")


# --- Projects Section ---
st.header("Personal Projects")
proj_col1, proj_col2 = st.columns(2)

with proj_col1:
    st.subheader("Retail Analysis - Contoso Dataset")
    st.markdown("""
    *Phân tích hơn 100,000 giao dịch bán lẻ bằng SQL nâng cao (CTEs, Window Functions) để phân khúc khách hàng và xác định các nhóm giá trị cao. Xây dựng báo cáo doanh thu cho thấy sự tăng trưởng và các mẫu hình theo mùa.*
    - **Tech Stack:** `PostgreSQL`, `DBeaver`, `Advanced SQL`
    """)

with proj_col2:
    st.subheader("Thesis: ML for Love Factors")
    st.markdown("""
    *Thiết kế khảo sát, thu thập và làm sạch dữ liệu từ 196 người trẻ. Sử dụng các mô hình Machine Learning (Random Forest, Logistic Regression, SVM) để xác định các yếu tố quan trọng trong một mối quan hệ lâu dài.*
    - **Tech Stack:** `Python`, `Scikit-learn`, `Pandas`
    - [Link to Report](https://github.com/salaghati/sustainability-portfolio/blob/main/Thesis.pdf)
    """)

st.markdown("---")

st.header("Projects in this Portfolio")
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Sustainability Social Media Analysis")
    st.markdown("""
        This project analyzes over 3,000 social media posts related to sustainability to uncover engagement patterns.
        - **Objective:** Identify key topics, effective hashtags, and optimal posting strategies.
        - **Analysis includes:**
            - KPI Dashboard (Engagement Rate, Total Interactions).
            - Platform Performance Comparison.
            - In-depth Hashtag and Sentiment Analysis.
        - **Navigate:** Use the `Social_Media_Overview` and `Social_Media_Analysis` pages in the sidebar.
    """)

with col2:
    st.subheader("🚌 NYC Green Taxi Trip Insights")
    st.markdown("""
        An interactive dashboard exploring NYC Green Taxi trip data from January 2020 to identify operational patterns.
        - **Objective:** Analyze trip characteristics to understand service usage and operational efficiency.
        - **Analysis includes:**
            - Key Metrics (Revenue, Trip Duration, Passenger Count).
            - Trip Distance & Duration Distributions.
            - Peak Hour Analysis with a Timing Heatmap.
        - **Navigate:** Use the `Transport_Overview` and `Transport_Timing` pages in the sidebar.
    """)

# --- CV Section ---
st.markdown("---")
st.header("Download CV")
CV_PATH = "[CV]-[Data Analyst]-[Trinh Anh Tu].pdf"
if os.path.exists(CV_PATH):
    with open(CV_PATH, "rb") as f:
        pdf_bytes = f.read()
    st.download_button(
        "Download Resume (PDF)",
        data=pdf_bytes,
        file_name="Resume_Trinh_Anh_Tu_Data_Analyst.pdf",
        mime="application/pdf"
    )