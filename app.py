import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import zipfile
from utils.data_loader import *

def main():
    st.title("📊 Sales Insights Tool")
    uploaded_file = st.file_uploader("Upload ANY sales data", type=["csv", "xlsx"])
    
    if uploaded_file:
        df = load_data(uploaded_file)
        col_types = analyze_columns(df)
        plots = []  # To collect plots for export

        # Date filter
        if col_types['date']:
            df[col_types['date'][0]] = pd.to_datetime(df[col_types['date'][0]])
            min_date = df[col_types['date'][0]].min()
            max_date = df[col_types['date'][0]].max()
            
            date_range = st.date_input(
                "Select Date Range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )
            mask = (df[col_types['date'][0]] >= pd.to_datetime(date_range[0])) & \
                   (df[col_types['date'][0]] <= pd.to_datetime(date_range[1]))
            df = df[mask]
            
            if len(df) == 0:
                st.error("No data in selected date range!")
                st.stop()

        # Show raw data & column types
        st.subheader("Raw Data")
        st.write(df)

        st.subheader("🔍 Detected Structure")
        st.write(f"Dates: {col_types['date']}")
        st.write(f"Numbers: {col_types['numeric']}")
        st.write(f"Categories: {col_types['categorical']}")

        # Quick Metrics
        st.subheader("📈 Quick Insights")
        if col_types['numeric']:
            value_col = col_types['numeric'][0]
            cols = st.columns(3)
            cols[0].metric("Total", f"{df[value_col].sum():,.2f}")
            cols[1].metric("Average", f"{df[value_col].mean():,.2f}")
            cols[2].metric("Records", len(df))

        # Trend Plot
        if col_types['date'] and col_types['numeric']:
            st.subheader("📅 Auto-Detected Trend")
            fig1 = create_trend_plot(df, col_types['date'][0], col_types['numeric'][0])
            st.pyplot(fig1)
            plots.append(fig1)

        # Top Performers
        if col_types['categorical'] and col_types['numeric']:
            st.subheader("🏆 Top Performers")
            fig2 = create_top_items_plot(df, col_types['categorical'][0], col_types['numeric'][0])
            st.pyplot(fig2)
            plots.append(fig2)

        # Correlation
        if len(col_types['numeric']) >= 2:
            st.subheader("📊 Correlation Analysis")
            x_axis = st.selectbox("X-Axis", col_types['numeric'])
            y_axis = st.selectbox("Y-Axis", col_types['numeric'], index=1)
            fig3 = create_scatter_plot(df, x_axis, y_axis)
            st.pyplot(fig3)
            plots.append(fig3)

        # 📦 Export ZIP
        if st.button("Export Report"):
            buffer = BytesIO()
            with zipfile.ZipFile(buffer, 'w') as zip_file:
                

                # Save plots
                for i, plot in enumerate(plots):
                    img_buffer = BytesIO()
                    plot.savefig(img_buffer, format='png')
                    zip_file.writestr(f"plot_{i+1}.png", img_buffer.getvalue())

            st.download_button(
                label="Download Report (ZIP)",
                data=buffer.getvalue(),
                file_name="sales_report.zip",
                mime="application/zip"
            )

if __name__ == "__main__":
    main()
