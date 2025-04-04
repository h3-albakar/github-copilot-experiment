# Function Creation Task 1: Context-Based

## Task Description

Create a new function for the `DataCleaner` class that follows the existing code patterns. The class is used to clean and prepare financial data for analysis.

## Requirements

1. Add a new method called `remove_duplicates` to the `DataCleaner` class
2. The method should identify and remove duplicate rows based on specified columns
3. Follow the existing code patterns and style
4. Include appropriate error handling and logging

## Existing Code

```python
import pandas as pd
import numpy as np
import logging

class DataCleaner:
    """
    A class for cleaning and preparing financial data for analysis.
    Part of the RS Copilot library.
    """
    
    def __init__(self, log_level=logging.INFO):
        """
        Initialize the DataCleaner.
        
        Args:
            log_level: Logging level (default: INFO)
        """
        self.logger = self._setup_logger(log_level)
        self.logger.info("DataCleaner initialized")
        
    def _setup_logger(self, log_level):
        """Set up logger for the class."""
        logger = logging.getLogger("DataCleaner")
        logger.setLevel(log_level)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
        
    def remove_missing_values(self, df, columns=None, threshold=None):
        """
        Remove rows with missing values in specified columns.
        
        Args:
            df: Input DataFrame
            columns: List of columns to check for missing values (default: all columns)
            threshold: Minimum number of non-NA values to keep row (default: None)
            
        Returns:
            DataFrame with missing values removed
        """
        if df is None or df.empty:
            self.logger.warning("Empty DataFrame provided")
            return df
            
        self.logger.info(f"Removing missing values from DataFrame with shape {df.shape}")
        
        if columns is None:
            columns = df.columns
        else:
            # Validate columns
            invalid_cols = [col for col in columns if col not in df.columns]
            if invalid_cols:
                self.logger.warning(f"Columns not in DataFrame: {invalid_cols}")
                columns = [col for col in columns if col in df.columns]
                
        if not columns:
            self.logger.warning("No valid columns to process")
            return df
            
        # Remove rows with missing values
        if threshold is not None:
            result = df.dropna(subset=columns, thresh=threshold)
        else:
            result = df.dropna(subset=columns)
            
        removed = df.shape[0] - result.shape[0]
        self.logger.info(f"Removed {removed} rows with missing values")
        
        return result
        
    def remove_outliers(self, df, column, method='zscore', threshold=3.0):
        """
        Remove outliers from a specific column.
        
        Args:
            df: Input DataFrame
            column: Column to check for outliers
            method: Method to identify outliers ('zscore' or 'iqr')
            threshold: Threshold for outlier detection
            
        Returns:
            DataFrame with outliers removed
        """
        if df is None or df.empty:
            self.logger.warning("Empty DataFrame provided")
            return df
            
        if column not in df.columns:
            self.logger.warning(f"Column '{column}' not in DataFrame")
            return df
            
        self.logger.info(f"Removing outliers from column '{column}' using {method} method")
        
        result = df.copy()
        
        if method == 'zscore':
            # Z-score method
            z_scores = np.abs((result[column] - result[column].mean()) / result[column].std())
            result = result[z_scores <= threshold]
            
        elif method == 'iqr':
            # IQR method
            Q1 = result[column].quantile(0.25)
            Q3 = result[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            result = result[(result[column] >= lower_bound) & (result[column] <= upper_bound)]
            
        else:
            self.logger.warning(f"Unknown method '{method}', returning original DataFrame")
            return df
            
        removed = df.shape[0] - result.shape[0]
        self.logger.info(f"Removed {removed} outliers")
        
        return result
        
    def standardize_column_names(self, df):
        """
        Standardize column names to snake_case.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with standardized column names
        """
        if df is None or df.empty:
            self.logger.warning("Empty DataFrame provided")
            return df
            
        self.logger.info("Standardizing column names")
        
        # Convert to lowercase and replace spaces with underscores
        new_columns = {col: col.lower().replace(' ', '_') for col in df.columns}
        
        # Remove special characters
        for old_col, new_col in new_columns.items():
            new_columns[old_col] = ''.join(c if c.isalnum() or c == '_' else '_' for c in new_col)
            
        # Rename columns
        result = df.rename(columns=new_columns)
        
        self.logger.info(f"Renamed columns: {new_columns}")
        
        return result
    
    # TODO: Add a new method called remove_duplicates
    # The method should follow the existing patterns and style
```

## Expected Implementation

Your implementation should:

1. Follow the existing code patterns (parameter validation, logging, etc.)
2. Allow specifying which columns to consider when identifying duplicates
3. Have an option to keep the first or last occurrence of duplicates
4. Return the DataFrame with duplicates removed
5. Include appropriate logging messages

## Evaluation Criteria

Your solution will be evaluated based on:
1. Adherence to existing code patterns
2. Correctness of implementation
3. Error handling
4. Documentation quality

## Time Expectation

This task should take approximately 10-15 minutes to complete.
