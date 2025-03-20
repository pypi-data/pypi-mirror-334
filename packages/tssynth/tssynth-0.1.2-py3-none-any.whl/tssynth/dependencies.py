from dataclasses import dataclass
from tssynth import logger
import numpy as np


class Dependencies:
    """Collection of sensor dependency relationships.

    This class provides various mathematical relationships between sensor signals,
    allowing for the creation of synthetic dependent time series with configurable
    noise and time delays.
    """

    @dataclass
    class Base:
        """Base class for dependency relationships.

        All dependency types inherit from this class, providing common parameters
        for time delays and noise injection.

        Attributes:
            delay (int): Number of time steps to delay applying the dependency
            noise_level (float): Standard deviation of Gaussian noise to add
            apply_before_anomaly (bool): Whether to apply dependency before anomaly injection
        """

        delay: int = 0  # Time delay in steps
        noise_level: float = 0.1  # Amount of noise in relationship
        apply_before_anomaly: bool = True

        def apply(
            self, source: np.ndarray, rng: np.random.Generator
        ) -> np.ndarray:
            """Apply dependency relationship to source signal.

            Args:
                source (np.ndarray): Input signal to transform
                rng (np.random.Generator): NumPy random number generator

            Returns:
                np.ndarray: Transformed signal with applied relationship and noise
            """
            logger.debug(
                f"Applying base dependency with delay={self.delay}, noise_level={self.noise_level}"
            )
            raise NotImplementedError

    @dataclass
    class Linear(Base):
        """Linear relationship: target = slope * source + intercept

        Implements a linear transformation of the source signal with configurable
        slope and intercept parameters.

        Attributes:
            slope (float): Multiplicative factor for the linear relationship
            intercept (float): Constant offset added to the transformed signal
        """

        slope: float = 1.0
        intercept: float = 0.0

        def apply(
            self,
            source: np.ndarray,
            rng: np.random.Generator,
            return_indices: bool = False,
        ) -> np.ndarray:
            logger.debug(
                f"Applying linear dependency: slope={self.slope}, intercept={self.intercept}"
            )

            # Apply linear transformation to entire signal
            target = self.slope * source + self.intercept

            # Handle delay if present
            if self.delay > 0:
                target = np.roll(target, self.delay)
                target[: self.delay] = source[
                    : self.delay
                ]  # Use source values for delay period

            # Add noise to entire signal
            noise = rng.normal(0, self.noise_level, len(source))
            target = target + noise

            return target

    @dataclass
    class Inverse(Base):
        """Inverse relationship: target = scale / source

        Implements an inverse relationship between source and target signals.
        Includes an offset parameter to prevent division by zero.

        Attributes:
            scale (float): Scaling factor for the inverse relationship
            offset (float): Value added to source to prevent division by zero
        """

        scale: float = 1.0
        offset: float = 0.0  # Prevent division by zero

        def apply(
            self,
            source: np.ndarray,
            rng: np.random.Generator,
            return_indices: bool = False,
        ) -> np.ndarray:
            logger.debug(
                f"Applying inverse dependency: scale={self.scale}, offset={self.offset}"
            )
            if np.any(np.abs(source + self.offset) < 1e-10):
                logger.warning(
                    "Near-zero values detected in source signal for inverse relationship"
                )

            start_normal_source = source[: self.delay]
            rest_source = source[self.delay :]
            rest_target = self.scale / (rest_source + self.offset)
            target = np.concatenate([start_normal_source, rest_target])
            noise = rng.normal(0, self.noise_level, len(source))
            return target + noise

    @dataclass
    class Exponential(Base):
        """Exponential relationship: target = scale * exp(rate * source)

        Implements an exponential transformation of the source signal.
        Uses proportional noise scaling with signal magnitude.

        Attributes:
            scale (float): Scaling factor for the output
            rate (float): Rate parameter in the exponential function
        """

        scale: float = 1.0
        rate: float = 1.0

        def apply(
            self,
            source: np.ndarray,
            rng: np.random.Generator,
            return_indices: bool = False,
        ) -> np.ndarray:
            logger.debug(
                f"Applying exponential dependency: scale={self.scale}, rate={self.rate}"
            )
            if np.any(np.abs(self.rate * source) > 100):
                logger.warning(
                    "Large values detected in exponential calculation - may lead to overflow"
                )

            start_normal_source = source[: self.delay]
            rest_source = source[self.delay :]
            rest_target = self.scale * np.exp(self.rate * rest_source)
            target = np.concatenate([start_normal_source, rest_target])
            noise = rng.normal(0, self.noise_level, len(source))
            return target + noise

    @dataclass
    class Threshold(Base):
        """Threshold-based relationship with different behavior above/below threshold.

        Implements a piecewise linear relationship that changes behavior at a
        specified threshold value.

        Attributes:
            threshold (float): Value at which behavior changes
            slope_below (float): Slope for values below threshold
            slope_above (float): Slope for values above threshold
        """

        threshold: float = 0.0
        slope_below: float = 1.0
        slope_above: float = 2.0

        def apply(
            self,
            source: np.ndarray,
            rng: np.random.Generator,
            return_indices: bool = False,
        ) -> np.ndarray:
            logger.debug(
                f"Applying threshold dependency: threshold={self.threshold}, "
                f"slope_below={self.slope_below}, slope_above={self.slope_above}"
            )
            start_normal_source = source[: self.delay]
            rest_source = source[self.delay :]
            rest_target = np.where(
                rest_source > self.threshold,
                self.slope_above * (rest_source - self.threshold),
                self.slope_below * rest_source,
            )
            target = np.concatenate([start_normal_source, rest_target])
            noise = rng.normal(0, self.noise_level, len(source))
            return target + noise

    @dataclass
    class Periodic(Base):
        """Periodic relationship modulated by source signal.

        Implements a sinusoidal relationship where the source signal
        modulates the frequency of oscillation.

        Attributes:
            amplitude (float): Peak amplitude of the periodic signal
            period (float): The period of oscillation before modulation
        """

        amplitude: float = 1.0
        period: float = 1.0  # Base frequency

        def apply(
            self,
            source: np.ndarray,
            rng: np.random.Generator,
            return_indices: bool = False,
        ) -> np.ndarray:
            logger.debug(
                f"Applying periodic dependency: amplitude={self.amplitude}, period={self.period}"
            )
            if self.period <= 0:
                logger.warning(
                    "Period is not positive - may produce unexpected results"
                )

            start_normal_source = source[: self.delay]

            rest_source = source[self.delay :]
            time = np.arange(len(rest_source))
            rest_target = self.amplitude * np.sin(
                2 * np.pi * time / self.period
            )
            rest_target = rest_target * rest_source

            target = np.concatenate([start_normal_source, rest_target])
            noise = rng.normal(0, self.noise_level, len(source))
            return target + noise
