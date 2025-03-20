Core
====

The core module contains the main time series generation functionality.

SensorConfig
------------

The ``SensorConfig`` class provides configuration options for individual sensors in a multi-sensor time series system. It allows you to specify trends, noise, and anomalies for each sensor.

MultiSensorTS
-------------

The ``MultiSensorTS`` class is the main entry point for generating multi-sensor time series data. It allows you to create complex time series with multiple sensors, each with its own trends, noise, and dependencies.

Example:

.. doctest::

    >>> from tssynth import MultiSensorTS, Trends, Noise, Dependencies
    >>> import numpy as np
    >>> np.random.seed(42)  # For reproducibility
    >>> 
    >>> # Create a multi-sensor time series generator
    >>> ts = MultiSensorTS(length=1000)
    >>> 
    >>> # Add temperature sensor with periodic trend and noise
    >>> _ = ts.add_sensor(
    ...     name="temperature",
    ...     trend=Trends.Periodic(amplitude=5, period=100),
    ...     noise=Noise.Gaussian(std=0.5)
    ... )
    >>> 
    >>> # Add humidity sensor with linear trend
    >>> _ = ts.add_sensor(
    ...     name="humidity",
    ...     trend=Trends.Linear(slope=0.1, intercept=50),
    ...     noise=Noise.Uniform(low=-1, high=1)
    ... )
    >>> 
    >>> # Add dependency between temperature and humidity
    >>> _ = ts.add_dependency(
    ...     target="humidity",
    ...     source="temperature",
    ...     dependency=Dependencies.Linear(slope=-0.3, intercept=60)
    ... )
    >>> 
    >>> # Generate the time series data
    >>> data = ts.generate()
    >>> len(data)  # Check length
    1000
    >>> sorted(data.columns)  # Check available columns
    ['humidity', 'humidity_anomaly', 'temperature', 'temperature_anomaly']
    >>> -10 <= float(data['temperature'].min()) <= 10  # Check temperature range
    True

Common Use Cases
----------------

1. Creating a Single Sensor
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. doctest::

    >>> from tssynth import MultiSensorTS, Trends, Noise
    >>> 
    >>> # Create a single temperature sensor with daily cycles
    >>> ts = MultiSensorTS(length=24*7)  # One week of hourly data
    >>> _ = ts.add_sensor(
    ...     name="temperature",
    ...     trend=Trends.Periodic(amplitude=10, period=24),  # Daily cycle
    ...     noise=Noise.Gaussian(std=1.0)  # Random fluctuations
    ... )
    >>> data = ts.generate()
    >>> len(data)  # One week of hourly readings
    168

2. Multiple Independent Sensors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. doctest::

    >>> from tssynth import MultiSensorTS, Trends, Noise
    >>> 
    >>> # Create multiple independent sensors
    >>> ts = MultiSensorTS(length=100)
    >>> 
    >>> # Temperature with daily cycle
    >>> _ = ts.add_sensor(
    ...     name="temperature",
    ...     trend=Trends.Periodic(amplitude=5, period=24)
    ... )
    >>> 
    >>> # Pressure with upward trend
    >>> _ = ts.add_sensor(
    ...     name="pressure",
    ...     trend=Trends.Linear(slope=0.05, intercept=1000)
    ... )
    >>> 
    >>> # Wind speed with random variations
    >>> _ = ts.add_sensor(
    ...     name="wind_speed",
    ...     trend=Trends.Constant(value=10),
    ...     noise=Noise.Gaussian(std=2.0)
    ... )
    >>> 
    >>> data = ts.generate()
    >>> sorted(data.columns)  # Check all sensors are present
    ['pressure', 'pressure_anomaly', 'temperature', 'temperature_anomaly', 'wind_speed', 'wind_speed_anomaly']

3. Sensors with Dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. doctest::

    >>> from tssynth import MultiSensorTS, Trends, Dependencies
    >>> 
    >>> # Create sensors with dependencies
    >>> ts = MultiSensorTS(length=100)
    >>> 
    >>> # Temperature affects both humidity and pressure
    >>> _ = ts.add_sensor(
    ...     name="temperature",
    ...     trend=Trends.Periodic(amplitude=10, period=24)
    ... )
    >>> 
    >>> _ = ts.add_sensor(
    ...     name="humidity",
    ...     trend=Trends.Constant(value=50)
    ... )
    >>> 
    >>> _ = ts.add_sensor(
    ...     name="pressure",
    ...     trend=Trends.Constant(value=1013)
    ... )
    >>> 
    >>> # Add inverse relationship between temperature and humidity
    >>> _ = ts.add_dependency(
    ...     target="humidity",
    ...     source="temperature",
    ...     dependency=Dependencies.Linear(slope=-2, intercept=70)
    ... )
    >>> 
    >>> # Add direct relationship between temperature and pressure
    >>> _ = ts.add_dependency(
    ...     target="pressure",
    ...     source="temperature",
    ...     dependency=Dependencies.Linear(slope=0.5, intercept=1008)
    ... )
    >>> 
    >>> data = ts.generate()
    >>> sorted(data.columns)
    ['humidity', 'humidity_anomaly', 'pressure', 'pressure_anomaly', 'temperature', 'temperature_anomaly']
