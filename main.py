"""
Main script for weather trend analysis.

This script performs comprehensive trend analysis on weather data including:
- Temperature trends (summer and winter)
- Rainfall trends
- Statistical significance testing
- Visualization with confidence intervals
"""
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from utils import load_config, setup_logging, ensure_output_dirs
from data import WeatherDataLoader
from analysis import TrendAnalyzer
from visualization import TrendVisualizer
import logging


def main():
    """Main execution function."""

    # Load configuration
    config = load_config('config/config.yaml')

    # Setup logging
    logger = setup_logging(config)
    logger.info("=" * 80)
    logger.info("Starting Weather Trend Analysis")
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

        # Initialize analyzer
        analyzer = TrendAnalyzer(confidence_level=confidence_level)

        # Initialize visualizer
        output_config = config['output']
        visualizer = TrendVisualizer(
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

        summer_results = analyzer.analyze_trend(summer_years, summer_values, 'Summer Temp')
        visualizer.create_all_plots(
            summer_years, summer_values, summer_results,
            'Summer Temp', 'Avg Temp (°C)', confidence_level
        )

        # Predict future temperature
        pred_temp = analyzer.predict_value(
            summer_results['slope'],
            summer_results['intercept'],
            prediction_year
        )
        logger.info(f"Predicted summer avg temp in {prediction_year}: {pred_temp:.2f}°C")

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

        # Statistical significance
        significance_level = analysis_config['significance_level']

        if summer_results['p_value'] < significance_level:
            logger.info("Summer temperature trend is statistically significant.")
        else:
            logger.info("Summer temperature trend is NOT statistically significant.")

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
        logger.info("=" * 80)

    except Exception as e:
        logger.error(f"Error during analysis: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()