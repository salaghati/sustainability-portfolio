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
st.markdown("Welcome! This application showcases my **business analysis** and **data analysis** projects, demonstrating expertise in requirements gathering, system design, data processing, and insight generation. **Please use the sidebar to navigate.**")
st.markdown("---")

# --- About Me Section ---
st.header("About Me")

# Create columns for potential profile image and text
about_col1, about_col2 = st.columns([1, 3])

with about_col1:
    # Profile image with styling
    st.markdown("""
    <div style="text-align: center; margin-bottom: 1rem;">
    """, unsafe_allow_html=True)
    
    try:
        st.image("assets/image.png", 
                width=200, 
                caption="")
        
        # Add name and title below image
        st.markdown("""
        <div style="text-align: center; 
                    background: linear-gradient(135deg, #667eea, #764ba2); 
                    border-radius: 10px; 
                    padding: 1rem; 
                    color: white;
                    margin-top: 1rem;">
            <div style="font-size: 1.2rem; font-weight: 600;">Trinh Anh Tu</div>
            <div style="font-size: 0.9rem; opacity: 0.9;">Business & Data Analyst</div>
        </div>
        """, unsafe_allow_html=True)
    except:
        # Fallback to original placeholder if image fails to load
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea, #764ba2); 
                    border-radius: 15px; 
                    padding: 2rem; 
                    text-align: center; 
                    color: white;">
            <div style="font-size: 3rem;">👨‍💻</div>
            <div style="font-size: 1.2rem; font-weight: 600;">Trinh Anh Tu</div>
            <div style="font-size: 0.9rem; opacity: 0.9;">Business & Data Analyst</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

with about_col2:
    st.markdown("""
    Welcome to my portfolio! I am a recent **Information Systems graduate** from the University of Information Technology - VNU-HCM.
    
    With a **curious mindset** and **proactive attitude**, I am passionate about bridging the gap between business needs and technical solutions through:
    
    **🎯 Business Analysis:**
    - Requirements gathering and stakeholder management
    - Process optimization and workflow design
    - System documentation and user story creation
    
    **📊 Data Analysis:**
    - Data-driven insights and decision support
    - Statistical analysis and visualization
    - Business intelligence and reporting
    
    I am actively seeking opportunities as a **Business Analyst** or **Data Analyst** where I can leverage my technical skills and business acumen to drive meaningful impact.
    """)

# --- Projects Section ---
st.markdown("---")
st.header("Projects")

# Portfolio Projects
st.subheader("📊 Portfolio Projects")
st.markdown("*Featured projects showcased in this application*")

# Highlight Game Manager v2
st.markdown("### 🎮 **Game Manager System v2** ⭐")
st.info("""
**Full-stack Business Management System**

*Complete web application for managing gaming machines across multiple branches with comprehensive business analytics and reporting.*

**🎯 Key Features:**
- **Machine Management:** CRUD operations, soft delete, branch assignment
- **Point Transactions:** Daily data entry with automatic balance calculation  
- **User Management:** Role-based (Admin/User) and branch-based authorization
- **Business Intelligence:** Comprehensive reporting and audit trails
- **Product & Warehouse:** Inventory management and daily auditing

**💻 Tech Stack:** `Node.js`, `React.js`, `SQLite`, `Bootstrap`, `JWT Authentication`

**👨‍💼 Role:** Lead Business Analyst & System Designer

**📋 Navigate:** See `Game Manager v2 Portfolio` page for complete documentation and wireframes.
""")

st.markdown("### 📊 **Data Analysis Projects**")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**📈 Sustainability Social Media Analysis**")
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
    st.markdown("**🚌 NYC Green Taxi Trip Insights**")
    st.markdown("""
        An interactive dashboard exploring NYC Green Taxi trip data from January 2020 to identify operational patterns.
        - **Objective:** Analyze trip characteristics to understand service usage and operational efficiency.
        - **Analysis includes:**
            - Key Metrics (Revenue, Trip Duration, Passenger Count).
            - Trip Distance & Duration Distributions.
            - Peak Hour Analysis with a Timing Heatmap.
        - **Navigate:** Use the `Transport_Overview` and `Transport_Timing` pages in the sidebar.
    """)

# Additional Projects
st.subheader("🔬 Additional Projects")
st.markdown("*Other data analysis and development projects*")

proj_col1, proj_col2, proj_col3 = st.columns(3)

with proj_col1:
    st.markdown("**🏢 Retail Analysis - Contoso Dataset**")
    st.markdown("""
    *Analyzed over 100,000 retail transactions using advanced SQL (CTEs, Window Functions) to segment customers and identify high-value groups. Built revenue reports showing growth and seasonal patterns.*
    - **Tech Stack:** `PostgreSQL`, `DBeaver`, `Advanced SQL`
    """)

with proj_col2:
    st.markdown("**💕 Thesis: ML for Love Factors**")
    st.markdown("""
    *Designed a survey, collected, and cleaned data from 196 young individuals. Used Machine Learning models (Random Forest, Logistic Regression, SVM) to identify key factors in long-term relationships.*
    - **Tech Stack:** `Python`, `Scikit-learn`, `Pandas`
    - [Link to Report](https://github.com/salaghati/sustainability-portfolio/blob/main/Thesis.pdf)
    """)

with proj_col3:
    st.markdown("**📚 Academic Research**")
    st.markdown("""
    *Research projects and academic work completed during university studies and internships.*
    - **Focus Areas:** `Machine Learning`, `Data Mining`, `Statistical Analysis`
    - **Applications:** `Social Research`, `Predictive Modeling`, `Business Intelligence`
    """)

# --- Work Experience & Education ---
st.markdown("---")
st.header("Background")
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
        - *Developed dashboards and analyzed sales data to identify trends. Supported data cleaning and transformation processes.*
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