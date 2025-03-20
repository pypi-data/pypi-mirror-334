import pytest
import numpy as np
from numpy.random import default_rng
from tssynth.anomalies import Anomalies, Dependencies


@pytest.fixture
def rng():
    """Fixture for reproducible random number generation"""
    return default_rng(42)


@pytest.fixture
def sample_series():
    """Fixture for a sample time series"""
    return np.zeros(100)


class TestPointAnomalies:
    def test_fixed_position_point_anomaly(self, sample_series, rng):
        point_anomaly = Anomalies.Point(position=50, magnitude=5.0)
        modified = point_anomaly.apply(sample_series.copy(), rng)

        assert modified[50] == 5.0
        assert np.sum(modified != 0) == 1  # Only one point should be modified

    def test_random_position_point_anomaly(self, sample_series, rng):
        point_anomaly = Anomalies.Point(magnitude=5.0)  # No position specified
        modified = point_anomaly.apply(sample_series.copy(), rng)

        assert np.sum(modified == 5.0) == 1  # One point should be modified
        assert np.sum(modified != 0) == 1

    def test_return_indices_point_anomaly(self, sample_series, rng):
        point_anomaly = Anomalies.Point(position=25, magnitude=5.0)
        modified, indices = point_anomaly.apply(
            sample_series.copy(), rng, return_indices=True
        )

        assert len(indices) == 1
        assert indices[0] == 25
        assert modified[indices[0]] == 5.0

    def test_position_exceeds_length(self, sample_series, rng):
        point_anomaly = Anomalies.Point(
            position=150, magnitude=5.0
        )  # Position > length
        with pytest.raises(ValueError, match="Position exceeds series length"):
            point_anomaly.apply(sample_series.copy(), rng)


class TestCollectiveAnomalies:
    def test_fixed_position_collective_anomaly(self, sample_series, rng):
        collective_anomaly = Anomalies.Collective(
            start=30, duration=5, magnitude=5.0
        )
        modified = collective_anomaly.apply(sample_series.copy(), rng)

        assert np.all(modified[30:35] == 5.0)
        assert np.sum(modified != 0) == 5  # Five points should be modified

    def test_random_position_collective_anomaly(self, sample_series, rng):
        collective_anomaly = Anomalies.Collective(
            duration=5, magnitude=5.0
        )  # No start specified
        modified = collective_anomaly.apply(sample_series.copy(), rng)

        assert np.sum(modified == 5.0) == 5  # Five points should be modified
        assert np.sum(modified != 0) == 5

    def test_return_indices_collective_anomaly(self, sample_series, rng):
        collective_anomaly = Anomalies.Collective(
            start=20, duration=5, magnitude=5.0
        )
        modified, indices = collective_anomaly.apply(
            sample_series.copy(), rng, return_indices=True
        )

        assert len(indices) == 5
        assert np.array_equal(indices, np.arange(20, 25))
        assert np.all(modified[indices] == 5.0)

    def test_boundary_collective_anomaly(self, sample_series, rng):
        # Test when anomaly would exceed series length
        collective_anomaly = Anomalies.Collective(
            start=98, duration=5, magnitude=5.0
        )
        modified = collective_anomaly.apply(sample_series.copy(), rng)

        assert np.all(modified[98:] == 5.0)  # Should only modify up to the end
        assert np.sum(modified != 0) == 2  # Only 2 points should be modified


def test_base_anomaly():
    """Test that Base class raises NotImplementedError"""
    base_anomaly = Anomalies.Base()
    with pytest.raises(NotImplementedError):
        base_anomaly.apply(np.array([]), default_rng())


def test_base_dependency():
    """Test that Dependencies.Base class raises NotImplementedError"""
    base_dep = Dependencies.Base()
    with pytest.raises(NotImplementedError):
        base_dep.apply(np.array([]), default_rng())


# New tests for Dependencies classes


