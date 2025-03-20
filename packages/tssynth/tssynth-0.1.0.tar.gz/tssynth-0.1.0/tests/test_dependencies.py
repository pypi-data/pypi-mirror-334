import pytest
import numpy as np
from tssynth.dependencies import Dependencies
from tssynth.core import MultiSensorTS
from tssynth.trends import Trends


@pytest.fixture
def rng():
    """Fixture for reproducible random number generation"""
    return np.random.default_rng(42)


@pytest.fixture
def sample_signal():
    """Fixture for a simple test signal"""
    return np.array([1.0, 2.0, 3.0, 4.0, 5.0])


class TestLinearDependency:
    def test_basic_linear(self, sample_signal, rng):
        dep = Dependencies.Linear(slope=2.0, intercept=1.0, noise_level=0.0)
        result = dep.apply(sample_signal, rng)
        expected = sample_signal * 2.0 + 1.0
        np.testing.assert_array_almost_equal(result, expected)

    @pytest.skip("Skipping linear with delay test", allow_module_level=True)
    def test_linear_with_delay(self, sample_signal, rng):
        dep = Dependencies.Linear(slope=2.0, delay=2, noise_level=0.0)
        result = dep.apply(sample_signal, rng)
        expected = np.array([1.0, 2.0, 6.0, 8.0, 10.0])
        np.testing.assert_array_almost_equal(result, expected)

    def test_linear_with_noise(self, sample_signal, rng):
        dep = Dependencies.Linear(noise_level=1.0)
        result = dep.apply(sample_signal, rng)
        assert not np.array_equal(result, sample_signal)  # Should have noise
        assert len(result) == len(sample_signal)


class TestInverseDependency:
    def test_basic_inverse(self, sample_signal, rng):
        dep = Dependencies.Inverse(scale=1.0, offset=0.0, noise_level=0.0)
        result = dep.apply(sample_signal, rng)
        expected = 1.0 / sample_signal
        np.testing.assert_array_almost_equal(result, expected)

    def test_inverse_with_offset(self, rng):
        signal = np.array([-1.0, 0.0, 1.0])
        dep = Dependencies.Inverse(scale=1.0, offset=2.0, noise_level=0.0)
        result = dep.apply(signal, rng)
        expected = 1.0 / (signal + 2.0)
        np.testing.assert_array_almost_equal(result, expected)


class TestExponentialDependency:
    def test_basic_exponential(self, sample_signal, rng):
        dep = Dependencies.Exponential(scale=1.0, rate=1.0, noise_level=0.0)
        result = dep.apply(sample_signal, rng)
        expected = np.exp(sample_signal)
        np.testing.assert_array_almost_equal(result, expected)

    def test_exponential_scaling(self, sample_signal, rng):
        dep = Dependencies.Exponential(scale=2.0, rate=0.5, noise_level=0.0)
        result = dep.apply(sample_signal, rng)
        expected = 2.0 * np.exp(0.5 * sample_signal)
        np.testing.assert_array_almost_equal(result, expected)


class TestThresholdDependency:
    def test_basic_threshold(self, sample_signal, rng):
        dep = Dependencies.Threshold(
            threshold=3.0, slope_below=1.0, slope_above=2.0, noise_level=0.0
        )
        result = dep.apply(sample_signal, rng)
        expected = np.where(
            sample_signal > 3.0,
            2.0 * (sample_signal - 3.0),
            1.0 * sample_signal,
        )
        np.testing.assert_array_almost_equal(result, expected)


class TestPeriodicDependency:
    def test_basic_periodic(self, sample_signal, rng):
        dep = Dependencies.Periodic(
            amplitude=1.0,
            period=1.0,
            noise_level=0.0,
        )
        result = dep.apply(sample_signal, rng)
        assert len(result) == len(sample_signal)
        assert np.all(np.abs(result) <= dep.amplitude)

    def test_periodic_frequency_modulation(self, rng):
        signal = np.ones(100)  # Constant signal
        dep = Dependencies.Periodic(
            amplitude=20.0,
            period=3.0,
            noise_level=0.0,
        )
        result = dep.apply(signal, rng)
        # Should produce regular sine wave with base frequency
        peaks = np.where(np.diff(np.signbit(np.diff(result))))[0]
        assert len(peaks) > 0  # Should have some peaks


def test_base_dependency():
    """Test that Base dependency raises NotImplementedError"""
    dep = Dependencies.Base()
    with pytest.raises(NotImplementedError):
        dep.apply(np.array([1.0]), np.random.default_rng())


