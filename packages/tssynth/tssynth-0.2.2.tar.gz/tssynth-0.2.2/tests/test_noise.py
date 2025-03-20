import pytest
import numpy as np
from numpy.random import default_rng
from tssynth.noise import Noise


@pytest.fixture
def rng():
    """Fixture for reproducible random number generation"""
    return default_rng(42)


class TestNoiseBase:
    def test_base_noise_not_implemented(self):
        """Test that Base class raises NotImplementedError"""
        base_noise = Noise.Base()
        with pytest.raises(NotImplementedError):
            base_noise.generate(100, default_rng())


class TestGaussianNoise:
    def test_gaussian_noise_generation(self, rng):
        """Test that Gaussian noise generates with expected properties"""
        std = 2.0
        length = 10000
        gaussian_noise = Noise.Gaussian(std=std)

        noise = gaussian_noise.generate(length, rng)

        # Check shape
        assert len(noise) == length

        # Check statistical properties (with some tolerance)
        assert -0.1 < np.mean(noise) < 0.1  # Mean should be close to 0
        assert (
            1.9 < np.std(noise) < 2.1
        )  # Std should be close to specified value

    def test_gaussian_noise_reproducibility(self):
        """Test that Gaussian noise is reproducible with same seed"""
        length = 100
        gaussian_noise = Noise.Gaussian(std=1.0)

        rng1 = default_rng(42)
        rng2 = default_rng(42)

        noise1 = gaussian_noise.generate(length, rng1)
        noise2 = gaussian_noise.generate(length, rng2)

        # Same seed should produce identical noise
        assert np.array_equal(noise1, noise2)

    def test_gaussian_noise_different_seeds(self):
        """Test that Gaussian noise differs with different seeds"""
        length = 100
        gaussian_noise = Noise.Gaussian(std=1.0)

        rng1 = default_rng(42)
        rng2 = default_rng(43)

        noise1 = gaussian_noise.generate(length, rng1)
        noise2 = gaussian_noise.generate(length, rng2)

        # Different seeds should produce different noise
        assert not np.array_equal(noise1, noise2)


class TestUniformNoise:
    def test_uniform_noise_generation(self, rng):
        """Test that Uniform noise generates with expected properties"""
        low = -3.0
        high = 5.0
        length = 10000
        uniform_noise = Noise.Uniform(low=low, high=high)

        noise = uniform_noise.generate(length, rng)

        # Check shape
        assert len(noise) == length

        # Check bounds
        assert np.min(noise) >= low
        assert np.max(noise) <= high

        # Check statistical properties (with some tolerance)
        expected_mean = (low + high) / 2
        assert expected_mean - 0.1 < np.mean(noise) < expected_mean + 0.1

    def test_uniform_noise_reproducibility(self):
        """Test that Uniform noise is reproducible with same seed"""
        length = 100
        uniform_noise = Noise.Uniform(low=-1.0, high=1.0)

        rng1 = default_rng(42)
        rng2 = default_rng(42)

        noise1 = uniform_noise.generate(length, rng1)
        noise2 = uniform_noise.generate(length, rng2)

        # Same seed should produce identical noise
        assert np.array_equal(noise1, noise2)


class TestMultiplicativeNoise:
    def test_multiplicative_noise_generation(self, rng):
        """Test that Multiplicative noise generates with expected properties"""
        factor = 0.2
        length = 10000
        multiplicative_noise = Noise.Multiplicative(factor=factor)

        noise = multiplicative_noise.generate(length, rng)

        # Check shape
        assert len(noise) == length

        # Check statistical properties (with some tolerance)
        assert 0.9 < np.mean(noise) < 1.1  # Mean should be close to 1
        assert 0.18 < np.std(noise) < 0.22  # Std should be close to factor

    def test_multiplicative_noise_reproducibility(self):
        """Test that Multiplicative noise is reproducible with same seed"""
        length = 100
        multiplicative_noise = Noise.Multiplicative(factor=0.1)

        rng1 = default_rng(42)
        rng2 = default_rng(42)

        noise1 = multiplicative_noise.generate(length, rng1)
        noise2 = multiplicative_noise.generate(length, rng2)

        # Same seed should produce identical noise
        assert np.array_equal(noise1, noise2)

    def test_multiplicative_noise_different_factors(self, rng):
        """Test that different factors produce different noise scales"""
        length = 1000
        factor1 = 0.1
        factor2 = 0.3

        noise1 = Noise.Multiplicative(factor=factor1).generate(length, rng)
        # Create a new RNG with the same seed to ensure comparable results
        rng2 = default_rng(42)
        noise2 = Noise.Multiplicative(factor=factor2).generate(length, rng2)

        # Higher factor should result in higher standard deviation
        assert np.std(noise1) < np.std(noise2)
