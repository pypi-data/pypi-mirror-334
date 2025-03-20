Anomalies
=========

The ``Anomalies`` class provides various types of synthetic anomalies that can be injected into time series data to simulate real-world data irregularities. These anomalies are useful for testing anomaly detection algorithms and evaluating system robustness.

Point Anomalies
---------------

Point anomalies represent single-point deviations in the time series, simulating isolated measurement errors or sudden events.

Example:

.. doctest::

    >>> from tssynth import Anomalies
    >>> import numpy as np
    >>> np.random.seed(42)  # For reproducibility
    >>> 
    >>> # Create a point anomaly at position 10 with magnitude 5.0
    >>> anomaly = Anomalies.Point(position=10, magnitude=5.0)
    >>> series = np.zeros(100)
    >>> modified_series = anomaly.apply(series, np.random.default_rng(42))
    >>> modified_series[10]  # Check the anomaly value
    np.float64(5.0)
    >>> modified_series[9]  # Check adjacent value is unchanged
    np.float64(0.0)

Visualization of a point anomaly:

.. image:: _static/images/point_anomaly_example.png
   :alt: Visualization of a time series with a point anomaly
   :align: center
   :width: 80%

Collective Anomalies
--------------------

Collective anomalies represent sequential deviations in the time series, simulating system malfunctions or persistent measurement errors.

Example:

.. doctest::

    >>> from tssynth import Anomalies
    >>> import numpy as np
    >>> np.random.seed(42)  # For reproducibility
    >>> 
    >>> # Create a collective anomaly starting at position 20 with duration 10
    >>> anomaly = Anomalies.Collective(start=20, duration=10, magnitude=3.0)
    >>> series = np.zeros(100)
    >>> modified_series = anomaly.apply(series, np.random.default_rng(42))
    >>> modified_series[20:23]  # Check first few values of the anomaly
    array([3., 3., 3.])
    >>> modified_series[19]  # Check value before anomaly is unchanged
    np.float64(0.0)
