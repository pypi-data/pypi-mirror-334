import pytest
import numpy as np
import pandas as pd
from numpy.random import default_rng
from tssynth.patterns import Patterns
from tssynth.trends import Trends
from tssynth.noise import Noise
from tssynth.anomalies import Anomalies


@pytest.fixture
def rng():
    """Fixture for reproducible random number generation"""
    return default_rng(42)


class TestSolarPanel:
    def test_solar_panel_initialization(self):
        """Test that SolarPanel initializes with default parameters"""
        solar_panel = Patterns.SolarPanel()

        # Check that the object was created successfully
        assert isinstance(solar_panel, Patterns.SolarPanel)

        # Check that the sensors were added
        df = solar_panel.generate()
        assert "temperature" in df.columns
        assert "humidity" in df.columns
        assert "power" in df.columns

        # Check the length of the generated data
        assert len(df) == 1000  # Default length

    def test_solar_panel_custom_length(self):
        """Test SolarPanel with custom length parameter"""
        custom_length = 500
        solar_panel = Patterns.SolarPanel(length=custom_length)

        df = solar_panel.generate()
        assert len(df) == custom_length

    def test_solar_panel_custom_sampling_rate(self):
        """Test SolarPanel with custom sampling rate"""
        solar_panel = Patterns.SolarPanel(
            sampling_rate=5, sampling_rate_units="h"
        )

        df = solar_panel.generate()
        # Check that timestamps have appropriate intervals
        time_diff = df.index[1] - df.index[0]
        assert time_diff == pd.Timedelta(hours=5)

    def test_solar_panel_custom_temperature_parameters(self):
        """Test SolarPanel with custom temperature parameters"""
        custom_temp = 30.0
        custom_range = 5.0
        custom_seasonal = 10.0

        solar_panel = Patterns.SolarPanel(
            temp_setpoint=custom_temp,
            daily_range=custom_range,
            seasonal_amplitude=custom_seasonal,
        )

        df = solar_panel.generate()

        # Temperature should oscillate around the setpoint
        assert df["temperature"].mean() > custom_temp - custom_seasonal
        assert df["temperature"].mean() < custom_temp + custom_seasonal

        # Check that the range of values is influenced by our parameters
        temp_range = df["temperature"].max() - df["temperature"].min()
        assert temp_range > custom_range  # At minimum the daily range

    def test_solar_panel_custom_components(self):
        """Test SolarPanel with custom trend, noise, and anomaly components"""
        # Create custom components
        custom_temp_trend = Trends.Linear(slope=0.01, intercept=25)
        custom_temp_noise = Noise.Gaussian(std=0.2)
        custom_temp_anomaly = Anomalies.Point(position=50, magnitude=10)

        solar_panel = Patterns.SolarPanel(
            temp_trend=custom_temp_trend,
            temp_noise=custom_temp_noise,
            temp_anomalies=[custom_temp_anomaly],
        )

        df = solar_panel.generate()

        # With a linear trend, we expect the end to be higher than the beginning
        assert df["temperature"].iloc[-1] > df["temperature"].iloc[0]

        # The anomaly should create a spike at position 50
        # Find the largest absolute difference between consecutive points
        diffs = np.abs(df["temperature"].diff()).dropna()
        assert diffs.max() > 5  # The anomaly should create a significant spike

    def test_solar_panel_humidity_custom_components(self):
        """Test SolarPanel with custom humidity components"""
        custom_humidity_trend = Trends.Periodic(
            amplitude=5, period=100, offset=50
        )
        custom_humidity_noise = Noise.Uniform(low=-1, high=1)

        solar_panel = Patterns.SolarPanel(
            humidity_trend=custom_humidity_trend,
            humidity_noise=custom_humidity_noise,
        )

        df = solar_panel.generate()

        # With a periodic trend centered at 50, we expect the mean to be close to 50
        assert 100 < df["humidity"].mean() < 105

        # The range should be influenced by the amplitude
        humidity_range = df["humidity"].max() - df["humidity"].min()
        assert humidity_range > 8  # Amplitude is 5, plus some noise

    def test_solar_panel_power_custom_components(self):
        """Test SolarPanel with custom power components"""
        custom_power_trend = Trends.Linear(slope=0.05, intercept=10)
        custom_power_noise = Noise.Multiplicative(factor=0.05)

        solar_panel = Patterns.SolarPanel(
            power_trend=custom_power_trend, power_noise=custom_power_noise
        )

        df = solar_panel.generate()

        # With a linear trend, we expect the end to be higher than the beginning
        assert df["power"].iloc[-1] > df["power"].iloc[0]

        # The starting value should be close to the intercept
        assert 8 < df["power"].iloc[0] < 12
