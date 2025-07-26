import pandas as pd
from typing import Dict, List, Any
from io import BytesIO
import chardet

def load_data(uploaded_file) -> pd.DataFrame:
    """Load data from uploaded file with robust error handling"""
    if uploaded_file is None:
        raise ValueError("No file uploaded")
    
    try:
        # Detect file encoding first
        raw_data = uploaded_file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        
        # Reset file pointer
        uploaded_file.seek(0)
        
        if uploaded_file.name.endswith('.csv'):
            # Try reading with detected encoding, fallback to others
            try:
                df = pd.read_csv(BytesIO(raw_data), encoding=encoding)
            except:
                # Try common encodings if detected one fails
                for enc in ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']:
                    try:
                        uploaded_file.seek(0)
                        df = pd.read_csv(uploaded_file, encoding=enc)
                        break
                    except:
                        continue
                else:
                    raise ValueError("Could not read CSV file with any encoding")
            
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(BytesIO(raw_data))
        else:
            raise ValueError("Unsupported file format. Only CSV and Excel files are supported")
        
        # Validate we got data
        if df.empty:
            raise ValueError("The file appears to be empty or couldn't be parsed")
            
        return df
        
    except Exception as e:
        raise ValueError(f"Error loading file: {str(e)}")

def analyze_columns(df: pd.DataFrame) -> Dict[str, List[str]]:
    """Analyze dataframe columns and categorize them"""
    if df.empty:
        return {
            'date': [],
            'numeric': [],
            'categorical': []
        }
    
    col_types = {
        'date': [],
        'numeric': [],
        'categorical': []
    }
    
    for col in df.columns:
        # Date detection
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            col_types['date'].append(col)
        # Numeric detection
        elif pd.api.types.is_numeric_dtype(df[col]):
            col_types['numeric'].append(col)
        # Categorical detection
        else:
            col_types['categorical'].append(col)
    
    return col_types