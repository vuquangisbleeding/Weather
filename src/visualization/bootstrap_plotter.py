"""
Visualization module for bootstrap resampling results.
"""
import numpy as np
import matplotlib.pyplot as plt
import logging
import os

logger = logging.getLogger(__name__)


class BootstrapVisualizer:
    """
    Visualizer for bootstrap analysis results.
    """

    def __init__(self, output_dir='outputs/plots', save_plots=True, show_plots=False,
                 plot_format='png', dpi=300, figsize=(10, 6)):
        """
        Initialize bootstrap visualizer.

        Parameters:
        -----------
        output_dir : str
            Directory to save plots
        save_plots : bool
            Whether to save plots to files
        show_plots : bool
            Whether to display plots interactively
        plot_format : str
            Format for saved plots
        dpi : int
            DPI for saved plots
        figsize : tuple
            Figure size (width, height)
        """
        self.output_dir = output_dir
        self.save_plots = save_plots
        self.show_plots = show_plots
        self.plot_format = plot_format
        self.dpi = dpi
        self.figsize = figsize

        if self.save_plots:
            os.makedirs(self.output_dir, exist_ok=True)

    def plot_bootstrap_distribution(self, bootstrap_results, parameter_name='slope',
                                    label='Parameter', units='units/year'):
        """
        Plot histogram of bootstrap distribution with confidence intervals.

        Parameters:
        -----------
        bootstrap_results : dict
            Results from BootstrapAnalyzer
        parameter_name : str
            'slope' or 'intercept'
        label : str
            Label for the plot
        units : str
            Units for the parameter
        """
        if parameter_name == 'slope':
            values = bootstrap_results['slopes']
            mean = bootstrap_results['slope_mean']
            ci = bootstrap_results['slope_ci']
        else:
            values = bootstrap_results['intercepts']
            mean = bootstrap_results['intercept_mean']
            ci = bootstrap_results['intercept_ci']

        fig, ax = plt.subplots(figsize=self.figsize)

        # Histogram
        n_bins = min(50, len(values) // 100)
        ax.hist(values, bins=n_bins, density=True, alpha=0.7, color='skyblue',
                edgecolor='black', label='Bootstrap Distribution')

        # Mean line
        ax.axvline(mean, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean:.4f}')

        # Confidence interval
        ax.axvline(ci[0], color='orange', linestyle=':', linewidth=2,
                   label=f'95% CI: [{ci[0]:.4f}, {ci[1]:.4f}]')
        ax.axvline(ci[1], color='orange', linestyle=':', linewidth=2)

        # Shading for CI
        ax.axvspan(ci[0], ci[1], alpha=0.2, color='orange')

        ax.set_xlabel(f'{label} ({units})', fontsize=12)
        ax.set_ylabel('Density', fontsize=12)
        ax.set_title(f'Bootstrap Distribution of {label}', fontsize=14, fontweight='bold')
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        if self.save_plots:
            filename = f"bootstrap_{label.lower().replace(' ', '_')}_{parameter_name}.{self.plot_format}"
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=self.dpi, bbox_inches='tight')
            logger.info(f"Saved bootstrap distribution plot: {filepath}")

        if self.show_plots:
            plt.show()
        else:
            plt.close()

    def plot_prediction_uncertainty(self, years, values, bootstrap_pred_results,
                                    regression_results, label='Metric', ylabel='Value'):
        """
        Plot trend with bootstrap prediction uncertainty.

        Parameters:
        -----------
        years : array-like
            Original year values
        values : array-like
            Original metric values
        bootstrap_pred_results : dict
            Results from bootstrap_prediction
        regression_results : dict
            Results from linear_regression
        label : str
            Label for the plot
        ylabel : str
            Y-axis label
        """
        x = np.array(years)
        y = np.array(values)
        target_year = bootstrap_pred_results['target_year']
        pred_mean = bootstrap_pred_results['mean']
        pred_ci = bootstrap_pred_results['ci']

        slope = regression_results['slope']
        intercept = regression_results['intercept']

        fig, ax = plt.subplots(figsize=self.figsize)

        # Original data
        ax.scatter(x, y, s=100, alpha=0.7, label='Observed Data', zorder=3)

        # Regression line
        x_line = np.array([x.min(), target_year])
        y_line = slope * x_line + intercept
        ax.plot(x_line, y_line, 'r-', linewidth=2, label='Trend Line', zorder=2)

        # Prediction point with uncertainty
        ax.scatter([target_year], [pred_mean], s=200, marker='*', color='orange',
                   edgecolor='black', linewidth=1.5, label=f'Prediction {target_year}', zorder=4)

        # Prediction confidence interval (vertical line)
        ax.plot([target_year, target_year], [pred_ci[0], pred_ci[1]],
                color='orange', linewidth=3, label='95% Prediction CI', zorder=3)

        # Add error bar caps
        cap_width = (target_year - x.min()) * 0.02
        ax.plot([target_year - cap_width, target_year + cap_width], [pred_ci[0], pred_ci[0]],
                color='orange', linewidth=2)
        ax.plot([target_year - cap_width, target_year + cap_width], [pred_ci[1], pred_ci[1]],
                color='orange', linewidth=2)

        # Annotations
        ax.text(target_year, pred_mean, f'  {pred_mean:.2f}',
                fontsize=10, va='center', fontweight='bold')

        ax.set_xlabel('Year', fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.set_title(f'{label} with Bootstrap Prediction Uncertainty', fontsize=14, fontweight='bold')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        if self.save_plots:
            filename = f"bootstrap_prediction_{label.lower().replace(' ', '_')}.{self.plot_format}"
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=self.dpi, bbox_inches='tight')
            logger.info(f"Saved bootstrap prediction plot: {filepath}")

        if self.show_plots:
            plt.show()
        else:
            plt.close()

    def plot_method_comparison(self, comparison_results, label='Slope'):
        """
        Plot comparison between parametric and bootstrap confidence intervals.

        Parameters:
        -----------
        comparison_results : dict
            Results from compare_methods
        label : str
            Label for the plot
        """
        param = comparison_results['parametric']
        boot = comparison_results['bootstrap']

        fig, ax = plt.subplots(figsize=(8, 6))

        # Method labels and positions
        methods = ['Parametric\n(t-distribution)', 'Bootstrap\n(Resampling)']
        positions = [1, 2]

        # Point estimates
        estimates = [param['slope'], boot['slope']]
        ax.scatter(positions, estimates, s=200, color=['blue', 'green'],
                   marker='o', label='Point Estimate', zorder=3)

        # Confidence intervals
        param_ci = param['slope_ci']
        boot_ci = boot['slope_ci']

        ax.plot([1, 1], [param_ci[0], param_ci[1]], color='blue', linewidth=3,
                label='95% CI (Parametric)')
        ax.plot([2, 2], [boot_ci[0], boot_ci[1]], color='green', linewidth=3,
                label='95% CI (Bootstrap)')

        # Error bar caps
        cap_width = 0.1
        for pos, ci, color in [(1, param_ci, 'blue'), (2, boot_ci, 'green')]:
            ax.plot([pos - cap_width, pos + cap_width], [ci[0], ci[0]],
                    color=color, linewidth=2)
            ax.plot([pos - cap_width, pos + cap_width], [ci[1], ci[1]],
                    color=color, linewidth=2)

        # Add values as text
        ax.text(1, param['slope'], f"  {param['slope']:.4f}", va='center', fontsize=9)
        ax.text(2, boot['slope'], f"  {boot['slope']:.4f}", va='center', fontsize=9)

        ax.set_xticks(positions)
        ax.set_xticklabels(methods, fontsize=11)
        ax.set_ylabel(f'{label} Estimate', fontsize=12)
        ax.set_title(f'Comparison: Parametric vs Bootstrap Methods', fontsize=14, fontweight='bold')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3, axis='y')

        # Add ratio text
        ratio = comparison_results['ci_width_ratio']
        ax.text(1.5, ax.get_ylim()[1] * 0.95,
                f'Bootstrap/Parametric CI width ratio: {ratio:.3f}',
                ha='center', fontsize=10, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        plt.tight_layout()

        if self.save_plots:
            filename = f"bootstrap_comparison_{label.lower()}.{self.plot_format}"
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=self.dpi, bbox_inches='tight')
            logger.info(f"Saved bootstrap comparison plot: {filepath}")

        if self.show_plots:
            plt.show()
        else:
            plt.close()

    def plot_bootstrap_slopes_scatter(self, bootstrap_results, parametric_slope,
                                      label='Parameter'):
        """
        Plot scatter of bootstrap slope estimates.

        Parameters:
        -----------
        bootstrap_results : dict
            Bootstrap results
        parametric_slope : float
            Original parametric slope estimate
        label : str
            Label for plot
        """
        slopes = bootstrap_results['slopes']

        fig, ax = plt.subplots(figsize=self.figsize)

        # Scatter plot with jitter
        iterations = np.arange(len(slopes))
        ax.scatter(iterations, slopes, alpha=0.3, s=1, color='steelblue')

        # Mean line
        ax.axhline(bootstrap_results['slope_mean'], color='red', linestyle='--',
                   linewidth=2, label=f"Bootstrap Mean: {bootstrap_results['slope_mean']:.4f}")

        # Parametric estimate
        ax.axhline(parametric_slope, color='green', linestyle=':', linewidth=2,
                   label=f"Parametric: {parametric_slope:.4f}")

        # Confidence interval band
        ci = bootstrap_results['slope_ci']
        ax.axhspan(ci[0], ci[1], alpha=0.2, color='orange', label='95% CI')

        ax.set_xlabel('Bootstrap Iteration', fontsize=12)
        ax.set_ylabel(f'{label} Estimate', fontsize=12)
        ax.set_title(f'Bootstrap {label} Estimates Across Iterations', fontsize=14, fontweight='bold')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        if self.save_plots:
            filename = f"bootstrap_scatter_{label.lower().replace(' ', '_')}.{self.plot_format}"
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=self.dpi, bbox_inches='tight')
            logger.info(f"Saved bootstrap scatter plot: {filepath}")

        if self.show_plots:
            plt.show()
        else:
            plt.close()