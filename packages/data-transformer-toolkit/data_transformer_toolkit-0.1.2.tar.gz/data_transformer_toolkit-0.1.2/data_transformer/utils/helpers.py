"""
Helper utilities for data transformation operations.
"""
from typing import Any, Dict, List, Union, Optional
import pandas as pd
import numpy as np
import json
import csv
import io


def detect_data_type(data: Any) -> str:
    """
    Detect the type of data provided.
    
    Args:
        data: Data to analyze
        
    Returns:
        String describing the data type ('dataframe', 'array', 'list', 'dict', etc.)
    """
    if isinstance(data, pd.DataFrame):
        return 'dataframe'
    elif isinstance(data, pd.Series):
        return 'series'
    elif isinstance(data, np.ndarray):
        return 'array'
    elif isinstance(data, list):
        return 'list'
    elif isinstance(data, dict):
        return 'dict'
    elif isinstance(data, str):
        return 'string'
    elif isinstance(data, (int, float)):
        return 'numeric'
    else:
        return 'unknown'


def convert_to_dataframe(data: Any, column_name: Optional[str] = None) -> pd.DataFrame:
    """
    Convert various data types to a pandas DataFrame.
    
    Args:
        data: Data to convert
        column_name: Name for the column if data is a simple list or array
        
    Returns:
        Pandas DataFrame
    """
    if isinstance(data, pd.DataFrame):
        return data
    
    if isinstance(data, pd.Series):
        return data.to_frame(name=column_name or 'value')
    
    if isinstance(data, np.ndarray):
        if data.ndim == 1:
            return pd.DataFrame({column_name or 'value': data})
        else:
            return pd.DataFrame(data)
    
    if isinstance(data, list):
        if all(isinstance(item, dict) for item in data):
            return pd.DataFrame(data)
        else:
            return pd.DataFrame({column_name or 'value': data})
    
    if isinstance(data, dict):
        return pd.DataFrame(data)
    
    # For scalar values
    return pd.DataFrame({column_name or 'value': [data]})


def parse_csv_data(csv_data: str, **kwargs) -> pd.DataFrame:
    """
    Parse CSV string data into a DataFrame.
    
    Args:
        csv_data: CSV data as a string
        **kwargs: Additional arguments to pass to pandas.read_csv
        
    Returns:
        Pandas DataFrame
    """
    return pd.read_csv(io.StringIO(csv_data), **kwargs)


def parse_json_data(json_data: str) -> Union[pd.DataFrame, Dict, List]:
    """
    Parse JSON string data.
    
    Args:
        json_data: JSON data as a string
        
    Returns:
        Parsed data (DataFrame if possible, otherwise dict or list)
    """
    parsed = json.loads(json_data)
    
    if isinstance(parsed, list) and all(isinstance(item, dict) for item in parsed):
        return pd.DataFrame(parsed)
    
    return parsed


def export_to_csv(data: Union[pd.DataFrame, np.ndarray, List, Dict]) -> str:
    """
    Export data to CSV format.
    
    Args:
        data: Data to export
        
    Returns:
        CSV string
    """
    df = convert_to_dataframe(data)
    return df.to_csv(index=False)


def export_to_json(data: Union[pd.DataFrame, np.ndarray, List, Dict]) -> str:
    """
    Export data to JSON format.
    
    Args:
        data: Data to export
        
    Returns:
        JSON string
    """
    if isinstance(data, pd.DataFrame):
        return data.to_json(orient='records')
    
    if isinstance(data, np.ndarray):
        return json.dumps(data.tolist())
    
    return json.dumps(data)


def summarize_data(data: Union[pd.DataFrame, np.ndarray, List, Dict]) -> Dict[str, Any]:
    """
    Generate a summary of the data.
    
    Args:
        data: Data to summarize
        
    Returns:
        Dictionary with summary statistics
    """
    data_type = detect_data_type(data)
    
    if data_type == 'dataframe':
        return {
            'type': 'dataframe',
            'shape': data.shape,
            'columns': list(data.columns),
            'dtypes': {col: str(dtype) for col, dtype in data.dtypes.items()},
            'missing_values': data.isnull().sum().to_dict(),
            'numeric_summary': data.describe().to_dict() if not data.empty else {}
        }
    
    elif data_type == 'series':
        return {
            'type': 'series',
            'length': len(data),
            'dtype': str(data.dtype),
            'missing_values': data.isnull().sum(),
            'summary': data.describe().to_dict() if not data.empty else {}
        }
    
    elif data_type == 'array':
        return {
            'type': 'array',
            'shape': data.shape,
            'dtype': str(data.dtype),
            'summary': {
                'min': float(np.min(data)) if data.size > 0 and np.issubdtype(data.dtype, np.number) else None,
                'max': float(np.max(data)) if data.size > 0 and np.issubdtype(data.dtype, np.number) else None,
                'mean': float(np.mean(data)) if data.size > 0 and np.issubdtype(data.dtype, np.number) else None,
                'std': float(np.std(data)) if data.size > 0 and np.issubdtype(data.dtype, np.number) else None
            }
        }
    
    elif data_type == 'list':
        return {
            'type': 'list',
            'length': len(data),
            'element_types': list(set(type(item).__name__ for item in data))
        }
    
    elif data_type == 'dict':
        return {
            'type': 'dict',
            'keys': list(data.keys()),
            'value_types': {key: type(value).__name__ for key, value in data.items()}
        }
    
    else:
        return {
            'type': data_type
        }
