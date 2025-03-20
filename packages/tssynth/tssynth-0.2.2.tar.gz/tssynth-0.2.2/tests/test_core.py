import pytest
import numpy as np
import pandas as pd
from tssynth.core import MultiSensorTS
from tssynth.trends import Trends
from tssynth.noise import Noise
from tssynth.anomalies import Anomalies
from tssynth.dependencies import Dependencies


@pytest.fixture
def basic_ts():
    """Create a basic MultiSensorTS instance for testing."""
    return MultiSensorTS(
        length=100, sampling_rate=1.0, sampling_rate_units="s", seed=42
    )


def test_initialization():
    """Test basic initialization of MultiSensorTS."""
    ts = MultiSensorTS(length=100, sampling_rate=0.5, sampling_rate_units="ms")
    assert ts.length == 100
    assert ts.sampling_rate == 0.5
    assert ts.sampling_rate_units == "ms"
    assert len(ts.sensors) == 0
    assert len(ts.dependencies) == 0


def test_add_sensor(basic_ts):
    """Test adding a sensor with basic components."""
    trend = Trends.Linear(slope=1.0, intercept=0.0)
    noise = Noise.Gaussian(std=0.1)

    basic_ts.add_sensor(name="test_sensor", trend=trend, noise=noise)

    assert "test_sensor" in basic_ts.sensors
    assert basic_ts.sensors["test_sensor"].trend == trend
    assert basic_ts.sensors["test_sensor"].noise == noise
    assert len(basic_ts.sensors["test_sensor"].anomalies) == 0


def test_generate_basic_signal(basic_ts):
    """Test generating a basic signal with trend and noise."""
    trend = Trends.Linear(slope=1.0, intercept=0.0)
    noise = Noise.Gaussian(std=0.1)

    basic_ts.add_sensor(name="test_sensor", trend=trend, noise=noise)

    df = basic_ts.generate()

    assert isinstance(df, pd.DataFrame)
    assert "test_sensor" in df.columns
    assert "test_sensor_anomaly" in df.columns
    assert len(df) == basic_ts.length
    assert not df[
        "test_sensor_anomaly"
    ].any()  # No anomalies should be present


def test_generate_with_anomalies(basic_ts):
    """Test generating a signal with anomalies."""
    trend = Trends.Linear(slope=1.0, intercept=0.0)
    anomaly = Anomalies.Point(magnitude=5.0, position=50)

    basic_ts.add_sensor(name="test_sensor", trend=trend, anomalies=[anomaly])

    df = basic_ts.generate()

    assert "test_sensor_anomaly" in df.columns
    assert (
        df["test_sensor_anomaly"].sum() > 0
    )  # Should have at least one anomaly


def test_add_dependency(basic_ts):
    """Test adding and generating dependent sensors."""
    # Add source sensor
    basic_ts.add_sensor(
        name="source", trend=Trends.Linear(slope=1.0, intercept=0.0)
    )

    # Add target sensor with dependency
    basic_ts.add_sensor(
        name="target", trend=Trends.Linear(slope=0.5, intercept=1.0)
    )

    dependency = Dependencies.Linear(slope=0.5, intercept=0.0)
    basic_ts.add_dependency("target", "source", dependency)

    df = basic_ts.generate()

    assert "source" in df.columns
    assert "target" in df.columns
    assert len(basic_ts.dependencies["target"]) == 1


def test_generate_similar(basic_ts):
    """Test generating similar time series."""
    trend = Trends.Linear(slope=1.0, intercept=0.0)
    noise = Noise.Gaussian(std=0.1)

    basic_ts.add_sensor(name="test_sensor", trend=trend, noise=noise)

    similar_samples = basic_ts.generate_similar(n_samples=3)

    assert len(similar_samples) == 3
    assert all(isinstance(df, pd.DataFrame) for df in similar_samples)
    assert all("test_sensor" in df.columns for df in similar_samples)
    assert all(len(df) == basic_ts.length for df in similar_samples)


