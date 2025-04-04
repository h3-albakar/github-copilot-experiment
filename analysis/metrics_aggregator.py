"""
Metrics Aggregator for GitHub Copilot Experiment

This script aggregates metrics from the experiment submissions and generates
visualizations for the final report.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yaml
import json
from datetime import datetime

def load_metrics(metrics_dir):
    """
    Load metrics from YAML files in the specified directory.
    
    Args:
        metrics_dir: Directory containing metrics files
        
    Returns:
        DataFrame with aggregated metrics
    """
    print(f"Loading metrics from {metrics_dir}...")
    
    all_metrics = []
    
    # Walk through the directory
    for root, dirs, files in os.walk(metrics_dir):
        for file in files:
            if file.endswith('.yaml'):
                file_path = os.path.join(root, file)
                
                try:
                    # Load YAML file
                    with open(file_path, 'r') as f:
                        metrics = yaml.safe_load(f)
                    
                    # Add file path for reference
                    metrics['file_path'] = file_path
                    
                    # Determine which tool was used based on directory
                    if 'edge-copilot' in file_path:
                        metrics['tool'] = 'Edge Copilot'
                    elif 'github-copilot' in file_path:
                        metrics['tool'] = 'GitHub Copilot'
                    else:
                        metrics['tool'] = 'Unknown'
                    
                    all_metrics.append(metrics)
                    
                except Exception as e:
                    print(f"Error loading {file_path}: {str(e)}")
    
    # Convert to DataFrame
    if all_metrics:
        df = pd.json_normalize(all_metrics)
        print(f"Loaded {len(df)} metrics files")
        return df
    else:
        print("No metrics files found")
        return pd.DataFrame()

def calculate_time_savings(df):
    """
    Calculate time savings between Edge Copilot and GitHub Copilot.
    
    Args:
        df: DataFrame with metrics
        
    Returns:
        DataFrame with time savings metrics
    """
    print("Calculating time savings...")
    
    # Group by task category and tool
    grouped = df.groupby(['task_info.category', 'tool'])['time_metrics.total_minutes'].mean().reset_index()
    
    # Pivot to get Edge Copilot and GitHub Copilot columns
    pivot = grouped.pivot(index='task_info.category', columns='tool', values='time_metrics.total_minutes')
    
    # Calculate time savings
    pivot['time_savings'] = pivot['Edge Copilot'] - pivot['GitHub Copilot']
    pivot['time_savings_percent'] = (pivot['time_savings'] / pivot['Edge Copilot']) * 100
    
    return pivot

def calculate_quality_metrics(df):
    """
    Calculate quality metrics between Edge Copilot and GitHub Copilot.
    
    Args:
        df: DataFrame with metrics
        
    Returns:
        DataFrame with quality metrics
    """
    print("Calculating quality metrics...")
    
    # Group by task category and tool
    grouped = df.groupby(['task_info.category', 'tool'])['performance_metrics.quality_score'].mean().reset_index()
    
    # Pivot to get Edge Copilot and GitHub Copilot columns
    pivot = grouped.pivot(index='task_info.category', columns='tool', values='performance_metrics.quality_score')
    
    # Calculate quality improvement
    pivot['quality_improvement'] = pivot['GitHub Copilot'] - pivot['Edge Copilot']
    pivot['quality_improvement_percent'] = (pivot['quality_improvement'] / pivot['Edge Copilot']) * 100
    
    return pivot

def calculate_tool_interaction_metrics(df):
    """
    Calculate tool interaction metrics between Edge Copilot and GitHub Copilot.
    
    Args:
        df: DataFrame with metrics
        
    Returns:
        DataFrame with tool interaction metrics
    """
    print("Calculating tool interaction metrics...")
    
    # Calculate average prompt count
    prompt_count = df.groupby('tool')['tool_interaction.prompt_count'].mean()
    
    # Calculate percentage of character limitations encountered
    char_limit = df.groupby('tool')['tool_interaction.character_limitations_encountered'].mean() * 100
    
    # Calculate average context switching count
    context_switching = df.groupby('tool')['tool_interaction.context_switching_count'].mean()
    
    # Calculate average satisfaction rating
    satisfaction = df.groupby('tool')['performance_metrics.satisfaction_rating'].mean()
    
    # Combine metrics
    metrics = pd.DataFrame({
        'avg_prompt_count': prompt_count,
        'character_limitations_percent': char_limit,
        'avg_context_switching': context_switching,
        'avg_satisfaction_rating': satisfaction
    })
    
    # Calculate differences
    metrics['prompt_count_diff'] = metrics.loc['Edge Copilot', 'avg_prompt_count'] - metrics.loc['GitHub Copilot', 'avg_prompt_count']
    metrics['context_switching_diff'] = metrics.loc['Edge Copilot', 'avg_context_switching'] - metrics.loc['GitHub Copilot', 'avg_context_switching']
    metrics['satisfaction_diff'] = metrics.loc['GitHub Copilot', 'avg_satisfaction_rating'] - metrics.loc['Edge Copilot', 'avg_satisfaction_rating']
    
    return metrics

def calculate_roi(time_savings_df, hourly_cost=25, license_cost=100):
    """
    Calculate ROI based on time savings.
    
    Args:
        time_savings_df: DataFrame with time savings metrics
        hourly_cost: Hourly cost of a graduate (in £)
        license_cost: Annual cost of GitHub Copilot license (in £)
        
    Returns:
        Dictionary with ROI metrics
    """
    print("Calculating ROI...")
    
    # Calculate average time savings per task in hours
    avg_time_savings_per_task = time_savings_df['time_savings'].mean() / 60
    
    # Estimate number of tasks per week (assuming 40-hour work week)
    tasks_per_week = 40 / (time_savings_df['Edge Copilot'].mean() / 60)
    
    # Calculate weekly time savings in hours
    weekly_time_savings = avg_time_savings_per_task * tasks_per_week
    
    # Calculate annual time savings (48 working weeks per year)
    annual_time_savings = weekly_time_savings * 48
    
    # Calculate annual cost savings
    annual_cost_savings = annual_time_savings * hourly_cost
    
    # Calculate ROI
    roi = ((annual_cost_savings - license_cost) / license_cost) * 100
    
    # Calculate payback period in months
    payback_period = (license_cost / annual_cost_savings) * 12
    
    return {
        'avg_graduate_hourly_cost': hourly_cost,
        'github_copilot_annual_license': license_cost,
        'weekly_time_savings_hours': weekly_time_savings,
        'annual_time_savings_hours': annual_time_savings,
        'annual_cost_savings': annual_cost_savings,
        'roi_percent': roi,
        'payback_period_months': payback_period
    }

def plot_time_savings(time_savings_df, output_dir):
    """
    Plot time savings comparison.
    
    Args:
        time_savings_df: DataFrame with time savings metrics
        output_dir: Directory to save the plot
    """
    print("Plotting time savings...")
    
    # Create figure
    plt.figure(figsize=(10, 6))
    
    # Create bar chart
    ax = time_savings_df[['Edge Copilot', 'GitHub Copilot']].plot(kind='bar', rot=0)
    
    # Add time savings percentage as text
    for i, v in enumerate(time_savings_df['time_savings_percent']):
        ax.text(i, max(time_savings_df['Edge Copilot'][i], time_savings_df['GitHub Copilot'][i]) + 1, 
                f"{v:.1f}% saved", ha='center')
    
    # Set labels and title
    plt.xlabel('Task Category')
    plt.ylabel('Average Time (minutes)')
    plt.title('Time Comparison: Edge Copilot vs GitHub Copilot')
    
    # Add legend
    plt.legend(title='Tool')
    
    # Add grid
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Tight layout
    plt.tight_layout()
    
    # Save figure
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, 'time_savings.png'))
    plt.close()

def plot_quality_metrics(quality_df, output_dir):
    """
    Plot quality metrics comparison.
    
    Args:
        quality_df: DataFrame with quality metrics
        output_dir: Directory to save the plot
    """
    print("Plotting quality metrics...")
    
    # Create figure
    plt.figure(figsize=(10, 6))
    
    # Create bar chart
    ax = quality_df[['Edge Copilot', 'GitHub Copilot']].plot(kind='bar', rot=0)
    
    # Add quality improvement percentage as text
    for i, v in enumerate(quality_df['quality_improvement_percent']):
        ax.text(i, max(quality_df['Edge Copilot'][i], quality_df['GitHub Copilot'][i]) + 0.1, 
                f"{v:.1f}% better", ha='center')
    
    # Set labels and title
    plt.xlabel('Task Category')
    plt.ylabel('Average Quality Score (1-5)')
    plt.title('Quality Comparison: Edge Copilot vs GitHub Copilot')
    
    # Add legend
    plt.legend(title='Tool')
    
    # Add grid
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Set y-axis limits
    plt.ylim(0, 5.5)
    
    # Tight layout
    plt.tight_layout()
    
    # Save figure
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, 'quality_metrics.png'))
    plt.close()

def plot_tool_interaction(interaction_df, output_dir):
    """
    Plot tool interaction metrics.
    
    Args:
        interaction_df: DataFrame with tool interaction metrics
        output_dir: Directory to save the plot
    """
    print("Plotting tool interaction metrics...")
    
    # Create figure
    plt.figure(figsize=(12, 8))
    
    # Create subplots
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    
    # Plot prompt count
    axes[0, 0].bar(['Edge Copilot', 'GitHub Copilot'], interaction_df['avg_prompt_count'])
    axes[0, 0].set_title('Average Prompt Count')
    axes[0, 0].grid(axis='y', linestyle='--', alpha=0.7)
    
    # Plot character limitations
    axes[0, 1].bar(['Edge Copilot', 'GitHub Copilot'], interaction_df['character_limitations_percent'])
    axes[0, 1].set_title('Character Limitations Encountered (%)')
    axes[0, 1].grid(axis='y', linestyle='--', alpha=0.7)
    
    # Plot context switching
    axes[1, 0].bar(['Edge Copilot', 'GitHub Copilot'], interaction_df['avg_context_switching'])
    axes[1, 0].set_title('Average Context Switching Count')
    axes[1, 0].grid(axis='y', linestyle='--', alpha=0.7)
    
    # Plot satisfaction rating
    axes[1, 1].bar(['Edge Copilot', 'GitHub Copilot'], interaction_df['avg_satisfaction_rating'])
    axes[1, 1].set_title('Average Satisfaction Rating (1-5)')
    axes[1, 1].set_ylim(0, 5.5)
    axes[1, 1].grid(axis='y', linestyle='--', alpha=0.7)
    
    # Set overall title
    fig.suptitle('Tool Interaction Metrics Comparison', fontsize=16)
    
    # Tight layout
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    # Save figure
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, 'tool_interaction.png'))
    plt.close()

def plot_roi(roi_metrics, output_dir):
    """
    Plot ROI metrics.
    
    Args:
        roi_metrics: Dictionary with ROI metrics
        output_dir: Directory to save the plot
    """
    print("Plotting ROI metrics...")
    
    # Create figure
    plt.figure(figsize=(10, 6))
    
    # Create bar chart for cost comparison
    labels = ['Annual License Cost', 'Annual Cost Savings']
    values = [roi_metrics['github_copilot_annual_license'], roi_metrics['annual_cost_savings']]
    
    plt.bar(labels, values, color=['#ff9999', '#66b3ff'])
    
    # Add ROI as text
    plt.text(1, values[1] + 5, f"ROI: {roi_metrics['roi_percent']:.1f}%", ha='center')
    
    # Add payback period as text
    plt.text(1, values[1] + 15, f"Payback: {roi_metrics['payback_period_months']:.1f} months", ha='center')
    
    # Set labels and title
    plt.ylabel('Cost (£)')
    plt.title('GitHub Copilot ROI Analysis')
    
    # Add grid
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Tight layout
    plt.tight_layout()
    
    # Save figure
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, 'roi_analysis.png'))
    plt.close()

def generate_report(metrics_df, time_savings_df, quality_df, interaction_df, roi_metrics, output_dir):
    """
    Generate a summary report of the analysis.
    
    Args:
        metrics_df: DataFrame with all metrics
        time_savings_df: DataFrame with time savings metrics
        quality_df: DataFrame with quality metrics
        interaction_df: DataFrame with tool interaction metrics
        roi_metrics: Dictionary with ROI metrics
        output_dir: Directory to save the report
    """
    print("Generating summary report...")
    
    # Create report
    report = {
        'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'metrics_count': len(metrics_df),
        'participants_count': metrics_df['task_info.participant_name'].nunique(),
        'time_savings': {
            'average_minutes_per_task': time_savings_df['time_savings'].mean(),
            'average_percent': time_savings_df['time_savings_percent'].mean(),
            'by_category': time_savings_df.to_dict()
        },
        'quality_metrics': {
            'average_improvement': quality_df['quality_improvement'].mean(),
            'average_percent': quality_df['quality_improvement_percent'].mean(),
            'by_category': quality_df.to_dict()
        },
        'tool_interaction': interaction_df.to_dict(),
        'roi_analysis': roi_metrics
    }
    
    # Save report as JSON
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, 'analysis_summary.json'), 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"Report saved to {os.path.join(output_dir, 'analysis_summary.json')}")

def main():
    """Main function to run the analysis."""
    # Set paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    metrics_dir = os.path.join(base_dir, 'metrics', 'submissions')
    output_dir = os.path.join(base_dir, 'analysis', 'results')
    
    # Load metrics
    metrics_df = load_metrics(metrics_dir)
    
    if metrics_df.empty:
        print("No metrics to analyze. Exiting.")
        return
    
    # Calculate metrics
    time_savings_df = calculate_time_savings(metrics_df)
    quality_df = calculate_quality_metrics(metrics_df)
    interaction_df = calculate_tool_interaction_metrics(metrics_df)
    roi_metrics = calculate_roi(time_savings_df)
    
    # Generate plots
    plot_time_savings(time_savings_df, output_dir)
    plot_quality_metrics(quality_df, output_dir)
    plot_tool_interaction(interaction_df, output_dir)
    plot_roi(roi_metrics, output_dir)
    
    # Generate report
    generate_report(metrics_df, time_savings_df, quality_df, interaction_df, roi_metrics, output_dir)
    
    print("Analysis complete!")

if __name__ == "__main__":
    main()
