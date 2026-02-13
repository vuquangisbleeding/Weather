# Weather Trend Analysis

Analyze weather trends using Python, with features for statistical analysis, bootstrap resampling, visualization, and automated testing.

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Configuration](#configuration)
- [Testing](#testing)
- [Requirements](#requirements)
- [Contribution](#contribution)
- [Mathematical Explanations](#mathematical-explanations)

## Introduction
This project performs weather trend analysis (temperature, rainfall, etc.) based on historical data. It supports linear analysis, bootstrap for uncertainty estimation, statistical method comparison, and result visualization.

## Installation
1. Clone the repository:
	```bash
	git clone <repo-url>
	cd Weather
	```
2. Install required packages:
	```bash
	pip install -r requirements.txt
	```
3. (Optional) For interactive visualization, install Plotly:
	```bash
	pip install plotly
	```

## Interactive Visualization with Plotly
To view and interact with weather data:
1. Run the following script:
	```bash
	python plotly_interactive_weather.py
	```
2. A browser window will open with an interactive chart. Use the range slider to select date ranges, and interact with the legend to toggle variables.

## Project Structure
```
Weather/
├── main.py                  # Run basic trend analysis
├── main_with_bootstrap.py   # Run analysis with bootstrap
├── requirements.txt         # Required packages
├── config/
│   └── config.yaml          # Configuration file
├── data/
│   └── weather_data.csv     # Sample weather data
├── outputs/
│   ├── plots/               # Saved plots
│   └── reports/             # Saved reports
├── src/
│   ├── analysis/            # Analysis, bootstrap
│   ├── data/                # Data loading and processing
│   ├── utils/               # Config, logging utilities
│   └── visualization/       # Plotting
└── test/                    # Unit tests
```

## Usage
### 1. Basic trend analysis
```bash
python main.py
```
### 2. Trend analysis with bootstrap
```bash
python main_with_bootstrap.py
```
Results will be saved in the `outputs/plots/` directory.

## Configuration
Edit the file `config/config.yaml` to change:
- Input data path
- Bootstrap parameters (number of iterations, seed, ...)
- Statistical significance/confidence levels
- Prediction year, summer/winter months

Example:
```yaml
data:
  input_file: "data/weather_data.csv"
  date_column: "date"
analysis:
  summer_months: [6, 7, 8]
  winter_months: [12, 1, 2]
  confidence_level: 0.95
  significance_level: 0.05
  prediction_year: 2030
  bootstrap:
	 enabled: true
	 n_iterations: 10000
	 random_seed: 42
	 compare_methods: true
output:
  plots_dir: "outputs/plots"
```

## Testing
Run all unit tests with pytest:
```bash
pytest --maxfail=1 --disable-warnings -q
```

## Requirements
- Python >= 3.8
- Packages: pandas, numpy, matplotlib, scipy, pyyaml, pytest, pytest-cov, (optional: plotly)

## Contribution
All contributions, bug reports, or improvement ideas are welcome!

## Mathematical Explanations

### 1. Linear Regression
Used to find the best-fit line $y = a x + b$ describing the trend between year (x) and weather metric (y).

**Coefficient formulas:**
$$
a = \frac{\sum_{i=1}^n (x_i - \bar{x})(y_i - \bar{y})}{\sum_{i=1}^n (x_i - \bar{x})^2} \\
b = \bar{y} - a \bar{x}
$$
where $\bar{x}$, $\bar{y}$ are the means of x and y.

**Pearson correlation coefficient:**
$$
r = \frac{\sum_{i=1}^n (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum_{i=1}^n (x_i - \bar{x})^2 \sum_{i=1}^n (y_i - \bar{y})^2}}
$$

### 2. Statistical Significance Testing (p-value, confidence interval)
- **p-value**: Probability of observing the result if the true slope is zero. If p < 0.05, the trend is significant.
- **95% confidence interval for slope:**
$$
CI = [a - t_{\alpha/2} \cdot SE_a,\ a + t_{\alpha/2} \cdot SE_a]
$$
where $SE_a$ is the standard error of the slope, $t_{\alpha/2}$ is the t-distribution critical value.

### 3. Bootstrap Resampling
Repeatedly resample (with replacement) from the original data (e.g., 10,000 times), compute regression coefficients each time, and use the empirical distribution to estimate confidence intervals and standard errors without normality assumptions.

**Bootstrap confidence interval:**
$$
CI = [\text{percentile}_{2.5\%},\ \text{percentile}_{97.5\%}]
$$

### 4. Visualization
- **Scatter plot**: Shows actual data points.
- **Trend line**: Linear or quadratic regression line.
- **Confidence band**: Confidence region around the trend line.
- **Residuals plot**: Plot of residuals to check model assumptions.
- **Bootstrap distribution**: Empirical distribution of regression coefficients.
- **Scatter plot**: Shows actual data points.

## Contribution
All contributions, bug reports, or improvement ideas are welcome!
