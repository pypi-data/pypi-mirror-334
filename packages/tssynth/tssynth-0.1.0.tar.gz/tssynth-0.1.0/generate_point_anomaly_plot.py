from tssynth import Anomalies
import numpy as np
import matplotlib.pyplot as plt

# Set seed for reproducibility
np.random.seed(42)

# Create a point anomaly at position 10 with magnitude 5.0
anomaly = Anomalies.Point(position=10, magnitude=5.0)
series = np.zeros(100)
modified_series = anomaly.apply(series, np.random.default_rng(42))

# Plot the series with the point anomaly
plt.figure(figsize=(10, 5))
plt.plot(modified_series)
plt.title("Time Series with Point Anomaly")
plt.xlabel("Time")
plt.ylabel("Value")
plt.grid(True)
plt.axvline(
    x=10, color="r", linestyle="--", alpha=0.5, label="Anomaly Position"
)
plt.legend()

# Save the plot
plt.savefig(
    "docs/source/_static/images/point_anomaly_example.png",
    dpi=300,
    bbox_inches="tight",
)
print("Plot saved to docs/source/_static/images/point_anomaly_example.png")
