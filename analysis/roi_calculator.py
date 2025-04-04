"""
ROI Calculator for GitHub Copilot Experiment

This script calculates the return on investment for GitHub Copilot licenses
based on the experiment results.
"""

import os
import json
import pandas as pd
import numpy as np
from datetime import datetime

def calculate_roi(
    time_savings_minutes_per_task,
    tasks_per_week,
    hourly_cost,
    license_cost,
    working_weeks_per_year=48,
    num_graduates=None
):
    """
    Calculate ROI for GitHub Copilot licenses.
    
    Args:
        time_savings_minutes_per_task: Average time savings per task in minutes
        tasks_per_week: Average number of tasks per week per graduate
        hourly_cost: Hourly cost of a graduate (in £)
        license_cost: Annual cost of GitHub Copilot license per user (in £)
        working_weeks_per_year: Number of working weeks per year (default: 48)
        num_graduates: Number of graduates to calculate total ROI for (default: None)
        
    Returns:
        Dictionary with ROI metrics
    """
    # Calculate time savings
    time_savings_hours_per_task = time_savings_minutes_per_task / 60
    weekly_time_savings = time_savings_hours_per_task * tasks_per_week
    annual_time_savings = weekly_time_savings * working_weeks_per_year
    
    # Calculate cost savings
    annual_cost_savings = annual_time_savings * hourly_cost
    
    # Calculate ROI
    roi_percent = ((annual_cost_savings - license_cost) / license_cost) * 100
    
    # Calculate payback period in months
    payback_period_months = (license_cost / annual_cost_savings) * 12
    
    # Calculate total ROI if number of graduates is provided
    total_metrics = None
    if num_graduates is not None:
        total_annual_time_savings = annual_time_savings * num_graduates
        total_annual_cost_savings = annual_cost_savings * num_graduates
        total_license_cost = license_cost * num_graduates
        total_roi_percent = ((total_annual_cost_savings - total_license_cost) / total_license_cost) * 100
        
        total_metrics = {
            'num_graduates': num_graduates,
            'total_annual_time_savings_hours': total_annual_time_savings,
            'total_annual_cost_savings': total_annual_cost_savings,
            'total_license_cost': total_license_cost,
            'total_roi_percent': total_roi_percent
        }
    
    # Return metrics
    return {
        'inputs': {
            'time_savings_minutes_per_task': time_savings_minutes_per_task,
            'tasks_per_week': tasks_per_week,
            'hourly_cost': hourly_cost,
            'license_cost': license_cost,
            'working_weeks_per_year': working_weeks_per_year
        },
        'per_graduate': {
            'weekly_time_savings_hours': weekly_time_savings,
            'annual_time_savings_hours': annual_time_savings,
            'annual_cost_savings': annual_cost_savings,
            'roi_percent': roi_percent,
            'payback_period_months': payback_period_months
        },
        'total': total_metrics
    }

def load_experiment_data(summary_file):
    """
    Load experiment data from analysis summary file.
    
    Args:
        summary_file: Path to analysis summary JSON file
        
    Returns:
        Dictionary with experiment data for ROI calculation
    """
    try:
        with open(summary_file, 'r') as f:
            summary = json.load(f)
        
        # Extract relevant metrics
        time_savings = summary['time_savings']['average_minutes_per_task']
        
        # Estimate tasks per week based on average task time
        # Assuming 40-hour work week and using Edge Copilot time as baseline
        edge_time_minutes = 0
        for category in summary['time_savings']['by_category']['Edge Copilot']:
            edge_time_minutes += summary['time_savings']['by_category']['Edge Copilot'][category]
        edge_time_minutes /= len(summary['time_savings']['by_category']['Edge Copilot'])
        
        tasks_per_week = (40 * 60) / edge_time_minutes
        
        return {
            'time_savings_minutes_per_task': time_savings,
            'tasks_per_week': tasks_per_week
        }
    except Exception as e:
        print(f"Error loading experiment data: {str(e)}")
        return None

