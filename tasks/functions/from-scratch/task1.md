# Function Creation Task 1: From Scratch

## Task Description

Create a Python function that performs data binning (discretization) on a numeric column in a pandas DataFrame. This is a common preprocessing step in data science for converting continuous variables into categorical ones.

## Requirements

1. Create a function called `bin_numeric_data` that takes the following parameters:
   - `df`: A pandas DataFrame
   - `column`: The name of the numeric column to bin
   - `num_bins`: Number of bins to create (default: 5)
   - `labels`: Optional list of labels for the bins
   - `strategy`: Binning strategy ('equal-width' or 'equal-frequency', default: 'equal-width')

2. The function should:
   - Create bins according to the specified strategy
   - Add a new column to the DataFrame with the binned values
   - Return the modified DataFrame
   - Handle basic error cases

3. Include docstrings and comments to explain your code

## Example Usage

```python
import pandas as pd
import numpy as np

# Sample data
data = pd.DataFrame({
    'age': [22, 35, 46, 28, 32, 59, 41, 37, 25, 53],
    'income': [25000, 48000, 52000, 32000, 57000, 96000, 61000, 55000, 28000, 72000]
})

# Bin the 'age' column into 3 categories
result = bin_numeric_data(data, 'age', num_bins=3, labels=['Young', 'Middle-aged', 'Senior'])
print(result)
```

## Expected Output

The function should add a new column named `{original_column}_binned` with the binned values:

```
   age  income       age_binned
0   22   25000           Young
1   35   48000     Middle-aged
2   46   52000     Middle-aged
3   28   32000           Young
4   32   48000     Middle-aged
5   59   96000          Senior
6   41   61000     Middle-aged
7   37   55000     Middle-aged
8   25   28000           Young
9   53   72000          Senior
```

## Evaluation Criteria

Your solution will be evaluated based on:
1. Correctness of implementation
2. Code quality and organization
3. Error handling
4. Documentation quality

## Time Expectation

This task should take approximately 15-20 minutes to complete.
