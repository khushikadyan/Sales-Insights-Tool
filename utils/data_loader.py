import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def load_data(uploaded_file):
    """Universal data loader with auto-type detection"""
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file, encoding='latin-1')
    else:
        df = pd.read_excel(uploaded_file)
    
    # Auto-convert potential date columns
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                df[col] = pd.to_datetime(df[col], errors='ignore')
            except:
                pass
    return df

def analyze_columns(df):
    """Classify columns automatically"""
    return {
        'date': [c for c in df.columns if pd.api.types.is_datetime64_any_dtype(df[c])],
        'numeric': df.select_dtypes(include=['number']).columns.tolist(),
        'categorical': df.select_dtypes(include=['object', 'category']).columns.tolist()
    }

def create_trend_plot(df, date_col, value_col):
    """Matplotlib trend plot"""
    plt.figure(figsize=(10, 4))
    df['Period'] = df[date_col].dt.to_period('M').astype(str)
    trend_data = df.groupby('Period')[value_col].sum()
    
    plt.plot(trend_data.index, trend_data.values, marker='o', linestyle='-')
    plt.title(f"Monthly Trend of {value_col}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    return plt

def create_top_items_plot(df, category_col, value_col):
    """Matplotlib top categories plot"""
    top_items = df.groupby(category_col)[value_col].sum().nlargest(5)
    
    plt.figure(figsize=(8, 4))
    top_items.plot(kind='bar', color='skyblue')
    plt.title(f"Top {category_col} by {value_col}")
    plt.tight_layout()
    return plt

def create_scatter_plot(df, x_col, y_col):
    plt.figure(figsize=(8, 4))
    plt.scatter(df[x_col], df[y_col], alpha=0.5)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title(f"{x_col} vs {y_col}")
    return plt

def create_pie_chart(df, category_col, value_col):
    top_cats = df.groupby(category_col)[value_col].sum().nlargest(5)
    plt.figure(figsize=(6, 6))
    plt.pie(top_cats, labels=top_cats.index, autopct='%1.1f%%')
    plt.title(f"Market Share by {category_col}")
    return plt