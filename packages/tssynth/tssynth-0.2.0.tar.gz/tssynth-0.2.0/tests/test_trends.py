import pytest
import numpy as np
from tssynth.trends import Trends


def test_linear_trend_basic():
    """Test basic linear trend generation with default parameters."""
    trend = Trends.Linear()
    length = 10
    values = trend.generate(length)

    assert len(values) == length
    assert values[0] == 0  # intercept
    assert values[-1] == length - 1  # slope * (length-1)
    assert np.allclose(np.diff(values), 1)  # constant difference of 1


def test_linear_trend_custom():
    """Test linear trend with custom slope and intercept."""
    trend = Trends.Linear(slope=2.0, intercept=5.0)
    length = 5
    values = trend.generate(length)

    assert len(values) == length
    assert values[0] == 5.0  # intercept
    assert values[-1] == 13.0  # slope * (length-1) + intercept
    assert np.allclose(np.diff(values), 2.0)


def test_periodic_trend():
    """Test periodic trend generation."""
    trend = Trends.Periodic(amplitude=2.0, period=4.0, phase=0.0, offset=1.0)
    length = 8
    values = trend.generate(length)

    assert len(values) == length
    assert np.allclose(values[4], values[0])  # values repeat after one period
    assert np.isclose(np.max(values), 3.0)  # offset + amplitude
    assert np.isclose(np.min(values), -1.0)  # offset - amplitude


def test_exponential_trend():
    """Test exponential trend generation."""
    trend = Trends.Exponential(growth_rate=0.1, base=1.0)
    length = 10
    values = trend.generate(length)

    assert len(values) == length
    assert np.isclose(values[0], 1.0)  # base value
    assert values[-1] > values[0]  # growing trend
    assert np.all(values > 0)  # all values should be positive


def test_logistic_trend():
    """Test logistic trend generation."""
    trend = Trends.Logistic(
        growth_rate=0.5, carrying_capacity=100.0, initial_population=1.0
    )
    length = 100
    values = trend.generate(length)

    assert len(values) == length
    assert (
        values[-1] < 100.0
    )  # should approach but not exceed carrying capacity
    assert values[0] < values[-1]  # should grow
    assert np.all(values > 0)  # all values should be positive
    assert np.all(values <= 100.0)  # should not exceed carrying capacity


def test_composite_trend():
    """Test composite trend combining multiple trends."""
    linear = Trends.Linear(slope=1.0, intercept=0.0)
    periodic = Trends.Periodic(amplitude=1.0, period=10.0)

    composite = Trends.Composite(trends=[linear, periodic])
    length = 20
    values = composite.generate(length)

    assert len(values) == length

    # Generate individual components
    linear_values = linear.generate(length)
    periodic_values = periodic.generate(length)

    # Verify composite is sum of components
    assert np.allclose(values, linear_values + periodic_values)


def test_zero_length():
    """Test handling of zero length input."""
    trends = [
        Trends.Linear(),
        Trends.Periodic(),
        Trends.Exponential(),
        Trends.Logistic(),
        Trends.Composite(trends=[Trends.Linear()]),
    ]

    for trend in trends:
        values = trend.generate(0)
        assert len(values) == 0


def test_negative_length():
    """Test handling of negative length input."""
    trend = Trends.Linear()
    with pytest.raises(ValueError):
        trend.generate(-1)
