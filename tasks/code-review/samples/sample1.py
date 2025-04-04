"""
Credit Risk Scoring Model

This script implements a basic credit risk scoring model for loan applications.
It processes applicant data and calculates a risk score based on various factors.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import math

# Global variables
MIN_CREDIT_SCORE = 300
MAX_CREDIT_SCORE = 850
MIN_AGE = 18
MAX_DEBT_TO_INCOME = 0.43  # 43% is typically the maximum allowed DTI

def calculate_risk_score(applicant_data):
    """Calculate risk score for a loan applicant."""
    # Extract applicant information
    credit_score = applicant_data['credit_score']
    income = applicant_data['annual_income']
    loan_amount = applicant_data['loan_amount']
    employment_years = applicant_data['employment_years']
    age = applicant_data['age']
    existing_debt = applicant_data['existing_debt']
    
    # Check if applicant meets minimum requirements
    if credit_score < MIN_CREDIT_SCORE or age < MIN_AGE:
        return 0  # Automatic rejection
    
    # Calculate debt-to-income ratio
    dti_ratio = (existing_debt + loan_amount) / income if income > 0 else float('inf')
    if dti_ratio > MAX_DEBT_TO_INCOME:
        return 0  # Automatic rejection due to high DTI
    
    # Base score calculation
    base_score = 0
    
    # Credit score component (0-40 points)
    credit_factor = (credit_score - MIN_CREDIT_SCORE) / (MAX_CREDIT_SCORE - MIN_CREDIT_SCORE)
    base_score += credit_factor * 40
    
    # Income to loan ratio component (0-30 points)
    income_to_loan_ratio = income / loan_amount if loan_amount > 0 else float('inf')
    if income_to_loan_ratio >= 3:
        income_points = 30
    elif income_to_loan_ratio >= 2:
        income_points = 20
    elif income_to_loan_ratio >= 1:
        income_points = 10
    else:
        income_points = 0
    base_score += income_points
    
    # Employment history component (0-15 points)
    if employment_years >= 5:
        employment_points = 15
    elif employment_years >= 2:
        employment_points = 10
    elif employment_years >= 1:
        employment_points = 5
    else:
        employment_points = 0
    base_score += employment_points
    
    # DTI component (0-15 points)
    if dti_ratio <= 0.2:
        dti_points = 15
    elif dti_ratio <= 0.3:
        dti_points = 10
    elif dti_ratio <= 0.4:
        dti_points = 5
    else:
        dti_points = 0
    base_score += dti_points
    
    # Final score (0-100)
    final_score = min(100, math.floor(base_score))
    
    return final_score

def process_applicants(applicant_file):
    """Process all applicants in the given file."""
    try:
        # Load applicant data
        applicants_df = pd.read_csv(applicant_file)
        
        # Process each applicant
        results = []
        for i, applicant in applicants_df.iterrows():
            score = calculate_risk_score(applicant)
            
            # Determine risk category
            if score >= 80:
                risk_category = 'Low Risk'
                approved = True
            elif score >= 60:
                risk_category = 'Moderate Risk'
                approved = True
            elif score >= 40:
                risk_category = 'Medium Risk'
                approved = True
            elif score >= 20:
                risk_category = 'High Risk'
                approved = False
            else:
                risk_category = 'Very High Risk'
                approved = False
            
            # Add to results
            results.append({
                'applicant_id': applicant['applicant_id'],
                'risk_score': score,
                'risk_category': risk_category,
                'approved': approved
            })
        
        # Create results dataframe
        results_df = pd.DataFrame(results)
        
        # Save results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'risk_scores_{timestamp}.csv'
        results_df.to_csv(output_file, index=False)
        
        print(f'Processed {len(results)} applicants. Results saved to {output_file}')
        
        # Return approval rate
        approval_rate = sum(results_df['approved']) / len(results_df) * 100
        print(f'Approval rate: {approval_rate:.2f}%')
        
        return results_df
    
    except Exception as e:
        print(f'Error processing applicants: {str(e)}')
        return None

# Example usage
if __name__ == '__main__':
    # This would be replaced with actual file path
    applicant_file = 'loan_applicants.csv'
    results = process_applicants(applicant_file)
    
    # Print summary statistics
    if results is not None:
        print('\nSummary Statistics:')
        print(f'Average Risk Score: {results["risk_score"].mean():.2f}')
        print('\nRisk Category Distribution:')
        print(results['risk_category'].value_counts())
