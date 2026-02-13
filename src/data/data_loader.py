"""
Data loading and preprocessing module for weather analysis.
"""
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class WeatherDataLoader:
    """
    Loader for weather data with preprocessing capabilities.
    """

    def __init__(self, file_path, date_column='date'):
        """
        Initialize data loader.

        Parameters:
        -----------
        file_path : str
            Path to the CSV file containing weather data
        date_column : str
            Name of the date column in the dataset
        """
        self.file_path = file_path
        self.date_column = date_column
        self.df = None

    def load_data(self):
        """
        Load weather data from CSV file.

        Returns:
        --------
        pd.DataFrame
            Loaded weather data
        """
        logger.info(f"Loading data from {self.file_path}")
        try:
            self.df = pd.read_csv(self.file_path, parse_dates=[self.date_column])
            logger.info(f"Data loaded successfully. Shape: {self.df.shape}")
            return self.df
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise

    def clean_data(self):
        """
        Clean data by removing rows with missing values in key columns.

        Returns:
        --------
        pd.DataFrame
            Cleaned weather data
        """
        if self.df is None:
            raise ValueError("Data not loaded yet. Call load_data() first.")

        logger.info("Cleaning data...")
        initial_rows = len(self.df)

        # Drop rows with missing values in relevant columns
        required_columns = [self.date_column, 'temp_celsius', 'rainfall_mm', 'humidity_percent']
        self.df = self.df.dropna(subset=required_columns)

        rows_removed = initial_rows - len(self.df)
        logger.info(f"Removed {rows_removed} rows with missing values. Remaining: {len(self.df)} rows")

        return self.df

    def add_temporal_features(self):
        """
        Add year and month columns from date column.

        Returns:
        --------
        pd.DataFrame
            Data with temporal features
        """
        if self.df is None:
            raise ValueError("Data not loaded yet. Call load_data() first.")

        logger.info("Adding temporal features (year, month)...")
        self.df['year'] = self.df[self.date_column].dt.year
        self.df['month'] = self.df[self.date_column].dt.month

        year_range = f"{self.df['year'].min()} - {self.df['year'].max()}"
        logger.info(f"Data spans years: {year_range}")

        return self.df

    def prepare_data(self):
        """
        Complete data preparation pipeline: load, clean, and add features.

        Returns:
        --------
        pd.DataFrame
            Fully prepared weather data
        """
        self.load_data()
        self.clean_data()
        self.add_temporal_features()

        logger.info("Data preparation completed successfully")
        return self.df

    def get_seasonal_data(self, months, metric='temp_celsius'):
        """
        Extract data for specific months (seasonal data).

        Parameters:
        -----------
        months : list
            List of month numbers to filter
        metric : str
            Column name for the metric to analyze

        Returns:
        --------
        pd.DataFrame
            Filtered seasonal data
        """
        if self.df is None:
            raise ValueError("Data not loaded yet. Call load_data() first.")

        seasonal_df = self.df[self.df['month'].isin(months)].copy()
        # Drop missing values for the specific metric
        seasonal_df = seasonal_df.dropna(subset=[metric])

        logger.info(f"Extracted seasonal data for months {months}: {len(seasonal_df)} records")
        return seasonal_df