def test_sampling_rate_jitter(basic_ts):
    """Test that sampling rate jitter produces different timestamps."""
    basic_ts.sampling_rate_jitter = 0.1
    basic_ts.add_sensor(
        name="test_sensor", trend=Trends.Linear(slope=1.0, intercept=0.0)
    )

    df1 = basic_ts.generate()
    df2 = basic_ts.generate()

    # Check that timestamps are different due to jitter
    assert not (df1.index == df2.index).all()


def test_error_on_missing_dependency():
    """Test that appropriate error is raised for missing dependency source."""
    ts = MultiSensorTS(length=100)

    # Add target sensor
    ts.add_sensor(name="target", trend=Trends.Linear(slope=1.0, intercept=0.0))

    # Add dependency to non-existent source
    dependency = Dependencies.Linear(slope=0.5, intercept=0.0)
    ts.add_dependency("target", "non_existent_source", dependency)

    with pytest.raises(ValueError, match="Source sensor .* not found"):
        ts.generate()


def test_empty_sensor():
    """Test generating a sensor with no components."""
    ts = MultiSensorTS(length=50)
    ts.add_sensor(name="empty_sensor")

    df = ts.generate()
    assert "empty_sensor" in df.columns
    assert "empty_sensor_anomaly" in df.columns
    assert (df["empty_sensor"] == 0).all()  # Should be all zeros
    assert not df["empty_sensor_anomaly"].any()  # No anomalies


def test_multiple_dependencies():
    """Test sensor with multiple dependencies."""
    ts = MultiSensorTS(length=100, seed=42)

    # Add source sensors
    ts.add_sensor(
        name="source1", trend=Trends.Linear(slope=1.0, intercept=0.0)
    )
    ts.add_sensor(
        name="source2", trend=Trends.Periodic(amplitude=1.0, period=10)
    )

    # Add target with multiple dependencies
    ts.add_sensor(name="target")
    ts.add_dependency("target", "source1", Dependencies.Linear(slope=0.5))
    ts.add_dependency("target", "source2", Dependencies.Linear(slope=0.3))

    df = ts.generate()
    assert all(col in df.columns for col in ["source1", "source2", "target"])
    assert len(ts.dependencies["target"]) == 2


def test_generate_similar_with_no_anomalies():
    """Test generating similar series with anomalies disabled."""
    ts = MultiSensorTS(length=100, seed=42)

    ts.add_sensor(
        name="test_sensor",
        trend=Trends.Linear(slope=1.0),
        anomalies=[Anomalies.Point(magnitude=5.0, position=50)],
    )

    similar_samples = ts.generate_similar(n_samples=3, include_anomalies=False)

    assert len(similar_samples) == 3
    assert all(not df["test_sensor_anomaly"].any() for df in similar_samples)


def test_variation_scale_override():
    """Test overriding variation scale in generate_similar."""
    ts = MultiSensorTS(length=100, seed=42, variation_scale=0.1)

    ts.add_sensor(name="test_sensor", trend=Trends.Linear(slope=1.0))

    # Generate with different variation scales
    samples_small = ts.generate_similar(n_samples=5, variation_scale=0.01)
    samples_large = ts.generate_similar(n_samples=5, variation_scale=0.5)

    # Verify original variation scale wasn't changed
    assert ts.variation_scale == 0.1

    # Large variation should produce more diverse signals
    small_std = np.std([df["test_sensor"].std() for df in samples_small])
    large_std = np.std([df["test_sensor"].std() for df in samples_large])
    assert large_std > small_std


def test_dependency_before_after_anomaly():
    """Test dependency application before and after anomalies."""
    ts = MultiSensorTS(length=100, seed=42)

    # Add source with anomaly
    ts.add_sensor(
        name="source",
        trend=Trends.Linear(slope=1.0),
        anomalies=[Anomalies.Point(magnitude=5.0, position=50)],
    )

    # Add two targets with different dependency timing
    ts.add_sensor(name="target_before")
    ts.add_sensor(name="target_after")

    before_dep = Dependencies.Linear(slope=1.0, apply_before_anomaly=True)
    after_dep = Dependencies.Linear(slope=1.0, apply_before_anomaly=False)

    ts.add_dependency("target_before", "source", before_dep)
    ts.add_dependency("target_after", "source", after_dep)

    df = ts.generate()

    # The anomaly effect should be different between the two targets
    assert not (df["target_before"] == df["target_after"]).all()


