from typing import Tuple, Dict, Any
import pandas as pd
from utils.data_loader import load_data, analyze_columns

def process_data(uploaded_file, date_range=None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Load and process the uploaded data"""
    df = load_data(uploaded_file)
    col_types = analyze_columns(df)
    
    # Apply date filter if provided
    if date_range and col_types['date']:
        date_col = col_types['date'][0]
        df[date_col] = pd.to_datetime(df[date_col])
        mask = (df[date_col] >= pd.to_datetime(date_range[0])) & \
               (df[date_col] <= pd.to_datetime(date_range[1]))
        df = df[mask]
    
    return df, col_types

def calculate_metrics(df, numeric_col: str) -> Dict[str, float]:
    """Calculate basic metrics for numeric column"""
    return {
        'total': df[numeric_col].sum(),
        'average': df[numeric_col].mean(),
        'count': len(df)
    }