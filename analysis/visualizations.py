"""
Visualizations for GitHub Copilot Experiment

This script generates additional visualizations for the experiment results.
It works with the data processed by metrics_aggregator.py.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
from datetime import datetime

def load_analysis_summary(file_path):
    """
    Load analysis summary from JSON file.
    
    Args:
        file_path: Path to the analysis summary JSON file
        
    Returns:
        Dictionary with analysis summary
    """
    print(f"Loading analysis summary from {file_path}...")
    
    try:
        with open(file_path, 'r') as f:
            summary = json.load(f)
        print("Analysis summary loaded successfully")
        return summary
    except Exception as e:
        print(f"Error loading analysis summary: {str(e)}")
        return None

def plot_time_savings_by_task_type(summary, output_dir):
    """
    Plot time savings by task type.
    
    Args:
        summary: Analysis summary dictionary
        output_dir: Directory to save the plot
    """
    print("Plotting time savings by task type...")
    
    # Extract time savings by category
    time_savings = summary['time_savings']['by_category']
    
    # Convert to DataFrame
    categories = list(time_savings['time_savings'].keys())
    edge_times = [time_savings['Edge Copilot'][cat] for cat in categories]
    github_times = [time_savings['GitHub Copilot'][cat] for cat in categories]
    savings_percent = [time_savings['time_savings_percent'][cat] for cat in categories]
    
    df = pd.DataFrame({
        'Category': categories,
        'Edge Copilot': edge_times,
        'GitHub Copilot': github_times,
        'Savings (%)': savings_percent
    })
    
    # Sort by savings percentage
    df = df.sort_values('Savings (%)', ascending=False)
    
    # Create figure
    plt.figure(figsize=(12, 8))
    
    # Create bar chart
    ax = plt.subplot(111)
    x = np.arange(len(df['Category']))
    width = 0.35
    
    edge_bars = ax.bar(x - width/2, df['Edge Copilot'], width, label='Edge Copilot', color='#ff9999')
    github_bars = ax.bar(x + width/2, df['GitHub Copilot'], width, label='GitHub Copilot', color='#66b3ff')
    
    # Add savings percentage as text
    for i, (edge, github, savings) in enumerate(zip(df['Edge Copilot'], df['GitHub Copilot'], df['Savings (%)'])):
        ax.text(i, max(edge, github) + 1, f"{savings:.1f}%", ha='center')
    
    # Set labels and title
    ax.set_xlabel('Task Category')
    ax.set_ylabel('Average Time (minutes)')
    ax.set_title('Time Savings by Task Type: Edge Copilot vs GitHub Copilot')
    ax.set_xticks(x)
    ax.set_xticklabels(df['Category'])
    
    # Add legend
    ax.legend()
    
    # Add grid
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Tight layout
    plt.tight_layout()
    
    # Save figure
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, 'time_savings_by_task_type.png'))
    plt.close()

def plot_quality_radar(summary, output_dir):
    """
    Plot quality metrics as a radar chart.
    
    Args:
        summary: Analysis summary dictionary
        output_dir: Directory to save the plot
    """
    print("Plotting quality radar chart...")
    
    # Extract quality metrics by category
    quality = summary['quality_metrics']['by_category']
    
    # Convert to DataFrame
    categories = list(quality['quality_improvement'].keys())
    edge_scores = [quality['Edge Copilot'][cat] for cat in categories]
    github_scores = [quality['GitHub Copilot'][cat] for cat in categories]
    
    # Create radar chart
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, polar=True)
    
    # Number of categories
    N = len(categories)
    
    # Angle of each axis
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]  # Close the loop
    
    # Add the first point at the end to close the polygon
    edge_scores += edge_scores[:1]
    github_scores += github_scores[:1]
    
    # Plot data
    ax.plot(angles, edge_scores, 'o-', linewidth=2, label='Edge Copilot', color='#ff9999')
    ax.fill(angles, edge_scores, alpha=0.25, color='#ff9999')
    
    ax.plot(angles, github_scores, 'o-', linewidth=2, label='GitHub Copilot', color='#66b3ff')
    ax.fill(angles, github_scores, alpha=0.25, color='#66b3ff')
    
    # Set category labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    
    # Set y-axis limits
    ax.set_ylim(0, 5)
    
    # Add legend
    ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    
    # Set title
    plt.title('Quality Metrics by Task Category', size=15, y=1.1)
    
    # Save figure
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, 'quality_radar.png'))
    plt.close()

def plot_context_switching_impact(summary, output_dir):
    """
    Plot the impact of context switching on task completion time.
    
    Args:
        summary: Analysis summary dictionary
        output_dir: Directory to save the plot
    """
    print("Plotting context switching impact...")
    
    # Extract tool interaction metrics
    interaction = summary['tool_interaction']
    
    # Create figure
    plt.figure(figsize=(10, 6))
    
    # Create bar chart
    tools = ['Edge Copilot', 'GitHub Copilot']
    context_switching = [interaction['avg_context_switching']['Edge Copilot'], 
                         interaction['avg_context_switching']['GitHub Copilot']]
    
    bars = plt.bar(tools, context_switching, color=['#ff9999', '#66b3ff'])
    
    # Add values as text
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                 f"{height:.1f}", ha='center', va='bottom')
    
    # Set labels and title
    plt.xlabel('Tool')
    plt.ylabel('Average Context Switches per Task')
    plt.title('Context Switching Comparison: Edge Copilot vs GitHub Copilot')
    
    # Add annotation about impact
    plt.annotate(
        f"GitHub Copilot reduces context switching by {interaction['context_switching_diff']:.1f} times per task",
        xy=(0.5, 0.9),
        xycoords='axes fraction',
        ha='center',
        va='center',
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8)
    )
    
    # Add grid
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Tight layout
    plt.tight_layout()
    
    # Save figure
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, 'context_switching_impact.png'))
    plt.close()

def plot_roi_breakdown(summary, output_dir):
    """
    Plot ROI breakdown.
    
    Args:
        summary: Analysis summary dictionary
        output_dir: Directory to save the plot
    """
    print("Plotting ROI breakdown...")
    
    # Extract ROI metrics
    roi = summary['roi_analysis']
    
    # Create figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot time savings
    ax1.bar(['Weekly', 'Annual'], 
            [roi['weekly_time_savings_hours'], roi['annual_time_savings_hours']],
            color=['#66b3ff', '#66b3ff'])
    
    ax1.set_ylabel('Time Saved (hours)')
    ax1.set_title('Time Savings')
    
    # Add values as text
    ax1.text(0, roi['weekly_time_savings_hours'] + 0.5, 
             f"{roi['weekly_time_savings_hours']:.1f} hrs/week", 
             ha='center')
    
    ax1.text(1, roi['annual_time_savings_hours'] + 5, 
             f"{roi['annual_time_savings_hours']:.1f} hrs/year", 
             ha='center')
    
    # Plot financial impact
    ax2.bar(['License Cost', 'Cost Savings', 'Net Benefit'], 
            [roi['github_copilot_annual_license'], 
             roi['annual_cost_savings'],
             roi['annual_cost_savings'] - roi['github_copilot_annual_license']],
            color=['#ff9999', '#66b3ff', '#99ff99'])
    
    ax2.set_ylabel('Amount (£)')
    ax2.set_title('Financial Impact (Annual)')
    
    # Add values as text
    ax2.text(0, roi['github_copilot_annual_license'] + 5, 
             f"£{roi['github_copilot_annual_license']}", 
             ha='center')
    
    ax2.text(1, roi['annual_cost_savings'] + 5, 
             f"£{roi['annual_cost_savings']:.0f}", 
             ha='center')
    
    ax2.text(2, (roi['annual_cost_savings'] - roi['github_copilot_annual_license']) + 5, 
             f"£{roi['annual_cost_savings'] - roi['github_copilot_annual_license']:.0f}", 
             ha='center')
    
    # Add ROI information
    fig.suptitle(f"GitHub Copilot ROI Analysis\nROI: {roi['roi_percent']:.1f}% | Payback Period: {roi['payback_period_months']:.1f} months", 
                 fontsize=16)
    
    # Add grid
    ax1.grid(axis='y', linestyle='--', alpha=0.7)
    ax2.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Tight layout
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    # Save figure
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, 'roi_breakdown.png'))
    plt.close()

def plot_satisfaction_comparison(summary, output_dir):
    """
    Plot satisfaction rating comparison.
    
    Args:
        summary: Analysis summary dictionary
        output_dir: Directory to save the plot
    """
    print("Plotting satisfaction comparison...")
    
    # Extract satisfaction ratings
    interaction = summary['tool_interaction']
    
    # Create figure
    plt.figure(figsize=(10, 6))
    
    # Create bar chart
    tools = ['Edge Copilot', 'GitHub Copilot']
    satisfaction = [interaction['avg_satisfaction_rating']['Edge Copilot'], 
                    interaction['avg_satisfaction_rating']['GitHub Copilot']]
    
    bars = plt.bar(tools, satisfaction, color=['#ff9999', '#66b3ff'])
    
    # Add values as text
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                 f"{height:.1f}", ha='center', va='bottom')
    
    # Set labels and title
    plt.xlabel('Tool')
    plt.ylabel('Average Satisfaction Rating (1-5)')
    plt.title('User Satisfaction Comparison: Edge Copilot vs GitHub Copilot')
    
    # Add annotation about improvement
    plt.annotate(
        f"GitHub Copilot satisfaction rating is {interaction['satisfaction_diff']:.1f} points higher",
        xy=(0.5, 0.9),
        xycoords='axes fraction',
        ha='center',
        va='center',
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8)
    )
    
    # Set y-axis limits
    plt.ylim(0, 5.5)
    
    # Add grid
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Tight layout
    plt.tight_layout()
    
    # Save figure
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, 'satisfaction_comparison.png'))
    plt.close()

def generate_summary_dashboard(summary, output_dir):
    """
    Generate a summary dashboard with key metrics.
    
    Args:
        summary: Analysis summary dictionary
        output_dir: Directory to save the plot
    """
    print("Generating summary dashboard...")
    
    # Create figure
    fig = plt.figure(figsize=(12, 8))
    
    # Set up grid
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
    
    # Time savings
    ax1 = fig.add_subplot(gs[0, 0])
    time_savings_percent = summary['time_savings']['average_percent']
    ax1.text(0.5, 0.5, f"{time_savings_percent:.1f}%", 
             ha='center', va='center', fontsize=36)
    ax1.text(0.5, 0.2, "Average Time Savings", 
             ha='center', va='center', fontsize=14)
    ax1.axis('off')
    
    # Quality improvement
    ax2 = fig.add_subplot(gs[0, 1])
    quality_improvement_percent = summary['quality_metrics']['average_percent']
    ax2.text(0.5, 0.5, f"{quality_improvement_percent:.1f}%", 
             ha='center', va='center', fontsize=36)
    ax2.text(0.5, 0.2, "Average Quality Improvement", 
             ha='center', va='center', fontsize=14)
    ax2.axis('off')
    
    # ROI
    ax3 = fig.add_subplot(gs[1, 0])
    roi_percent = summary['roi_analysis']['roi_percent']
    ax3.text(0.5, 0.5, f"{roi_percent:.1f}%", 
             ha='center', va='center', fontsize=36)
    ax3.text(0.5, 0.2, "Return on Investment", 
             ha='center', va='center', fontsize=14)
    ax3.axis('off')
    
    # Payback period
    ax4 = fig.add_subplot(gs[1, 1])
    payback_period = summary['roi_analysis']['payback_period_months']
    ax4.text(0.5, 0.5, f"{payback_period:.1f}", 
             ha='center', va='center', fontsize=36)
    ax4.text(0.5, 0.2, "Payback Period (months)", 
             ha='center', va='center', fontsize=14)
    ax4.axis('off')
    
    # Add title
    fig.suptitle("GitHub Copilot Experiment: Key Metrics", fontsize=20, y=0.98)
    
    # Add generation timestamp
    plt.figtext(0.5, 0.01, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                ha='center', fontsize=10)
    
    # Save figure
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, 'summary_dashboard.png'))
    plt.close()

def main():
    """Main function to run the visualizations."""
    # Set paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    summary_file = os.path.join(base_dir, 'analysis', 'results', 'analysis_summary.json')
    output_dir = os.path.join(base_dir, 'analysis', 'results')
    
    # Load analysis summary
    summary = load_analysis_summary(summary_file)
    
    if summary is None:
        print("No analysis summary found. Run metrics_aggregator.py first.")
        return
    
    # Generate visualizations
    plot_time_savings_by_task_type(summary, output_dir)
    plot_quality_radar(summary, output_dir)
    plot_context_switching_impact(summary, output_dir)
    plot_roi_breakdown(summary, output_dir)
    plot_satisfaction_comparison(summary, output_dir)
    generate_summary_dashboard(summary, output_dir)
    
    print("Visualizations complete!")

if __name__ == "__main__":
    main()
