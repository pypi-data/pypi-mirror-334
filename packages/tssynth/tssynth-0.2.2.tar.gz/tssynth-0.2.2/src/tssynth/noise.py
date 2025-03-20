import numpy as np
from dataclasses import dataclass
from numpy.random import Generator


class Noise:
    """Collection of noise patterns for time series.

    This class provides various noise generators that can be used to add realistic
    variability to synthetic time series data. Available noise types include
    Gaussian (normal), uniform, and multiplicative noise patterns.
    """

    @dataclass
    class Base:
        """Base class for all noise types.

        This abstract class defines the interface that all noise generators must implement.
        Subclasses should implement the generate() method to provide specific noise patterns.
        """

        def generate(self, length: int, rng: Generator) -> np.ndarray:
            """Generate a noise sequence.

            Parameters
            ----------
            length : int
                The number of noise samples to generate
            rng : numpy.random.Generator
                Random number generator instance to use

            Returns
            -------
            numpy.ndarray
                Array of noise values with the specified length

            Raises
            ------
            NotImplementedError
                This is an abstract method that must be implemented by subclasses
            """
            raise NotImplementedError

    @dataclass
    class Gaussian(Base):
        """Gaussian (normal) distributed noise generator.

        Parameters
        ----------
        std : float, default=1.0
            Standard deviation of the Gaussian distribution. Controls the amplitude
            of the noise.
        """

        std: float = 1.0

        def generate(self, length: int, rng: Generator) -> np.ndarray:
            """Generate Gaussian distributed noise.

            Parameters
            ----------
            length : int
                The number of noise samples to generate
            rng : numpy.random.Generator
                Random number generator instance to use

            Returns
            -------
            numpy.ndarray
                Array of normally distributed noise values with mean 0 and
                specified standard deviation
            """
            return rng.normal(0, self.std, length)

    @dataclass
    class Uniform(Base):
        """Uniform distributed noise generator.

        Parameters
        ----------
        low : float, default=-1.0
            Lower bound of the uniform distribution
        high : float, default=1.0
            Upper bound of the uniform distribution
        """

        low: float = -1.0
        high: float = 1.0

        def generate(self, length: int, rng: Generator) -> np.ndarray:
            """Generate uniformly distributed noise.

            Parameters
            ----------
            length : int
                The number of noise samples to generate
            rng : numpy.random.Generator
                Random number generator instance to use

            Returns
            -------
            numpy.ndarray
                Array of uniformly distributed noise values between low and high
            """
            return rng.uniform(self.low, self.high, length)

    @dataclass
    class Multiplicative(Base):
        """Multiplicative noise generator.

        Generates noise values centered around 1.0, suitable for multiplicative
        noise effects. The noise follows a normal distribution with mean 1.0.

        Parameters
        ----------
        factor : float, default=0.1
            Standard deviation of the noise. A factor of 0.1 means the noise
            values will typically vary between 0.9 and 1.1 (±1 standard deviation)
        """

        factor: float = 0.1

        def generate(self, length: int, rng: Generator) -> np.ndarray:
            """Generate multiplicative noise.

            Parameters
            ----------
            length : int
                The number of noise samples to generate
            rng : numpy.random.Generator
                Random number generator instance to use

            Returns
            -------
            numpy.ndarray
                Array of normally distributed noise values with mean 1 and
                specified standard deviation (factor)
            """
            return rng.normal(1, self.factor, length)