@pytest.fixture
def linear_source():
    """Fixture for a linear source signal"""
    return np.linspace(0, 10, 100)


class TestLinearDependency:
    def test_linear_dependency_no_delay(self, linear_source, rng):
        """Test linear dependency with no delay"""
        slope = 2.0
        intercept = 5.0
        noise_level = 0.0  # No noise for deterministic testing

        linear_dep = Dependencies.Linear(
            slope=slope, intercept=intercept, noise_level=noise_level
        )

        result = linear_dep.apply(linear_source, rng)

        # Check that the transformation is correct
        expected = slope * linear_source + intercept
        assert np.allclose(result, expected)

    def test_linear_dependency_with_delay(self, linear_source, rng):
        """Test linear dependency with delay"""
        slope = 2.0
        intercept = 5.0
        delay = 3
        noise_level = 0.0  # No noise for deterministic testing

        linear_dep = Dependencies.Linear(
            slope=slope,
            intercept=intercept,
            delay=delay,
            noise_level=noise_level,
        )

        result = linear_dep.apply(linear_source, rng)

        # Create expected result with delay
        delayed_source = np.roll(linear_source, delay)
        delayed_source[:delay] = delayed_source[delay]  # Fill initial values
        expected = slope * delayed_source + intercept

        assert np.allclose(result, expected)

    def test_linear_dependency_with_noise(self, linear_source, rng):
        """Test linear dependency with noise"""
        slope = 2.0
        intercept = 5.0
        noise_level = 1.0

        linear_dep = Dependencies.Linear(
            slope=slope, intercept=intercept, noise_level=noise_level
        )

        result = linear_dep.apply(linear_source, rng)

        # The result should not be exactly equal to the expected due to noise
        expected = slope * linear_source + intercept
        assert not np.allclose(result, expected)

        # But the mean difference should be close to zero
        diff = result - expected
        assert -0.5 < np.mean(diff) < 0.5

        # And the standard deviation should be close to the noise level
        assert (
            0.7 < np.std(diff) < 1.3
        )  # Wider bounds to account for sampling variation


class TestInverseDependency:
    def test_inverse_dependency_basic(self, linear_source, rng):
        """Test inverse dependency with basic parameters"""
        scale = 10.0
        offset = 1.0  # Prevent division by zero
        noise_level = 0.0  # No noise for deterministic testing

        inverse_dep = Dependencies.Inverse(
            scale=scale, offset=offset, noise_level=noise_level
        )

        result = inverse_dep.apply(linear_source, rng)

        # Check that the transformation is correct
        expected = scale / (linear_source + offset)
        assert np.allclose(result, expected)

    def test_inverse_dependency_with_delay(self, linear_source, rng):
        """Test inverse dependency with delay"""
        scale = 10.0
        offset = 1.0
        delay = 5
        noise_level = 0.0

        inverse_dep = Dependencies.Inverse(
            scale=scale, offset=offset, delay=delay, noise_level=noise_level
        )

        result = inverse_dep.apply(linear_source, rng)

        # Create expected result with delay
        delayed_source = np.roll(linear_source, delay)
        delayed_source[:delay] = delayed_source[delay]
        expected = scale / (delayed_source + offset)

        assert np.allclose(result, expected)


