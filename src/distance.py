"""Distance calculation utilities."""

import math
from typing import Sequence


def euclidean_distance(point1: Sequence[float], point2: Sequence[float]) -> float:
    """Return the Euclidean distance between two 2-D points."""
    if len(point1) != 2 or len(point2) != 2:
        raise ValueError("Coordinates must contain exactly two values: [x, y].")

    return math.sqrt(
        (float(point2[0]) - float(point1[0])) ** 2
        + (float(point2[1]) - float(point1[1])) ** 2
    )
