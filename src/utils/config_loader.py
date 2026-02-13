"""
Utility functions for configuration and logging setup.
"""
import yaml
import logging
import os
from pathlib import Path


def load_config(config_path='config/config.yaml'):
    """
    Load configuration from YAML file.

    Parameters:
    -----------
    config_path : str
        Path to the configuration file

    Returns:
    --------
    dict
        Configuration dictionary
    """
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config


def setup_logging(config):
    """
    Setup logging configuration.

    Parameters:
    -----------
    config : dict
        Configuration dictionary containing logging settings
    """
    log_config = config.get('logging', {})
    log_level = getattr(logging, log_config.get('level', 'INFO'))
    log_file = log_config.get('log_file', 'logs/weather_analysis.log')
    console_output = log_config.get('console_output', True)

    # Create logs directory if it doesn't exist
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # Configure logging
    handlers = [logging.FileHandler(log_file, encoding='utf-8')]
    if console_output:
        handlers.append(logging.StreamHandler())

    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlers
    )

    return logging.getLogger(__name__)


def ensure_output_dirs(config):
    """
    Create output directories if they don't exist.

    Parameters:
    -----------
    config : dict
        Configuration dictionary containing output settings
    """
    output_config = config.get('output', {})
    plots_dir = output_config.get('plots_dir', 'outputs/plots')
    reports_dir = output_config.get('reports_dir', 'outputs/reports')

    os.makedirs(plots_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)