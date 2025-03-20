import numpy as np
import pandas as pd
from tssynth import logger

from .noise import Noise
from .trends import Trends
from typing import Optional
from .core import MultiSensorTS
from .anomalies import Anomalies
from .dependencies import Dependencies


class Patterns:
    """Collection of pre-built pattern configurations"""

    class SolarPanel(MultiSensorTS):
        """Solar panel pattern with customizable components"""

        def __init__(
            self,
            length: int = 1000,
            sampling_rate: float = 10,
            sampling_rate_units: str = "m",
            sampling_rate_jitter: float = 0.0,
            # Solar panel specific parameters
            temp_setpoint: float = 22.0,
            daily_range: float = 3.0,
            seasonal_amplitude: float = 6.0,
            # Customizable components
            temp_trend: Optional[Trends.Base] = None,
            temp_noise: Optional[Noise.Base] = None,
            temp_anomalies: Optional[list[Anomalies.Base]] = None,
            humidity_trend: Optional[Trends.Base] = None,
            humidity_noise: Optional[Noise.Base] = None,
            humidity_anomalies: Optional[list[Anomalies.Base]] = None,
            power_trend: Optional[Trends.Base] = None,
            power_noise: Optional[Noise.Base] = None,
            power_anomalies: Optional[list[Anomalies.Base]] = None,
        ):
            super().__init__(
                length=length,
                sampling_rate=sampling_rate,
                sampling_rate_units=sampling_rate_units,
                sampling_rate_jitter=sampling_rate_jitter,
            )

            # Calculate periods for both HVAC and seasonal cycles
            sampling_rate_timedelta = pd.Timedelta(
                sampling_rate, sampling_rate_units
            )
            logger.debug(f"Sampling rate timedelta: {sampling_rate_timedelta}")

            hours_per_sample = sampling_rate_timedelta.total_seconds() / 3600
            hvac_period = (
                12 / hours_per_sample
            )  # 12 hours divided by hours per sample
            seasonal_period = (
                365 / 2 * 24
            ) / hours_per_sample  # 6 months in samples
            logger.debug(
                f"Solar panel period: {hvac_period} samples (12 hour cycle)"
            )
            logger.debug(
                f"Seasonal period: {seasonal_period} samples (6 month cycle)"
            )

            phase_shift = np.pi / 2

            # Create combined temperature trend (HVAC + seasonal)
            temp_daily = Trends.Periodic(
                amplitude=daily_range,
                period=hvac_period,
                offset=temp_setpoint,
                phase=phase_shift,
            )

            temp_seasonal = Trends.Periodic(
                amplitude=seasonal_amplitude,
                period=seasonal_period,
                offset=0,  # Offset is already in daily component
                phase=phase_shift * 1.6,
            )

            # Create combined power trend
            power_daily = Trends.Periodic(
                amplitude=10,
                period=hvac_period,
                offset=1.0,
                phase=phase_shift,
            )

            power_seasonal = Trends.Periodic(
                amplitude=5,  # Smaller seasonal effect on power
                period=seasonal_period,
                offset=0,
                phase=phase_shift * 1.6,
            )

            # Add sensors with combined trends
            self.add_sensor(
                name="temperature",
                trend=temp_trend
                or Trends.Composite([temp_daily, temp_seasonal]),
                noise=temp_noise or Noise.Gaussian(std=0.5),
                anomalies=temp_anomalies or [],
            )

            # Set up humidity sensor
            self.add_sensor(
                name="humidity",
                trend=humidity_trend
                or Trends.Linear(slope=-0.1, intercept=60),
                noise=humidity_noise or Noise.Gaussian(std=2.0),
                anomalies=humidity_anomalies or [],
            )

            # Add dependencies
            self.add_dependency(
                target="humidity",
                source="temperature",
                dependency=Dependencies.Linear(slope=-0.3, intercept=60),
            )

            self.add_sensor(
                name="power",
                trend=power_trend
                or Trends.Composite([power_daily, power_seasonal]),
                noise=power_noise or Noise.Multiplicative(factor=0.1),
                anomalies=power_anomalies or [],
            )
