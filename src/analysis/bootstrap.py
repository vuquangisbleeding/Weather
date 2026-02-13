"""
Bootstrap resampling module for uncertainty estimation in trend analysis.

Bootstrap resampling is a statistical technique that estimates the sampling
distribution of a statistic by repeatedly resampling with replacement from
the original data. This allows us to:
- Estimate confidence intervals without parametric assumptions
- Assess the stability of our trend estimates
- Quantify uncertainty in predictions
"""
import numpy as np
import logging
from typing import Tuple, Dict, List

logger = logging.getLogger(__name__)


class BootstrapAnalyzer:
    """
    Bootstrap resampling analyzer for trend analysis.

    Bootstrap resampling works by:
    1. Repeatedly sampling (with replacement) from the original data
    2. Calculating the statistic (e.g., slope) for each resampled dataset
    3. Using the distribution of these statistics to estimate uncertainty

    This is particularly useful when:
    - Sample sizes are small
    - We don't want to assume normality
    - We want robust confidence intervals
    """

    def __init__(self, n_bootstrap=10000, confidence_level=0.95, random_seed=None):
        """
        Initialize bootstrap analyzer.

        Parameters:
        -----------
        n_bootstrap : int
            Number of bootstrap iterations (default: 10000)
            More iterations = more accurate estimates but slower
        confidence_level : float
            Confidence level for intervals (default: 0.95)
        random_seed : int, optional
            Random seed for reproducibility
        """
        self.n_bootstrap = n_bootstrap
        self.confidence_level = confidence_level
        self.random_seed = random_seed

        if random_seed is not None:
            np.random.seed(random_seed)

    def bootstrap_linear_regression(self, years, values) -> Dict:
        """
        Perform bootstrap resampling for linear regression.

        The bootstrap process:
        1. For each iteration (e.g., 10000 times):
           - Randomly sample n points with replacement from (years, values)
           - Calculate slope and intercept for this sample
        2. Use the distribution of 10000 slopes to estimate:
           - Mean slope (point estimate)
           - Confidence interval (percentile method)
           - Standard error

        Parameters:
        -----------
        years : array-like
            Year values (x-axis)
        values : array-like
            Metric values (y-axis)

        Returns:
        --------
        dict
            Dictionary containing:
            - slopes: array of bootstrap slope estimates
            - intercepts: array of bootstrap intercept estimates
            - slope_mean: mean of bootstrap slopes
            - slope_ci: bootstrap confidence interval for slope
            - intercept_mean: mean of bootstrap intercepts
            - intercept_ci: bootstrap confidence interval for intercept
            - slope_se: bootstrap standard error of slope
            - intercept_se: bootstrap standard error of intercept
        """
        x = np.array(years)
        y = np.array(values)
        n = len(x)

        logger.info(f"Starting bootstrap with {self.n_bootstrap} iterations...")

        # Arrays to store bootstrap estimates
        bootstrap_slopes = np.zeros(self.n_bootstrap)
        bootstrap_intercepts = np.zeros(self.n_bootstrap)

        # Bootstrap resampling
        for i in range(self.n_bootstrap):
            # Sample with replacement
            indices = np.random.choice(n, size=n, replace=True)
            x_boot = x[indices]
            y_boot = y[indices]

            # Calculate regression for this bootstrap sample
            x_mean = np.mean(x_boot)
            y_mean = np.mean(y_boot)

            Sxy = np.sum((x_boot - x_mean) * (y_boot - y_mean))
            Sxx = np.sum((x_boot - x_mean) ** 2)

            if Sxx > 0:
                slope = Sxy / Sxx
                intercept = y_mean - slope * x_mean
            else:
                slope = 0
                intercept = y_mean

            bootstrap_slopes[i] = slope
            bootstrap_intercepts[i] = intercept

            # Progress logging
            if (i + 1) % 1000 == 0:
                logger.debug(f"Bootstrap iteration {i + 1}/{self.n_bootstrap}")

        # Calculate statistics from bootstrap distribution
        alpha = 1 - self.confidence_level

        slope_mean = np.mean(bootstrap_slopes)
        slope_ci = np.percentile(bootstrap_slopes, [alpha / 2 * 100, (1 - alpha / 2) * 100])
        slope_se = np.std(bootstrap_slopes)

        intercept_mean = np.mean(bootstrap_intercepts)
        intercept_ci = np.percentile(bootstrap_intercepts, [alpha / 2 * 100, (1 - alpha / 2) * 100])
        intercept_se = np.std(bootstrap_intercepts)

        results = {
            'slopes': bootstrap_slopes,
            'intercepts': bootstrap_intercepts,
            'slope_mean': slope_mean,
            'slope_ci': slope_ci,
            'intercept_mean': intercept_mean,
            'intercept_ci': intercept_ci,
            'slope_se': slope_se,
            'intercept_se': intercept_se,
            'n_bootstrap': self.n_bootstrap
        }

        logger.info(f"Bootstrap completed: slope = {slope_mean:.3f} "
                    f"(95% CI: {slope_ci[0]:.3f} to {slope_ci[1]:.3f})")

        return results

    def bootstrap_prediction(self, years, values, target_year) -> Dict:
        """
        Bootstrap prediction for a future year with uncertainty.

        This estimates the uncertainty in our prediction by:
        1. For each bootstrap sample, calculate slope and intercept
        2. Use each to make a prediction for target_year
        3. The distribution of predictions gives us uncertainty

        Parameters:
        -----------
        years : array-like
            Year values
        values : array-like
            Metric values
        target_year : int
            Year to predict for

        Returns:
        --------
        dict
            Dictionary containing:
            - predictions: array of bootstrap predictions
            - mean: mean prediction
            - ci: confidence interval for prediction
            - se: standard error of prediction
        """
        x = np.array(years)
        y = np.array(values)
        n = len(x)

        logger.info(f"Bootstrap prediction for year {target_year}...")

        bootstrap_predictions = np.zeros(self.n_bootstrap)

        for i in range(self.n_bootstrap):
            # Bootstrap resample
            indices = np.random.choice(n, size=n, replace=True)
            x_boot = x[indices]
            y_boot = y[indices]

            # Calculate regression
            x_mean = np.mean(x_boot)
            y_mean = np.mean(y_boot)

            Sxy = np.sum((x_boot - x_mean) * (y_boot - y_mean))
            Sxx = np.sum((x_boot - x_mean) ** 2)

            if Sxx > 0:
                slope = Sxy / Sxx
                intercept = y_mean - slope * x_mean
            else:
                slope = 0
                intercept = y_mean

            # Make prediction
            prediction = slope * target_year + intercept
            bootstrap_predictions[i] = prediction

        # Calculate statistics
        alpha = 1 - self.confidence_level

        mean_pred = np.mean(bootstrap_predictions)
        ci_pred = np.percentile(bootstrap_predictions, [alpha / 2 * 100, (1 - alpha / 2) * 100])
        se_pred = np.std(bootstrap_predictions)

        results = {
            'predictions': bootstrap_predictions,
            'mean': mean_pred,
            'ci': ci_pred,
            'se': se_pred,
            'target_year': target_year
        }

        logger.info(f"Prediction for {target_year}: {mean_pred:.2f} "
                    f"(95% CI: {ci_pred[0]:.2f} to {ci_pred[1]:.2f})")

        return results

    def bootstrap_r_squared(self, years, values) -> Dict:
        """
        Bootstrap R-squared values to assess model fit uncertainty.

        Parameters:
        -----------
        years : array-like
            Year values
        values : array-like
            Metric values

        Returns:
        --------
        dict
            Dictionary containing:
            - r_squared_values: array of bootstrap R² values
            - mean: mean R²
            - ci: confidence interval for R²
            - se: standard error of R²
        """
        x = np.array(years)
        y = np.array(values)
        n = len(x)

        bootstrap_r2 = np.zeros(self.n_bootstrap)

        for i in range(self.n_bootstrap):
            # Bootstrap resample
            indices = np.random.choice(n, size=n, replace=True)
            x_boot = x[indices]
            y_boot = y[indices]

            # Calculate regression
            x_mean = np.mean(x_boot)
            y_mean = np.mean(y_boot)

            Sxy = np.sum((x_boot - x_mean) * (y_boot - y_mean))
            Sxx = np.sum((x_boot - x_mean) ** 2)
            Syy = np.sum((y_boot - y_mean) ** 2)

            if Sxx > 0 and Syy > 0:
                r = Sxy / np.sqrt(Sxx * Syy)
                r2 = r ** 2
            else:
                r2 = 0

            bootstrap_r2[i] = r2

        # Calculate statistics
        alpha = 1 - self.confidence_level

        mean_r2 = np.mean(bootstrap_r2)
        ci_r2 = np.percentile(bootstrap_r2, [alpha / 2 * 100, (1 - alpha / 2) * 100])
        se_r2 = np.std(bootstrap_r2)

        results = {
            'r_squared_values': bootstrap_r2,
            'mean': mean_r2,
            'ci': ci_r2,
            'se': se_r2
        }

        logger.info(f"Bootstrap R²: {mean_r2:.3f} (95% CI: {ci_r2[0]:.3f} to {ci_r2[1]:.3f})")

        return results

    def compare_methods(self, years, values) -> Dict:
        """
        Compare parametric (t-distribution) vs bootstrap confidence intervals.

        This helps us understand:
        - How robust are parametric assumptions?
        - Is the bootstrap CI wider or narrower?
        - Are the methods giving similar results?

        Parameters:
        -----------
        years : array-like
            Year values
        values : array-like
            Metric values

        Returns:
        --------
        dict
            Comparison of parametric vs bootstrap methods
        """
        from scipy.stats import linregress, t

        x = np.array(years)
        y = np.array(values)
        n = len(x)

        # Parametric method (from scipy)
        res = linregress(x, y)

        # Calculate parametric CI
        x_mean = np.mean(x)
        Sxx = np.sum((x - x_mean) ** 2)
        y_pred = res.slope * x + res.intercept
        residuals = y - y_pred
        residual_std = np.sqrt(np.sum(residuals ** 2) / (n - 2))
        slope_se_param = residual_std / np.sqrt(Sxx)

        alpha = 1 - self.confidence_level
        t_crit = t.ppf(1 - alpha / 2, df=n - 2)
        slope_ci_param = (res.slope - t_crit * slope_se_param,
                          res.slope + t_crit * slope_se_param)

        # Bootstrap method
        bootstrap_results = self.bootstrap_linear_regression(years, values)

        comparison = {
            'parametric': {
                'slope': res.slope,
                'slope_ci': slope_ci_param,
                'slope_se': slope_se_param
            },
            'bootstrap': {
                'slope': bootstrap_results['slope_mean'],
                'slope_ci': bootstrap_results['slope_ci'],
                'slope_se': bootstrap_results['slope_se']
            },
            'ci_width_ratio': (bootstrap_results['slope_ci'][1] - bootstrap_results['slope_ci'][0]) /
                              (slope_ci_param[1] - slope_ci_param[0])
        }

        logger.info("=== Method Comparison ===")
        logger.info(f"Parametric CI width: {slope_ci_param[1] - slope_ci_param[0]:.6f}")
        logger.info(f"Bootstrap CI width: {bootstrap_results['slope_ci'][1] - bootstrap_results['slope_ci'][0]:.6f}")
        logger.info(f"Ratio (Bootstrap/Parametric): {comparison['ci_width_ratio']:.3f}")

        return comparison