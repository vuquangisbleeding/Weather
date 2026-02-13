"""
Unit tests for BootstrapAnalyzer.
"""
import pytest
import numpy as np
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from analysis import BootstrapAnalyzer


@pytest.fixture
def sample_linear_data():
    """Create sample linear data for testing."""
    np.random.seed(42)
    years = np.array([2015, 2016, 2017, 2018, 2019, 2020])
    # Linear trend with small noise
    values = 0.5 * years - 980 + np.random.randn(6) * 0.1
    return years, values


@pytest.fixture
def perfect_linear_data():
    """Create perfect linear data (no noise) for testing."""
    years = np.array([2015, 2016, 2017, 2018, 2019, 2020])
    values = 0.5 * years - 980
    return years, values


class TestBootstrapAnalyzer:
    """Test suite for BootstrapAnalyzer."""

    def test_initialization(self):
        """Test bootstrap analyzer initialization."""
        analyzer = BootstrapAnalyzer(n_bootstrap=1000, confidence_level=0.95, random_seed=42)
        assert analyzer.n_bootstrap == 1000
        assert analyzer.confidence_level == 0.95
        assert analyzer.random_seed == 42

    def test_bootstrap_linear_regression_structure(self, sample_linear_data):
        """Test that bootstrap returns correct structure."""
        analyzer = BootstrapAnalyzer(n_bootstrap=100, random_seed=42)
        years, values = sample_linear_data

        results = analyzer.bootstrap_linear_regression(years, values)

        # Check all required keys present
        assert 'slopes' in results
        assert 'intercepts' in results
        assert 'slope_mean' in results
        assert 'slope_ci' in results
        assert 'intercept_mean' in results
        assert 'intercept_ci' in results
        assert 'slope_se' in results
        assert 'intercept_se' in results
        assert 'n_bootstrap' in results

        # Check correct lengths
        assert len(results['slopes']) == 100
        assert len(results['intercepts']) == 100
        assert len(results['slope_ci']) == 2
        assert len(results['intercept_ci']) == 2

    def test_bootstrap_slope_estimate(self, perfect_linear_data):
        """Test that bootstrap slope is close to true slope."""
        analyzer = BootstrapAnalyzer(n_bootstrap=1000, random_seed=42)
        years, values = perfect_linear_data

        results = analyzer.bootstrap_linear_regression(years, values)

        # With perfect linear data, bootstrap slope should be very close to 0.5
        assert abs(results['slope_mean'] - 0.5) < 0.01

    def test_bootstrap_confidence_intervals(self, sample_linear_data):
        """Test that confidence intervals are reasonable."""
        analyzer = BootstrapAnalyzer(n_bootstrap=1000, random_seed=42)
        years, values = sample_linear_data

        results = analyzer.bootstrap_linear_regression(years, values)

        slope_ci = results['slope_ci']
        intercept_ci = results['intercept_ci']

        # Lower bound < upper bound
        assert slope_ci[0] < slope_ci[1]
        assert intercept_ci[0] < intercept_ci[1]

        # Mean should be within CI
        assert slope_ci[0] <= results['slope_mean'] <= slope_ci[1]
        assert intercept_ci[0] <= results['intercept_mean'] <= intercept_ci[1]

    def test_bootstrap_prediction_structure(self, sample_linear_data):
        """Test bootstrap prediction returns correct structure."""
        analyzer = BootstrapAnalyzer(n_bootstrap=100, random_seed=42)
        years, values = sample_linear_data

        results = analyzer.bootstrap_prediction(years, values, 2030)

        # Check structure
        assert 'predictions' in results
        assert 'mean' in results
        assert 'ci' in results
        assert 'se' in results
        assert 'target_year' in results

        # Check lengths
        assert len(results['predictions']) == 100
        assert len(results['ci']) == 2
        assert results['target_year'] == 2030

    def test_bootstrap_prediction_reasonable(self, perfect_linear_data):
        """Test that prediction is reasonable."""
        analyzer = BootstrapAnalyzer(n_bootstrap=1000, random_seed=42)
        years, values = perfect_linear_data

        # True prediction: 0.5 * 2030 - 980 = 35
        results = analyzer.bootstrap_prediction(years, values, 2030)

        # Bootstrap prediction should be close
        assert abs(results['mean'] - 35) < 0.1

    def test_bootstrap_prediction_ci_contains_mean(self, sample_linear_data):
        """Test that prediction CI contains the mean."""
        analyzer = BootstrapAnalyzer(n_bootstrap=500, random_seed=42)
        years, values = sample_linear_data

        results = analyzer.bootstrap_prediction(years, values, 2025)

        ci = results['ci']
        mean = results['mean']

        # Mean should be within CI
        assert ci[0] <= mean <= ci[1]

    def test_bootstrap_r_squared_structure(self, sample_linear_data):
        """Test bootstrap R² returns correct structure."""
        analyzer = BootstrapAnalyzer(n_bootstrap=100, random_seed=42)
        years, values = sample_linear_data

        results = analyzer.bootstrap_r_squared(years, values)

        assert 'r_squared_values' in results
        assert 'mean' in results
        assert 'ci' in results
        assert 'se' in results

        assert len(results['r_squared_values']) == 100

    def test_bootstrap_r_squared_bounds(self, sample_linear_data):
        """Test that R² values are between 0 and 1."""
        analyzer = BootstrapAnalyzer(n_bootstrap=500, random_seed=42)
        years, values = sample_linear_data

        results = analyzer.bootstrap_r_squared(years, values)

        # All R² values should be between 0 and 1
        assert all(0 <= r2 <= 1 for r2 in results['r_squared_values'])
        assert 0 <= results['mean'] <= 1

    def test_compare_methods_structure(self, sample_linear_data):
        """Test that compare_methods returns correct structure."""
        analyzer = BootstrapAnalyzer(n_bootstrap=500, random_seed=42)
        years, values = sample_linear_data

        comparison = analyzer.compare_methods(years, values)

        assert 'parametric' in comparison
        assert 'bootstrap' in comparison
        assert 'ci_width_ratio' in comparison

        # Check parametric results
        assert 'slope' in comparison['parametric']
        assert 'slope_ci' in comparison['parametric']
        assert 'slope_se' in comparison['parametric']

        # Check bootstrap results
        assert 'slope' in comparison['bootstrap']
        assert 'slope_ci' in comparison['bootstrap']
        assert 'slope_se' in comparison['bootstrap']

    def test_bootstrap_reproducibility(self, sample_linear_data):
        """Test that same random seed gives same results."""
        years, values = sample_linear_data

        analyzer1 = BootstrapAnalyzer(n_bootstrap=100, random_seed=42)
        results1 = analyzer1.bootstrap_linear_regression(years, values)

        analyzer2 = BootstrapAnalyzer(n_bootstrap=100, random_seed=42)
        results2 = analyzer2.bootstrap_linear_regression(years, values)

        # Should get identical results with same seed
        assert abs(results1['slope_mean'] - results2['slope_mean']) < 1e-10
        assert abs(results1['slope_se'] - results2['slope_se']) < 1e-10

    def test_bootstrap_different_seeds(self, sample_linear_data):
        """Test that different random seeds give different samples."""
        years, values = sample_linear_data

        analyzer1 = BootstrapAnalyzer(n_bootstrap=100, random_seed=42)
        results1 = analyzer1.bootstrap_linear_regression(years, values)

        analyzer2 = BootstrapAnalyzer(n_bootstrap=100, random_seed=99)
        results2 = analyzer2.bootstrap_linear_regression(years, values)

        # Bootstrap samples should differ
        # (but estimates should still be similar)
        assert not np.array_equal(results1['slopes'], results2['slopes'])

        # But means should be close (both estimating same thing)
        assert abs(results1['slope_mean'] - results2['slope_mean']) < 0.05

    def test_bootstrap_with_small_n(self):
        """Test bootstrap with very small sample size."""
        analyzer = BootstrapAnalyzer(n_bootstrap=100, random_seed=42)

        # Only 3 points
        years = np.array([2015, 2016, 2017])
        values = np.array([10, 11, 12])

        results = analyzer.bootstrap_linear_regression(years, values)

        # Should still work, but results may be less stable
        assert 'slope_mean' in results
        assert results['slope_mean'] > 0  # Positive trend

    def test_bootstrap_confidence_level(self):
        """Test different confidence levels."""
        years = np.array([2015, 2016, 2017, 2018, 2019, 2020])
        values = np.array([10, 11, 12, 13, 14, 15])

        # 90% CI should be narrower than 95% CI
        analyzer_90 = BootstrapAnalyzer(n_bootstrap=1000, confidence_level=0.90, random_seed=42)
        results_90 = analyzer_90.bootstrap_linear_regression(years, values)

        analyzer_95 = BootstrapAnalyzer(n_bootstrap=1000, confidence_level=0.95, random_seed=42)
        results_95 = analyzer_95.bootstrap_linear_regression(years, values)

        width_90 = results_90['slope_ci'][1] - results_90['slope_ci'][0]
        width_95 = results_95['slope_ci'][1] - results_95['slope_ci'][0]

        assert width_90 < width_95

    def test_bootstrap_n_iterations_effect(self, sample_linear_data):
        """Test that more iterations give more stable estimates."""
        years, values = sample_linear_data

        # Few iterations
        analyzer_few = BootstrapAnalyzer(n_bootstrap=50, random_seed=42)
        results_few = analyzer_few.bootstrap_linear_regression(years, values)

        # Many iterations
        analyzer_many = BootstrapAnalyzer(n_bootstrap=2000, random_seed=42)
        results_many = analyzer_many.bootstrap_linear_regression(years, values)

        # More iterations should give smaller SE (more stable)
        # (This is a probabilistic test, may occasionally fail)
        assert results_many['slope_se'] <= results_few['slope_se'] * 1.2

    def test_comparison_ratio_positive(self, sample_linear_data):
        """Test that CI width ratio is positive."""
        analyzer = BootstrapAnalyzer(n_bootstrap=500, random_seed=42)
        years, values = sample_linear_data

        comparison = analyzer.compare_methods(years, values)

        # Ratio should be positive
        assert comparison['ci_width_ratio'] > 0