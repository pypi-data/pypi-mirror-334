import numpy as np
from typing import List
from dataclasses import dataclass


class Trends:
    """Collection of trend patterns for time series.

    This class provides various mathematical functions for generating trend
    components in synthetic time series data, including linear, periodic,
    exponential, and logistic patterns.
    """

    @dataclass
    class Base:
        """Base class for all trends.

        Provides the interface that all trend classes must implement.
        Each trend type should define how it generates a time series of
        specified length.
        """

        def generate(self, length: int) -> np.ndarray:
            """Generate trend values for the specified length.

            Args:
                length (int): Number of time steps to generate

            Returns:
                np.ndarray: Array of trend values
            """
            raise NotImplementedError

    @dataclass
    class Constant(Base):
        """Constant trend generator.

        Generates a constant value for all time steps.
        Useful for baseline signals or when trend should be determined entirely by dependencies.

        Attributes:
            value (float): The constant value to generate
        """

        value: float = 0.0

        def generate(self, length: int) -> np.ndarray:
            """Generate constant trend values.

            Args:
                length (int): Number of time steps to generate

            Returns:
                np.ndarray: Array of constant values
            """
            if length < 0:
                raise ValueError("Length must be greater than 0")
            return np.full(length, self.value)

    @dataclass
    class Linear(Base):
        """Linear trend generator.

        Generates a straight line defined by slope and intercept:
        y = slope * t + intercept

        Attributes:
            slope (float): Rate of change per time step
            intercept (float): Starting value at t=0
        """

        slope: float = 1.0
        intercept: float = 0.0

        def generate(self, length: int) -> np.ndarray:
            """Generate linear trend values.

            Args:
                length (int): Number of time steps to generate

            Returns:
                np.ndarray: Array of linear trend values
            """
            if length < 0:
                raise ValueError("Length must be greater than 0")
            time = np.arange(length)
            return self.slope * time + self.intercept

    @dataclass
    class Periodic(Base):
        """Periodic (sinusoidal) trend generator.

        Generates a sine wave with configurable amplitude, period, phase, and offset:
        y = amplitude * sin(2π * t/period + phase) + offset

        Attributes:
            amplitude (float): Peak deviation from the center
            period (float): Number of time steps for one complete cycle
            phase (float): Phase shift in radians
            offset (float): Vertical shift from zero
        """

        amplitude: float = 1.0
        period: float = 100.0
        phase: float = 0.0
        offset: float = 0.0

        def generate(self, length: int) -> np.ndarray:
            """Generate periodic trend values.

            Args:
                length (int): Number of time steps to generate

            Returns:
                np.ndarray: Array of periodic trend values
            """
            time = np.arange(length)
            return (
                self.amplitude
                * np.sin(2 * np.pi * time / self.period + self.phase)
                + self.offset
            )

    @dataclass
    class Exponential(Base):
        """Exponential trend generator.

        Generates exponential growth or decay:
        y = base * exp(growth_rate * t)

        Attributes:
            growth_rate (float): Rate of exponential growth (positive) or decay (negative)
            base (float): Initial value at t=0
        """

        growth_rate: float = 0.1
        base: float = 1.0

        def generate(self, length: int) -> np.ndarray:
            """Generate exponential trend values.

            Args:
                length (int): Number of time steps to generate

            Returns:
                np.ndarray: Array of exponential trend values
            """
            time = np.arange(length)
            return self.base * np.exp(self.growth_rate * time)

    @dataclass
    class Logistic(Base):
        """Logistic (sigmoid) trend generator.

        Generates an S-shaped curve commonly used for population growth:
        y = carrying_capacity / (1 + exp(-growth_rate * (t - carrying_capacity/2)))

        Attributes:
            growth_rate (float): Steepness of the curve
            carrying_capacity (float): Maximum value (asymptote)
            initial_population (float): Starting value
        """

        growth_rate: float = 0.1
        carrying_capacity: float = 100.0
        initial_population: float = 1.0

        def generate(self, length: int) -> np.ndarray:
            """Generate logistic trend values.

            Args:
                length (int): Number of time steps to generate

            Returns:
                np.ndarray: Array of logistic trend values
            """
            time = np.arange(length)
            return self.carrying_capacity / (
                1
                + np.exp(
                    -self.growth_rate * (time - self.carrying_capacity / 2)
                )
            )

    @dataclass
    class Composite(Base):
        """Combines multiple trends by adding their outputs.

        Allows creation of complex trends by superimposing multiple basic trends.
        For example, combining a linear trend with a periodic trend creates
        an oscillating signal with an overall upward/downward trend.

        Attributes:
            trends (List[Trends.Base]): List of trend components to combine
        """

        trends: List["Trends.Base"]

        def generate(self, length: int) -> np.ndarray:
            """Generate combined trend values.

            Args:
                length (int): Number of time steps to generate

            Returns:
                np.ndarray: Array of combined trend values
            """
            result = np.zeros(length)
            for trend in self.trends:
                result += trend.generate(length)
            return result
