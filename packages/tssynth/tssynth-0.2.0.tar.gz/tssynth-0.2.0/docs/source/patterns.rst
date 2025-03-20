Patterns
========

The ``Patterns`` class provides pre-built pattern configurations for common use cases, making it easier to generate realistic synthetic data for specific domains.

Solar Panel Pattern
-------------------

Simulates solar panel system behavior with temperature, humidity, and power components, including daily and seasonal variations.

Example:

.. doctest::

    >>> from tssynth import Patterns
    >>> import numpy as np
    >>> np.random.seed(42)  # For reproducibility
    >>> 
    >>> # Create a solar panel pattern with default parameters
    >>> solar = Patterns.SolarPanel(
    ...     length=1000,
    ...     sampling_rate=1,
    ...     sampling_rate_units='h',
    ...     temp_setpoint=25.0,  # Average temperature
    ...     daily_range=5.0,     # Daily temperature variation
    ...     seasonal_amplitude=8.0  # Seasonal temperature variation
    ... )
    >>> data = solar.generate()
    >>> 
    >>> # Check data properties
    >>> len(data)  # Check length
    1000
    >>> sorted(data.columns)  # Check available columns
    ['humidity', 'humidity_anomaly', 'power', 'power_anomaly', 'temperature', 'temperature_anomaly']
    >>> bool(15 <= data['temperature'].mean() <= 35)  # Check temperature range
    True
