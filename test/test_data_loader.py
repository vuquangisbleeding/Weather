"""
Unit tests for WeatherDataLoader.
"""
import pytest
import pandas as pd
import numpy as np
from io import StringIO
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from data import WeatherDataLoader


@pytest.fixture
def sample_weather_data():
    """Create sample weather data for testing."""
    data = """date,temp_celsius,rainfall_mm,humidity_percent
2020-01-01,15.5,10.2,65
2020-01-02,16.0,0.0,60
2020-06-15,28.5,5.0,70
2020-06-16,,3.0,68
2020-12-20,8.0,15.0,75
"""
    return StringIO(data)


@pytest.fixture
def temp_csv_file(tmp_path, sample_weather_data):
    """Create a temporary CSV file for testing."""
    csv_path = tmp_path / "test_weather.csv"
    with open(csv_path, 'w') as f:
        f.write(sample_weather_data.getvalue())
    return str(csv_path)


class TestWeatherDataLoader:
    """Test suite for WeatherDataLoader."""

    def test_initialization(self, temp_csv_file):
        """Test loader initialization."""
        loader = WeatherDataLoader(temp_csv_file, date_column='date')
        assert loader.file_path == temp_csv_file
        assert loader.date_column == 'date'
        assert loader.df is None

    def test_load_data(self, temp_csv_file):
        """Test data loading."""
        loader = WeatherDataLoader(temp_csv_file, date_column='date')
        df = loader.load_data()

        assert df is not None
        assert len(df) == 5
        assert 'date' in df.columns
        assert 'temp_celsius' in df.columns
        assert pd.api.types.is_datetime64_any_dtype(df['date'])

    def test_clean_data(self, temp_csv_file):
        """Test data cleaning."""
        loader = WeatherDataLoader(temp_csv_file, date_column='date')
        loader.load_data()
        df_cleaned = loader.clean_data()

        # Should remove row with missing temp_celsius
        assert len(df_cleaned) == 4
        assert not df_cleaned['temp_celsius'].isnull().any()

    def test_add_temporal_features(self, temp_csv_file):
        """Test adding year and month columns."""
        loader = WeatherDataLoader(temp_csv_file, date_column='date')
        loader.load_data()
        df = loader.add_temporal_features()

        assert 'year' in df.columns
        assert 'month' in df.columns
        assert df['year'].iloc[0] == 2020
        assert df['month'].iloc[0] == 1
        assert df['month'].iloc[2] == 6

    def test_prepare_data(self, temp_csv_file):
        """Test complete data preparation pipeline."""
        loader = WeatherDataLoader(temp_csv_file, date_column='date')
        df = loader.prepare_data()

        # Check all steps completed
        assert len(df) == 4  # Cleaned
        assert 'year' in df.columns  # Temporal features added
        assert 'month' in df.columns
        assert not df['temp_celsius'].isnull().any()

    def test_get_seasonal_data(self, temp_csv_file):
        """Test extracting seasonal data."""
        loader = WeatherDataLoader(temp_csv_file, date_column='date')
        loader.prepare_data()

        # Get summer months (June = 6)
        summer_data = loader.get_seasonal_data([6], metric='temp_celsius')
        assert len(summer_data) == 1  # Only one June record with valid temp

        # Get winter months (January = 1, December = 12)
        winter_data = loader.get_seasonal_data([1, 12], metric='temp_celsius')
        assert len(winter_data) == 3  # January and December records

    def test_load_data_error_handling(self):
        """Test error handling for invalid file path."""
        loader = WeatherDataLoader('nonexistent_file.csv')

        with pytest.raises(Exception):
            loader.load_data()

    def test_clean_data_without_loading(self, temp_csv_file):
        """Test that cleaning without loading raises error."""
        loader = WeatherDataLoader(temp_csv_file)

        with pytest.raises(ValueError, match="Data not loaded yet"):
            loader.clean_data()