def generate_roi_report(roi_metrics, output_file):
    """
    Generate a detailed ROI report.
    
    Args:
        roi_metrics: Dictionary with ROI metrics
        output_file: Path to save the report
    """
    # Create report
    report = {
        'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'roi_metrics': roi_metrics,
        'summary': {
            'per_graduate': {
                'annual_time_savings_hours': roi_metrics['per_graduate']['annual_time_savings_hours'],
                'annual_cost_savings': roi_metrics['per_graduate']['annual_cost_savings'],
                'roi_percent': roi_metrics['per_graduate']['roi_percent'],
                'payback_period_months': roi_metrics['per_graduate']['payback_period_months']
            }
        }
    }
    
    # Add total metrics if available
    if roi_metrics['total'] is not None:
        report['summary']['total'] = {
            'num_graduates': roi_metrics['total']['num_graduates'],
            'total_annual_time_savings_hours': roi_metrics['total']['total_annual_time_savings_hours'],
            'total_annual_cost_savings': roi_metrics['total']['total_annual_cost_savings'],
            'total_roi_percent': roi_metrics['total']['total_roi_percent']
        }
    
    # Save report
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"ROI report saved to {output_file}")
    
    # Print summary
    print("\nROI Summary:")
    print(f"Annual Time Savings per Graduate: {roi_metrics['per_graduate']['annual_time_savings_hours']:.1f} hours")
    print(f"Annual Cost Savings per Graduate: £{roi_metrics['per_graduate']['annual_cost_savings']:.2f}")
    print(f"ROI: {roi_metrics['per_graduate']['roi_percent']:.1f}%")
    print(f"Payback Period: {roi_metrics['per_graduate']['payback_period_months']:.1f} months")
    
    if roi_metrics['total'] is not None:
        print(f"\nTotal for {roi_metrics['total']['num_graduates']} Graduates:")
        print(f"Total Annual Time Savings: {roi_metrics['total']['total_annual_time_savings_hours']:.1f} hours")
        print(f"Total Annual Cost Savings: £{roi_metrics['total']['total_annual_cost_savings']:.2f}")
        print(f"Total ROI: {roi_metrics['total']['total_roi_percent']:.1f}%")

def main():
    """Main function to run the ROI calculator."""
    # Set paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    summary_file = os.path.join(base_dir, 'analysis', 'results', 'analysis_summary.json')
    output_file = os.path.join(base_dir, 'analysis', 'results', 'roi_report.json')
    
    # Default values
    hourly_cost = 25  # £25 per hour for a graduate
    license_cost = 100  # £100 per year for GitHub Copilot license
    num_graduates = 8  # Number of graduates in the experiment
    
    # Check if summary file exists
    if os.path.exists(summary_file):
        # Load experiment data
        experiment_data = load_experiment_data(summary_file)
        
        if experiment_data is not None:
            # Calculate ROI using experiment data
            roi_metrics = calculate_roi(
                time_savings_minutes_per_task=experiment_data['time_savings_minutes_per_task'],
                tasks_per_week=experiment_data['tasks_per_week'],
                hourly_cost=hourly_cost,
                license_cost=license_cost,
                num_graduates=num_graduates
            )
        else:
            print("Using default values for ROI calculation")
            # Use default values
            roi_metrics = calculate_roi(
                time_savings_minutes_per_task=10,  # Assume 10 minutes saved per task
                tasks_per_week=20,  # Assume 20 tasks per week
                hourly_cost=hourly_cost,
                license_cost=license_cost,
                num_graduates=num_graduates
            )
    else:
        print(f"Summary file {summary_file} not found. Using default values.")
        # Use default values
        roi_metrics = calculate_roi(
            time_savings_minutes_per_task=10,  # Assume 10 minutes saved per task
            tasks_per_week=20,  # Assume 20 tasks per week
            hourly_cost=hourly_cost,
            license_cost=license_cost,
            num_graduates=num_graduates
        )
    
    # Generate ROI report
    generate_roi_report(roi_metrics, output_file)

if __name__ == "__main__":
    main()
