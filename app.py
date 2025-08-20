"""
Main Streamlit app - Portfolio landing page and About Me section.
"""
import os
import base64
import streamlit as st

# Page config with wide layout and custom theme
st.set_page_config(
    page_title="Trinh Anh Tu - Data Analyst Portfolio",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styling */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hero section */
    .hero {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .hero h1 {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .hero p {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-bottom: 1.5rem;
        font-weight: 300;
    }
    
    /* Skills badges */
    .skills {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        justify-content: center;
        margin-top: 1rem;
    }
    
    .skill-badge {
        background: rgba(255,255,255,0.2);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 500;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    /* Professional cards */
    .card {
        background: linear-gradient(135deg, rgba(0, 64, 128, 0.9), rgba(0, 48, 96, 0.9));
        border: none;
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 20px rgba(0,0,0,0.15);
        border-left: 4px solid rgba(255,255,255,0.3);
        color: white;
    }
    
    .card h3 {
        color: white;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .card p {
        color: rgba(255,255,255,0.9);
    }
    
    /* Contact buttons */
    .contact-btn {
        display: inline-block;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 10px;
        text-decoration: none;
        font-weight: 500;
        margin: 0.25rem;
        transition: transform 0.2s;
    }
    
    .contact-btn:hover {
        transform: translateY(-2px);
        text-decoration: none;
        color: white;
    }
    
    /* Project cards */
    .project-card {
        background: linear-gradient(135deg, rgba(0, 64, 128, 0.8), rgba(0, 48, 96, 0.8));
        border-radius: 15px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
        border: 1px solid rgba(255,255,255,0.2);
        transition: transform 0.2s;
        color: white;
    }
    
    .project-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.25);
        background: linear-gradient(135deg, rgba(0, 64, 128, 0.9), rgba(0, 48, 96, 0.9));
    }
    
    .project-card h4 {
        color: white;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    
    .project-card p {
        color: rgba(255,255,255,0.9);
        font-size: 0.9rem;
        line-height: 1.5;
    }
    
    /* Avatar styling */
    .avatar {
        width: 180px;
        height: 180px;
        border-radius: 50%;
        object-fit: cover;
        border: 4px solid #e2e8f0;
        margin: 0 auto;
        display: block;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }
    
    /* Info box */
    .info-box {
        background: linear-gradient(135deg, rgba(0, 64, 128, 0.7), rgba(0, 48, 96, 0.7));
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        color: white;
        backdrop-filter: blur(10px);
    }
</style>
""", unsafe_allow_html=True)

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
    """Render About Me section with enhanced styling."""
    
    # Hero section with gradient background
    st.markdown("""
        <div class="hero">
        <h1>Trinh Anh Tu</h1>
        <p>Data Analyst Portfolio - Social Media Analytics & Sustainability</p>
        <div class="skills">
            <span class="skill-badge">Python</span>
            <span class="skill-badge">Pandas</span>
            <span class="skill-badge">SQL</span>
            <span class="skill-badge">Streamlit</span>
            <span class="skill-badge">Data Visualization</span>
            <span class="skill-badge">Altair</span>
            <span class="skill-badge">A/B Testing</span>
        </div>
            </div>
    """, unsafe_allow_html=True)

    # Quick intro with usage guide
    st.info("**Welcome!** Use the sidebar filters on each page to explore different aspects of the data. Click the buttons below to navigate between analysis pages.")

    # Main content in columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # About me card
        st.markdown("""
        <div class="card">
            <h3>About Me</h3>
            <p>Data Analyst specializing in social media data analysis, dashboard development and A/B testing. 
            Experienced with Python (pandas), SQL, and data visualization to support business decision making.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Expertise with better hierarchy
        st.markdown("### Core Expertise")
        
        # Create expertise in cards
        expertise_col1, expertise_col2 = st.columns(2)
        
        with expertise_col1:
            st.markdown("""
            **Analytics & Insights**
            - Social Media Analytics & Engagement Metrics
            - Statistical Analysis & A/B Testing  
            - Data Cleaning & Preprocessing
            """)
        
        with expertise_col2:
            st.markdown("""
            **Technical Skills**
            - Dashboard Development with Streamlit
            - Data Visualization (Altair/Matplotlib)
            - Python (Pandas, NumPy) & SQL
            """)

    with col2:
        # Profile image with better styling
        if os.path.exists(PROFILE_IMG_PATH):
            with open(PROFILE_IMG_PATH, "rb") as f:
                b64_img = base64.b64encode(f.read()).decode("utf-8")
            st.markdown(
                f'<img class="avatar" src="data:image/*;base64,{b64_img}" alt="Trinh Anh Tu" />',
                unsafe_allow_html=True
                    )
        else:
            st.markdown("""
            <div style="width:180px; height:180px; border-radius:50%; background:linear-gradient(135deg, #667eea, #764ba2); 
                       display:flex; align-items:center; justify-content:center; 
                       color:white; font-weight:bold; font-size:2.5rem; margin:0 auto; box-shadow: 0 4px 20px rgba(0,0,0,0.15);">
                TA
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Contact section with CTA buttons
        st.markdown("### Let's Connect")
        st.markdown("""
        <div style="text-align: center;">
            <a href="mailto:trinhanhtu01@gmail.com" class="contact-btn">Email Me</a><br>
            <a href="https://linkedin.com/in/tú-trịnh" class="contact-btn" target="_blank">LinkedIn</a><br>
            <a href="https://github.com/salaghati" class="contact-btn" target="_blank">GitHub</a>
        </div>
        """, unsafe_allow_html=True)

    # CV section with better layout
    st.markdown("---")
    st.markdown("### Resume & CV")
    
    cv_col1, cv_col2, cv_col3 = st.columns([1, 2, 1])
    
    with cv_col2:
        if os.path.exists(CV_PATH):
            with open(CV_PATH, "rb") as f:
                pdf_bytes = f.read()

            st.download_button(
                "Download Resume (PDF)",
                data=pdf_bytes,
                file_name="Resume_Trinh_Anh_Tu_Data_Analyst.pdf",
                mime="application/pdf",
                use_container_width=True,
                type="primary"
            )
            
            with st.expander("Preview CV online"):
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
    """Enhanced navigation section with project cards."""
    st.markdown("---")
    st.header("Portfolio Project")
    
    # Brief description with usage instructions
    st.markdown("""
    **Interactive Social Media Analytics Dashboard**
    
    Explore 3000+ sustainability-focused social media posts through interactive visualizations. 
    Use filters to dive deep into engagement patterns, hashtag performance, and optimal posting strategies.
    """)
    
    # Add screenshot
    if os.path.exists("dashboard_screenshot.png"):
        st.image("dashboard_screenshot.png", caption="Dashboard Preview", use_column_width=True)
    
    # Project cards in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="project-card">
            <h4>Overview Dashboard</h4>
            <p>Key performance indicators, engagement trends, and platform analysis. Perfect starting point to understand the data landscape.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("View Overview", use_container_width=True, type="primary"):
            st.switch_page("pages/01_Project_Overview.py")
    
    with col2:
        st.markdown("""
        <div class="project-card">
            <h4>Trends Analysis</h4>
            <p>Deep dive into hashtag performance, optimal posting times, and call-to-action effectiveness across platforms.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("View Trends", use_container_width=True, type="primary"):
            st.switch_page("pages/02_Trends.py")
    
    with col3:
        st.markdown("""
        <div class="project-card">
            <h4>Key Highlights</h4>
            <p><strong>3000+</strong> posts analyzed<br>
            <strong>5</strong> social platforms<br>
            <strong>Interactive</strong> filtering & export</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("*Explore the data above*")

    # Technical details in expander
    with st.expander("Technical Implementation Details"):
        st.markdown("""
        **Tech Stack:** Python, Streamlit, Pandas, Altair  
        **Data Processing:** ETL pipeline with data validation  
        **Visualizations:** Interactive charts with filtering  
        **Deployment:** Streamlit Cloud with CI/CD  
        **Performance:** Cached data loading, optimized queries  
        """)


def main() -> None:
    """Main application function with enhanced layout."""
    
    # Main title with better hierarchy
    st.title("Data Analyst Portfolio")
    st.markdown("### *Trinh Anh Tu - Social Media Analytics Specialist*")
    
    about_me_section()
    navigation_section()
    
    # Footer with better styling
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; opacity: 0.7; padding: 2rem;">
        <p style="font-size: 0.9rem;">
            © 2024 Trinh Anh Tu | Built with Streamlit & Python | 
            <a href="https://github.com/salaghati" target="_blank" style="color: #667eea;">View Source Code</a>
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()