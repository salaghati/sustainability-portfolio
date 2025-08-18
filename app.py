"""
Main Streamlit app - Portfolio landing page and About Me section.
"""
import os
import base64
import streamlit as st

# Page config
st.set_page_config(
    page_title="Trinh Anh Tu - Data Analyst Portfolio",
    layout="wide",
    initial_sidebar_state="expanded"
)

# File paths with relative path fallback for Streamlit Cloud
CV_PATH = "[CV]-[Data Analyst]-[Trinh Anh Tu].pdf"
PROFILE_IMG_PATH = "profile.jpg"

# Fallback to absolute paths for local development
if not os.path.exists(CV_PATH):
    CV_PATH = "/Users/macm1/Documents/Practice DA/Social Media Data/[CV]-[Data Analyst]-[Trinh Anh Tu].pdf"
if not os.path.exists(PROFILE_IMG_PATH):
    PROFILE_IMG_PATH = "/Users/macm1/Documents/Practice DA/Social Media Data/profile.jpg"


def render_pdf_inline(pdf_path: str, height: int = 900) -> None:
    """Render PDF inline using base64 encoding."""
    try:
        if isinstance(pdf_path, str) and os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()
        else:
            pdf_bytes = pdf_path.read()
        
        b64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
        html = f'<iframe src="data:application/pdf;base64,{b64_pdf}" width="100%" height="{height}" type="application/pdf"></iframe>'
        st.components.v1.html(html, height=height, scrolling=True)
    except Exception as e:
        st.error(f"Cannot display PDF: {e}")
        st.info("Your browser may block PDF display. Try downloading the file instead.")


def about_me_section() -> None:
    """Render About Me section with profile, skills and resume."""
    st.markdown(
        """
        <style>
        .hero {
            background: linear-gradient(90deg, #0ea5e9, #22c55e); 
            padding: 24px; 
            border-radius: 12px; 
            color: white;
            text-align: center;
            margin-bottom: 2rem;
        }
        .hero h1 {
            font-size: 28px; 
            font-weight: 700; 
            margin-bottom: 8px;
        }
        .hero p {
            opacity: 0.9; 
            font-size: 16px;
        }
        .skills {
            display: flex; 
            flex-wrap: wrap; 
            gap: 8px; 
            margin-top: 16px;
            justify-content: center;
        }
        .skill {
            background: rgba(255,255,255,0.2); 
            color: white; 
            padding: 6px 12px; 
            border-radius: 20px; 
            font-size: 12px;
            border: 1px solid rgba(255,255,255,0.3);
        }
        .card {
            background: #ffffff; 
            border: 1px solid #e5e7eb; 
            border-radius: 12px; 
            padding: 20px; 
            margin-bottom: 1rem;
            color: #0f172a;
        }
        .avatar {
            width: 200px; 
            height: 200px; 
            border-radius: 50%; 
            object-fit: cover; 
            border: 4px solid #e5e7eb;
            margin: 0 auto;
            display: block;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Hero section
    st.markdown(
        """
        <div class="hero">
            <h1>Trinh Anh Tu</h1>
            <p>Data Analyst Portfolio - Social Media Analytics & Sustainability</p>
            <div class="skills">
                <span class="skill">Python</span>
                <span class="skill">Pandas</span>
                <span class="skill">SQL</span>
                <span class="skill">Streamlit</span>
                <span class="skill">Data Visualization</span>
                <span class="skill">Altair</span>
                <span class="skill">A/B Testing</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### About Me")
        st.write("""
        Data Analyst specializing in social media data analysis, dashboard development and A/B testing. 
        Experienced with Python (pandas), SQL, and data visualization to support business decision making.
        """)
        
        st.markdown("#### Expertise")
        st.markdown("""
        - Social Media Analytics & Engagement Metrics
        - Dashboard Development with Streamlit  
        - Data Cleaning & Preprocessing
        - Statistical Analysis & A/B Testing
        - Data Visualization with Altair/Matplotlib
        """)
        
        st.markdown("### Contact")
        st.markdown("""
        **Email:** trinhanhtu01@gmail.com  
        **LinkedIn:** linkedin.com/in/tú-trịnh  
        **GitHub:** github.com/salaghati
        """)

    with col2:
        # Profile image
        if os.path.exists(PROFILE_IMG_PATH):
            with open(PROFILE_IMG_PATH, "rb") as f:
                b64_img = base64.b64encode(f.read()).decode("utf-8")
            st.markdown(
                f'<img class="avatar" src="data:image/*;base64,{b64_img}" alt="Trinh Anh Tu" />',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div style="width:200px; height:200px; border-radius:50%; background:#0ea5e9; 
                           display:flex; align-items:center; justify-content:center; 
                           color:white; font-weight:bold; font-size:48px; margin:0 auto;">
                    TA
                </div>
                """,
                unsafe_allow_html=True
            )
        
        st.markdown("### Resume/CV")
        st.write("Download my CV to see detailed experience and projects.")
        
        # CV section
        if os.path.exists(CV_PATH):
            with open(CV_PATH, "rb") as f:
                pdf_bytes = f.read()
                
            st.download_button(
                "Download Resume (PDF)",
                data=pdf_bytes,
                file_name="Resume_Trinh_Anh_Tu_Data_Analyst.pdf",
                mime="application/pdf",
                use_container_width=True
            )
            
            with st.expander("View CV online"):
                render_pdf_inline(CV_PATH, height=600)
        else:
            st.warning("CV file not found.")
            uploaded_cv = st.file_uploader(
                "Upload CV (PDF)", 
                type=["pdf"], 
                help="Upload CV file to display"
            )
            if uploaded_cv is not None:
                render_pdf_inline(uploaded_cv, height=600)


def navigation_section() -> None:
    """Render navigation to other pages."""
    st.markdown("---")
    st.subheader("Portfolio Project")
    st.markdown(
        """
        Explore the social media data analysis dashboard about sustainability. 
        This project demonstrates data analysis, visualization and Streamlit development skills.
        """
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Overview")
        st.write("Key performance indicators, engagement trends and platform analysis")
        if st.button("View Overview", use_container_width=True):
            st.switch_page("pages/01_Overview.py")
    
    with col2:
        st.markdown("#### Trends Analysis")
        st.write("Hashtag performance, time heatmap and CTA analysis")
        if st.button("View Trends", use_container_width=True):
            st.switch_page("pages/02_Trends.py")
    
    with col3:
        st.markdown("#### Highlights")
        st.markdown("""
        • 3000+ social media posts analyzed  
        • Multiple platforms & metrics  
        • Interactive filtering & export
        """)


def main() -> None:
    """Main application function."""
    # Minimal sidebar
    with st.sidebar:
        st.markdown("### Project Info")
        st.info(
            """
            **Dataset**: 3000+ sustainability posts  
            **Platforms**: Facebook, Instagram, LinkedIn, TikTok, X  
            **Metrics**: Engagement rate, sentiment, topics  
            **Tech Stack**: Python, Streamlit, Altair
            """
        )

    st.title("Data Analyst Portfolio")
    st.caption("Welcome to Trinh Anh Tu's data analysis portfolio")
    
    about_me_section()
    
    navigation_section()
    
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; opacity: 0.7; padding: 20px;">
            <p>© 2024 Trinh Anh Tu | Built with Streamlit & Python | 
            <a href="https://github.com/salaghati" target="_blank">GitHub</a></p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()