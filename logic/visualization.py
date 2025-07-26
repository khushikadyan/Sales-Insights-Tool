import matplotlib.pyplot as plt
import pandas as pd
from typing import List, Dict, Any
from io import BytesIO
import zipfile

def generate_visualizations(df: pd.DataFrame, col_types: Dict[str, Any]) -> List[plt.Figure]:
    """Generate all visualizations based on data and column types"""
    figures = []
    
    # Trend plot
    if col_types['date'] and col_types['numeric']:
        fig = create_trend_plot(df, col_types['date'][0], col_types['numeric'][0])
        figures.append(fig)
    
    # Top performers plot
    if col_types['categorical'] and col_types['numeric']:
        fig = create_top_items_plot(df, col_types['categorical'][0], col_types['numeric'][0])
        figures.append(fig)
    
    # Correlation plot if multiple numeric columns
    if len(col_types['numeric']) >= 2:
        fig = create_scatter_plot(df, col_types['numeric'][0], col_types['numeric'][1])
        figures.append(fig)
    
    return figures

def create_trend_plot(df: pd.DataFrame, date_col: str, value_col: str) -> plt.Figure:
    """Create a trend line plot"""
    fig, ax = plt.subplots(figsize=(10, 6))
    df.groupby(date_col)[value_col].sum().plot(ax=ax)
    ax.set_title(f"Trend of {value_col} over time")
    ax.set_ylabel(value_col)
    ax.grid(True)
    plt.tight_layout()
    return fig

def create_top_items_plot(df: pd.DataFrame, category_col: str, value_col: str) -> plt.Figure:
    """Create a bar plot of top performers"""
    top_items = df.groupby(category_col)[value_col].sum().nlargest(10)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    top_items.plot(kind='barh', ax=ax)
    ax.set_title(f"Top {category_col} by {value_col}")
    ax.set_xlabel(value_col)
    plt.tight_layout()
    return fig

def create_scatter_plot(df: pd.DataFrame, x_col: str, y_col: str) -> plt.Figure:
    """Create a scatter plot for correlation analysis"""
    fig, ax = plt.subplots(figsize=(10, 6))
    df.plot.scatter(x=x_col, y=y_col, ax=ax)
    ax.set_title(f"{x_col} vs {y_col} Correlation")
    ax.grid(True)
    plt.tight_layout()
    return fig

def prepare_visualizations_export(figures: List[plt.Figure]) -> BytesIO:
    """Prepare visualizations for export (without Streamlit dependency)"""
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, 'w') as zip_file:
        for i, fig in enumerate(figures):
            img_buffer = BytesIO()
            fig.savefig(img_buffer, format='png', dpi=120, bbox_inches='tight')
            zip_file.writestr(f"plot_{i+1}.png", img_buffer.getvalue())
    buffer.seek(0)
    return buffer
