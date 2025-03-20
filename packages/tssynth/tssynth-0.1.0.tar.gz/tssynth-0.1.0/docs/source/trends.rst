Trends
======

The ``Trends`` class provides mathematical functions for generating trend components in synthetic time series data. These patterns are essential for simulating real-world data with underlying patterns and long-term behaviors.

Linear Trend
------------

Generates a straight line defined by slope and intercept, useful for simulating constant growth or decline.

Example:

.. doctest::

    >>> from tssynth import Trends
    >>> import numpy as np
    >>> 
    >>> # Create a linear trend with slope 0.5 and intercept 10
    >>> trend = Trends.Linear(slope=0.5, intercept=10)
    >>> values = trend.generate(100)
    >>> len(values)  # Check length
    100
    >>> float(values[0])  # Check first value (should be close to intercept)
    10.0
    >>> float(values[-1] - values[0])  # Check total increase (should be close to slope * 99)
    49.5

Periodic Trend
--------------

Generates a sine wave with configurable amplitude, period, phase, and offset, ideal for simulating seasonal or cyclical patterns.

Example:

.. doctest::

    >>> from tssynth import Trends
    >>> import numpy as np
    >>> 
    >>> # Create a periodic trend with amplitude 5 and period 20
    >>> trend = Trends.Periodic(amplitude=5, period=20)
    >>> values = trend.generate(100)
    >>> len(values)  # Check length
    100
    >>> bool(-5.1 <= min(values) <= -4.9)  # Check minimum value
    True
    >>> bool(4.9 <= max(values) <= 5.1)  # Check maximum value
    True
    >>> bool(abs(values[0] - values[20]) < 0.1)  # Check periodicity
    True

Exponential Trend
-----------------

Generates exponential growth or decay, suitable for modeling phenomena with accelerating or decelerating rates.

Logistic Trend
--------------

Generates an S-shaped curve commonly used for population growth or adoption curves, where growth starts slow, accelerates, then levels off.

Composite Trend
---------------

Combines multiple trends by adding their outputs, allowing for complex patterns that incorporate multiple trend components.

Example:

.. doctest::

    >>> from tssynth import Trends
    >>> import numpy as np
    >>> 
    >>> # Create a composite trend with linear and periodic components
    >>> trend = Trends.Composite([
    ...     Trends.Linear(slope=0.1, intercept=0),
    ...     Trends.Periodic(amplitude=2, period=10)
    ... ])
    >>> values = trend.generate(100)
    >>> len(values)  # Check length
    100
