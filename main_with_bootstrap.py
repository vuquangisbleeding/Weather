"""
Main script for weather trend analysis WITH BOOTSTRAP RESAMPLING.

This script includes all original analyses PLUS bootstrap resampling to:
- Estimate uncertainty in trend estimates without parametric assumptions
- Compare bootstrap vs parametric confidence intervals
- Provide robust prediction intervals
"""
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from utils import load_config, setup_logging, ensure_output_dirs
from data import WeatherDataLoader
from analysis import TrendAnalyzer, BootstrapAnalyzer
from visualization import TrendVisualizer, BootstrapVisualizer
import logging


def main():
    """Main execution function with bootstrap analysis."""

    # Load configuration
    config = load_config('config/config.yaml')

    # Setup logging
    logger = setup_logging(config)
    logger.info("=" * 80)
    logger.info("Starting Weather Trend Analysis WITH BOOTSTRAP RESAMPLING")
    logger.info("=" * 80)

    # Ensure output directories exist
    ensure_output_dirs(config)

    try:
        # ===== DATA LOADING AND PREPARATION =====
        data_config = config['data']
        data_loader = WeatherDataLoader(
            file_path=data_config['input_file'],
            date_column=data_config['date_column']
        )

        # Prepare data (load, clean, add temporal features)
        df = data_loader.prepare_data()

        # ===== ANALYSIS SETUP =====
        analysis_config = config['analysis']
        summer_months = analysis_config['summer_months']
        winter_months = analysis_config['winter_months']
        prediction_year = analysis_config['prediction_year']
        confidence_level = analysis_config['confidence_level']

        # Bootstrap config
        bootstrap_config = analysis_config.get('bootstrap', {})
        bootstrap_enabled = bootstrap_config.get('enabled', False)
        n_bootstrap = bootstrap_config.get('n_iterations', 10000)
        random_seed = bootstrap_config.get('random_seed', None)
        compare_methods = bootstrap_config.get('compare_methods', True)

        # Initialize analyzers
        analyzer = TrendAnalyzer(confidence_level=confidence_level)

        if bootstrap_enabled:
            bootstrap_analyzer = BootstrapAnalyzer(
                n_bootstrap=n_bootstrap,
                confidence_level=confidence_level,
                random_seed=random_seed
            )
            logger.info(f"Bootstrap enabled with {n_bootstrap} iterations")

        # Initialize visualizers
        output_config = config['output']
        visualizer = TrendVisualizer(
            output_dir=output_config['plots_dir'],
            save_plots=output_config['save_plots'],
            show_plots=output_config['show_plots'],
            plot_format=output_config['plot_format'],
            dpi=output_config['plot_dpi'],
            figsize=tuple(output_config['figure_size'].values())
        )

        if bootstrap_enabled:
            bootstrap_visualizer = BootstrapVisualizer(
                output_dir=output_config['plots_dir'],
                save_plots=output_config['save_plots'],
                show_plots=output_config['show_plots'],
                plot_format=output_config['plot_format'],
                dpi=output_config['plot_dpi'],
                figsize=tuple(output_config['figure_size'].values())
            )

        # ===== SUMMER TEMPERATURE ANALYSIS =====
        logger.info("\n" + "=" * 80)
        logger.info("SUMMER TEMPERATURE TREND ANALYSIS")
        logger.info("=" * 80)

        summer_temps = analyzer.calculate_seasonal_average(df, summer_months, 'temp_celsius')
        summer_years = summer_temps.index.values
        summer_values = summer_temps.values

        # Standard analysis
        summer_results = analyzer.analyze_trend(summer_years, summer_values, 'Summer Temp')
        visualizer.create_all_plots(
            summer_years, summer_values, summer_results,
            'Summer Temp', 'Avg Temp (°C)', confidence_level
        )

        # Bootstrap analysis
        if bootstrap_enabled:
            logger.info("\n--- Bootstrap Analysis for Summer Temperature ---")

            # Bootstrap regression
            summer_bootstrap = bootstrap_analyzer.bootstrap_linear_regression(
                summer_years, summer_values
            )

            # Visualize bootstrap distribution
            bootstrap_visualizer.plot_bootstrap_distribution(
                summer_bootstrap, 'slope', 'Summer Temperature Slope', '°C/year'
            )

            # Bootstrap prediction
            logger.info(f"\n--- Bootstrap Prediction for {prediction_year} ---")
            summer_pred_bootstrap = bootstrap_analyzer.bootstrap_prediction(
                summer_years, summer_values, prediction_year
            )

            # Visualize prediction with uncertainty
            bootstrap_visualizer.plot_prediction_uncertainty(
                summer_years, summer_values, summer_pred_bootstrap,
                summer_results, 'Summer Temperature', 'Avg Temp (°C)'
            )

            # Compare methods
            if compare_methods:
                logger.info("\n--- Method Comparison: Parametric vs Bootstrap ---")
                comparison = bootstrap_analyzer.compare_methods(summer_years, summer_values)
                bootstrap_visualizer.plot_method_comparison(comparison, 'Summer Temp Slope')

            # Scatter plot of bootstrap iterations
            bootstrap_visualizer.plot_bootstrap_slopes_scatter(
                summer_bootstrap, summer_results['slope'], 'Summer Temperature Slope'
            )

        # Standard prediction (for comparison)
        pred_temp = analyzer.predict_value(
            summer_results['slope'],
            summer_results['intercept'],
            prediction_year
        )
        logger.info(f"\nParametric prediction for {prediction_year}: {pred_temp:.2f}°C")

        if bootstrap_enabled:
            logger.info(f"Bootstrap prediction for {prediction_year}: "
                        f"{summer_pred_bootstrap['mean']:.2f}°C "
                        f"(95% CI: {summer_pred_bootstrap['ci'][0]:.2f} to "
                        f"{summer_pred_bootstrap['ci'][1]:.2f}°C)")

        # ===== WINTER TEMPERATURE ANALYSIS =====
        logger.info("\n" + "=" * 80)
        logger.info("WINTER TEMPERATURE TREND ANALYSIS")
        logger.info("=" * 80)

        winter_temps = analyzer.calculate_seasonal_average(df, winter_months, 'temp_celsius')
        winter_years = winter_temps.index.values
        winter_values = winter_temps.values

        winter_results = analyzer.analyze_trend(winter_years, winter_values, 'Winter Temp')
        visualizer.create_all_plots(
            winter_years, winter_values, winter_results,
            'Winter Temp', 'Avg Temp (°C)', confidence_level
        )

        # Bootstrap for winter
        if bootstrap_enabled:
            logger.info("\n--- Bootstrap Analysis for Winter Temperature ---")
            winter_bootstrap = bootstrap_analyzer.bootstrap_linear_regression(
                winter_years, winter_values
            )
            bootstrap_visualizer.plot_bootstrap_distribution(
                winter_bootstrap, 'slope', 'Winter Temperature Slope', '°C/year'
            )

        # ===== SUMMER RAINFALL ANALYSIS =====
        logger.info("\n" + "=" * 80)
        logger.info("SUMMER RAINFALL TREND ANALYSIS")
        logger.info("=" * 80)

        summer_rainfall = analyzer.calculate_seasonal_average(df, summer_months, 'rainfall_mm')
        rainfall_years = summer_rainfall.index.values
        rainfall_values = summer_rainfall.values

        rainfall_results = analyzer.analyze_trend(rainfall_years, rainfall_values, 'Summer Rainfall')
        visualizer.create_all_plots(
            rainfall_years, rainfall_values, rainfall_results,
            'Summer Rainfall', 'Avg Rainfall (mm)', confidence_level
        )

        # Bootstrap for rainfall
        if bootstrap_enabled:
            logger.info("\n--- Bootstrap Analysis for Summer Rainfall ---")
            rainfall_bootstrap = bootstrap_analyzer.bootstrap_linear_regression(
                rainfall_years, rainfall_values
            )
            bootstrap_visualizer.plot_bootstrap_distribution(
                rainfall_bootstrap, 'slope', 'Summer Rainfall Slope', 'mm/year'
            )

        # ===== SUMMARY AND CONCLUSIONS =====
        logger.info("\n" + "=" * 80)
        logger.info("SUMMARY AND CONCLUSIONS")
        logger.info("=" * 80)

        # Temperature trends
        summer_warming = summer_results['slope'] * 10
        winter_warming = winter_results['slope'] * 10
        rainfall_trend = rainfall_results['slope']

        logger.info(f"Summers warming: {summer_warming:.2f}°C per decade.")
        logger.info(f"Winters warming: {winter_warming:.2f}°C per decade.")
        logger.info(f"Summer rainfall trend: {rainfall_trend:.2f} mm/year.")

        # Bootstrap summary
        if bootstrap_enabled:
            logger.info("\n--- Bootstrap Estimates ---")
            logger.info(f"Summer warming (bootstrap): {summer_bootstrap['slope_mean'] * 10:.2f}°C per decade")
            logger.info(f"  95% CI: [{summer_bootstrap['slope_ci'][0] * 10:.2f}, "
                        f"{summer_bootstrap['slope_ci'][1] * 10:.2f}]°C per decade")

            logger.info(f"Winter warming (bootstrap): {winter_bootstrap['slope_mean'] * 10:.2f}°C per decade")
            logger.info(f"  95% CI: [{winter_bootstrap['slope_ci'][0] * 10:.2f}, "
                        f"{winter_bootstrap['slope_ci'][1] * 10:.2f}]°C per decade")

            logger.info(f"Rainfall trend (bootstrap): {rainfall_bootstrap['slope_mean']:.2f} mm/year")
            logger.info(f"  95% CI: [{rainfall_bootstrap['slope_ci'][0]:.2f}, "
                        f"{rainfall_bootstrap['slope_ci'][1]:.2f}] mm/year")

        # Statistical significance
        significance_level = analysis_config['significance_level']

        if summer_results['p_value'] < significance_level:
            logger.info("\nSummer temperature trend is statistically significant.")
        else:
            logger.info("\nSummer temperature trend is NOT statistically significant.")

        if winter_results['p_value'] < significance_level:
            logger.info("Winter temperature trend is statistically significant.")
        else:
            logger.info("Winter temperature trend is NOT statistically significant.")

        if rainfall_results['p_value'] < significance_level:
            logger.info("Rainfall trend is statistically significant.")
        else:
            logger.info("Rainfall trend is NOT statistically significant.")

        logger.info("\n" + "=" * 80)
        logger.info("Weather Trend Analysis Completed Successfully")
        if bootstrap_enabled:
            logger.info(f"Bootstrap analysis performed with {n_bootstrap} iterations")
        logger.info("=" * 80)

    except Exception as e:
        logger.error(f"Error during analysis: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()