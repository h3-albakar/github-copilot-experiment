# Documentation Task 1: From Scratch

## Task Description

Create comprehensive documentation for the `FeatureSelector` class provided below. This class is used to select the most important features for machine learning models in financial applications.

## Requirements

1. Create a README.md file that explains:
   - The purpose of the `FeatureSelector` class
   - How to use the class (with examples)
   - Description of each method and its parameters
   - Explanation of the feature selection techniques implemented

2. Your documentation should be:
   - Clear and concise
   - Well-structured with appropriate headings
   - Suitable for data scientists who may not be familiar with all feature selection techniques
   - Include code examples showing how to use each method

## Code to Document

```python
import pandas as pd
import numpy as np
from sklearn.feature_selection import SelectKBest, f_regression, mutual_info_regression
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Lasso

class FeatureSelector:
    """
    A class for selecting the most important features for machine learning models.
    """
    
    def __init__(self):
        """Initialize the FeatureSelector."""
        self.selected_features = {}
        self.feature_importances = {}
    
    def select_by_correlation(self, X, y, threshold=0.05):
        """
        Select features based on correlation with target variable.
        
        Args:
            X: Feature DataFrame
            y: Target variable
            threshold: Minimum absolute correlation to include a feature
            
        Returns:
            List of selected feature names
        """
        # Calculate correlation with target
        correlation = pd.DataFrame()
        correlation['feature'] = X.columns
        correlation['correlation'] = [abs(np.corrcoef(X[col], y)[0, 1]) for col in X.columns]
        
        # Select features above threshold
        selected = correlation[correlation['correlation'] > threshold]['feature'].tolist()
        
        # Store results
        self.selected_features['correlation'] = selected
        self.feature_importances['correlation'] = dict(zip(
            correlation['feature'], correlation['correlation']
        ))
        
        return selected
    
    def select_by_mutual_information(self, X, y, k=10):
        """
        Select features based on mutual information with target variable.
        
        Args:
            X: Feature DataFrame
            y: Target variable
            k: Number of top features to select
            
        Returns:
            List of selected feature names
        """
        # Apply mutual information
        selector = SelectKBest(mutual_info_regression, k=min(k, X.shape[1]))
        selector.fit(X, y)
        
        # Get selected features
        feature_scores = pd.DataFrame()
        feature_scores['feature'] = X.columns
        feature_scores['score'] = selector.scores_
        
        # Sort by score and select top k
        feature_scores = feature_scores.sort_values('score', ascending=False)
        selected = feature_scores.head(k)['feature'].tolist()
        
        # Store results
        self.selected_features['mutual_information'] = selected
        self.feature_importances['mutual_information'] = dict(zip(
            feature_scores['feature'], feature_scores['score']
        ))
        
        return selected
    
    def select_by_random_forest(self, X, y, k=10):
        """
        Select features based on Random Forest feature importance.
        
        Args:
            X: Feature DataFrame
            y: Target variable
            k: Number of top features to select
            
        Returns:
            List of selected feature names
        """
        # Train Random Forest
        rf = RandomForestRegressor(n_estimators=100, random_state=42)
        rf.fit(X, y)
        
        # Get feature importances
        feature_importances = pd.DataFrame()
        feature_importances['feature'] = X.columns
        feature_importances['importance'] = rf.feature_importances_
        
        # Sort by importance and select top k
        feature_importances = feature_importances.sort_values('importance', ascending=False)
        selected = feature_importances.head(k)['feature'].tolist()
        
        # Store results
        self.selected_features['random_forest'] = selected
        self.feature_importances['random_forest'] = dict(zip(
            feature_importances['feature'], feature_importances['importance']
        ))
        
        return selected
    
    def select_by_lasso(self, X, y, alpha=0.1):
        """
        Select features based on Lasso regularization.
        
        Args:
            X: Feature DataFrame
            y: Target variable
            alpha: Regularization strength
            
        Returns:
            List of selected feature names
        """
        # Train Lasso model
        lasso = Lasso(alpha=alpha, random_state=42)
        lasso.fit(X, y)
        
        # Get feature coefficients
        feature_coefficients = pd.DataFrame()
        feature_coefficients['feature'] = X.columns
        feature_coefficients['coefficient'] = np.abs(lasso.coef_)
        
        # Select features with non-zero coefficients
        selected = feature_coefficients[feature_coefficients['coefficient'] > 0]['feature'].tolist()
        
        # Store results
        self.selected_features['lasso'] = selected
        self.feature_importances['lasso'] = dict(zip(
            feature_coefficients['feature'], feature_coefficients['coefficient']
        ))
        
        return selected
    
    def get_common_features(self, methods=None, min_methods=2):
        """
        Get features that are selected by multiple methods.
        
        Args:
            methods: List of methods to consider (default: all methods)
            min_methods: Minimum number of methods that must select a feature
            
        Returns:
            List of common feature names
        """
        if not self.selected_features:
            raise ValueError("No feature selection methods have been applied yet")
            
        if methods is None:
            methods = list(self.selected_features.keys())
        else:
            # Validate methods
            for method in methods:
                if method not in self.selected_features:
                    raise ValueError(f"Method '{method}' has not been applied yet")
        
        # Count occurrences of each feature
        all_features = []
        for method in methods:
            all_features.extend(self.selected_features[method])
            
        feature_counts = pd.Series(all_features).value_counts()
        
        # Select features that appear in at least min_methods
        common_features = feature_counts[feature_counts >= min_methods].index.tolist()
        
        return common_features
    
    def plot_feature_importances(self, method, top_n=10):
        """
        Plot feature importances for a specific method.
        
        Args:
            method: Feature selection method
            top_n: Number of top features to plot
            
        Returns:
            matplotlib figure
        """
        import matplotlib.pyplot as plt
        
        if method not in self.feature_importances:
            raise ValueError(f"Method '{method}' has not been applied yet")
            
        # Get feature importances
        importances = self.feature_importances[method]
        
        # Sort and select top N
        sorted_importances = dict(sorted(
            importances.items(), 
            key=lambda item: item[1], 
            reverse=True
        )[:top_n])
        
        # Create plot
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(list(sorted_importances.keys()), list(sorted_importances.values()))
        ax.set_xlabel('Importance')
        ax.set_ylabel('Feature')
        ax.set_title(f'Top {top_n} Features by {method.capitalize()}')
        
        return fig
```

## Expected Deliverable

Create a file named `README.md` with comprehensive documentation for the `FeatureSelector` class.

## Evaluation Criteria

Your documentation will be evaluated based on:
1. Clarity and completeness
2. Structure and organization
3. Quality of examples
4. Technical accuracy

## Time Expectation

This task should take approximately 15-20 minutes to complete.
