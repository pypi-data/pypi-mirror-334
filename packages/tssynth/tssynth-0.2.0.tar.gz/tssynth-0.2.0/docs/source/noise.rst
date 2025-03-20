Noise
=====

The ``Noise`` class provides various noise generators for adding realistic variability to synthetic time series data. These noise patterns help simulate measurement errors and natural fluctuations in real-world systems.

Gaussian Noise
--------------

Generates normally distributed noise, commonly used to simulate random measurement errors.

Example:

.. doctest::

    >>> from tssynth import Noise
    >>> import numpy as np
    >>> np.random.seed(42)  # For reproducibility
    >>> 
    >>> # Create Gaussian noise with standard deviation 1.0
    >>> noise = Noise.Gaussian(std=1.0)
    >>> values = noise.generate(100, np.random.default_rng(42))
    >>> len(values)  # Check length
    100
    >>> bool(abs(np.mean(values)) < 0.5)  # Check mean is close to 0
    True
    >>> bool(0.5 < np.std(values) < 1.5)  # Check standard deviation is close to 1.0
    True

Uniform Noise
-------------

Generates uniformly distributed noise, useful for simulating bounded random fluctuations.

Example:

.. doctest::

    >>> from tssynth import Noise
    >>> import numpy as np
    >>> np.random.seed(42)  # For reproducibility
    >>> 
    >>> # Create uniform noise between -1 and 1
    >>> noise = Noise.Uniform(low=-1.0, high=1.0)
    >>> values = noise.generate(100, np.random.default_rng(42))
    >>> len(values)  # Check length
    100
    >>> bool(min(values) >= -1.0)  # Check minimum bound
    True
    >>> bool(max(values) <= 1.0)  # Check maximum bound
    True

Multiplicative Noise
--------------------

Generates noise values centered around 1.0, suitable for simulating proportional errors or multiplicative effects.

Example:

.. doctest::

    >>> from tssynth import Noise
    >>> import numpy as np
    >>> np.random.seed(42)  # For reproducibility
    >>> 
    >>> # Create multiplicative noise with 10% variation
    >>> noise = Noise.Multiplicative(scale=0.1)  # 10% variation
    >>> values = noise.generate(100, np.random.default_rng(42))
    >>> len(values)  # Check length
    100
    >>> bool(0.9 <= np.mean(values) <= 1.1)  # Check mean is close to 1.0
    True