def test_dependency_application_after_anomalies():
    """Test that dependencies can be applied after anomalies"""
    # Create a MultiSensorTS with two sensors and a dependency
    ts = MultiSensorTS(length=100, seed=42)

    # Add a source sensor with a simple trend
    ts.add_sensor(name="source", trend=Trends.Linear(slope=0.1, intercept=0))

    # Add a target sensor with anomalies
    ts.add_sensor(
        name="target",
        trend=Trends.Linear(slope=0.05, intercept=5),
        anomalies=[Anomalies.Point(position=50, magnitude=10)],
    )

    # Add a dependency that should be applied after anomalies
    dependency = Dependencies.Linear(
        slope=0.5, intercept=2, apply_before_anomaly=False
    )
    ts.add_dependency(target="target", source="source", dependency=dependency)

    # Generate the data
    df = ts.generate()

    # Check that the dependency was applied after the anomaly
    # The anomaly should still be visible in the target signal
    assert df["target"].iloc[50] > df["target"].iloc[49] + 5
    assert df["target"].iloc[50] > df["target"].iloc[51] + 5


def test_vary_parameter():
    """Test the _vary_parameter method"""
    ts = MultiSensorTS(seed=42, variation_scale=0.2)

    # Test with a positive value
    original = 10.0
    varied = ts._vary_parameter(original)
    assert varied != original  # Should be different
    assert 8.0 < varied < 12.0  # Should be within 20% of original

    # Test with a negative value
    original = -5.0
    varied = ts._vary_parameter(original)
    assert varied != original  # Should be different
    assert -6.0 < varied < -4.0  # Should be within 20% of original

    # Test with zero
    original = 0.0
    varied = ts._vary_parameter(original)
    assert -0.1 < varied < 0.1  # Should be close to zero


def test_create_similar_trend():
    """Test the _create_similar_trend method"""
    ts = MultiSensorTS(seed=42, variation_scale=0.2)

    # Test with Linear trend
    original_trend = Trends.Linear(slope=2.0, intercept=5.0)
    similar_trend = ts._create_similar_trend(original_trend)

    assert isinstance(similar_trend, Trends.Linear)
    assert similar_trend.slope != original_trend.slope
    assert similar_trend.intercept != original_trend.intercept
    assert 1.6 < similar_trend.slope < 2.4  # Within 20% of original
    assert 3.9 < similar_trend.intercept < 6.1  # Within 20% of original

    # Test with Periodic trend
    original_trend = Trends.Periodic(
        amplitude=3.0,
        period=100,
        offset=10.0,
        phase=0.5,
    )
    similar_trend = ts._create_similar_trend(original_trend)

    assert isinstance(similar_trend, Trends.Periodic)
    assert similar_trend.amplitude != original_trend.amplitude
    assert similar_trend.period != original_trend.period
    assert similar_trend.offset != original_trend.offset
    assert similar_trend.phase != original_trend.phase
    assert 2.4 < similar_trend.amplitude < 3.6  # Within 20% of original
    assert 80 < similar_trend.period < 120  # Within 20% of original
    assert 8.0 < similar_trend.offset < 12.0  # Within 20% of original

    # Test with Composite trend
    sub_trend1 = Trends.Linear(slope=1.0, intercept=0.0)
    sub_trend2 = Trends.Periodic(amplitude=2.0, period=50, offset=0.0)
    original_trend = Trends.Composite([sub_trend1, sub_trend2])
    similar_trend = ts._create_similar_trend(original_trend)

    assert isinstance(similar_trend, Trends.Composite)
    assert len(similar_trend.trends) == len(original_trend.trends)
    assert isinstance(similar_trend.trends[0], Trends.Linear)
    assert isinstance(similar_trend.trends[1], Trends.Periodic)


