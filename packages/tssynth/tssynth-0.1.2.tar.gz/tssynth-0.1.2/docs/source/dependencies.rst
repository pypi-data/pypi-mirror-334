Dependencies
============

The ``Dependencies`` class provides mathematical relationships between sensor signals, enabling the creation of realistic multi-sensor systems where measurements influence each other.

Linear Dependency
-----------------

Implements a linear transformation of the source signal, useful for simple proportional relationships.

Example:

.. doctest::

    >>> from tssynth import Dependencies
    >>> import numpy as np
    >>> np.random.seed(42)  # For reproducibility
    >>> 
    >>> # Create a linear dependency with slope 2.0 and intercept 1.0
    >>> dep = Dependencies.Linear(slope=2.0, intercept=1.0)
    >>> source = np.array([1, 2, 3, 4, 5])
    >>> target = dep.apply(source, np.random.default_rng(42))
    >>> len(target)  # Check length
    5
    >>> 2.9 <= float(target[0]) <= 3.1  # Check first value (should be close to 2*1 + 1)
    True
    >>> 10.8 <= float(target[-1]) <= 11.2  # Check last value (should be close to 2*5 + 1)
    True

Inverse Dependency
------------------

Implements an inverse relationship between source and target signals, useful for modeling inversely proportional relationships.

Example:

.. doctest::

    >>> from tssynth import Dependencies
    >>> import numpy as np
    >>> np.random.seed(42)  # For reproducibility
    >>> 
    >>> # Create an inverse dependency with scale 1.0 and offset to avoid division by zero
    >>> dep = Dependencies.Inverse(scale=1.0, offset=0.1)
    >>> source = np.array([1, 2, 4, 8])
    >>> target = dep.apply(source, np.random.default_rng(42))
    >>> len(target)  # Check length
    4
    >>> 0.9 <= float(target[0]) <= 1.1  # Check first value (should be close to 1/1)
    True
    >>> 0.12 <= float(target[-1]) <= 0.13  # Check last value (should be close to 1/(8+0.1))
    True

Exponential Dependency
----------------------

Implements an exponential transformation of the source signal, suitable for modeling exponential relationships.

Example:

.. doctest::

    >>> from tssynth import Dependencies
    >>> import numpy as np
    >>> np.random.seed(42)  # For reproducibility
    >>> 
    >>> # Create an exponential dependency
    >>> dep = Dependencies.Exponential(scale=1.0, rate=0.693)  # ln(2) for base 2 equivalent
    >>> source = np.array([0, 1, 2, 3])
    >>> target = dep.apply(source, np.random.default_rng(42))
    >>> len(target)  # Check length
    4
    >>> 0.9 <= float(target[0]) <= 1.1  # Check first value (should be close to e^0)
    True
    >>> 7.0 <= float(target[-1]) <= 8.0  # Check last value (should be close to e^2)
    True

Threshold Dependency
--------------------

Implements a piecewise linear relationship that changes behavior at a specified threshold, useful for modeling systems with different operating regimes.

Example:

.. doctest::

    >>> from tssynth import Dependencies
    >>> import numpy as np
    >>> np.random.seed(42)  # For reproducibility
    >>> 
    >>> # Create a threshold dependency with different slopes above/below threshold
    >>> dep = Dependencies.Threshold(threshold=0.0, slope_below=0.5, slope_above=2.0, intercept=0.0)
    >>> source = np.array([-2, -1, 0, 1, 2])
    >>> target = dep.apply(source, np.random.default_rng(42))
    >>> len(target)  # Check length
    5
    >>> -1.1 <= float(target[0]) <= -0.9  # Check value below threshold
    True
    >>> 3.9 <= float(target[-1]) <= 4.1  # Check value above threshold
    True

Periodic Dependency
-------------------

Implements a sinusoidal relationship where the source signal modulates the frequency of oscillation, useful for modeling systems with periodic behavior.

Example:

.. doctest::

    >>> from tssynth import Dependencies
    >>> import numpy as np
    >>> np.random.seed(42)  # For reproducibility
    >>> 
    >>> # Create a periodic dependency
    >>> dep = Dependencies.Periodic(frequency=1.0, amplitude=1.0, phase=0.0)
    >>> source = np.array([0, 0.25, 0.5, 0.75, 1.0])
    >>> target = dep.apply(source, np.random.default_rng(42))
    >>> len(target)  # Check length
    5
    >>> -1.1 <= float(min(target)) <= -0.9  # Check minimum value
    True
    >>> 0.9 <= float(max(target)) <= 1.1  # Check maximum value
    True
