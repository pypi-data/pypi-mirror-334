"""
Unit tests for the Data Transformer Toolkit.
"""
import unittest
import pandas as pd
import numpy as np
from datetime import datetime
from data_transformer import DataTransformer
from data_transformer.core.operations import NumericOperation, TextOperation, DateTimeOperation


class TestDataTransformer(unittest.TestCase):
    """Test cases for the DataTransformer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.transformer = DataTransformer()
        
        # Sample data for testing
        self.numeric_data = pd.DataFrame({
            'A': [1, 2, 3, 4, 100],  # Contains an outlier
            'B': [10, 20, 30, 40, 50]
        })
        
        self.text_data = pd.DataFrame({
            'Text': [
                "Hello, World! 123",
                "   Data Transformation  456  ",
                "Python is great for data processing!"
            ]
        })
        
        self.date_data = pd.DataFrame({
            'Date': ['2023-01-01', '2023-02-15', '2023-03-30']
        })
    
    def test_numeric_operations(self):
        """Test numeric operations."""
        # Test normalization
        operations = [
            {
                'type': 'numeric',
                'method': 'normalize',
                'params': {'method': 'minmax'},
                'columns': ['A', 'B']
            }
        ]
        
        result = self.transformer.transform(self.numeric_data, operations)
        
        # Check if values are normalized between 0 and 1
        self.assertTrue((result['A'] >= 0).all() and (result['A'] <= 1).all())
        self.assertTrue((result['B'] >= 0).all() and (result['B'] <= 1).all())
        
        # Check if min is 0 and max is 1
        self.assertAlmostEqual(result['A'].min(), 0.0)
        self.assertAlmostEqual(result['A'].max(), 1.0)
        
        # Test outlier replacement
        operations = [
            {
                'type': 'numeric',
                'method': 'replace_outliers',
                'params': {'method': 'zscore', 'threshold': 2.0, 'replacement': 'median'},
                'columns': ['A']
            }
        ]
        
        result = self.transformer.transform(self.numeric_data, operations)
        
        # Check if the outlier was replaced
        self.assertNotEqual(result['A'].iloc[4], 100)
        
        # Test scaling
        operations = [
            {
                'type': 'numeric',
                'method': 'scale',
                'params': {'factor': 2.0, 'offset': 5.0},
                'columns': ['B']
            }
        ]
        
        result = self.transformer.transform(self.numeric_data, operations)
        
        # Check if values are scaled correctly
        expected = self.numeric_data['B'] * 2.0 + 5.0
        pd.testing.assert_series_equal(result['B'], expected)
    
    def test_text_operations(self):
        """Test text operations."""
        # Test text cleaning
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
            }
        ]
        
        result = self.transformer.transform(self.text_data, operations)
        
        # Check if text is cleaned
        self.assertEqual(result['Text'].iloc[0], "hello world")
        self.assertEqual(result['Text'].iloc[1], "data transformation")
        
        # Test tokenization
        operations = [
            {
                'type': 'text',
                'method': 'tokenize',
                'params': {},
                'columns': ['Text']
            }
        ]
        
        result = self.transformer.transform(self.text_data, operations)
        
        # Check if text is tokenized
        self.assertIsInstance(result['Text'].iloc[0], list)
        self.assertIn("Hello,", result['Text'].iloc[0])
        
        # Test pattern extraction
        operations = [
            {
                'type': 'text',
                'method': 'extract_pattern',
                'params': {'pattern': r'(\w+) is (\w+)'},
                'columns': ['Text']
            }
        ]
        
        result = self.transformer.transform(self.text_data, operations)
        
        # Check if pattern is extracted
        self.assertEqual(result['Text'].iloc[2], "Python is great")
    
    def test_datetime_operations(self):
        """Test datetime operations."""
        # Test date parsing
        operations = [
            {
                'type': 'datetime',
                'method': 'parse_date',
                'params': {'format': '%Y-%m-%d'},
                'columns': ['Date']
            }
        ]
        
        result = self.transformer.transform(self.date_data, operations)
        
        # Check if dates are parsed
        self.assertIsInstance(result['Date'].iloc[0], datetime)
        self.assertEqual(result['Date'].iloc[0].year, 2023)
        self.assertEqual(result['Date'].iloc[0].month, 1)
        self.assertEqual(result['Date'].iloc[0].day, 1)
        
        # Test adding time delta
        operations = [
            {
                'type': 'datetime',
                'method': 'parse_date',
                'params': {'format': '%Y-%m-%d'},
                'columns': ['Date']
            }
        ]
        
        result = self.transformer.transform(self.date_data, operations)
        
        # Check if time delta is added
        self.assertEqual(result['Date'].iloc[0].day, 8)  # 1 + 7 days
        
        # Test component extraction
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
        
        result = self.transformer.transform(self.date_data, operations)
        
        # Check if component is extracted
        self.assertEqual(result['Date'].iloc[0], 1)  # January
        self.assertEqual(result['Date'].iloc[1], 2)  # February
    
    def test_custom_operations(self):
        """Test custom operations."""
        # Define a custom operation
        def square_and_add(values, add_value=0):
            return values ** 2 + add_value
        
        # Register the custom operation
        self.transformer.register_custom_operation('square_and_add', square_and_add)
        
        # Define the operation
        operations = [
            {
                'type': 'custom',
                'method': 'square_and_add',
                'params': {'add_value': 10},
                'columns': ['A']
            }
        ]
        
        # Apply the transformation
        result = self.transformer.transform(self.numeric_data, operations)
        
        # Check if custom operation is applied
        expected = self.numeric_data['A'] ** 2 + 10
        pd.testing.assert_series_equal(result['A'], expected)
    
    def test_transformation_history(self):
        """Test transformation history tracking."""
        operations = [
            {
                'type': 'numeric',
                'method': 'normalize',
                'params': {'method': 'minmax'},
                'columns': ['A']
            },
            {
                'type': 'numeric',
                'method': 'scale',
                'params': {'factor': 2.0},
                'columns': ['B']
            }
        ]
        
        self.transformer.transform(self.numeric_data, operations)
        
        # Check if history is tracked
        history = self.transformer.get_transformation_history()
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]['operation'], 'numeric.normalize')
        self.assertEqual(history[0]['columns'], ['A'])
        self.assertEqual(history[1]['operation'], 'numeric.scale')
        self.assertEqual(history[1]['columns'], ['B'])
    
    def test_pipeline_creation(self):
        """Test creation of transformation pipelines."""
        # Define a reusable pipeline
        operations = [
            {
                'type': 'numeric',
                'method': 'normalize',
                'params': {'method': 'minmax'},
                'columns': ['A']
            },
            {
                'type': 'numeric',
                'method': 'scale',
                'params': {'factor': 2.0},
                'columns': ['A']
            }
        ]
        
        pipeline = self.transformer.create_pipeline(operations)
        
        # Apply the pipeline
        result = pipeline(self.numeric_data)
        
        # Check if pipeline is applied correctly
        self.assertTrue((result['A'] >= 0).all() and (result['A'] <= 2).all())
        self.assertAlmostEqual(result['A'].max(), 2.0)


class TestNumericOperation(unittest.TestCase):
    """Test cases for the NumericOperation class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.op = NumericOperation()
        self.data = np.array([1, 2, 3, 4, 100])  # Contains an outlier
    
    def test_normalize(self):
        """Test normalization methods."""
        # Test minmax normalization
        result = self.op.normalize(self.data, method='minmax')
        self.assertAlmostEqual(result.min(), 0.0)
        self.assertAlmostEqual(result.max(), 1.0)
        
        # Test zscore normalization
        result = self.op.normalize(self.data, method='zscore')
        self.assertAlmostEqual(result.mean(), 0.0, places=10)
        
        # Test robust normalization
        result = self.op.normalize(self.data, method='robust')
        median = np.median(self.data)
        q1 = np.percentile(self.data, 25)
        q3 = np.percentile(self.data, 75)
        iqr = q3 - q1
        self.assertAlmostEqual(result[2], (3 - median) / iqr)
    
    def test_scale(self):
        """Test scaling operation."""
        result = self.op.scale(self.data, factor=2.0, offset=5.0)
        expected = self.data * 2.0 + 5.0
        np.testing.assert_array_equal(result, expected)
    
    def test_clip(self):
        """Test clipping operation."""
        result = self.op.clip(self.data, min_value=2, max_value=50)
        self.assertEqual(result.min(), 2)
        self.assertEqual(result.max(), 50)
    
    def test_round_values(self):
        """Test rounding operation."""
        data = np.array([1.234, 2.567, 3.789])
        result = self.op.round_values(data, decimals=1)
        expected = np.array([1.2, 2.6, 3.8])
        np.testing.assert_array_equal(result, expected)
    
    def test_replace_outliers(self):
        """Test outlier replacement."""
        # Test IQR method
        result = self.op.replace_outliers(self.data, method='iqr', threshold=1.5, replacement='median')
        self.assertNotEqual(result[4], 100)
        
        # Test zscore method
        result = self.op.replace_outliers(self.data, method='zscore', threshold=2.0, replacement='mean')
        self.assertNotEqual(result[4], 100)
        
        # Test nearest replacement
        result = self.op.replace_outliers(self.data, method='zscore', threshold=2.0, replacement='nearest')
        self.assertNotEqual(result[4], 100)
        self.assertEqual(result[4], 4)  # Nearest non-outlier value


