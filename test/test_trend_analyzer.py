"""
Unit tests for TrendAnalyzer.
"""
import pytest
import pandas as pd
import numpy as np
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from analysis import TrendAnalyzer


@pytest.fixture
def sample_time_series():
    """Create sample time series data for testing."""
    years = np.array([2015, 2016, 2017, 2018, 2019, 2020])
    # Linear trend: y = 0.5x + some_offset, with small noise
    values = 0.5 * years + 10 + np.random.randn(6) * 0.1
    return years, values


@pytest.fixture
def sample_dataframe():
    """Create sample DataFrame with weather data."""
    data = {
        'year': [2015, 2015, 2016, 2016, 2017, 2017],
        'month': [6, 7, 6, 7, 6, 7],
        'temp_celsius': [25.0, 26.0, 25.5, 26.5, 26.0, 27.0]
    }
    return pd.DataFrame(data)


class TestTrendAnalyzer:
    """Test suite for TrendAnalyzer."""

    def test_initialization(self):
        """Test analyzer initialization."""
        analyzer = TrendAnalyzer(confidence_level=0.95)
        assert analyzer.confidence_level == 0.95
        assert analyzer.alpha == 0.05

    def test_calculate_seasonal_average(self, sample_dataframe):
        """Test calculation of seasonal averages."""
        analyzer = TrendAnalyzer()

        # Calculate summer average (months 6, 7)
        summer_avg = analyzer.calculate_seasonal_average(
            sample_dataframe, [6, 7], 'temp_celsius'
        )

        assert len(summer_avg) == 3  # Three years
        assert 2015 in summer_avg.index
        assert 2016 in summer_avg.index
        assert 2017 in summer_avg.index

        # Check average for 2015: (25.0 + 26.0) / 2 = 25.5
        assert abs(summer_avg[2015] - 25.5) < 0.01

    def test_linear_regression_basic(self, sample_time_series):
        """Test basic linear regression."""
        analyzer = TrendAnalyzer()
        years, values = sample_time_series

        results = analyzer.linear_regression(years, values)

        # Check that all expected keys are present
        assert 'slope' in results
        assert 'intercept' in results
        assert 'r_value' in results
        assert 'p_value' in results
        assert 'slope_se' in results
        assert 'intercept_se' in results
        assert 'residual_std' in results
        assert 'slope_ci' in results
        assert 'intercept_ci' in results

        # Check that slope is approximately 0.5 (our test data)
        assert 0.4 < results['slope'] < 0.6

        # Check that correlation is high (close to 1)
        assert results['r_value'] > 0.9

    def test_linear_regression_perfect_fit(self):
        """Test linear regression with perfect linear data."""
        analyzer = TrendAnalyzer()

        years = np.array([2015, 2016, 2017, 2018, 2019])
        values = 2 * years + 5  # Perfect linear: y = 2x + 5

        results = analyzer.linear_regression(years, values)

        # Should have slope ≈ 2 and intercept ≈ 5
        assert abs(results['slope'] - 2.0) < 0.001
        assert abs(results['intercept'] - (2 * 2015 + 5)) < 0.001

        # Should have perfect correlation
        assert abs(results['r_value'] - 1.0) < 0.001

    def test_scipy_linear_regression(self, sample_time_series):
        """Test scipy linear regression."""
        analyzer = TrendAnalyzer()
        years, values = sample_time_series

        scipy_results = analyzer.scipy_linear_regression(years, values)

        assert scipy_results is not None
        assert 'slope' in scipy_results
        assert 'intercept' in scipy_results
        assert 'r_value' in scipy_results
        assert 'p_value' in scipy_results

    def test_polynomial_regression(self, sample_time_series):
        """Test polynomial regression."""
        analyzer = TrendAnalyzer()
        years, values = sample_time_series

        poly_results = analyzer.polynomial_regression(years, values, degree=2)

        assert poly_results is not None
        assert 'coefficients' in poly_results
        assert 'r_squared' in poly_results
        assert 'polynomial' in poly_results
        assert len(poly_results['coefficients']) == 3  # degree 2 = 3 coefficients
        assert 0 <= poly_results['r_squared'] <= 1

    def test_polynomial_regression_insufficient_data(self):
        """Test polynomial regression with insufficient data points."""
        analyzer = TrendAnalyzer()

        years = np.array([2015, 2016])
        values = np.array([10.0, 11.0])

        # Should return None for degree 2 with only 2 points
        poly_results = analyzer.polynomial_regression(years, values, degree=2)
        assert poly_results is None

    def test_predict_value(self):
        """Test value prediction."""
        analyzer = TrendAnalyzer()

        slope = 0.5
        intercept = 10.0
        target_year = 2025

        prediction = analyzer.predict_value(slope, intercept, target_year)

        expected = 0.5 * 2025 + 10.0
        assert abs(prediction - expected) < 0.001

    def test_analyze_trend_complete(self, sample_time_series):
        """Test complete trend analysis."""
        analyzer = TrendAnalyzer()
        years, values = sample_time_series

        results = analyzer.analyze_trend(years, values, label="Test Metric")

        # Check main results
        assert 'slope' in results
        assert 'intercept' in results
        assert 'r_value' in results
        assert 'p_value' in results

        # Check additional results
        assert 'scipy_results' in results
        assert 'poly_results' in results

        # Scipy results should be present
        assert results['scipy_results'] is not None

        # Poly results should be present (enough data points)
        assert results['poly_results'] is not None

    def test_confidence_intervals(self, sample_time_series):
        """Test that confidence intervals are reasonable."""
        analyzer = TrendAnalyzer(confidence_level=0.95)
        years, values = sample_time_series

        results = analyzer.linear_regression(years, values)

        slope_ci = results['slope_ci']
        intercept_ci = results['intercept_ci']

        # CI should be a tuple of (lower, upper)
        assert len(slope_ci) == 2
        assert len(intercept_ci) == 2

        # Lower bound should be less than upper bound
        assert slope_ci[0] < slope_ci[1]
        assert intercept_ci[0] < intercept_ci[1]

        # Slope should be within its CI
        assert slope_ci[0] <= results['slope'] <= slope_ci[1]