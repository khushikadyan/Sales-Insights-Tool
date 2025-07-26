import streamlit as st

def apply_custom_styles():
    st.markdown("""
    <style>
    /* Main app container – override Streamlit’s own rule */
    section[data-testid="stApp"] {
        background-color: #f8fafc !important;
    }

    /* Make sure the body also gets it (fallback) */
    body {
        background-color: #f8fafc !important;
    }
                
    
    /* --- FEATURE SECTION --- */
.features {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 2rem;
    padding: 4rem 0;
}

.feature-card {
    background: rgba(255, 255, 255, 0.55);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 16px;
    padding: 2.2rem 1.8rem;
    text-align: center;
    box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.feature-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 12px 40px rgba(31, 38, 135, 0.25);
}

.feature-icon {
    font-size: 3.2rem;
    margin-bottom: 1.2rem;
    color: #2563eb;
}

.feature-card h3 {
    font-size: 1.25rem;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 0.6rem;
}

.feature-desc {
    font-size: 0.95rem;
    color: #475569;
    line-height: 1.6;
}

         
                
    </style>
    """, unsafe_allow_html=True)