import streamlit as st
from ui.styles import apply_custom_styles
from PIL import Image
import io
import requests

def show_landing():
    apply_custom_styles()
    
    st.markdown('<div class="hero"><div class="hero-card">', unsafe_allow_html=True)
    left, right = st.columns([1.3, 1])
    with left:
        # Hero text content
        st.markdown("""
        <div class="hero-text">
            <h1 class="hero-title">Sales Data Insights Tool</h1>
            <p class="hero-subtitle">
                Transform raw sales data into clear, actionable insights in seconds.<br>
                No setup required. No data leaves your browser.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Get Started button
        if st.button("Get Started →", key="btn_go", type="primary"):
            st.session_state.page = "analyze"
            st.rerun()
    
    with right:
        st.markdown('<div class="hero-image">',unsafe_allow_html=True)
        # Display image using Streamlit's native method
        try:
            # For local image
            image = Image.open("HOMIE.png")
            st.image(image, use_container_width=True)
        except:
            # For remote image (fallback)
            try:
                response = requests.get("https://raw.githubusercontent.com/yourusername/yourrepo/main/assets/HOMIE.png")
                image = Image.open(io.BytesIO(response.content))
                st.image(image, use_column_width=True)
            except:
                st.warning("Could not load hero image")

    # --- FEATURE CARDS ---
    st.markdown('<div class="features">', unsafe_allow_html=True)

    cards = [
       ("📊", "Automatic Analysis", "Upload any CSV/Excel and get instant visualizations with AI-powered pattern detection."),
        ("📅", "Time Trends", "Interactive charts with zoom/pan to analyze seasonality and growth trends."),
        ("📥", "Export Options", "One-click export of PNGs, Excel sheets, and interactive HTML reports."),
        ("🔒", "Privacy First", "100% browser-side processing - your data never leaves your computer."),
    ]

    for icon, title, desc in cards:
        st.markdown(
            f"""
            <div class="feature-card">
                <div class="feature-icon">{icon}</div>
                <h3>{title}</h3>
                <div class="feature-desc">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # --- FOOTER ---
    st.markdown(
        """
        <footer>
            <p>Khushi Kadyan</p>
        </footer>
        """,
        unsafe_allow_html=True,
    )
