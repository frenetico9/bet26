"""
Miscellaneous utility functions used across the backend.
Currently this module defines a logistic (sigmoid) function which is used
by the predictor. Separating it into its own module makes it easy to
reuse these utilities elsewhere in the project.
"""
import math


def logistic(x: float) -> float:
    """Compute the logistic function for a real number."""
    return 1.0 / (1.0 + math.exp(-x))