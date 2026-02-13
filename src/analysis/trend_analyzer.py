"""
Trend analysis module for weather data using linear regression.
"""
import numpy as np
from scipy.stats import t, linregress
import logging

logger = logging.getLogger(__name__)


class TrendAnalyzer:
    """
    Analyzer for calculating trends in time series data using linear regression.
    """

    def __init__(self, confidence_level=0.95):
        """
        Initialize trend analyzer.

        Parameters:
        -----------
        confidence_level : float
            Confidence level for confidence intervals (default: 0.95)
        """
        self.confidence_level = confidence_level
        self.alpha = 1 - confidence_level

    def calculate_seasonal_average(self, df, months, metric='temp_celsius'):
        """
        Calculate yearly average for specific months.

        Parameters:
        -----------
        df : pd.DataFrame
            Weather data with 'year', 'month', and metric columns
        months : list
            List of month numbers to include
        metric : str
            Column name for the metric to average

        Returns:
        --------
        pd.Series
            Yearly averages indexed by year
        """
        seasonal_data = df[df['month'].isin(months)]
        seasonal_data = seasonal_data.dropna(subset=[metric])
        yearly_avg = seasonal_data.groupby('year')[metric].mean()

        logger.info(f"Calculated seasonal average for months {months}, metric '{metric}': {len(yearly_avg)} years")
        return yearly_avg

    def linear_regression(self, years, values):
        """
        Perform linear regression using least squares method.

        Parameters:
        -----------
        years : array-like
            Year values (x-axis)
        values : array-like
            Metric values (y-axis)

        Returns:
        --------
        dict
            Dictionary containing regression results:
            - slope: regression slope
            - intercept: regression intercept
            - r_value: correlation coefficient
            - p_value: statistical significance
            - slope_se: standard error of slope
            - intercept_se: standard error of intercept
            - residual_std: standard deviation of residuals
            - slope_ci: 95% confidence interval for slope
            - intercept_ci: 95% confidence interval for intercept
        """
        x = np.array(years)
        y = np.array(values)
        n = len(x)

        if n < 3:
            logger.warning(f"Not enough data points ({n}) for reliable regression analysis")

        # Calculate means
        x_mean = np.mean(x)
        y_mean = np.mean(y)

        # Calculate slope and intercept using least squares
        Sxy = np.sum((x - x_mean) * (y - y_mean))
        Sxx = np.sum((x - x_mean) ** 2)

        slope = Sxy / Sxx if Sxx > 0 else 0
        intercept = y_mean - slope * x_mean

        # Calculate Pearson correlation coefficient
        r_num = np.sum((x - x_mean) * (y - y_mean))
        r_den = np.sqrt(np.sum((x - x_mean) ** 2) * np.sum((y - y_mean) ** 2))
        r_value = r_num / r_den if r_den != 0 else 0

        # Calculate p-value using t-distribution
        if n > 2 and abs(r_value) < 1:
            t_stat = r_value * np.sqrt((n - 2) / (1 - r_value ** 2))
            p_value = 2 * t.sf(np.abs(t_stat), df=n - 2)
        else:
            t_stat = 0
            p_value = 1

        # Calculate standard errors and confidence intervals
        y_pred = slope * x + intercept
        residuals = y - y_pred
        residual_std = np.sqrt(np.sum(residuals ** 2) / (n - 2)) if n > 2 else 0

        slope_se = residual_std / np.sqrt(Sxx) if Sxx > 0 and n > 2 else 0
        intercept_se = residual_std * np.sqrt(1 / n + x_mean ** 2 / Sxx) if Sxx > 0 and n > 2 else 0

        # 95% confidence intervals
        t_crit = t.ppf(1 - self.alpha / 2, df=n - 2) if n > 2 else 0
        slope_ci = (slope - t_crit * slope_se, slope + t_crit * slope_se)
        intercept_ci = (intercept - t_crit * intercept_se, intercept + t_crit * intercept_se)

        results = {
            'slope': slope,
            'intercept': intercept,
            'r_value': r_value,
            'p_value': p_value,
            'slope_se': slope_se,
            'intercept_se': intercept_se,
            'residual_std': residual_std,
            'slope_ci': slope_ci,
            'intercept_ci': intercept_ci,
            'n_points': n
        }

        logger.debug(f"Linear regression completed: slope={slope:.3f}, r={r_value:.3f}, p={p_value:.4f}")
        return results

    def scipy_linear_regression(self, years, values):
        """
        Perform linear regression using scipy's linregress for comparison.

        Parameters:
        -----------
        years : array-like
            Year values (x-axis)
        values : array-like
            Metric values (y-axis)

        Returns:
        --------
        dict
            Dictionary containing scipy regression results
        """
        try:
            x = np.array(years)
            y = np.array(values)
            res = linregress(x, y)

            results = {
                'slope': res.slope,
                'intercept': res.intercept,
                'r_value': res.rvalue,
                'p_value': res.pvalue,
                'stderr': res.stderr
            }

            logger.debug(f"Scipy regression: slope={res.slope:.3f}, r={res.rvalue:.3f}, p={res.pvalue:.4f}")
            return results
        except Exception as e:
            logger.error(f"Scipy linregress failed: {e}")
            return None

    def polynomial_regression(self, years, values, degree=2):
        """
        Perform polynomial regression.

        Parameters:
        -----------
        years : array-like
            Year values (x-axis)
        values : array-like
            Metric values (y-axis)
        degree : int
            Degree of polynomial (default: 2 for quadratic)

        Returns:
        --------
        dict
            Dictionary containing polynomial regression results:
            - coefficients: polynomial coefficients
            - r_squared: coefficient of determination
            - polynomial: numpy poly1d object
        """
        x = np.array(years)
        y = np.array(values)
        n = len(x)

        if n < degree + 1:
            logger.warning(f"Not enough data points ({n}) for degree {degree} polynomial")
            return None

        # Fit polynomial
        coefficients = np.polyfit(x, y, degree)
        poly = np.poly1d(coefficients)

        # Calculate R-squared
        y_pred = poly(x)
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0

        results = {
            'coefficients': coefficients,
            'r_squared': r_squared,
            'polynomial': poly,
            'degree': degree
        }

        logger.debug(f"Polynomial regression (degree {degree}): R²={r_squared:.3f}")
        return results

    def predict_value(self, slope, intercept, target_year):
        """
        Predict value for a future year using linear trend.

        Parameters:
        -----------
        slope : float
            Regression slope
        intercept : float
            Regression intercept
        target_year : int
            Year to predict for

        Returns:
        --------
        float
            Predicted value
        """
        prediction = slope * target_year + intercept
        logger.info(f"Predicted value for year {target_year}: {prediction:.2f}")
        return prediction

    def analyze_trend(self, years, values, label="Metric"):
        """
        Complete trend analysis with logging.

        Parameters:
        -----------
        years : array-like
            Year values
        values : array-like
            Metric values
        label : str
            Label for the metric being analyzed

        Returns:
        --------
        dict
            Complete analysis results from linear regression
        """
        logger.info(f"Analyzing trend for: {label}")

        # Perform linear regression
        results = self.linear_regression(years, values)

        # Log results
        logger.info(f"{label} regression: y = {results['slope']:.3f}x + {results['intercept']:.2f}")
        logger.info(
            f"Slope: {results['slope']:.3f} per year (95% CI: {results['slope_ci'][0]:.3f} to {results['slope_ci'][1]:.3f})")
        logger.info(
            f"Intercept: {results['intercept']:.2f} (95% CI: {results['intercept_ci'][0]:.2f} to {results['intercept_ci'][1]:.2f})")
        logger.info(f"Correlation coefficient r = {results['r_value']:.2f}")
        logger.info(f"P-value = {results['p_value']:.4f}")

        # Compare with scipy
        scipy_results = self.scipy_linear_regression(years, values)
        if scipy_results:
            logger.info(f"[scipy] regression: y = {scipy_results['slope']:.3f}x + {scipy_results['intercept']:.2f}")
            logger.info(f"[scipy] Slope: {scipy_results['slope']:.3f} per year")
            logger.info(f"[scipy] Intercept: {scipy_results['intercept']:.2f}")
            logger.info(f"[scipy] r = {scipy_results['r_value']:.2f}")
            logger.info(f"[scipy] p-value = {scipy_results['p_value']:.4f}")

        # Polynomial regression
        poly_results = self.polynomial_regression(years, values, degree=2)
        if poly_results:
            coefs = poly_results['coefficients']
            logger.info(f"[poly2] regression: y = {coefs[0]:.5f}x^2 + {coefs[1]:.3f}x + {coefs[2]:.2f}")
            logger.info(f"[poly2] R^2 = {poly_results['r_squared']:.3f}")

        results['scipy_results'] = scipy_results
        results['poly_results'] = poly_results

        return results