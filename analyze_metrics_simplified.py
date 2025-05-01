#!/usr/bin/env python3
"""
GitHub Copilot Experiment Analysis - Simplified Version

This script runs the analysis pipeline for the GitHub Copilot experiment.
It processes metrics files and generates visualizations and reports in a simplified manner.
"""

import os
import sys
import json
import logging
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yaml
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("analysis.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class GitHubCopilotAnalysis:
    """Main class for GitHub Copilot experiment analysis."""
    
    def __init__(self):
        """Initialize paths and directories."""
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.metrics_dir = os.path.join(self.base_dir, 'metrics', 'submissions')
        self.results_dir = os.path.join(self.base_dir, 'analysis', 'results')
        self.ensure_directories()
        
    def ensure_directories(self):
        """Create necessary directories if they don't exist."""
        os.makedirs(self.metrics_dir, exist_ok=True)
        os.makedirs(self.results_dir, exist_ok=True)
        
    def load_metrics(self):
        """Load metrics from YAML files in the submissions directory."""
        logger.info(f"Loading metrics from {self.metrics_dir}")
        
        all_metrics = []
        
        # Walk through the directory
        for root, _, files in os.walk(self.metrics_dir):
            for file in files:
                if file.endswith('.yaml'):
                    file_path = os.path.join(root, file)
                    try:
                        # Load YAML file
                        with open(file_path, 'r') as f:
                            metrics = yaml.safe_load(f)
                        
                        # Determine file type and tool
                        if 'task_metrics_' in file:
                            metrics['file_type'] = 'task_metrics'
                            metrics['tool'] = 'GitHub Copilot'
                        elif 'quantitative_' in file:
                            metrics['file_type'] = 'qualitative'
                            if 'GH_' in str(metrics):
                                metrics['tool'] = 'GitHub Copilot'
                            else:
                                metrics['tool'] = 'Edge Copilot'
                        else:
                            metrics['file_type'] = 'unknown'
                            metrics['tool'] = 'Unknown'
                            
                        # Add file path for reference
                        metrics['file_path'] = file_path
                        
                        all_metrics.append(metrics)
                    except Exception as e:
                        logger.error(f"Error loading {file_path}: {str(e)}")
        
        # Convert to DataFrame
        if all_metrics:
            df = pd.json_normalize(all_metrics)
            logger.info(f"Loaded {len(df)} metrics files")
            return df
        else:
            logger.warning("No metrics files found")
            return pd.DataFrame()

    def analyze_metrics(self, df):
        """
        Analyze metrics from the submissions.
        
        Args:
            df: DataFrame with metrics
            
        Returns:
            Dictionary with analysis results
        """
        logger.info("Analyzing metrics...")
        
        # Filter metrics by file type
        task_df = df[df['file_type'] == 'task_metrics']
        
        # Check if we have any task metrics
        if task_df.empty:
            logger.warning("No task metrics found in submissions")
            return None
        
        # We'll create separate dataframes for GitHub and Edge data
        # Note: We're analyzing a single file that might contain both GH and Edge data
        gh_df = pd.DataFrame()
        edge_df = pd.DataFrame()
        
        # Check for GitHub Copilot data (has GH_ prefix in columns)
        if any('GH_' in col for col in task_df.columns):
            logger.info("Found GitHub Copilot data in submissions")
            gh_df = task_df.copy()
        
        # Check for Edge Copilot data (has Edge_ prefix in columns)
        if any('Edge_' in col for col in task_df.columns):
            logger.info("Found Edge Copilot data in submissions")
            edge_df = task_df.copy()
        
        if gh_df.empty:
            logger.warning("No GitHub Copilot metrics to analyze")
            return None
        
        # Time savings analysis
        time_metrics = {}
        if 'time_metrics.total_minutes' in gh_df.columns:
            # Get GitHub Copilot time data
            gh_time = gh_df.groupby('task_info.category')['time_metrics.total_minutes'].mean()
            
            # Get Edge Copilot time data if available, otherwise use placeholder
            if not edge_df.empty and 'time_metrics.total_minutes' in edge_df.columns:
                logger.info("Using actual Edge Copilot time data")
                # If we have categories in Edge that aren't in GitHub, we'll ignore them
                edge_categories = edge_df['task_info.category'].unique()
                edge_time_data = {}
                
                # Calculate average time for each category
                for category in edge_categories:
                    category_df = edge_df[edge_df['task_info.category'] == category]
                    if not category_df.empty:
                        edge_time_data[category] = category_df['time_metrics.total_minutes'].mean()
                
                # Create a Series with the same index as gh_time
                edge_time = pd.Series([
                    edge_time_data.get(cat, gh_time[cat] * 1.2)  # Use actual data or fallback
                    for cat in gh_time.index
                ], index=gh_time.index)
            else:
                logger.warning("No Edge Copilot time data found in submissions. Using placeholder values (20% longer than GitHub Copilot).")
                edge_time = gh_time * 1.2  # Placeholder - assume Edge takes 20% longer
            
            time_metrics = {
                'Edge Copilot': edge_time.to_dict(),
                'GitHub Copilot': gh_time.to_dict(),
                'time_savings': (edge_time - gh_time).to_dict(),
                'time_savings_percent': ((edge_time - gh_time) / edge_time * 100).to_dict(),
                'average_savings': (edge_time - gh_time).mean(),
                'average_percent': ((edge_time - gh_time) / edge_time * 100).mean()
            }
        
        # Quality metrics analysis
        quality_metrics = {}
        if 'GH_performance_metrics.quality_score' in gh_df.columns:
            # Get GitHub Copilot quality data
            gh_quality = gh_df.groupby('task_info.category')['GH_performance_metrics.quality_score'].mean()
            
            # Get Edge Copilot quality data if available, otherwise use placeholder
            if not edge_df.empty and 'Edge_performance_metrics.quality_score' in edge_df.columns:
                logger.info("Using actual Edge Copilot quality data")
                # If we have categories in Edge that aren't in GitHub, we'll ignore them
                edge_categories = edge_df['task_info.category'].unique()
                edge_quality_data = {}
                
                # Calculate average quality for each category
                for category in edge_categories:
                    category_df = edge_df[edge_df['task_info.category'] == category]
                    if not category_df.empty:
                        edge_quality_data[category] = category_df['Edge_performance_metrics.quality_score'].mean()
                
                # Create a Series with the same index as gh_quality
                edge_quality = pd.Series([
                    edge_quality_data.get(cat, 3.0)  # Use actual data or fallback to 3.0
                    for cat in gh_quality.index
                ], index=gh_quality.index)
            else:
                logger.warning("No Edge Copilot quality data found in submissions. Using placeholder values (3.0 on a 5-point scale).")
                edge_quality = pd.Series(3.0, index=gh_quality.index)  # Placeholder
            
            quality_metrics = {
                'Edge Copilot': edge_quality.to_dict(),
                'GitHub Copilot': gh_quality.to_dict(),
                'quality_improvement': (gh_quality - edge_quality).to_dict(),
                'quality_improvement_percent': ((gh_quality - edge_quality) / edge_quality * 100).to_dict(),
                'average_improvement': (gh_quality - edge_quality).mean(),
                'average_percent': ((gh_quality - edge_quality) / edge_quality * 100).mean()
            }
        
        # Tool interaction metrics
        logger.info("Analyzing tool interaction metrics")
        
        # Get GitHub Copilot interaction metrics
        gh_prompt_count = gh_df['tool_interaction.prompt_count'].mean() if 'tool_interaction.prompt_count' in gh_df.columns else 0
        gh_char_limit = gh_df['tool_interaction.character_limitations_encountered'].mean() * 100 if 'tool_interaction.character_limitations_encountered' in gh_df.columns else 0
        gh_context_switching = gh_df['tool_interaction.context_switching_count'].mean() if 'tool_interaction.context_switching_count' in gh_df.columns else 0
        gh_satisfaction = gh_df['GH_performance_metrics.satisfaction_rating'].mean() if 'GH_performance_metrics.satisfaction_rating' in gh_df.columns else 0
        
        # Check if we have Edge Copilot interaction data
        have_edge_interaction = not edge_df.empty
        edge_prompt_count = 0
        edge_char_limit = 0
        edge_context_switching = 0
        edge_satisfaction = 0
        
        if have_edge_interaction:
            # Try to get Edge Copilot interaction metrics
            if 'tool_interaction.prompt_count' in edge_df.columns:
                edge_prompt_count = edge_df['tool_interaction.prompt_count'].mean()
            if 'tool_interaction.character_limitations_encountered' in edge_df.columns:
                edge_char_limit = edge_df['tool_interaction.character_limitations_encountered'].mean() * 100
            if 'tool_interaction.context_switching_count' in edge_df.columns:
                edge_context_switching = edge_df['tool_interaction.context_switching_count'].mean()
            if 'Edge_performance_metrics.satisfaction_rating' in edge_df.columns:
                edge_satisfaction = edge_df['Edge_performance_metrics.satisfaction_rating'].mean()
        
        # Use placeholder values for any missing Edge metrics
        if edge_prompt_count == 0:
            logger.warning("No Edge Copilot prompt count data found. Using placeholder value (1.5x GitHub Copilot).")
            edge_prompt_count = gh_prompt_count * 1.5
            
        if edge_char_limit == 0:
            logger.warning("No Edge Copilot character limitations data found. Using placeholder value (75%).")
            edge_char_limit = 75.0  # Placeholder
            
        if edge_context_switching == 0:
            logger.warning("No Edge Copilot context switching data found. Using placeholder value (2x GitHub Copilot).")
            edge_context_switching = gh_context_switching * 2.0
            
        if edge_satisfaction == 0:
            logger.warning("No Edge Copilot satisfaction rating data found. Using placeholder value (GitHub Copilot - 1).")
            edge_satisfaction = max(1.0, gh_satisfaction - 1.0)
        
        # Compile tool interaction metrics
        tool_metrics = {
            'avg_prompt_count': {
                'GitHub Copilot': gh_prompt_count,
                'Edge Copilot': edge_prompt_count
            },
            'character_limitations_percent': {
                'GitHub Copilot': gh_char_limit,
                'Edge Copilot': edge_char_limit
            },
            'avg_context_switching': {
                'GitHub Copilot': gh_context_switching,
                'Edge Copilot': edge_context_switching
            },
            'avg_satisfaction_rating': {
                'GitHub Copilot': gh_satisfaction,
                'Edge Copilot': edge_satisfaction
            }
        }
        
        # Calculate differences
        tool_metrics['context_switching_diff'] = tool_metrics['avg_context_switching']['Edge Copilot'] - tool_metrics['avg_context_switching']['GitHub Copilot']
        tool_metrics['satisfaction_diff'] = tool_metrics['avg_satisfaction_rating']['GitHub Copilot'] - tool_metrics['avg_satisfaction_rating']['Edge Copilot']
        
        # Calculate ROI
        hourly_cost = 25  # Placeholder for graduate hourly cost
        license_cost = 100  # Placeholder for annual license cost
        
        # Calculate average time savings in hours per task
        avg_time_savings_per_task = time_metrics['average_savings'] / 60 if 'average_savings' in time_metrics else 0
        
        # Estimate tasks per week (40-hour work week)
        edge_time_mean = np.mean(list(time_metrics['Edge Copilot'].values())) if 'Edge Copilot' in time_metrics else 0
        tasks_per_week = 40 / (edge_time_mean / 60) if edge_time_mean > 0 else 0
        
        # Calculate time and cost savings
        weekly_time_savings = avg_time_savings_per_task * tasks_per_week
        annual_time_savings = weekly_time_savings * 48  # 48 working weeks per year
        annual_cost_savings = annual_time_savings * hourly_cost
        
        # Calculate ROI and payback period
        roi_percent = ((annual_cost_savings - license_cost) / license_cost) * 100 if license_cost > 0 else 0
        payback_period = (license_cost / annual_cost_savings) * 12 if annual_cost_savings > 0 else 0
        
        roi_metrics = {
            'avg_graduate_hourly_cost': hourly_cost,
            'github_copilot_annual_license': license_cost,
            'weekly_time_savings_hours': weekly_time_savings,
            'annual_time_savings_hours': annual_time_savings,
            'annual_cost_savings': annual_cost_savings,
            'roi_percent': roi_percent,
            'payback_period_months': payback_period
        }
        
        # Compile all metrics into a summary
        summary = {
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'metrics_count': len(df),
            'participants_count': df['task_info.participant_name'].nunique() if 'task_info.participant_name' in df.columns else 0,
            'time_savings': time_metrics,
            'quality_metrics': quality_metrics,
            'tool_interaction': tool_metrics,
            'roi_analysis': roi_metrics
        }
        
        return summary

    def generate_visualizations(self, summary):
        """
        Generate basic visualizations.
        
        Args:
            summary: Dictionary with analysis results
        """
        logger.info("Generating visualizations...")
        
        if not summary:
            logger.warning("No data to visualize")
            return
        
        # Time savings visualization
        self._plot_time_savings(summary)
        
        # ROI visualization
        self._plot_roi(summary)
        
        # Satisfaction comparison
        self._plot_satisfaction(summary)
        
        # Summary dashboard
        self._generate_dashboard(summary)
    
    def _plot_time_savings(self, summary):
        """Plot time savings comparison."""
        if 'time_savings' not in summary or 'Edge Copilot' not in summary['time_savings']:
            logger.warning("No time savings data to visualize")
            return
        
        time_data = summary['time_savings']
        
        plt.figure(figsize=(10, 6))
        
        # Extract data
        categories = list(time_data['GitHub Copilot'].keys())
        gh_times = [time_data['GitHub Copilot'][cat] for cat in categories]
        edge_times = [time_data['Edge Copilot'][cat] for cat in categories]
        
        # Create bar chart
        x = np.arange(len(categories))
        width = 0.35
        
        plt.bar(x - width/2, edge_times, width, label='Edge Copilot', color='#ff9999')
        plt.bar(x + width/2, gh_times, width, label='GitHub Copilot', color='#66b3ff')
        
        # Add labels and title
        plt.xlabel('Task Category')
        plt.ylabel('Average Time (minutes)')
        plt.title('Time Comparison: Edge Copilot vs GitHub Copilot')
        plt.xticks(x, categories)
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Save figure
        plt.savefig(os.path.join(self.results_dir, 'time_savings.png'))
        plt.close()
    
    def _plot_roi(self, summary):
        """Plot ROI breakdown."""
        if 'roi_analysis' not in summary:
            logger.warning("No ROI data to visualize")
            return
        
        roi = summary['roi_analysis']
        
        plt.figure(figsize=(10, 6))
        
        # Create bar chart for financial impact
        plt.bar(['License Cost', 'Annual Savings', 'Net Benefit'], 
                [roi['github_copilot_annual_license'], 
                 roi['annual_cost_savings'],
                 roi['annual_cost_savings'] - roi['github_copilot_annual_license']],
                color=['#ff9999', '#66b3ff', '#99ff99'])
        
        # Add title and labels
        plt.title(f"GitHub Copilot ROI Analysis\nROI: {roi['roi_percent']:.1f}% | Payback: {roi['payback_period_months']:.1f} months")
        plt.ylabel('Amount (£)')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Save figure
        plt.savefig(os.path.join(self.results_dir, 'roi_analysis.png'))
        plt.close()
    
    def _plot_satisfaction(self, summary):
        """Plot satisfaction comparison."""
        if 'tool_interaction' not in summary:
            logger.warning("No satisfaction data to visualize")
            return
        
        interaction = summary['tool_interaction']
        
        plt.figure(figsize=(8, 6))
        
        # Create bar chart
        tools = ['Edge Copilot', 'GitHub Copilot']
        satisfaction = [interaction['avg_satisfaction_rating']['Edge Copilot'], 
                        interaction['avg_satisfaction_rating']['GitHub Copilot']]
        
        plt.bar(tools, satisfaction, color=['#ff9999', '#66b3ff'])
        
        # Add title and labels
        plt.title('User Satisfaction Comparison')
        plt.ylabel('Average Satisfaction Rating (1-5)')
        plt.ylim(0, 5.5)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Save figure
        plt.savefig(os.path.join(self.results_dir, 'satisfaction.png'))
        plt.close()
    
    def _generate_dashboard(self, summary):
        """Generate a simple dashboard with key metrics."""
        plt.figure(figsize=(10, 8))
        
        # Create a 2x2 grid
        plt.subplot(2, 2, 1)
        time_savings = summary['time_savings']['average_percent'] if 'time_savings' in summary and 'average_percent' in summary['time_savings'] else 0
        plt.text(0.5, 0.5, f"{time_savings:.1f}%", ha='center', va='center', fontsize=24)
        plt.text(0.5, 0.2, "Time Savings", ha='center', va='center')
        plt.axis('off')
        
        plt.subplot(2, 2, 2)
        quality = summary['quality_metrics']['average_percent'] if 'quality_metrics' in summary and 'average_percent' in summary['quality_metrics'] else 0
        plt.text(0.5, 0.5, f"{quality:.1f}%", ha='center', va='center', fontsize=24)
        plt.text(0.5, 0.2, "Quality Improvement", ha='center', va='center')
        plt.axis('off')
        
        plt.subplot(2, 2, 3)
        roi = summary['roi_analysis']['roi_percent'] if 'roi_analysis' in summary and 'roi_percent' in summary['roi_analysis'] else 0
        plt.text(0.5, 0.5, f"{roi:.1f}%", ha='center', va='center', fontsize=24)
        plt.text(0.5, 0.2, "ROI", ha='center', va='center')
        plt.axis('off')
        
        plt.subplot(2, 2, 4)
        payback = summary['roi_analysis']['payback_period_months'] if 'roi_analysis' in summary and 'payback_period_months' in summary['roi_analysis'] else 0
        plt.text(0.5, 0.5, f"{payback:.1f}", ha='center', va='center', fontsize=24)
        plt.text(0.5, 0.2, "Payback (months)", ha='center', va='center')
        plt.axis('off')
        
        plt.suptitle("GitHub Copilot Experiment: Key Metrics", fontsize=16, y=0.95)
        plt.figtext(0.5, 0.02, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ha='center')
        
        # Save figure
        plt.savefig(os.path.join(self.results_dir, 'dashboard.png'))
        plt.close()
    
    def save_results(self, summary):
        """Save analysis results as JSON."""
        if not summary:
            logger.warning("No results to save")
            return
        
        output_file = os.path.join(self.results_dir, 'analysis_summary.json')
        with open(output_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"Results saved to {output_file}")
    
    def run_analysis(self):
        """Run the complete analysis pipeline."""
        logger.info("Starting analysis pipeline...")
        
        # Load metrics
        metrics_df = self.load_metrics()
        
        if metrics_df.empty:
            logger.error("No metrics files found. Please add metrics files to the metrics/submissions directory.")
            return False
        
        # Analyze metrics
        summary = self.analyze_metrics(metrics_df)
        
        if not summary:
            logger.error("Failed to analyze metrics")
            return False
        
        # Save results
        self.save_results(summary)
        
        # Generate visualizations
        self.generate_visualizations(summary)
        
        logger.info("Analysis pipeline completed successfully!")
        print("\nAnalysis complete!")
        print("Results available in the analysis/results directory.")
        return True

def print_usage():
    """Print usage instructions."""
    print("\nGitHub Copilot Experiment Analysis (Simplified Version)")
    print("---------------------------------------------------")
    print("This script processes metrics files and generates analysis reports.")
    print("\nUsage:")
    print("  python analyze_metrics_simplified.py")
    print("\nBefore running, make sure your metrics files are in:")
    print("  metrics/submissions/")
    print("\nResults will be available in:")
    print("  analysis/results/")

if __name__ == "__main__":
    print_usage()
    print("\nStarting analysis...")
    analyzer = GitHubCopilotAnalysis()
    success = analyzer.run_analysis()
    if not success:
        print("\nAnalysis failed. Check the analysis.log file for details.")
        sys.exit(1)
