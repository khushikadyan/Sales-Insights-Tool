import streamlit as st
from datetime import datetime
from typing import Tuple, Optional, Any
import pandas as pd
from utils.data_loader import load_data, analyze_columns
from logic.data_processing import calculate_metrics
from logic.visualization import create_trend_plot, create_top_items_plot, create_scatter_plot
import time
from io import BytesIO
import base64
import matplotlib.pyplot as plt

# ---------- 1.  BULLET-PROOF CSS ----------
def _inject_global_styles() -> None:
    """
    Inject once per page render; selectors match the *actual* Streamlit nodes.
    """
    st.markdown(
        """
        <style>
        /* ---------- 100 % viewport override ---------- */
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #1e1e2e, #302b63) !important;
            font-family: 'Segoe UI', Roboto, sans-serif !important;
            color: #f8f9fa !important;
            padding: 1rem !important;
        }

        /* ---------- Upload card (glass-morphic) ---------- */
        [data-testid="stFileUploadDropzone"] {
            background: rgba(255,255,255,0.08) !important;
            backdrop-filter: blur(12px) !important;
            border: 2px dashed rgba(255,255,255,0.35) !important;
            border-radius: 24px !important;
            padding: 3rem 2rem !important;
            box-shadow: 0 0 0 6px rgba(255,255,255,0.05), 0 8px 32px rgba(0,0,0,0.25) !important;
            transition: all 0.4s ease !important;
        }
        [data-testid="stFileUploadDropzone"]:hover {
            background: rgba(255,255,255,0.15) !important;
            border-color: #fff !important;
        }

        /* ---------- Buttons ---------- */
        button[data-testid="baseButton-primary"] {
            background: linear-gradient(90deg, #667eea, #764ba2) !important;
            color: #fff !important;
            border: none !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            padding: 0.6rem 1.4rem !important;
            transition: all 0.3s ease !important;
        }
        button[data-testid="baseButton-primary"]:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(102,126,234,0.6) !important;
        }

        /* ---------- Tabs ---------- */
        [role="tab"] {
            color: #a1a1aa !important;
            background: rgba(255,255,255,0.1) !important;
            border-bottom: 2px solid transparent !important;
            padding: 0.5rem 1rem !important;
            border-radius: 8px 8px 0 0 !important;
            font-weight: 600 !important;
            transition: all 0.25s ease !important;
        }
        [aria-selected="true"] {
            color: #fff !important;
            background: rgba(102,126,234,0.8) !important;
            border-bottom-color: #667eea !important;
        }

        /* ---------- Cards / expanders / metrics ---------- */
        .stExpander,
        [data-testid="stTabs"],
        [data-testid="metric-container"] {
            background: rgba(255,255,255,0.05) !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            border-radius: 16px !important;
            padding: 1.5rem !important;
            backdrop-filter: blur(12px) !important;
            margin-bottom: 1rem !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
        }

        /* ---------- Metric Styling ---------- */
        [data-testid="metric-container"] {
            background: rgba(255,255,255,0.05) !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            border-radius: 16px !important;
            padding: 1.5rem !important;
            backdrop-filter: blur(12px) !important;
            margin-bottom: 1rem !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
        }
        
        /* Metric value (big number) */
        [data-testid="stMetricValue"] > div {
            color: white !important;
            font-size: 1.75rem !important;
        }
        
        /* Metric label */
        [data-testid="stMetricLabel"] > div {
            color: rgba(255,255,255,0.8) !important;
            font-size: 1rem !important;
        }
        
        /* Metric delta (change indicator) */
        [data-testid="stMetricDelta"] > div {
            font-size: 0.9rem !important;
        }
        
        /* Positive delta */
        div[data-testid="stMetricDelta"] svg {
            color: #2ecc71 !important;
        }
        
        /* Negative delta */
        div[data-testid*="stMetricDelta"]:has(svg[fill="hsl(5, 86%, 58%)"]) {
            color: #e74c3c !important;
        }

        /* ---------- Text elements ---------- */
        h1, h2, h3, h4, h5, h6 {
            color: #f8f9fa !important;
        }
        
        /* ---------- Dataframes ---------- */
        [data-testid="stDataFrame"] {
            background: rgba(255,255,255,0.05) !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            border-radius: 8px !important;
        }
        
        /* ---------- Input widgets ---------- */
        .stDateInput, .stSelectbox {
            background: rgba(255,255,255,0.05) !important;
            border-radius: 8px !important;
            padding: 0.5rem !important;
        }
        
        /* Responsive tweaks */
        @media (max-width: 768px) {
            [data-testid="stAppViewContainer"] { padding: 0.5rem !important; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Constants
MAX_FILE_SIZE_MB = 50
SUPPORTED_FILE_TYPES = ["csv", "xlsx"]

def validate_uploaded_file(uploaded_file):
    """Validates the uploaded file meets requirements"""
    if uploaded_file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise ValueError(f"File size exceeds {MAX_FILE_SIZE_MB}MB limit")
    if uploaded_file.name.split('.')[-1].lower() not in SUPPORTED_FILE_TYPES:
        raise ValueError(f"Unsupported file type. Please upload {', '.join(SUPPORTED_FILE_TYPES)}")

def display_loading_animation():
    """Shows a loading animation during processing"""
    with st.spinner('Analyzing your data...'):
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.02)
            progress_bar.progress(i + 1)
        progress_bar.empty()

def main_ui() -> Tuple[Optional[Any], Optional[Tuple[datetime, datetime]], bool]:
    # Inject global styles FIRST
    _inject_global_styles()

    # ===== MAIN UI =====
    st.title("📊 Sales Insights Tool")
    st.markdown("Upload your sales data to analyze trends, metrics, and correlations.")
    
    # File Uploader
    uploaded_file = st.file_uploader(
        "Upload sales data (CSV or Excel)", 
        type=SUPPORTED_FILE_TYPES,
        help=f"Maximum file size: {MAX_FILE_SIZE_MB}MB"
    )
    
    date_range = None
    export_requested = False
    
    if uploaded_file:
        try:
            validate_uploaded_file(uploaded_file)
            display_loading_animation()
            
            # Show raw data section
            with st.expander("🔍 Data Overview", expanded=True):
                display_data_preview(uploaded_file)
            
            # Date filter section
            date_range = display_date_filter(uploaded_file)
            st.markdown("---")

            # Insights sections with smaller charts
            display_insights_sections(uploaded_file, date_range)
            
            # Export button
            export_requested = st.button("📤 Export Report", type="primary")
            
        except Exception as e:
            st.error(str(e))
    
    return uploaded_file, date_range, export_requested  

def display_data_preview(uploaded_file):
    """Display raw data and column information"""
    df = load_data(uploaded_file)
    col_types = analyze_columns(df)
    
    st.subheader("Raw Data Preview")
    st.dataframe(df.head(5), height=200)
    
    st.subheader("Detected Structure")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Dates**")
        st.write(col_types['date'] or "None detected")
    with col2:
        st.markdown("**Numbers**")
        st.write(col_types['numeric'] or "None detected")
    with col3:
        st.markdown("**Categories**")
        st.write(col_types['categorical'] or "None detected")

def display_date_filter(uploaded_file) -> Optional[Tuple[datetime, datetime]]:
    """Display date range selector and return selected range"""
    df = load_data(uploaded_file)
    col_types = analyze_columns(df)
    
    if col_types['date']:
        date_col = col_types['date'][0]
        df[date_col] = pd.to_datetime(df[date_col])
        min_date, max_date = df[date_col].min(), df[date_col].max()
        
        st.subheader("Date Range Filter")
        date_range = st.date_input(
            "Select date range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            format="YYYY-MM-DD"
        )
        return date_range
    return None

def display_insights_sections(uploaded_file, date_range):
    """Display all insights sections with optimized chart sizes"""
    st.subheader("Analysis Results")
    
    tab1, tab2, tab3 = st.tabs(["Key Metrics", "Trend Analysis", "Correlations"])
    
    with tab1:
        display_metrics(uploaded_file, date_range)
    
    with tab2:
        display_trends(uploaded_file, date_range)
    
    with tab3:
        display_correlations(uploaded_file, date_range)

def display_metrics(uploaded_file, date_range):
    """Display key metrics"""
    df = load_data(uploaded_file)
    if date_range and 'date' in analyze_columns(df):
        date_col = analyze_columns(df)['date'][0]
        df[date_col] = pd.to_datetime(df[date_col])
        mask = (df[date_col] >= pd.to_datetime(date_range[0])) & \
               (df[date_col] <= pd.to_datetime(date_range[1]))
        df = df[mask]
    
    col_types = analyze_columns(df)
    if col_types['numeric']:
        metrics = calculate_metrics(df, col_types['numeric'][0])
        cols = st.columns(3)
        cols[0].metric("Total", f"${metrics['total']:,.2f}")
        cols[1].metric("Average", f"${metrics['average']:,.2f}")
        cols[2].metric("Records", f"{metrics['count']:,}")

def display_trends(uploaded_file, date_range):
    """Display trend visualizations with smaller size"""
    df = load_data(uploaded_file)
    if date_range and 'date' in analyze_columns(df):
        date_col = analyze_columns(df)['date'][0]
        df[date_col] = pd.to_datetime(df[date_col])
        mask = (df[date_col] >= pd.to_datetime(date_range[0])) & \
               (df[date_col] <= pd.to_datetime(date_range[1]))
        df = df[mask]
    
    col_types = analyze_columns(df)
    if col_types['date'] and col_types['numeric']:
        st.subheader("Sales Trend")
        fig = create_trend_plot(df, col_types['date'][0], col_types['numeric'][0])
        fig.set_size_inches(5, 2)  # Smaller figure size
        st.pyplot(fig, use_container_width=True)
    
    if col_types['categorical'] and col_types['numeric']:
        st.subheader("Top Items")
        fig = create_top_items_plot(df, col_types['categorical'][0], col_types['numeric'][0])
        fig.set_size_inches(5, 2)  # Smaller figure size
        st.pyplot(fig, use_container_width=True)

def display_correlations(uploaded_file, date_range):
    """Display correlation analysis with smaller chart"""
    df = load_data(uploaded_file)
    if date_range and 'date' in analyze_columns(df):
        date_col = analyze_columns(df)['date'][0]
        df[date_col] = pd.to_datetime(df[date_col])
        mask = (df[date_col] >= pd.to_datetime(date_range[0])) & \
               (df[date_col] <= pd.to_datetime(date_range[1]))
        df = df[mask]
    
    col_types = analyze_columns(df)
    if len(col_types['numeric']) >= 2:
        st.subheader("Correlation Analysis")
        x_axis = st.selectbox("X-Axis", col_types['numeric'])
        y_axis = st.selectbox("Y-Axis", col_types['numeric'], index=1)
        fig = create_scatter_plot(df, x_axis, y_axis)
        fig.set_size_inches(3, 1)  # Smaller figure size
        st.pyplot(fig, use_container_width=True)

if __name__ == "__main__":
    main_ui()