viz.plot_trend_analysis(years, avg_temps, regression_results, label='Summer Temp', ylabel='Temperature (°C)')
viz.plot_residuals(years, avg_temps, regression_results, label='Summer Temp')
viz.plot_bootstrap_distribution(bootstrap_results, parameter_name='slope', label='Slope', units='°C/year')

# Report: Multiple Visualization Types in the Project

## 1. Concept
- **Scatter plot with trend line**: Plots actual data points with a linear (and optionally quadratic) regression line.
- **Residuals plot**: Plots the residuals (difference between actual and predicted values), helping to check model assumptions.
- **Confidence bands**: Confidence region around the regression line, showing prediction uncertainty.
- **Bootstrap distribution**: Histogram of regression parameters from bootstrap, illustrating non-parametric uncertainty.

## 2. Usage in This Project
The project implements various visualization types, specifically:

- **TrendVisualizer class (src/visualization/trend_plotter.py):**
  - `plot_trend_analysis`: Plots scatter, linear trend line, quadratic trend line (if available), and confidence band.
  - `plot_residuals`: Plots residuals for each year.
- **BootstrapVisualizer class (src/visualization/bootstrap_plotter.py):**
  - `plot_bootstrap_distribution`: Plots histogram of bootstrap distribution for slope/intercept, with mean and confidence interval.
  - `plot_prediction_uncertainty`: Plots trend line with bootstrap uncertainty band.

All plots are automatically saved to the `outputs/plots/` directory.

## 3. Example
Example using TrendVisualizer to plot temperature trends:
```python
from visualization import TrendVisualizer
viz = TrendVisualizer(output_dir='outputs/plots', save_plots=True)
viz.plot_trend_analysis(years, avg_temps, regression_results, label='Summer Temp', ylabel='Temperature (°C)')
viz.plot_residuals(years, avg_temps, regression_results, label='Summer Temp')
```

Example using BootstrapVisualizer to plot bootstrap distribution:
```python
from visualization import BootstrapVisualizer
viz = BootstrapVisualizer(output_dir='outputs/plots', save_plots=True)
viz.plot_bootstrap_distribution(bootstrap_results, parameter_name='slope', label='Slope', units='°C/year')
```

## 4. Meaning and Advantages
- **Comprehensive, multi-dimensional visual analysis**: Not only shows trends but also checks assumptions and uncertainty.
- **Easily detect anomalies and check model quality.**
- **Supports comparison between methods (parametric vs bootstrap).**
- **Automatically saved, easy to integrate into reports or dashboards.**

## 5. Conclusion
The project provides a diverse, modern visualization system, helping users deeply understand the data, models, and reliability of weather trend analysis results.

---
*Report auto-generated on 13/02/2026.*
