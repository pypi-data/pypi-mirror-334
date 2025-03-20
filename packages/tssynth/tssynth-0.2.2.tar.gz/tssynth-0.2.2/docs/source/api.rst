API Reference
=============

This section contains the complete API reference for all tssynth classes and functions.

Core
----

.. autoclass:: tssynth.core.SensorConfig
   :members:
   :undoc-members:

.. autoclass:: tssynth.core.MultiSensorTS
   :members:
   :undoc-members:

Trends
------

.. autoclass:: tssynth.trends.Trends.Base
   :members:
   :undoc-members:

.. autoclass:: tssynth.trends.Trends.Linear
   :members:
   :undoc-members:
   :no-index:

.. autoclass:: tssynth.trends.Trends.Periodic
   :members:
   :undoc-members:
   :no-index:

.. autoclass:: tssynth.trends.Trends.Exponential
   :members:
   :undoc-members:
   :no-index:

.. autoclass:: tssynth.trends.Trends.Logistic
   :members:
   :undoc-members:
   :no-index:

.. autoclass:: tssynth.trends.Trends.Composite
   :members:
   :undoc-members:
   :no-index:

Noise
-----

.. autoclass:: tssynth.noise.Noise.Base
   :members:
   :undoc-members:

.. autoclass:: tssynth.noise.Noise.Gaussian
   :members:
   :undoc-members:

.. autoclass:: tssynth.noise.Noise.Uniform
   :members:
   :undoc-members:

.. autoclass:: tssynth.noise.Noise.Multiplicative
   :members:
   :undoc-members:

Anomalies
---------

.. autoclass:: tssynth.anomalies.Anomalies.Base
   :members:
   :undoc-members:
   :special-members: __init__

.. autoclass:: tssynth.anomalies.Anomalies.Point
   :members:
   :undoc-members:
   :special-members: __init__
   :no-index:

.. autoclass:: tssynth.anomalies.Anomalies.Collective
   :members:
   :undoc-members:
   :special-members: __init__
   :no-index:

Dependencies
------------

.. autoclass:: tssynth.dependencies.Dependencies.Base
   :members:
   :undoc-members:
   :special-members: __init__
   :no-index:

.. autoclass:: tssynth.dependencies.Dependencies.Linear
   :members:
   :undoc-members:
   :no-index:
   :special-members: __init__

.. autoclass:: tssynth.dependencies.Dependencies.Inverse
   :members:
   :undoc-members:
   :no-index:
   :special-members: __init__

.. autoclass:: tssynth.dependencies.Dependencies.Exponential
   :members:
   :undoc-members:
   :no-index:
   :special-members: __init__

.. autoclass:: tssynth.dependencies.Dependencies.Threshold
   :members:
   :undoc-members:
   :no-index:
   :special-members: __init__

.. autoclass:: tssynth.dependencies.Dependencies.Periodic
   :members:
   :undoc-members:
   :no-index:
   :special-members: __init__

Patterns
--------

.. autoclass:: tssynth.patterns.Patterns.SolarPanel
   :members:
   :undoc-members: 