@pytest.mark.parametrize(
    "dependency_class",
    [
        Dependencies.Linear,
        Dependencies.Inverse,
        Dependencies.Exponential,
        Dependencies.Threshold,
        Dependencies.Periodic,
    ],
)
def test_all_dependencies_handle_empty_array(dependency_class, rng):
    """Test that all dependencies can handle empty arrays"""
    dep = dependency_class()
    empty_signal = np.array([])
    result = dep.apply(empty_signal, rng)
    assert len(result) == 0


def test_dependency_chain_with_multiple_sources():
    """Test dependency chain with multiple sources"""
    # Create a MultiSensorTS with multiple sensors and dependencies
    ts = MultiSensorTS(length=100, seed=42)

    # Add source sensors first
    ts.add_sensor(name="source1", trend=Trends.Linear(slope=0.1, intercept=0))
    ts.add_sensor(
        name="source2",
        trend=Trends.Periodic(amplitude=5, period=50, offset=10),
    )

    # Add intermediate sensor with its base trend
    ts.add_sensor(
        name="intermediate", trend=Trends.Linear(slope=0.05, intercept=5)
    )

    # Add dependency from source1 to intermediate
    ts.add_dependency(
        target="intermediate",
        source="source1",
        dependency=Dependencies.Linear(slope=0.5, intercept=2),
    )

    # Add target sensor that depends on both intermediate and source2
    ts.add_sensor(
        name="target",
        trend=Trends.Constant(
            value=0
        ),  # Base signal will be determined by dependencies
    )

    # Add dependencies to target
    ts.add_dependency(
        target="target",
        source="intermediate",
        dependency=Dependencies.Linear(slope=1.5, intercept=0),
    )
    ts.add_dependency(
        target="target",
        source="source2",
        dependency=Dependencies.Linear(slope=0.3, intercept=1),
    )

    # Generate the data
    df = ts.generate()

    # Check that all sensors are present
    assert "source1" in df.columns
    assert "source2" in df.columns
    assert "intermediate" in df.columns
    assert "target" in df.columns

    # Calculate the base signal for intermediate (without dependencies)
    t = np.arange(100)
    intermediate_base = 0.05 * t + 5  # From the Linear trend

    # Calculate source1's contribution to intermediate
    source1_values = 0.1 * t  # From source1's Linear trend
    intermediate_from_source1 = 0.5 * source1_values + 2  # From the dependency

    # Expected intermediate values (base + dependency effect)
    expected_intermediate = intermediate_base + intermediate_from_source1

    # Calculate source2's contribution to target
    source2_values = (
        5 * np.sin(2 * np.pi * t / 50) + 10
    )  # From source2's Periodic trend
    target_from_source2 = 0.3 * source2_values + 1

    # Calculate target's expected values
    target_from_intermediate = 1.5 * df["intermediate"]
    expected_target = target_from_intermediate + target_from_source2

    # Verify the dependencies were applied correctly
    np.testing.assert_array_almost_equal(
        df["intermediate"], expected_intermediate, decimal=2
    )
    np.testing.assert_array_almost_equal(
        df["target"], expected_target, decimal=2
    )


def test_dependency_with_missing_source():
    """Test handling of dependency with missing source"""
    # Create a MultiSensorTS
    ts = MultiSensorTS(length=100, seed=42)

    # Add a target sensor
    ts.add_sensor(name="target", trend=Trends.Linear(slope=0.1, intercept=0))

    # Try to add a dependency with a non-existent source
    with pytest.raises(
        ValueError, match="Source sensor 'nonexistent' not found"
    ):
        ts.add_dependency(
            target="target",
            source="nonexistent",
            dependency=Dependencies.Linear(slope=1.0, intercept=0),
        )


def test_dependency_with_missing_target():
    """Test handling of dependency with missing target"""
    # Create a MultiSensorTS
    ts = MultiSensorTS(length=100, seed=42)

    # Add a source sensor
    ts.add_sensor(name="source", trend=Trends.Linear(slope=0.1, intercept=0))

    # Try to add a dependency with a non-existent target
    with pytest.raises(
        ValueError, match="Target sensor 'nonexistent' not found"
    ):
        ts.add_dependency(
            target="nonexistent",
            source="source",
            dependency=Dependencies.Linear(slope=1.0, intercept=0),
        )
