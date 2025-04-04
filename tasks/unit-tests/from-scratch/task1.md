# Unit Testing Task 1: From Scratch

## Task Description

Create comprehensive unit tests for the `DataPreprocessor` class below. This class is used to preprocess financial data before it's used in machine learning models.

## Requirements

1. Write tests for all public methods in the `DataPreprocessor` class
2. Ensure tests cover both normal cases and edge cases
3. Follow best practices for unit testing
4. Use pytest as the testing framework
5. Aim for at least 90% code coverage

## Code to Test

```python
import pandas as pd
import numpy as np
from typing import List, Optional, Union, Dict

class DataPreprocessor:
    """
    A class for preprocessing financial data for machine learning models.
    """
    
    def __init__(self, missing_value_strategy: str = 'mean'):
        """
        Initialize the DataPreprocessor.
        
        Args:
            missing_value_strategy: Strategy for handling missing values.
                                   Options: 'mean', 'median', 'mode', 'drop'
        """
        self.missing_value_strategy = missing_value_strategy
        self.column_stats = {}
        
    def handle_missing_values(self, df: pd.DataFrame, columns: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Handle missing values in the dataframe based on the specified strategy.
        
        Args:
            df: Input dataframe
            columns: List of columns to process. If None, process all numeric columns.
            
        Returns:
            Processed dataframe with missing values handled
        """
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns.tolist()
            
        result_df = df.copy()
        
        for col in columns:
            if col not in result_df.columns:
                continue
                
            if result_df[col].isna().sum() == 0:
                continue
                
            if self.missing_value_strategy == 'mean':
                value = result_df[col].mean()
                self.column_stats[col] = {'mean': value}
                result_df[col].fillna(value, inplace=True)
            elif self.missing_value_strategy == 'median':
                value = result_df[col].median()
                self.column_stats[col] = {'median': value}
                result_df[col].fillna(value, inplace=True)
            elif self.missing_value_strategy == 'mode':
                value = result_df[col].mode()[0]
                self.column_stats[col] = {'mode': value}
                result_df[col].fillna(value, inplace=True)
            elif self.missing_value_strategy == 'drop':
                result_df.dropna(subset=[col], inplace=True)
            
        return result_df
    
    def remove_outliers(self, df: pd.DataFrame, columns: Optional[List[str]] = None, 
                        method: str = 'iqr', threshold: float = 1.5) -> pd.DataFrame:
        """
        Remove outliers from the dataframe.
        
        Args:
            df: Input dataframe
            columns: List of columns to process. If None, process all numeric columns.
            method: Method to identify outliers. Options: 'iqr', 'zscore'
            threshold: Threshold for outlier detection
            
        Returns:
            Dataframe with outliers removed
        """
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns.tolist()
            
        result_df = df.copy()
        
        for col in columns:
            if col not in result_df.columns:
                continue
                
            if method == 'iqr':
                Q1 = result_df[col].quantile(0.25)
                Q3 = result_df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                
                result_df = result_df[(result_df[col] >= lower_bound) & 
                                     (result_df[col] <= upper_bound)]
                
            elif method == 'zscore':
                mean = result_df[col].mean()
                std = result_df[col].std()
                z_scores = abs((result_df[col] - mean) / std)
                result_df = result_df[z_scores <= threshold]
                
        return result_df
    
    def normalize_data(self, df: pd.DataFrame, columns: Optional[List[str]] = None, 
                      method: str = 'minmax') -> pd.DataFrame:
        """
        Normalize data in the dataframe.
        
        Args:
            df: Input dataframe
            columns: List of columns to process. If None, process all numeric columns.
            method: Normalization method. Options: 'minmax', 'zscore'
            
        Returns:
            Dataframe with normalized data
        """
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns.tolist()
            
        result_df = df.copy()
        
        for col in columns:
            if col not in result_df.columns:
                continue
                
            if method == 'minmax':
                min_val = result_df[col].min()
                max_val = result_df[col].max()
                self.column_stats[col] = {'min': min_val, 'max': max_val}
                
                if max_val > min_val:
                    result_df[col] = (result_df[col] - min_val) / (max_val - min_val)
                
            elif method == 'zscore':
                mean = result_df[col].mean()
                std = result_df[col].std()
                self.column_stats[col] = {'mean': mean, 'std': std}
                
                if std > 0:
                    result_df[col] = (result_df[col] - mean) / std
                
        return result_df
    
    def get_column_stats(self) -> Dict:
        """
        Get statistics collected during preprocessing.
        
        Returns:
            Dictionary of column statistics
        """
        return self.column_stats
```

## Expected Deliverable

Create a file named `test_data_preprocessor.py` with comprehensive unit tests for the `DataPreprocessor` class.

## Evaluation Criteria

Your solution will be evaluated based on:
1. Test coverage (aim for at least 90%)
2. Test quality and organization
3. Edge case handling
4. Adherence to testing best practices

## Time Expectation

This task should take approximately 20-30 minutes to complete.
