"""
Example of code that could benefit from RS Copilot optimization prompts.

This file contains a long, complex function that handles multiple responsibilities
and would be a good candidate for optimization using RS Copilot prompts.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix

def process_and_analyze_financial_data(file_path, target_column='default', test_size=0.2, random_state=42, handle_missing=True, remove_outliers=True, normalize=True, categorical_columns=None, date_columns=None):
    """
    Process financial data, train a model, and analyze results.
    
    This function loads financial data, preprocesses it, trains a model,
    evaluates performance, and generates visualizations.
    
    Args:
        file_path: Path to the CSV file containing financial data
        target_column: Name of the target column (default: 'default')
        test_size: Proportion of data to use for testing (default: 0.2)
        random_state: Random seed for reproducibility (default: 42)
        handle_missing: Whether to handle missing values (default: True)
        remove_outliers: Whether to remove outliers (default: True)
        normalize: Whether to normalize numeric features (default: True)
        categorical_columns: List of categorical columns (default: None, auto-detect)
        date_columns: List of date columns (default: None, auto-detect)
        
    Returns:
        Dictionary containing processed data, model, and evaluation results
    """
    # Load data
    print(f"Loading data from {file_path}...")
    try:
        df = pd.read_csv(file_path)
        print(f"Loaded data with shape: {df.shape}")
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        return None
    
    # Check if target column exists
    if target_column not in df.columns:
        print(f"Target column '{target_column}' not found in data")
        return None
    
    # Separate features and target
    y = df[target_column]
    X = df.drop(target_column, axis=1)
    
    # Auto-detect column types if not specified
    if categorical_columns is None:
        categorical_columns = X.select_dtypes(include=['object', 'category']).columns.tolist()
    
    if date_columns is None:
        date_columns = []
        for col in X.columns:
            if 'date' in col.lower() or 'time' in col.lower():
                try:
                    pd.to_datetime(X[col])
                    date_columns.append(col)
                except:
                    pass
    
    numeric_columns = X.select_dtypes(include=['number']).columns.tolist()
    numeric_columns = [col for col in numeric_columns if col not in categorical_columns and col not in date_columns]
    
    print(f"Detected {len(categorical_columns)} categorical columns, {len(numeric_columns)} numeric columns, and {len(date_columns)} date columns")
    
    # Handle missing values
    if handle_missing:
        print("Handling missing values...")
        # For numeric columns, fill with median
        for col in numeric_columns:
            if X[col].isna().sum() > 0:
                median_value = X[col].median()
                X[col].fillna(median_value, inplace=True)
        
        # For categorical columns, fill with mode
        for col in categorical_columns:
            if X[col].isna().sum() > 0:
                mode_value = X[col].mode()[0]
                X[col].fillna(mode_value, inplace=True)
    
    # Process date columns
    print("Processing date columns...")
    for col in date_columns:
        # Convert to datetime
        X[col] = pd.to_datetime(X[col], errors='coerce')
        
        # Extract date components
        X[f'{col}_year'] = X[col].dt.year
        X[f'{col}_month'] = X[col].dt.month
        X[f'{col}_day'] = X[col].dt.day
        X[f'{col}_dayofweek'] = X[col].dt.dayofweek
        
        # Drop original column
        X.drop(col, axis=1, inplace=True)
    
    # Handle outliers in numeric columns
    if remove_outliers:
        print("Handling outliers...")
        for col in numeric_columns:
            # Calculate IQR
            Q1 = X[col].quantile(0.25)
            Q3 = X[col].quantile(0.75)
            IQR = Q3 - Q1
            
            # Define bounds
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            # Cap outliers instead of removing
            X[col] = X[col].clip(lower=lower_bound, upper=upper_bound)
    
    # Encode categorical variables
    print("Encoding categorical variables...")
    for col in categorical_columns:
        # One-hot encode
        dummies = pd.get_dummies(X[col], prefix=col, drop_first=False)
        X = pd.concat([X, dummies], axis=1)
        X.drop(col, axis=1, inplace=True)
    
    # Normalize numeric features
    if normalize:
        print("Normalizing numeric features...")
        scaler = StandardScaler()
        X[numeric_columns] = scaler.fit_transform(X[numeric_columns])
    
    # Split data into train and test sets
    print(f"Splitting data with test_size={test_size}...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    # Train model
    print("Training Random Forest model...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        class_weight='balanced',
        random_state=random_state
    )
    model.fit(X_train, y_train)
    
    # Make predictions
    print("Making predictions...")
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    
    y_train_prob = model.predict_proba(X_train)[:, 1]
    y_test_prob = model.predict_proba(X_test)[:, 1]
    
    # Calculate metrics
    print("Calculating performance metrics...")
    metrics = {
        'train_accuracy': accuracy_score(y_train, y_train_pred),
        'test_accuracy': accuracy_score(y_test, y_test_pred),
        'train_precision': precision_score(y_train, y_train_pred),
        'test_precision': precision_score(y_test, y_test_pred),
        'train_recall': recall_score(y_train, y_train_pred),
        'test_recall': recall_score(y_test, y_test_pred),
        'train_f1': f1_score(y_train, y_train_pred),
        'test_f1': f1_score(y_test, y_test_pred),
        'train_auc': roc_auc_score(y_train, y_train_prob),
        'test_auc': roc_auc_score(y_test, y_test_prob)
    }
    
    # Print metrics
    print("\nModel Performance Metrics:")
    print(f"Train Accuracy: {metrics['train_accuracy']:.4f}")
    print(f"Test Accuracy: {metrics['test_accuracy']:.4f}")
    print(f"Train AUC: {metrics['train_auc']:.4f}")
    print(f"Test AUC: {metrics['test_auc']:.4f}")
    
    # Calculate feature importance
    print("Calculating feature importance...")
    feature_importance = dict(zip(X.columns, model.feature_importances_))
    feature_importance = dict(sorted(
        feature_importance.items(),
        key=lambda item: item[1],
        reverse=True
    ))
    
    # Plot feature importance
    print("Generating feature importance plot...")
    top_features = dict(list(feature_importance.items())[:10])
    plt.figure(figsize=(10, 6))
    plt.barh(list(top_features.keys()), list(top_features.values()), color='skyblue')
    plt.xlabel('Importance')
    plt.title('Top 10 Feature Importance')
    plt.tight_layout()
    
    # Save plot
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    plt.savefig(f'feature_importance_{timestamp}.png')
    
    # Plot confusion matrix
    print("Generating confusion matrix plot...")
    cm = confusion_matrix(y_test, y_test_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix')
    plt.tight_layout()
    
    # Save plot
    plt.savefig(f'confusion_matrix_{timestamp}.png')
    
    # Return results
    return {
        'data': {
            'X_train': X_train,
            'X_test': X_test,
            'y_train': y_train,
            'y_test': y_test
        },
        'model': model,
        'metrics': metrics,
        'feature_importance': feature_importance
    }

# Example usage
if __name__ == "__main__":
    # This would be replaced with actual file path
    file_path = 'financial_data.csv'
    results = process_and_analyze_financial_data(file_path)
    
    if results:
        print("\nTop 5 most important features:")
        for i, (feature, importance) in enumerate(list(results['feature_importance'].items())[:5]):
            print(f"{i+1}. {feature}: {importance:.4f}")
