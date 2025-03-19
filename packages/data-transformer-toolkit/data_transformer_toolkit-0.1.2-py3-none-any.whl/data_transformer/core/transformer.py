"""
Core transformer module that provides the main interface for data transformation operations.
"""
from typing import Any, Dict, List, Union, Callable, Optional
import pandas as pd
import numpy as np
from data_transformer.core.operations import NumericOperation, TextOperation, DateTimeOperation, CustomOperation


class DataTransformer:
    """
    Main component class that provides a unified interface for data transformation operations.
    
    This class hides the implementation details and provides a simple API for end-users
    to perform various data transformation operations.
    """
    
    def __init__(self):
        """Initialize the DataTransformer with default operations."""
        self._numeric_ops = NumericOperation()
        self._text_ops = TextOperation()
        self._datetime_ops = DateTimeOperation()
        self._custom_ops = {}
        self._transformation_history = []
        
    def transform(self, data: Union[pd.DataFrame, np.ndarray, List, Dict], 
                  operations: List[Dict[str, Any]]) -> Union[pd.DataFrame, np.ndarray, List, Dict]:
        """
        Apply a sequence of transformation operations to the input data.
        
        Args:
            data: Input data to transform (DataFrame, array, list, or dict)
            operations: List of operation specifications, each containing:
                - 'type': The type of operation ('numeric', 'text', 'datetime', 'custom')
                - 'method': The method name to call
                - 'params': Dictionary of parameters for the method
                - 'columns': (Optional) Columns to apply the transformation to (for DataFrame)
        
        Returns:
            Transformed data in the same format as input
        """
        result = data
        
        for op in operations:
            op_type = op.get('type', '').lower()
            method = op.get('method', '')
            params = op.get('params', {})
            columns = op.get('columns', None)
            
            # Record the operation in history
            self._transformation_history.append({
                'operation': f"{op_type}.{method}",
                'parameters': params,
                'columns': columns
            })
            
            # Apply the operation based on type
            if op_type == 'numeric':
                result = self._apply_operation(result, self._numeric_ops, method, params, columns)
            elif op_type == 'text':
                result = self._apply_operation(result, self._text_ops, method, params, columns)
            elif op_type == 'datetime':
                result = self._apply_operation(result, self._datetime_ops, method, params, columns)
            elif op_type == 'custom' and method in self._custom_ops:
                result = self._apply_operation(result, None, method, params, columns, 
                                              custom_func=self._custom_ops[method])
        
        return result
    
    def _apply_operation(self, data, operation_obj, method_name, params, columns=None, custom_func=None):
        """
        Internal method to apply an operation to the data.
        
        Handles different data types and applies operations to specific columns if needed.
        """
        # If it's a DataFrame and columns are specified
        if isinstance(data, pd.DataFrame) and columns is not None:
            result = data.copy()
            
            for col in columns:
                if col in result.columns:
                    if custom_func:
                        result[col] = custom_func(result[col], **params)
                    else:
                        method = getattr(operation_obj, method_name)
                        result[col] = method(result[col], **params)
            
            return result
            
        # If it's a DataFrame but no columns specified, or other data types
        if custom_func:
            return custom_func(data, **params)
        else:
            method = getattr(operation_obj, method_name)
            return method(data, **params)
    
    def register_custom_operation(self, name: str, function: Callable):
        """
        Register a custom operation function.
        
        Args:
            name: Name to identify the custom operation
            function: Callable that implements the operation
        """
        self._custom_ops[name] = function
        
    def get_transformation_history(self) -> List[Dict[str, Any]]:
        """Return the history of applied transformations."""
        return self._transformation_history
    
    def create_pipeline(self, operations: List[Dict[str, Any]]) -> Callable:
        """
        Create a reusable transformation pipeline from a list of operations.
        
        Returns a function that can be applied to any compatible data.
        """
        def pipeline(data):
            return self.transform(data, operations)
        
        return pipeline