def test_create_similar_noise():
    """Test the _create_similar_noise method"""
    ts = MultiSensorTS(seed=42, variation_scale=0.2)

    # Test with Gaussian noise
    original_noise = Noise.Gaussian(std=1.5)
    similar_noise = ts._create_similar_noise(original_noise)

    assert isinstance(similar_noise, Noise.Gaussian)
    assert similar_noise.std != original_noise.std
    assert 1.2 < similar_noise.std < 1.8  # Within 20% of original

    # Test with Uniform noise
    original_noise = Noise.Uniform(low=-2.0, high=2.0)
    similar_noise = ts._create_similar_noise(original_noise)

    assert isinstance(similar_noise, Noise.Uniform)
    assert similar_noise.low != original_noise.low
    assert similar_noise.high != original_noise.high
    assert -2.4 < similar_noise.low < -1.6  # Within 20% of original
    assert 1.6 < similar_noise.high < 2.4  # Within 20% of original

    # Test with Multiplicative noise
    original_noise = Noise.Multiplicative(factor=0.2)
    similar_noise = ts._create_similar_noise(original_noise)

    assert isinstance(similar_noise, Noise.Multiplicative)
    assert similar_noise.factor != original_noise.factor
    assert 0.16 < similar_noise.factor < 0.24  # Within 20% of original


