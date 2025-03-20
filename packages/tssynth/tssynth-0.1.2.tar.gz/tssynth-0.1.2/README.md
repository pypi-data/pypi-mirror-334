# tssynth

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Generate realistic synthetic time series data with customizable patterns, seasonality, and noise components. Perfect for testing time series algorithms, machine learning models, or generating sample datasets.

## Features

✨ **Flexible Generation**: Create time series with various components:
- Linear, exponential, or custom trends
- Multiple seasonality patterns
- Configurable noise distributions
- Anomaly injection

🚀 **Easy to Use**: Simple, intuitive API built on numpy and pandas
```python
import tssynth as ts

# Generate a time series with multiple components
data = ts.generate(
    length=365,                    # One year of daily data
    trend="exponential",           # Exponential growth
    seasonality=["weekly", "yearly"],
    noise_type="gaussian",
    noise_level=0.05
)
```

## Installation

```bash
pip install tssynth
```

## Documentation

For detailed usage examples and API reference, visit our [documentation](https://tssynth.readthedocs.io).

### Quick Examples

```python
# Generate a simple trend
basic_trend = ts.generate(length=100, trend="linear")

# Add seasonality and anomalies
complex_ts = ts.generate(
    length=1000,
    trend="exponential",
    seasonality="monthly",
    anomalies={"frequency": 0.01, "magnitude": 3.0}
)

# Export to pandas DataFrame
df = complex_ts.to_dataframe()
```

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black .
isort .
```

## License

MIT License - See LICENSE file for details.

## Author

Will Judge (williamjudge94@gmail.com) 