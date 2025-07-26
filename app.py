import streamlit as st
from ui.landing import show_landing
from ui.force_css import force_css
from ui.layout import main_ui
from ui.styles import apply_custom_styles
from logic.data_processing import process_data
from logic.visualization import generate_visualizations, prepare_visualizations_export
import os
st.write(os.listdir('.'))

def render_analysis_page():
    """Handle the analysis page with all its functionality"""
    # Your existing analysis code
    uploaded_file, date_range, export_requested = main_ui()
    
    if uploaded_file:
        df, col_types = process_data(uploaded_file, date_range)
        visualizations = generate_visualizations(df, col_types)
        
        if export_requested and visualizations:
            zip_buffer = prepare_visualizations_export(visualizations)
            st.download_button(
                label="📥 Download Report (ZIP)",
                data=zip_buffer,
                file_name="sales_report.zip",
                mime="application/zip"
            )

def main():
    
    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = "landing"
    if 'should_scroll' not in st.session_state:
        st.session_state.should_scroll = False

    # Set page config
    st.set_page_config(
        page_title="Sales Insights Tool",
        page_icon="📊",
        layout="wide"
    )
    
    force_css()
    
    # Handle scrolling if needed
    if st.session_state.should_scroll:
        st.markdown("""
        <script>
            window.addEventListener('load', function() {
                const element = document.getElementById('sales-insights-tool');
                if (element) {
                    element.scrollIntoView({behavior: 'smooth'});
                }
            });
        </script>
        """, unsafe_allow_html=True)
        st.session_state.should_scroll = False
    
    # Page routing
    if st.session_state.page == "landing":
        show_landing()
    else:
        render_analysis_page()

if __name__ == "__main__":
    main()