def test_create_similar_dependency():
    """Test the _create_similar_dependency method"""
    ts = MultiSensorTS(seed=42, variation_scale=0.2)

    # Test with Linear dependency
    original_dep = Dependencies.Linear(
        slope=2.0, intercept=5.0, delay=3, noise_level=0.1
    )
    similar_dep = ts._create_similar_dependency(original_dep)

    assert isinstance(
        similar_dep, Dependencies.Linear
    ), f"Expected Dependencies.Linear, got {type(similar_dep)}"
    assert (
        similar_dep.slope != original_dep.slope
    ), f"Expected different slope, got {similar_dep.slope} and {original_dep.slope}"
    assert (
        similar_dep.intercept != original_dep.intercept
    ), f"Expected different intercept, got {similar_dep.intercept} and {original_dep.intercept}"
    assert (
        similar_dep.delay == original_dep.delay
    ), f"Expected delay to remain the same, got {similar_dep.delay} and {original_dep.delay}"
    assert (
        similar_dep.noise_level != original_dep.noise_level
    ), f"Expected different noise level, got {similar_dep.noise_level} and {original_dep.noise_level}"
    assert (
        1.6 < similar_dep.slope < 2.4
    ), f"Expected slope to be within 20% of original, got {similar_dep.slope} and {original_dep.slope}"
    assert (
        4.0 < similar_dep.intercept < 6.0
    ), f"Expected intercept to be within 20% of original, got {similar_dep.intercept} and {original_dep.intercept}"
    assert (
        0.08 < similar_dep.noise_level < 0.12
    ), f"Expected noise level to be within 20% of original, got {similar_dep.noise_level} and {original_dep.noise_level}"

    # Test with Inverse dependency
    original_dep = Dependencies.Inverse(
        scale=10.0, offset=1.0, delay=2, noise_level=0.2
    )
    similar_dep = ts._create_similar_dependency(original_dep)

    assert isinstance(
        similar_dep, Dependencies.Inverse
    ), f"Expected Dependencies.Inverse, got {type(similar_dep)}"
    assert (
        similar_dep.scale != original_dep.scale
    ), f"Expected different scale, got {similar_dep.scale} and {original_dep.scale}"
    assert (
        similar_dep.offset != original_dep.offset
    ), f"Expected different offset, got {similar_dep.offset} and {original_dep.offset}"
    assert (
        similar_dep.delay == original_dep.delay
    ), f"Expected delay to remain the same, got {similar_dep.delay} and {original_dep.delay}"
    assert (
        8.0 < similar_dep.scale < 12.0
    ), f"Expected scale to be within 20% of original, got {similar_dep.scale} and {original_dep.scale}"
    assert (
        0.8 < similar_dep.offset < 1.2
    ), f"Expected offset to be within 20% of original, got {similar_dep.offset} and {original_dep.offset}"

    # Test with Exponential dependency
    original_dep = Dependencies.Exponential(
        scale=2.0, rate=0.5, delay=1, noise_level=0.1
    )
    similar_dep = ts._create_similar_dependency(original_dep)

    assert isinstance(similar_dep, Dependencies.Exponential)
    assert (
        similar_dep.scale != original_dep.scale
    ), f"Expected different scale, got {similar_dep.scale} and {original_dep.scale}"
    assert (
        similar_dep.rate != original_dep.rate
    ), f"Expected different rate, got {similar_dep.rate} and {original_dep.rate}"
    assert (
        similar_dep.delay == original_dep.delay
    ), f"Expected delay to remain the same, got {similar_dep.delay} and {original_dep.delay}"
    assert (
        1.6 < similar_dep.scale < 2.4
    ), f"Expected scale to be within 20% of original, got {similar_dep.scale} and {original_dep.scale}"
    assert (
        0.4 < similar_dep.rate < 0.6
    ), f"Expected rate to be within 20% of original, got {similar_dep.rate} and {original_dep.rate}"

    # Test with Threshold dependency
    original_dep = Dependencies.Threshold(
        threshold=5.0,
        slope_below=1.0,
        slope_above=2.0,
        delay=0,
        noise_level=0.1,
    )
    similar_dep = ts._create_similar_dependency(original_dep)

    assert isinstance(similar_dep, Dependencies.Threshold)
    assert similar_dep.threshold != original_dep.threshold
    assert similar_dep.slope_below != original_dep.slope_below
    assert similar_dep.slope_above != original_dep.slope_above
    assert (
        similar_dep.delay == original_dep.delay
    ), f"Expected delay to remain the same, got {similar_dep.delay} and {original_dep.delay}"
    assert (
        4.0 < similar_dep.threshold < 6.0
    ), f"Expected threshold to be within 20% of original, got {similar_dep.threshold} and {original_dep.threshold}"
    assert (
        0.8 < similar_dep.slope_below < 1.2
    ), f"Expected slope_below to be within 20% of original, got {similar_dep.slope_below} and {original_dep.slope_below}"
    assert (
        1.6 < similar_dep.slope_above < 2.4
    ), f"Expected slope_above to be within 20% of original, got {similar_dep.slope_above} and {original_dep.slope_above}"

    # Test with Periodic dependency
    original_dep = Dependencies.Periodic(
        amplitude=3.0, base_frequency=0.5, delay=2, noise_level=0.1
    )
    similar_dep = ts._create_similar_dependency(original_dep)

    assert isinstance(similar_dep, Dependencies.Periodic)
    assert similar_dep.amplitude != original_dep.amplitude
    assert similar_dep.base_frequency != original_dep.base_frequency
    assert (
        similar_dep.delay == original_dep.delay
    ), f"Expected delay to remain the same, got {similar_dep.delay} and {original_dep.delay}"
    assert 2.4 < similar_dep.amplitude < 3.6  # Within 20% of original
    assert 0.4 < similar_dep.base_frequency < 0.6  # Within 20% of original


