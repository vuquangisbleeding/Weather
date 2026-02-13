"""
Visualization module for weather trend analysis.
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t
import logging
import os

logger = logging.getLogger(__name__)


class TrendVisualizer:
    """
    Visualizer for trend analysis plots.
    """

    def __init__(self, output_dir='outputs/plots', save_plots=True, show_plots=False,
                 plot_format='png', dpi=300, figsize=(10, 6)):
        """
        Initialize trend visualizer.

        Parameters:
        -----------
        output_dir : str
            Directory to save plots
        save_plots : bool
            Whether to save plots to files
        show_plots : bool
            Whether to display plots interactively
        plot_format : str
            Format for saved plots (png, jpg, pdf, etc.)
        dpi : int
            DPI for saved plots
        figsize : tuple
            Figure size (width, height) in inches
        """
        self.output_dir = output_dir
        self.save_plots = save_plots
        self.show_plots = show_plots
        self.plot_format = plot_format
        self.dpi = dpi
        self.figsize = figsize

        # Create output directory if needed
        if self.save_plots:
            os.makedirs(self.output_dir, exist_ok=True)

    def plot_trend_analysis(self, years, values, regression_results, label, ylabel,
                            confidence_level=0.95):
        """
        Create comprehensive trend analysis plot with linear and quadratic fits.

        Parameters:
        -----------
        years : array-like
            Year values
        values : array-like
            Metric values
        regression_results : dict
            Results from TrendAnalyzer containing slope, intercept, etc.
        label : str
            Label for the plot
        ylabel : str
            Y-axis label
        confidence_level : float
            Confidence level for confidence bands
        """
        x = np.array(years)
        y = np.array(values)
        n = len(x)

        slope = regression_results['slope']
        intercept = regression_results['intercept']
        residual_std = regression_results['residual_std']
        poly_results = regression_results.get('poly_results')

        # Create figure
        fig, ax = plt.subplots(figsize=self.figsize)

        # Scatter plot of actual data
        ax.scatter(x, y, label=f'Avg {label}', s=50, alpha=0.7, zorder=3)

        # Linear trend line
        y_pred = slope * x + intercept
        ax.plot(x, y_pred, color='red', linewidth=2, label='Linear Trend', zorder=2)

        # Quadratic trend line (if available)
        if poly_results and n >= 3:
            poly = poly_results['polynomial']
            x_dense = np.linspace(np.min(x), np.max(x), 200)
            ax.plot(x_dense, poly(x_dense), color='green', linestyle='--',
                    linewidth=2, label='Quadratic Trend', zorder=2)

        # Confidence band
        if n > 2:
            alpha = 1 - confidence_level
            t_crit = t.ppf(1 - alpha / 2, df=n - 2)
            Sxx = np.sum((x - np.mean(x)) ** 2)

            if Sxx > 0:
                conf_band = t_crit * residual_std * np.sqrt(1 / n + (x - np.mean(x)) ** 2 / Sxx)
                ax.fill_between(x, y_pred - conf_band, y_pred + conf_band,
                                color='orange', alpha=0.2,
                                label=f'{int(confidence_level * 100)}% Confidence Band', zorder=1)

        # Labels and formatting
        ax.set_xlabel('Year', fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.set_title(f'{label} Trend', fontsize=14, fontweight='bold')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        # Save plot
        if self.save_plots:
            filename = f"{label.lower().replace(' ', '_')}_trend.{self.plot_format}"
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=self.dpi, bbox_inches='tight')
            logger.info(f"Saved plot: {filepath}")

        # Show plot
        if self.show_plots:
            plt.show()
        else:
            plt.close()

    def plot_residuals(self, years, values, regression_results, label):
        """
        Create residuals plot.

        Parameters:
        -----------
        years : array-like
            Year values
        values : array-like
            Metric values
        regression_results : dict
            Results from TrendAnalyzer
        label : str
            Label for the plot
        """
        x = np.array(years)
        y = np.array(values)

        slope = regression_results['slope']
        intercept = regression_results['intercept']

        # Calculate residuals
        y_pred = slope * x + intercept
        residuals = y - y_pred

        # Create figure
        fig, ax = plt.subplots(figsize=self.figsize)

        # Scatter plot of residuals
        ax.scatter(x, residuals, color='purple', s=50, alpha=0.7, label='Residuals')
        ax.axhline(0, color='gray', linestyle='--', linewidth=2)

        # Labels and formatting
        ax.set_xlabel('Year', fontsize=12)
        ax.set_ylabel('Residual', fontsize=12)
        ax.set_title(f'{label} Residuals', fontsize=14, fontweight='bold')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        # Save plot
        if self.save_plots:
            filename = f"{label.lower().replace(' ', '_')}_residuals.{self.plot_format}"
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=self.dpi, bbox_inches='tight')
            logger.info(f"Saved plot: {filepath}")

        # Show plot
        if self.show_plots:
            plt.show()
        else:
            plt.close()

    def create_all_plots(self, years, values, regression_results, label, ylabel,
                         confidence_level=0.95):
        """
        Create both trend analysis and residuals plots.

        Parameters:
        -----------
        years : array-like
            Year values
        values : array-like
            Metric values
        regression_results : dict
            Results from TrendAnalyzer
        label : str
            Label for the plots
        ylabel : str
            Y-axis label for trend plot
        confidence_level : float
            Confidence level for confidence bands
        """
        logger.info(f"Creating plots for {label}")
        self.plot_trend_analysis(years, values, regression_results, label, ylabel, confidence_level)
        self.plot_residuals(years, values, regression_results, label)