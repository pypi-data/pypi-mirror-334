import sys
from .noise import Noise
from loguru import logger
from .trends import Trends
from .patterns import Patterns
from .core import MultiSensorTS
from .anomalies import Anomalies
from .dependencies import Dependencies

logger.remove()
logger.add(sys.stdout, level="INFO")

__all__ = [
    "MultiSensorTS",
    "Trends",
    "Noise",
    "Anomalies",
    "Patterns",
    "Dependencies",
]

__version__ = open("version.txt").read().strip()
