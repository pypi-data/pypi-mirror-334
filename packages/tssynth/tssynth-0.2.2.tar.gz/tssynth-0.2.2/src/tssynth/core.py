from typing import Optional, List
from dataclasses import dataclass, replace
import pandas as pd
import numpy as np

from .trends import Trends
from .noise import Noise
from .anomalies import Anomalies
from .dependencies import Dependencies


@dataclass
class SensorConfig:
    """Configuration for a single sensor"""

    name: str
    trend: Optional[Trends.Base] = None
    noise: Optional[Noise.Base] = None
    anomalies: List[Anomalies.Base] = None
    dependencies: List[Dependencies.Base] = None


class MultiSensorTS:
    def __init__(
        self,
        length: int = 1000,
        sampling_rate: float = 1.0,
        sampling_rate_units: str = "s",
        sampling_rate_jitter: float = 0.0,
        variation_scale: float = 0.1,
        seed: Optional[int] = None,
    ):
        """Initialize MultiSensorTS generator.

        Parameters
        ----------
        length : int, default=1000
            Number of samples to generate for each time series
        sampling_rate : float, default=1.0
            Base sampling interval in seconds (e.g., 1.0 for 1 second sampling)
        sampling_rate_units : str, default="s"
            Units for the sampling rate (e.g., "s" for seconds, "ms" for milliseconds)
        sampling_rate_jitter : float, default=0.0
            Maximum random time variation in seconds to add to each sample
            (e.g., 0.1 for ±100ms jitter)
        variation_scale : float, default=0.1
            Scale factor for parameter variations when generating similar samples.
            A value of 0.1 means parameters can vary by ±10% of their original value.
        seed : int, optional
            Random seed for reproducible results. If None, uses system random source.

        Notes
        -----
        The sampling rate jitter is uniformly distributed in the range
        [-sampling_rate_jitter, +sampling_rate_jitter].
        The variation scale is used by generate_similar() to create new samples
        with slightly different parameters.
        """
        self.length = length
        self.sampling_rate = sampling_rate
        self.sampling_rate_units = sampling_rate_units
        self.sampling_rate_jitter = sampling_rate_jitter
        self.variation_scale = variation_scale
        self.rng = np.random.default_rng(seed)
        self.sensors = {}
        self.dependencies = {}

    def add_sensor(
        self,
        name: str,
        trend: Optional[Trends.Base] = None,
        noise: Optional[Noise.Base] = None,
        anomalies: Optional[List[Anomalies.Base]] = None,
    ) -> "MultiSensorTS":
        self.sensors[name] = SensorConfig(
            name=name, trend=trend, noise=noise, anomalies=anomalies or []
        )
        return self

    def add_dependency(
        self, target: str, source: str, dependency: Dependencies.Base
    ) -> "MultiSensorTS":
        """Add a dependency between sensors.

        Args:
            target: Name of the target sensor
            source: Name of the source sensor
            dependency: Dependency relationship to apply

        Raises:
            ValueError: If either the target or source sensor does not exist
        """
        # Validate that both sensors exist
        if target not in self.sensors:
            raise ValueError(f"Target sensor '{target}' not found")
        if source not in self.sensors:
            raise ValueError(f"Source sensor '{source}' not found")

        if target not in self.dependencies:
            self.dependencies[target] = []
        self.dependencies[target].append((source, dependency))
        return self

    def generate(self) -> pd.DataFrame:
        """Generate time series for all sensors with jittered timestamps."""
        # Generate jittered timestamps
        base_times = np.arange(0, self.length) * self.sampling_rate
        if self.sampling_rate_jitter > 0:
            jitters = self.rng.uniform(
                -self.sampling_rate_jitter,
                self.sampling_rate_jitter,
                self.length,
            )
            timestamps = pd.to_datetime(
                base_times + jitters, unit=self.sampling_rate_units
            )
        else:
            timestamps = pd.to_datetime(
                base_times, unit=self.sampling_rate_units
            )

        results = {}
        base_signals = {}  # Store base signals for dependency calculations

        # Generate independent sensors first
        for name, config in self.sensors.items():
            if name not in self.dependencies:
                series, anomaly_mask, base_signal = (
                    self._generate_single_sensor(config)
                )
                results[name] = pd.Series(series, index=timestamps)
                results[f"{name}_anomaly"] = pd.Series(
                    anomaly_mask, index=timestamps
                )
                base_signals[name] = base_signal

        # Generate dependent sensors
        for name, config in self.sensors.items():
            if name in self.dependencies:
                series, anomaly_mask, base_signal = (
                    self._generate_single_sensor(config)
                )
                current_series = pd.Series(series, index=timestamps)

                for source, dependency in self.dependencies[name]:
                    if source not in results:
                        raise ValueError(
                            f"Source sensor '{source}' not found or not yet generated"
                        )

                    source_series = results[source]
                    source_base = pd.Series(
                        base_signals[source], index=timestamps
                    )

                    if dependency.apply_before_anomaly:
                        # Apply dependency to the base signal before anomalies
                        dependency_effect = dependency.apply(
                            source_base.values, self.rng
                        )
                        current_series = pd.Series(
                            base_signal, index=timestamps
                        ) + pd.Series(dependency_effect, index=timestamps)

                        # Reapply anomalies after dependency
                        if config.anomalies:
                            series_array = current_series.values
                            for anomaly in config.anomalies:
                                series_array, affected_indices = anomaly.apply(
                                    series_array.copy(),
                                    self.rng,
                                    return_indices=True,
                                )
                                anomaly_mask[affected_indices] = True
                            current_series = pd.Series(
                                series_array, index=timestamps
                            )
                    else:
                        # Apply dependency to the final signal (after anomalies)
                        dependency_effect = dependency.apply(
                            source_series.values, self.rng
                        )
                        current_series += pd.Series(
                            dependency_effect, index=timestamps
                        )

                results[name] = current_series
                results[f"{name}_anomaly"] = pd.Series(
                    anomaly_mask, index=timestamps
                )

        return pd.DataFrame(results)

    def _generate_single_sensor(
        self, config: SensorConfig
    ) -> tuple[np.ndarray, np.ndarray]:
        """Generate time series for a single sensor.

        Returns:
            tuple: (signal values, anomaly mask)
        """
        series = np.zeros(self.length)
        anomaly_mask = np.zeros(self.length, dtype=bool)

        # Add trend component
        if config.trend:
            series += config.trend.generate(self.length)

        # Add noise component
        if config.noise:
            series += config.noise.generate(self.length, self.rng)

        # Store base signal before dependencies and anomalies
        base_signal = series.copy()

        # Add anomalies and track their locations
        if config.anomalies:
            for anomaly in config.anomalies:
                series, affected_indices = anomaly.apply(
                    series.copy(), self.rng, return_indices=True
                )
                anomaly_mask[affected_indices] = True

        return series, anomaly_mask, base_signal

    def _vary_parameter(self, value: float) -> float:
        """Add random variation to a parameter.

        Returns a value that varies from the original by at most variation_scale percent.
        For example, if variation_scale is 0.1, the returned value will be within ±10%
        of the original value. The returned value is guaranteed to be different from
        the input value.
        """
        if value == 0:
            # Special case for zero to avoid scaling issues
            # Ensure we return a small non-zero value
            return self.rng.uniform(0.01, 0.1) * (
                -1 if self.rng.random() < 0.5 else 1
            )

        # Calculate the variation range
        max_variation = abs(value) * self.variation_scale
        min_variation = max_variation * 0.25  # At least 25% of max variation

        # Randomly choose positive or negative variation
        if self.rng.random() < 0.5:
            # Apply negative variation
            variation = -self.rng.uniform(min_variation, max_variation)
        else:
            # Apply positive variation
            variation = self.rng.uniform(min_variation, max_variation)

        return value + variation

    def _create_similar_trend(self, trend: Trends.Base) -> Trends.Base:
        """Create a similar trend with slightly varied parameters."""
        if isinstance(trend, Trends.Periodic):
            return replace(
                trend,
                amplitude=self._vary_parameter(trend.amplitude),
                period=self._vary_parameter(trend.period),
                phase=self._vary_parameter(trend.phase),
                offset=self._vary_parameter(trend.offset),
            )
        elif isinstance(trend, Trends.Linear):
            return replace(
                trend,
                slope=self._vary_parameter(trend.slope),
                intercept=self._vary_parameter(trend.intercept),
            )
        elif isinstance(trend, Trends.Exponential):
            return replace(
                trend,
                growth_rate=self._vary_parameter(trend.growth_rate),
                base=self._vary_parameter(trend.base),
            )
        return trend

    def _create_similar_noise(self, noise: Noise.Base) -> Noise.Base:
        """Create similar noise with slightly varied parameters."""
        if isinstance(noise, Noise.Gaussian):
            return replace(noise, std=self._vary_parameter(noise.std))
        elif isinstance(noise, Noise.Uniform):
            return replace(
                noise,
                low=self._vary_parameter(noise.low),
                high=self._vary_parameter(noise.high),
            )
        elif isinstance(noise, Noise.Multiplicative):
            return replace(noise, factor=self._vary_parameter(noise.factor))
        return noise

    def _create_similar_dependency(
        self, dep: Dependencies.Base
    ) -> Dependencies.Base:
        """Create similar dependency with slightly varied parameters."""
        if isinstance(dep, Dependencies.Linear):
            return replace(
                dep,
                slope=self._vary_parameter(dep.slope),
                intercept=self._vary_parameter(dep.intercept),
                noise_level=self._vary_parameter(dep.noise_level),
            )
        elif isinstance(dep, Dependencies.Inverse):
            return replace(
                dep,
                scale=self._vary_parameter(dep.scale),
                offset=self._vary_parameter(dep.offset),
                noise_level=self._vary_parameter(dep.noise_level),
            )
        # Add other dependency types as needed
        return dep

    def _create_similar_anomaly(
        self, anomaly: Anomalies.Base
    ) -> Anomalies.Base:
        """Create similar anomaly with slightly varied parameters."""
        if isinstance(anomaly, Anomalies.Point):
            return replace(
                anomaly,
                magnitude=self._vary_parameter(anomaly.magnitude),
                position=anomaly.position,  # Preserve the original position
            )
        elif isinstance(anomaly, Anomalies.Collective):
            return replace(
                anomaly,
                magnitude=self._vary_parameter(anomaly.magnitude),
                duration=max(1, int(self._vary_parameter(anomaly.duration))),
                start=anomaly.start,  # Preserve the original start position
            )
        return anomaly

    def generate_similar(
        self,
        n_samples: int = 1,
        include_anomalies: bool = True,
        anomaly_probability: float = 0.1,
        variation_scale: Optional[float] = None,
    ) -> List[pd.DataFrame]:
        """Generate similar time series with varied parameters.

        Args:
            n_samples: Number of similar samples to generate
            include_anomalies: Whether to include anomalies in the generated samples
            anomaly_probability: Probability of including anomalies in each sample
            variation_scale: Override default variation scale for this generation

        Returns:
            List of DataFrames containing similar time series
        """
        old_scale = self.variation_scale
        if variation_scale is not None:
            self.variation_scale = variation_scale

        samples = []
        for _ in range(n_samples):
            # Create temporary copies with varied parameters
            temp_sensors = {}
            for name, config in self.sensors.items():
                temp_sensors[name] = replace(
                    config,
                    trend=(
                        self._create_similar_trend(config.trend)
                        if config.trend
                        else None
                    ),
                    noise=(
                        self._create_similar_noise(config.noise)
                        if config.noise
                        else None
                    ),
                    anomalies=(
                        (
                            [
                                self._create_similar_anomaly(a)
                                for a in config.anomalies
                            ]
                            if include_anomalies
                            and self.rng.random() < anomaly_probability
                            else []
                        )
                        if config.anomalies
                        else []
                    ),
                )

            temp_dependencies = {}
            for target, deps in self.dependencies.items():
                temp_dependencies[target] = [
                    (source, self._create_similar_dependency(dep))
                    for source, dep in deps
                ]

            # Store original configuration
            orig_sensors = self.sensors
            orig_dependencies = self.dependencies

            # Use temporary configuration
            self.sensors = temp_sensors
            self.dependencies = temp_dependencies

            # Generate sample
            samples.append(self.generate())

            # Restore original configuration
            self.sensors = orig_sensors
            self.dependencies = orig_dependencies

        # Restore original variation scale
        self.variation_scale = old_scale

        return samples
