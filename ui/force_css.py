import streamlit as st


FORCE_CSS = """
<style>
:root {
    --primary: #6C5CE7;
    --secondary: #A29BFE;
    --dark: #3b344a;
    --light: #f8f9fa;
    --accent: #FD79A8;
    --bg-color: #3b344a ;
}
/* 1.  App background ---------------------------------------------------- */
section[data-testid="stAppViewContainer"] {
    background: var(--bg-color) !important;
}

/* 2.  Hero glass card ---------------------------------------------------- */
[data-testid="stHorizontalBlock"]:has(.hero-text) {
     background: linear-gradient(135deg, #1e1e2e, #302b63) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
    border-radius: 10px !important;
    padding: 3rem 2.5rem !important;
    box-shadow: 0 25px 50px -12px rgba(108, 92, 231, 0.15) !important;
    margin:  0 !important;
    animation: float 6s ease-in-out infinite !important;
}

/* 3.  Title & subtitle ---------------------------------------------------- */
.hero-title {
   font-size: clamp(3rem, 6vw, 4.5rem) !important;
    font-weight: 800 !important;
    background: linear-gradient(90deg, var(--primary), var(--secondary)) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    margin-bottom: 1.5rem !important;
}
.text-gradient {
    background: linear-gradient(90deg, var(--accent), #FF7675) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    font-weight: 600 !important;
}
.hero-subtitle {
     font-size: 1.25rem !important;
    color: var(--light) !important;
    line-height: 1.8 !important;
    margin-bottom: 2.5rem !important;
}

/* 4.  Image -------------------------------------------------------------- */
.hero-image img {
    max-width: 260px !important;
    width: 80% !important;
    filter: drop-shadow(0 15px 20px rgba(0,0,0,0.15)) !important;
    animation: float 6s ease-in-out infinite .5s !important;
}

/* Glass-morphic primary button */
div[data-testid="stHorizontalBlock"] button[kind="primary"] {
    background: rgba(255, 255, 255, 0.2) !important;
    color: white !important;
    height:80px !important;
    width:150px !important;
    border: 2px solid rgba(255, 255, 255, 0.4) !important;
    border-radius: 10px !important;
    backdrop-filter: blur(8px) !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15) !important;
    transition: all 0.3s ease !important;
    font-weight: 600 !important;
    padding: 0.6rem 1.4rem !important;
}

div[data-testid="stHorizontalBlock"] button[kind="primary"]:hover {
    background: rgba(255, 155, 255, 0.35) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25) !important;
}
/* 5.  Feature cards ------------------------------------------------------ */
.features {
            display: grid !important;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)) !important;
    gap: 2rem !important;
    
        }
.feature-card {
     background: rgba(255, 255, 255, 0.8) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(108, 92, 231) !important;
    border-radius: 20px !important;
    padding: 2.5rem !important;
    box-shadow: 0 8px 32px rgba(108, 92, 231, 0.1) !important;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
}
.feature-card:hover {
    transform: translateY(-6px) !important;
    box-shadow: 0 12px 40px rgba(31,38,135,0.25) !important;
    background-color:#838590 !important;
}
.feature-icon {
    font-size: 2.5rem !important;
    margin-bottom: 1.5rem !important;
    color: var(--primary) !important;
}
.feature-title {
    font-size: 1.5rem !important;
    color: var(--dark) !important;
    margin-bottom: 1rem !important;
}

.feature-desc {
    color: #666 !important;
    line-height: 1.6 !important;
}


@keyframes float {
    0%   { transform: translateY(0px) !important; }
    50%  { transform: translateY(-12px) !important; }
    100% { transform: translateY(0px) !important; }
}

/* 6.  Mobile stack ------------------------------------------------------- */
@media (max-width: 768px) {
    [data-testid="stHorizontalBlock"]:has(.hero-text) {
        flex-direction: column !important;
        text-align: center !important;
    }
}
</style>
"""

def force_css():
    """Call once per page render to ensure styles win."""
    st.html(FORCE_CSS)        # Streamlit ≥ 1.36
    # For older versions use st.markdown(FORCE_CSS, unsafe_allow_html=True)