"""
Basic usage examples for the Data Transformer Toolkit.

This example demonstrates how to use the DataTransformer component
for common data transformation tasks.
"""
import pandas as pd
import numpy as np
from data_transformer import DataTransformer


def numeric_transformations_example():
    """Example of numeric data transformations."""
    print("=== Numeric Transformations Example ===")
    
    # Create sample data
    data = pd.DataFrame({
        'A': [1, 2, 3, 4, 100],  # Contains an outlier
        'B': [10, 20, 30, 40, 50]
    })
    print("Original data:")
    print(data)
    
    # Initialize the transformer
    transformer = DataTransformer()
    
    # Define a sequence of operations
    operations = [
        {
            'type': 'numeric',
            'method': 'replace_outliers',
            'params': {'method': 'zscore', 'threshold': 2.0, 'replacement': 'median'},
            'columns': ['A']
        },
        {
            'type': 'numeric',
            'method': 'normalize',
            'params': {'method': 'minmax'},
            'columns': ['A', 'B']
        }
    ]
    
    # Apply the transformations
    result = transformer.transform(data, operations)
    
    print("\nTransformed data:")
    print(result)
    
    # Get the transformation history
    print("\nTransformation history:")
    for op in transformer.get_transformation_history():
        print(f"- {op['operation']} applied to {op['columns']} with params {op['parameters']}")


def text_transformations_example():
    """Example of text data transformations."""
    print("\n=== Text Transformations Example ===")
    
    # Create sample data
    data = pd.DataFrame({
        'Text': [
            "Hello, World! 123",
            "   Data Transformation  456  ",
            "Python is great for data processing!"
        ]
    })
    print("Original data:")
    print(data)
    
    # Initialize the transformer
    transformer = DataTransformer()
    
    # Define a sequence of operations
    operations = [
        {
            'type': 'text',
            'method': 'clean_text',
            'params': {
                'remove_punctuation': True,
                'remove_numbers': True,
                'lowercase': True,
                'remove_extra_spaces': True
            },
            'columns': ['Text']
        },
        {
            'type': 'text',
            'method': 'tokenize',
            'params': {},
            'columns': ['Text']
        }
    ]
    
    # Apply the transformations
    result = transformer.transform(data, operations)
    
    print("\nTransformed data (tokenized):")
    print(result)
    
    # Join the tokens back
    join_operation = [
        {
            'type': 'text',
            'method': 'join_tokens',
            'params': {'separator': ' '},
            'columns': ['Text']
        }
    ]
    
    result = transformer.transform(result, join_operation)
    
    print("\nJoined tokens:")
    print(result)


def datetime_transformations_example():
    """Example of datetime data transformations."""
    print("\n=== DateTime Transformations Example ===")
    
    # Create sample data
    data = pd.DataFrame({
        'Date': ['2023-01-01', '2023-02-15', '2023-03-30']
    })
    print("Original data:")
    print(data)
    
    # Initialize the transformer
    transformer = DataTransformer()
    
    # Define operations to parse dates and extract components
    operations = [
        {
            'type': 'datetime',
            'method': 'parse_date',
            'params': {'format': '%Y-%m-%d'},
            'columns': ['Date']
        },
        {
            'type': 'datetime',
            'method': 'extract_component',
            'params': {'component': 'month'},
            'columns': ['Date']
        }
    ]
    
    # Apply the transformations
    result = transformer.transform(data, operations)
    
    print("\nExtracted months:")
    print(result)


def custom_operation_example():
    """Example of using custom operations."""
    print("\n=== Custom Operation Example ===")
    
    # Create sample data
    data = pd.DataFrame({
        'Value': [1, 2, 3, 4, 5]
    })
    print("Original data:")
    print(data)
    
    # Define a custom operation
    def square_and_add(values, add_value=0):
        return values ** 2 + add_value
    
    # Initialize the transformer
    transformer = DataTransformer()
    
    # Register the custom operation
    transformer.register_custom_operation('square_and_add', square_and_add)
    
    # Define the operation
    operations = [
        {
            'type': 'custom',
            'method': 'square_and_add',
            'params': {'add_value': 10},
            'columns': ['Value']
        }
    ]
    
    # Apply the transformation
    result = transformer.transform(data, operations)
    
    print("\nTransformed data (squared and added 10):")
    print(result)


def pipeline_example():
    """Example of creating and using a transformation pipeline."""
    print("\n=== Pipeline Example ===")
    
    # Initialize the transformer
    transformer = DataTransformer()
    
    # Define a reusable pipeline
    normalization_pipeline = transformer.create_pipeline([
        {
            'type': 'numeric',
            'method': 'replace_outliers',
            'params': {'method': 'zscore', 'threshold': 2.0},
            'columns': ['Value']
        },
        {
            'type': 'numeric',
            'method': 'normalize',
            'params': {'method': 'minmax'},
            'columns': ['Value']
        }
    ])
    
    # Create two different datasets
    data1 = pd.DataFrame({'Value': [1, 2, 3, 4, 20]})
    data2 = pd.DataFrame({'Value': [10, 20, 30, 40, 200]})
    
    print("Dataset 1 original:")
    print(data1)
    print("\nDataset 2 original:")
    print(data2)
    
    # Apply the same pipeline to both datasets
    result1 = normalization_pipeline(data1)
    result2 = normalization_pipeline(data2)
    
    print("\nDataset 1 transformed:")
    print(result1)
    print("\nDataset 2 transformed:")
    print(result2)


if __name__ == "__main__":
    numeric_transformations_example()
    text_transformations_example()
    datetime_transformations_example()
    custom_operation_example()
    pipeline_example()
