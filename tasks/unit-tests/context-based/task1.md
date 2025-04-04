# Unit Testing Task 1: Context-Based

## Task Description

Complete the unit tests for the `SimpleStats` class by following the existing test patterns. This class provides basic statistical functions for financial data analysis.

## Requirements

1. Complete the missing test methods in the provided test file
2. Follow the existing testing patterns
3. Keep tests simple and focused

## Existing Code

### SimpleStats Class

```python
import numpy as np

class SimpleStats:
    """
    A class for basic statistical calculations on financial data.
    """
    
    @staticmethod
    def mean(data):
        """
        Calculate the mean of a list of numbers.
        
        Args:
            data: List or array of numbers
            
        Returns:
            Mean value
        """
        return sum(data) / len(data)
    
    @staticmethod
    def median(data):
        """
        Calculate the median of a list of numbers.
        
        Args:
            data: List or array of numbers
            
        Returns:
            Median value
        """
        sorted_data = sorted(data)
        n = len(sorted_data)
        
        if n % 2 == 0:
            # Even number of elements
            return (sorted_data[n//2 - 1] + sorted_data[n//2]) / 2
        else:
            # Odd number of elements
            return sorted_data[n//2]
    
    @staticmethod
    def variance(data):
        """
        Calculate the variance of a list of numbers.
        
        Args:
            data: List or array of numbers
            
        Returns:
            Variance value
        """
        mean = SimpleStats.mean(data)
        return sum((x - mean) ** 2 for x in data) / len(data)
    
    @staticmethod
    def std_dev(data):
        """
        Calculate the standard deviation of a list of numbers.
        
        Args:
            data: List or array of numbers
            
        Returns:
            Standard deviation value
        """
        return np.sqrt(SimpleStats.variance(data))
    
    @staticmethod
    def percentile(data, p):
        """
        Calculate the pth percentile of a list of numbers.
        
        Args:
            data: List or array of numbers
            p: Percentile (0-100)
            
        Returns:
            Percentile value
        """
        if p < 0 or p > 100:
            raise ValueError("Percentile must be between 0 and 100")
            
        sorted_data = sorted(data)
        n = len(sorted_data)
        
        if p == 0:
            return sorted_data[0]
        if p == 100:
            return sorted_data[-1]
            
        # Calculate the index
        idx = (n - 1) * (p / 100)
        idx_floor = int(np.floor(idx))
        idx_ceil = int(np.ceil(idx))
        
        if idx_floor == idx_ceil:
            return sorted_data[idx_floor]
            
        # Interpolate
        lower_value = sorted_data[idx_floor]
        upper_value = sorted_data[idx_ceil]
        fraction = idx - idx_floor
        
        return lower_value + fraction * (upper_value - lower_value)
```

### Existing Test File (Incomplete)

```python
import pytest
from simple_stats import SimpleStats

class TestSimpleStats:
    """Test suite for SimpleStats class."""
    
    def test_mean(self):
        """Test mean calculation."""
        # Test with integers
        assert SimpleStats.mean([1, 2, 3, 4, 5]) == 3
        
        # Test with floats
        assert SimpleStats.mean([1.5, 2.5, 3.5]) == 2.5
        
        # Test with negative numbers
        assert SimpleStats.mean([-10, -5, 0, 5, 10]) == 0
    
    def test_median(self):
        """Test median calculation."""
        # Test with odd number of elements
        assert SimpleStats.median([1, 3, 2, 5, 4]) == 3
        
        # Test with even number of elements
        assert SimpleStats.median([1, 2, 3, 4]) == 2.5
    
    # TODO: Complete the following test methods
    
    def test_variance(self):
        """Test variance calculation."""
        # Your implementation here
    
    def test_std_dev(self):
        """Test standard deviation calculation."""
        # Your implementation here
    
    def test_percentile(self):
        """Test percentile calculation."""
        # Your implementation here
    
    def test_edge_cases(self):
        """Test edge cases (empty list, single element, etc.)."""
        # Your implementation here
```

## Expected Deliverable

Complete the implementation of the missing test methods in the test file. Your implementation should follow the existing testing patterns.

## Evaluation Criteria

Your solution will be evaluated based on:
1. Correctness of test implementations
2. Test coverage of different scenarios
3. Adherence to existing testing patterns

## Time Expectation

This task should take approximately 10-15 minutes to complete.
