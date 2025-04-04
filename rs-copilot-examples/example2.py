"""
Example of code optimized using RS Copilot prompts.

This file shows how the long, complex function from example1.py could be
refactored and optimized using RS Copilot prompts for better modularity,
readability, and maintainability.

RS Copilot prompts used:
1. Long function optimization prompt - to identify logical sections
2. Modularized optimization prompt - to extract functions with clear responsibilities
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score

# Main function broken down into smaller, focused functions with clear responsibilities
def process_and_analyze_financial_data(
    file_path, 
    target_column='default', 
    test_size=0.2, 
    random_state=42
):
    """
    Process financial data, train a model, and analyze results.
    
    This function orchestrates the entire workflow by calling specialized
    functions for each step of the process.
    """
    # Load and prepare data
    df = load_data(file_path)
    if df is None:
        return None
    
    # Check if target column exists
    if target_column not in df.columns:
        print(f"Target column '{target_column}' not found in data")
        return None
    
    # Separate features and target
    y = df[target_column]
    X = df.drop(target_column, axis=1)
    
    # Identify column types
    column_types = identify_column_types(X)
    
    # Preprocess data
    X = preprocess_data(X, column_types)
    
    # Split data
    data_splits = split_data(X, y, test_size, random_state)
    
    # Train model
    model = train_model(data_splits['X_train'], data_splits['y_train'], random_state)
    
    # Evaluate model
    metrics = evaluate_model(model, data_splits)
    
    # Calculate feature importance
    feature_importance = calculate_feature_importance(model, X.columns)
    
    # Return results
    return {
        'data': data_splits,
        'model': model,
        'metrics': metrics,
        'feature_importance': feature_importance
    }

def load_data(file_path):
    """Load data from a CSV file."""
    print(f"Loading data from {file_path}...")
    try:
        df = pd.read_csv(file_path)
        print(f"Loaded data with shape: {df.shape}")
        return df
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        return None

def identify_column_types(df):
    """Identify column types in the DataFrame."""
    # Auto-detect column types
    categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    date_columns = []
    for col in df.columns:
        if 'date' in col.lower() or 'time' in col.lower():
            try:
                pd.to_datetime(df[col])
                date_columns.append(col)
            except:
                pass
    
    numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
    numeric_columns = [col for col in numeric_columns if col not in categorical_columns and col not in date_columns]
    
    print(f"Detected {len(categorical_columns)} categorical columns, {len(numeric_columns)} numeric columns, and {len(date_columns)} date columns")
    
    return {
        'categorical': categorical_columns,
        'numeric': numeric_columns,
        'date': date_columns
    }

def preprocess_data(df, column_types):
    """Preprocess the data by handling missing values, outliers, and encoding."""
    result = df.copy()
    
    # Handle missing values
    result = handle_missing_values(result, column_types)
    
    # Process date columns
    if column_types['date']:
        result = process_date_columns(result, column_types['date'])
    
    # Handle outliers
    result = handle_outliers(result, column_types['numeric'])
    
    # Encode categorical variables
    if column_types['categorical']:
        result = encode_categorical(result, column_types['categorical'])
    
    # Normalize numeric features
    result = normalize_features(result, column_types['numeric'])
    
    return result

def handle_missing_values(df, column_types):
    """Handle missing values in the DataFrame."""
    print("Handling missing values...")
    result = df.copy()
    
    # For numeric columns, fill with median
    for col in column_types['numeric']:
        if result[col].isna().sum() > 0:
            median_value = result[col].median()
            result[col].fillna(median_value, inplace=True)
    
    # For categorical columns, fill with mode
    for col in column_types['categorical']:
        if result[col].isna().sum() > 0:
            mode_value = result[col].mode()[0]
            result[col].fillna(mode_value, inplace=True)
    
    return result

def process_date_columns(df, date_columns):
    """Process date columns to extract useful features."""
    print("Processing date columns...")
    result = df.copy()
    
    for col in date_columns:
        # Convert to datetime
        result[col] = pd.to_datetime(result[col], errors='coerce')
        
        # Extract date components
        result[f'{col}_year'] = result[col].dt.year
        result[f'{col}_month'] = result[col].dt.month
        result[f'{col}_day'] = result[col].dt.day
        
        # Drop original column
        result.drop(col, axis=1, inplace=True)
    
    return result

def handle_outliers(df, numeric_columns):
    """Handle outliers in numeric columns."""
    print("Handling outliers...")
    result = df.copy()
    
    for col in numeric_columns:
        # Calculate IQR
        Q1 = result[col].quantile(0.25)
        Q3 = result[col].quantile(0.75)
        IQR = Q3 - Q1
        
        # Define bounds
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # Cap outliers instead of removing
        result[col] = result[col].clip(lower=lower_bound, upper=upper_bound)
    
    return result

def encode_categorical(df, categorical_columns):
    """Encode categorical variables."""
    print("Encoding categorical variables...")
    result = df.copy()
    
    for col in categorical_columns:
        # One-hot encode
        dummies = pd.get_dummies(result[col], prefix=col, drop_first=False)
        result = pd.concat([result, dummies], axis=1)
        result.drop(col, axis=1, inplace=True)
    
    return result

def normalize_features(df, numeric_columns):
    """Normalize numeric features."""
    print("Normalizing numeric features...")
    result = df.copy()
    
    scaler = StandardScaler()
    result[numeric_columns] = scaler.fit_transform(result[numeric_columns])
    
    return result

def split_data(X, y, test_size=0.2, random_state=42):
    """Split data into train and test sets."""
    print(f"Splitting data with test_size={test_size}...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    return {
        'X_train': X_train,
        'X_test': X_test,
        'y_train': y_train,
        'y_test': y_test
    }

def train_model(X_train, y_train, random_state=42):
    """Train a Random Forest model."""
    print("Training Random Forest model...")
    model = RandomForestClassifier(
        n_estimators=100,
        class_weight='balanced',
        random_state=random_state
    )
    model.fit(X_train, y_train)
    
    return model

def evaluate_model(model, data_splits):
    """Evaluate model performance."""
    print("Calculating performance metrics...")
    X_train = data_splits['X_train']
    y_train = data_splits['y_train']
    X_test = data_splits['X_test']
    y_test = data_splits['y_test']
    
    # Make predictions
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    
    y_train_prob = model.predict_proba(X_train)[:, 1]
    y_test_prob = model.predict_proba(X_test)[:, 1]
    
    # Calculate metrics
    metrics = {
        'train_accuracy': accuracy_score(y_train, y_train_pred),
        'test_accuracy': accuracy_score(y_test, y_test_pred),
        'train_auc': roc_auc_score(y_train, y_train_prob),
        'test_auc': roc_auc_score(y_test, y_test_prob)
    }
    
    # Print metrics
    print("\nModel Performance Metrics:")
    print(f"Train Accuracy: {metrics['train_accuracy']:.4f}")
    print(f"Test Accuracy: {metrics['test_accuracy']:.4f}")
    print(f"Train AUC: {metrics['train_auc']:.4f}")
    print(f"Test AUC: {metrics['test_auc']:.4f}")
    
    return metrics

def calculate_feature_importance(model, feature_names):
    """Calculate feature importance."""
    print("Calculating feature importance...")
    feature_importance = dict(zip(feature_names, model.feature_importances_))
    feature_importance = dict(sorted(
        feature_importance.items(),
        key=lambda item: item[1],
        reverse=True
    ))
    
    return feature_importance

# Example usage
if __name__ == "__main__":
    # This would be replaced with actual file path
    file_path = 'financial_data.csv'
    results = process_and_analyze_financial_data(file_path)
    
    if results:
        print("\nTop 5 most important features:")
        for i, (feature, importance) in enumerate(list(results['feature_importance'].items())[:5]):
            print(f"{i+1}. {feature}: {importance:.4f}")