def test_create_similar_anomaly():
    """Test the _create_similar_anomaly method"""
    ts = MultiSensorTS(seed=42, variation_scale=0.2)

    # Test with Point anomaly
    original_anomaly = Anomalies.Point(position=50, magnitude=10.0)
    similar_anomaly = ts._create_similar_anomaly(original_anomaly)

    assert isinstance(
        similar_anomaly, Anomalies.Point
    ), f"Expected Anomalies.Point, got {type(similar_anomaly)}"
    assert (
        similar_anomaly.position == original_anomaly.position
    ), f"Expected position to remain the same, got {similar_anomaly.position} and {original_anomaly.position}"
    assert (
        similar_anomaly.magnitude != original_anomaly.magnitude
    ), f"Expected magnitude to be different, got {similar_anomaly.magnitude} and {original_anomaly.magnitude}"
    assert (
        8.0 < similar_anomaly.magnitude < 12.0
    ), f"Expected magnitude to be within 20% of original, got {similar_anomaly.magnitude} and {original_anomaly.magnitude}"

    # Test with Collective anomaly
    original_anomaly = Anomalies.Collective(
        start=30, duration=5, magnitude=5.0
    )
    similar_anomaly = ts._create_similar_anomaly(original_anomaly)

    assert isinstance(similar_anomaly, Anomalies.Collective)
    assert (
        similar_anomaly.start == original_anomaly.start
    ), f"Expected start to remain the same, got {similar_anomaly.start} and {original_anomaly.start}"
    assert (
        similar_anomaly.duration != original_anomaly.duration
    ), f"Expected duration to not remain the same, got {similar_anomaly.duration} and {original_anomaly.duration}"
    assert (
        similar_anomaly.magnitude != original_anomaly.magnitude
    ), f"Expected magnitude to be different, got {similar_anomaly.magnitude} and {original_anomaly.magnitude}"
    assert (
        4.0 < similar_anomaly.magnitude < 6.0
    ), f"Expected magnitude to be within 20% of original, got {similar_anomaly.magnitude} and {original_anomaly.magnitude}"


@pytest.skip("Skipping generate_similar test", allow_module_level=True)
def test_generate_similar():
    """Test the generate_similar method"""
    # Create a MultiSensorTS with two sensors
    ts = MultiSensorTS(length=100, seed=42)

    # Add sensors
    ts.add_sensor(
        name="sensor1",
        trend=Trends.Linear(slope=0.1, intercept=0),
        noise=Noise.Gaussian(std=0.5),
        anomalies=[Anomalies.Point(position=50, magnitude=10)],
    )

    ts.add_sensor(
        name="sensor2",
        trend=Trends.Periodic(amplitude=5, period=50, offset=10),
        noise=Noise.Uniform(low=-1, high=1),
    )

    # Add dependency
    ts.add_dependency(
        target="sensor2",
        source="sensor1",
        dependency=Dependencies.Linear(slope=0.5, intercept=2),
    )

    # Generate similar time series
    n_samples = 3
    similar_dfs = ts.generate_similar(
        n_samples=n_samples,
        include_anomalies=True,
        variation_scale=0.5,
    )

    # Check that we got the right number of samples
    assert (
        len(similar_dfs) == n_samples
    ), f"Expected {n_samples} samples, got {len(similar_dfs)}"

    # Check that each sample has the same structure but different values
    original_df = ts.generate()

    for df in similar_dfs:
        # Same columns
        assert set(df.columns) == set(
            original_df.columns
        ), f"Expected {set(original_df.columns)}, got {set(df.columns)}"

        # Same length
        assert len(df) == len(
            original_df
        ), f"Expected {len(original_df)}, got {len(df)}"

        # Different values
        for col in df.columns:
            assert not np.array_equal(
                df[col].values, original_df[col].values
            ), f"Expected different values for {col}"

    # Test without anomalies
    similar_dfs_no_anomalies = ts.generate_similar(
        n_samples=2, include_anomalies=False
    )

    # Check that we got the right number of samples
    assert (
        len(similar_dfs_no_anomalies) == 2
    ), f"Expected 2 samples, got {len(similar_dfs_no_anomalies)}"

    # Test with custom variation scale
    similar_dfs_custom_scale = ts.generate_similar(
        n_samples=2, variation_scale=0.5
    )

    # Check that we got the right number of samples
    assert (
        len(similar_dfs_custom_scale) == 2
    ), f"Expected 2 samples, got {len(similar_dfs_custom_scale)}"
