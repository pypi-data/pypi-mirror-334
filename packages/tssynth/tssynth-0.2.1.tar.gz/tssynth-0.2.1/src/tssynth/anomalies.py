import numpy as np
from tssynth import logger
from typing import Optional
from dataclasses import dataclass
from numpy.random import Generator


class Anomalies:
    """Collection of anomaly patterns for time series.

    This class provides various types of synthetic anomalies that can be
    injected into time series data, including point anomalies and
    collective (sequential) anomalies.
    """

    @dataclass
    class Base:
        """Base class for all anomaly types.

        Provides the interface that all anomaly classes must implement.
        Each anomaly type should define how it modifies the input time series.
        """

        def apply(self, series: np.ndarray, rng: Generator) -> np.ndarray:
            """Apply the anomaly to the input time series.

            Args:
                series (np.ndarray): The input time series to modify
                rng (Generator): Random number generator for stochastic anomalies

            Returns:
                np.ndarray: The modified time series with injected anomaly
            """
            raise NotImplementedError

    @dataclass
    class Point(Base):
        """Single point anomaly injection.

        Adds a fixed magnitude to a single point in the time series.
        The position can be specified or randomly chosen.

        Attributes:
            position (Optional[int]): Index where anomaly should be injected.
                If None, a random position is chosen.
            magnitude (float): The value to add to the selected point.
        """

        position: Optional[int] = None
        magnitude: float = 5.0

        def apply(
            self,
            series: np.ndarray,
            rng: Generator,
            return_indices: bool = False,
        ) -> np.ndarray:
            """Apply point anomaly to the time series.

            Args:
                series (np.ndarray): The input time series to modify
                rng (Generator): Random number generator for position selection
                return_indices (bool): If True, returns both modified series
                    and indices of affected points

            Returns:
                np.ndarray or tuple: Modified time series, or if return_indices is True,
                    a tuple of (modified_series, affected_indices)
            """
            pos = (
                self.position
                if self.position is not None
                else rng.integers(0, len(series))
            )
            logger.debug(
                f"Applying point anomaly at position {pos} with magnitude {self.magnitude}"
            )

            if pos >= len(series):
                logger.error(
                    f"Position {pos} exceeds series length {len(series)}"
                )
                raise ValueError("Position exceeds series length")

            series[pos] += self.magnitude
            affected_indices = np.array([pos])
            if return_indices:
                return series, affected_indices
            return series

    @dataclass
    class Collective(Base):
        """Collective (sequential) anomaly injection.

        Adds a fixed magnitude to a consecutive sequence of points in the
        time series. The starting position can be specified or randomly chosen.

        Attributes:
            start (Optional[int]): Starting index for the anomaly sequence.
                If None, a random starting position is chosen.
            duration (int): Number of consecutive points to affect
            magnitude (float): The value to add to each point in the sequence
        """

        start: Optional[int] = None
        duration: int = 10
        magnitude: float = 5.0

        def apply(
            self,
            series: np.ndarray,
            rng: Generator,
            return_indices: bool = False,
        ) -> np.ndarray:
            """Apply collective anomaly to the time series.

            Args:
                series (np.ndarray): The input time series to modify
                rng (Generator): Random number generator for position selection
                return_indices (bool): If True, returns both modified series
                    and indices of affected points

            Returns:
                np.ndarray or tuple: Modified time series, or if return_indices is True,
                    a tuple of (modified_series, affected_indices)
            """
            start = (
                self.start
                if self.start is not None
                else rng.integers(0, len(series) - self.duration)
            )

            if start + self.duration > len(series):
                logger.warning(
                    f"Requested duration {self.duration} from position {start} "
                    f"exceeds series length {len(series)}. Truncating."
                )

            end = min(start + self.duration, len(series))
            logger.debug(
                f"Applying collective anomaly from position {start} to {end} "
                f"with magnitude {self.magnitude}"
            )

            series[start:end] += self.magnitude
            affected_indices = np.arange(start, end)
            if return_indices:
                return series, affected_indices
            return series


class Dependencies:
    """Collection of sensor dependency relationships"""

    @dataclass
    class Base:
        """Base class for dependencies"""

        delay: int = 0  # Time delay in steps
        noise_level: float = 0.1  # Amount of noise in relationship
        apply_before_anomaly: bool = True

        def apply(
            self, source: np.ndarray, rng: np.random.Generator
        ) -> np.ndarray:
            """Apply dependency relationship to source signal"""
            raise NotImplementedError

    @dataclass
    class Linear(Base):
        """Linear relationship: target = slope * source + intercept"""

        slope: float = 1.0
        intercept: float = 0.0

        def apply(
            self, source: np.ndarray, rng: np.random.Generator
        ) -> np.ndarray:
            delayed = np.roll(source, self.delay)
            if self.delay > 0:
                delayed[: self.delay] = delayed[
                    self.delay
                ]  # Fill initial values

            target = self.slope * delayed + self.intercept
            noise = rng.normal(0, self.noise_level, len(source))
            return target + noise

    @dataclass
    class Inverse(Base):
        """Inverse relationship: target = scale / source"""

        scale: float = 1.0
        offset: float = 0.0  # Prevent division by zero

        def apply(
            self, source: np.ndarray, rng: np.random.Generator
        ) -> np.ndarray:
            delayed = np.roll(source, self.delay)
            if self.delay > 0:
                delayed[: self.delay] = delayed[self.delay]

            target = self.scale / (delayed + self.offset)
            noise = rng.normal(0, self.noise_level, len(source))
            return target + noise

    @dataclass
    class Exponential(Base):
        """Exponential relationship: target = scale * exp(rate * source)"""

        scale: float = 1.0
        rate: float = 1.0

        def apply(
            self, source: np.ndarray, rng: np.random.Generator
        ) -> np.ndarray:
            delayed = np.roll(source, self.delay)
            if self.delay > 0:
                delayed[: self.delay] = delayed[self.delay]

            target = self.scale * np.exp(self.rate * delayed)
            noise = rng.normal(
                0, self.noise_level * target, len(source)
            )  # Proportional noise
            return target + noise

    @dataclass
    class Threshold(Base):
        """Threshold-based relationship with different behavior above/below threshold"""

        threshold: float = 0.0
        slope_below: float = 1.0
        slope_above: float = 2.0

        def apply(
            self, source: np.ndarray, rng: np.random.Generator
        ) -> np.ndarray:
            delayed = np.roll(source, self.delay)
            if self.delay > 0:
                delayed[: self.delay] = delayed[self.delay]

            target = np.where(
                delayed > self.threshold,
                self.slope_above * (delayed - self.threshold),
                self.slope_below * delayed,
            )
            noise = rng.normal(0, self.noise_level, len(source))
            return target + noise

    @dataclass
    class Periodic(Base):
        """Periodic relationship modulated by source signal"""

        amplitude: float = 1.0
        base_frequency: float = 1.0  # Base frequency

        def apply(
            self, source: np.ndarray, rng: np.random.Generator
        ) -> np.ndarray:
            delayed = np.roll(source, self.delay)
            if self.delay > 0:
                delayed[: self.delay] = delayed[self.delay]

            time = np.arange(len(source))
            # Frequency modulation based on source signal
            frequency = self.base_frequency * (1 + delayed)
            target = self.amplitude * np.sin(
                2 * np.pi * frequency * time / len(source)
            )
            noise = rng.normal(0, self.noise_level, len(source))
            return target + noise
