"""
Advanced usage examples for the Data Transformer Toolkit.

This example demonstrates more complex use cases and integration
with other libraries and data sources.
"""
import pandas as pd
import numpy as np
from data_transformer import DataTransformer
from data_transformer.utils.helpers import (
    parse_csv_data, 
    parse_json_data,
    export_to_csv,
    export_to_json,
    summarize_data
)


def data_cleaning_workflow():
    """Example of a complete data cleaning workflow."""
    print("=== Data Cleaning Workflow Example ===")
    
    # Sample data with various issues
    raw_data = """
    id,name,age,income,join_date
    1,John Doe,34,75000,2020-01-15
    2,Jane Smith,28,82000,2019-05-22
    3,Bob Johnson,45,NaN,2018-11-30
    4,Alice Brown,31,92000,2021-03-10
    5,Charlie Davis,invalid,65000,not-a-date
    6,Eve Wilson,29,150000,2020-08-05
    """
    
    # Parse the CSV data
    data = parse_csv_data(raw_data.strip(), skipinitialspace=True)
    print("Original data:")
    print(data)
    
    # Initialize the transformer
    transformer = DataTransformer()
    
    # Define a sequence of operations for cleaning
    cleaning_operations = [
        # Convert age to numeric, coercing errors to NaN
        {
            'type': 'custom',
            'method': 'convert_to_numeric',
            'params': {'errors': 'coerce'},
            'columns': ['age']
        },
        # Replace outliers in income
        {
            'type': 'numeric',
            'method': 'replace_outliers',
            'params': {'method': 'iqr', 'threshold': 1.5, 'replacement': 'median'},
            'columns': ['income']
        },
        # Parse dates
        {
            'type': 'datetime',
            'method': 'parse_date',
            'params': {'format': '%Y-%m-%d', 'errors': 'coerce'},
            'columns': ['join_date']
        },
        # Clean names
        {
            'type': 'text',
            'method': 'clean_text',
            'params': {'remove_punctuation': False, 'remove_extra_spaces': True},
            'columns': ['name']
        }
    ]
    
    # Register custom operation for converting to numeric
    def convert_to_numeric(values, errors='raise'):
        return pd.to_numeric(values, errors=errors)
    
    transformer.register_custom_operation('convert_to_numeric', convert_to_numeric)
    
    # Apply the cleaning operations
    cleaned_data = transformer.transform(data, cleaning_operations)
    print("\nCleaned data:")
    print(cleaned_data)
    
    # Get a summary of the cleaned data
    summary = summarize_data(cleaned_data)
    print("\nData summary:")
    for key, value in summary.items():
        if key != 'numeric_summary':
            print(f"{key}: {value}")
    
    # Export the cleaned data
    csv_output = export_to_csv(cleaned_data)
    json_output = export_to_json(cleaned_data)
    
    print("\nCSV output (first 100 chars):")
    print(csv_output[:100] + "...")
    print("\nJSON output (first 100 chars):")
    print(json_output[:100] + "...")





def time_series_example():
    """Example of time series data processing."""
    print("\n=== Time Series Example ===")
    
    # Create sample time series data
    dates = pd.date_range(start='2023-01-01', periods=10, freq='D')
    data = pd.DataFrame({
        'Date': dates,
        'Value': [10, 12, 15, 14, 16, 19, 18, 21, 24, 22]
    })
    print("Original time series data:")
    print(data)
    
    # Initialize the transformer
    transformer = DataTransformer()
    
    # Register custom operations for time series
    def calculate_rolling_mean(values, window=3):
        return values.rolling(window=window).mean()
    
    def calculate_pct_change(values):
        return values.pct_change() * 100
    
    transformer.register_custom_operation('rolling_mean', calculate_rolling_mean)
    transformer.register_custom_operation('pct_change', calculate_pct_change)
    
    # Define operations
    operations = [
        # Calculate percentage change
        {
            'type': 'custom',
            'method': 'pct_change',
            'params': {},
            'columns': ['Value']
        },
        # Calculate rolling mean
        {
            'type': 'custom',
            'method': 'rolling_mean',
            'params': {'window': 3},
            'columns': ['Value']
        }
    ]
    
    # Apply transformations
    transformed_data = transformer.transform(data, operations)
    
    print("\nTransformed time series data (% change with 3-day rolling average):")
    print(transformed_data)


def feature_engineering_example():
    """Example of feature engineering for machine learning."""
    print("\n=== Feature Engineering Example ===")
    
    # Create sample data
    data = pd.DataFrame({
        'age': [25, 30, 35, 40, 45, 50],
        'income': [50000, 60000, 75000, 90000, 85000, 100000],
        'education_years': [12, 16, 16, 18, 16, 20],
        'job_category': ['tech', 'finance', 'tech', 'healthcare', 'finance', 'tech']
    })
    print("Original data:")
    print(data)
    
    # Initialize the transformer
    transformer = DataTransformer()
    
    # Register custom operations for feature engineering
    def create_age_group(values):
        return pd.cut(values, bins=[0, 30, 40, 50, 100], 
                     labels=['young', 'middle', 'senior', 'elderly'])
    
    def one_hot_encode(values):
        return pd.get_dummies(values, prefix=values.name)
    
    def create_interaction_feature(data, col1, col2, operation='multiply'):
        if operation == 'multiply':
            return data[col1] * data[col2]
        elif operation == 'divide':
            return data[col1] / data[col2]
        elif operation == 'add':
            return data[col1] + data[col2]
        elif operation == 'subtract':
            return data[col1] - data[col2]
        return None
    
    transformer.register_custom_operation('create_age_group', create_age_group)
    transformer.register_custom_operation('one_hot_encode', one_hot_encode)
    
    # Define operations
    operations = [
        # Create age groups
        {
            'type': 'custom',
            'method': 'create_age_group',
            'params': {},
            'columns': ['age']
        },
        # Normalize numeric features
        {
            'type': 'numeric',
            'method': 'normalize',
            'params': {'method': 'zscore'},
            'columns': ['income', 'education_years']
        }
    ]
    
    # Apply transformations
    transformed_data = transformer.transform(data, operations)
    
    print("\nTransformed data with feature engineering:")
    print(transformed_data)
    
    # One-hot encoding requires special handling as it changes the DataFrame structure
    # We'll demonstrate it separately
    job_dummies = one_hot_encode(data['job_category'])
    print("\nOne-hot encoded job categories:")
    print(job_dummies)
    
    # Create an interaction feature
    income_per_education = create_interaction_feature(
        data, 'income', 'education_years', operation='divide'
    )
    print("\nInteraction feature (income per year of education):")
    print(income_per_education)


if __name__ == "__main__":
    data_cleaning_workflow()
    time_series_example()
    feature_engineering_example()