class TestTextOperation(unittest.TestCase):
    """Test cases for the TextOperation class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.op = TextOperation()
        self.data = ["Hello, World! 123", "   Data Transformation  456  "]
    
    def test_clean_text(self):
        """Test text cleaning."""
        result = self.op.clean_text(
            self.data[0], 
            remove_punctuation=True, 
            remove_numbers=True, 
            lowercase=True, 
            remove_extra_spaces=True
        )
        self.assertEqual(result, "hello world")
    
    def test_extract_pattern(self):
        """Test pattern extraction."""
        text = "Email: test@example.com, Phone: 123-456-7890"
        result = self.op.extract_pattern(text, pattern=r'Email: ([\w\.-]+@[\w\.-]+)')
        self.assertEqual(result, "Email: test@example.com")
        
        result = self.op.extract_pattern(text, pattern=r'Email: ([\w\.-]+@[\w\.-]+)', group=1)
        self.assertEqual(result, "test@example.com")
    
    def test_replace_pattern(self):
        """Test pattern replacement."""
        text = "Hello, World! 123"
        result = self.op.replace_pattern(text, pattern=r'\d+', replacement='NUM')
        self.assertEqual(result, "Hello, World! NUM")
    
    def test_tokenize(self):
        """Test tokenization."""
        result = self.op.tokenize(self.data[0])
        self.assertEqual(result, ["Hello,", "World!", "123"])
    
    def test_join_tokens(self):
        """Test token joining."""
        tokens = ["Hello", "World", "123"]
        result = self.op.join_tokens(tokens, separator='-')
        self.assertEqual(result, "Hello-World-123")


class TestDateTimeOperation(unittest.TestCase):
    """Test cases for the DateTimeOperation class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.op = DateTimeOperation()
        self.data = ["2023-01-01", "2023-02-15", "not-a-date"]
    
    def test_parse_date(self):
        """Test date parsing."""
        # Test with coerce errors
        result = self.op.parse_date(self.data, format='%Y-%m-%d', errors='coerce')
        self.assertIsInstance(result[0], datetime)
        self.assertEqual(result[0].year, 2023)
        self.assertEqual(result[0].month, 1)
        self.assertEqual(result[0].day, 1)
        self.assertIsNone(result[2])  # Invalid date should be None
        
        # Test with ignore errors
        result = self.op.parse_date(self.data, format='%Y-%m-%d', errors='ignore')
        self.assertIsInstance(result[0], datetime)
        self.assertEqual(result[2], "not-a-date")  # Invalid date should be unchanged
    
    def test_format_date(self):
        """Test date formatting."""
        dates = [datetime(2023, 1, 1), datetime(2023, 2, 15)]
        result = self.op.format_date(dates, format='%m/%d/%Y')
        self.assertEqual(result[0], "01/01/2023")
        self.assertEqual(result[1], "02/15/2023")
    
    def test_extract_component(self):
        """Test component extraction."""
        dates = [datetime(2023, 1, 1), datetime(2023, 2, 15)]
        
        # Test year extraction
        result = self.op.extract_component(dates, component='year')
        self.assertEqual(result[0], 2023)
        
        # Test month extraction
        result = self.op.extract_component(dates, component='month')
        self.assertEqual(result[0], 1)
        self.assertEqual(result[1], 2)
        
        # Test day extraction
        result = self.op.extract_component(dates, component='day')
        self.assertEqual(result[0], 1)
        self.assertEqual(result[1], 15)
    



if __name__ == '__main__':
    unittest.main()