class TestExponentialDependency:
    def test_exponential_dependency_basic(self, rng):
        """Test exponential dependency with basic parameters"""
        source = np.linspace(0, 2, 100)  # Smaller range to avoid overflow
        scale = 2.0
        rate = 0.5
        noise_level = 0.0

        exp_dep = Dependencies.Exponential(
            scale=scale, rate=rate, noise_level=noise_level
        )

        result = exp_dep.apply(source, rng)

        # Check that the transformation is correct
        expected = scale * np.exp(rate * source)
        assert np.allclose(result, expected)

    def test_exponential_dependency_with_delay(self, rng):
        """Test exponential dependency with delay"""
        source = np.linspace(0, 2, 100)
        scale = 2.0
        rate = 0.5
        delay = 4
        noise_level = 0.0

        exp_dep = Dependencies.Exponential(
            scale=scale, rate=rate, delay=delay, noise_level=noise_level
        )

        result = exp_dep.apply(source, rng)

        # Create expected result with delay
        delayed_source = np.roll(source, delay)
        delayed_source[:delay] = delayed_source[delay]
        expected = scale * np.exp(rate * delayed_source)

        assert np.allclose(result, expected)

    def test_exponential_dependency_with_noise(self, rng):
        """Test exponential dependency with proportional noise"""
        source = np.linspace(0, 2, 100)
        scale = 2.0
        rate = 0.5
        noise_level = 0.1

        exp_dep = Dependencies.Exponential(
            scale=scale, rate=rate, noise_level=noise_level
        )

        result = exp_dep.apply(source, rng)

        # The result should not be exactly equal to the expected due to noise
        expected = scale * np.exp(rate * source)
        assert not np.allclose(result, expected)


class TestThresholdDependency:
    def test_threshold_dependency_basic(self, linear_source, rng):
        """Test threshold dependency with basic parameters"""
        threshold = 5.0
        slope_below = 1.0
        slope_above = 2.0
        noise_level = 0.0

        threshold_dep = Dependencies.Threshold(
            threshold=threshold,
            slope_below=slope_below,
            slope_above=slope_above,
            noise_level=noise_level,
        )

        result = threshold_dep.apply(linear_source, rng)

        # Check that the transformation is correct
        expected = np.where(
            linear_source > threshold,
            slope_above * (linear_source - threshold),
            slope_below * linear_source,
        )
        assert np.allclose(result, expected)

    def test_threshold_dependency_with_delay(self, linear_source, rng):
        """Test threshold dependency with delay"""
        threshold = 5.0
        slope_below = 1.0
        slope_above = 2.0
        delay = 3
        noise_level = 0.0

        threshold_dep = Dependencies.Threshold(
            threshold=threshold,
            slope_below=slope_below,
            slope_above=slope_above,
            delay=delay,
            noise_level=noise_level,
        )

        result = threshold_dep.apply(linear_source, rng)

        # Create expected result with delay
        delayed_source = np.roll(linear_source, delay)
        delayed_source[:delay] = delayed_source[delay]
        expected = np.where(
            delayed_source > threshold,
            slope_above * (delayed_source - threshold),
            slope_below * delayed_source,
        )

        assert np.allclose(result, expected)


class TestPeriodicDependency:
    def test_periodic_dependency_basic(self, linear_source, rng):
        """Test periodic dependency with basic parameters"""
        amplitude = 2.0
        base_frequency = 0.5
        noise_level = 0.0

        periodic_dep = Dependencies.Periodic(
            amplitude=amplitude,
            base_frequency=base_frequency,
            noise_level=noise_level,
        )

        result = periodic_dep.apply(linear_source, rng)

        # Check that the result has the expected shape and properties
        assert len(result) == len(linear_source)
        assert -amplitude <= np.min(result) <= np.max(result) <= amplitude

    def test_periodic_dependency_with_delay(self, linear_source, rng):
        """Test periodic dependency with delay"""
        amplitude = 2.0
        base_frequency = 0.5
        delay = 5
        noise_level = 0.0

        periodic_dep = Dependencies.Periodic(
            amplitude=amplitude,
            base_frequency=base_frequency,
            delay=delay,
            noise_level=noise_level,
        )

        result = periodic_dep.apply(linear_source, rng)

        # Create expected result with delay
        delayed_source = np.roll(linear_source, delay)
        delayed_source[:delay] = delayed_source[delay]
        time = np.arange(len(linear_source))
        frequency = base_frequency * (1 + delayed_source)
        expected = amplitude * np.sin(
            2 * np.pi * frequency * time / len(linear_source)
        )

        assert np.allclose(result, expected)
