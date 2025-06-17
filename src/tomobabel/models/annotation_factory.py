import numpy as np

from src.tomobabel.models.annotation import Point, Vector
from src.tomobabel.models.basemodels import CoordsLogical


"""
These are helper functions for creating annotation objects directly from numpy arrays 
"""


def coords(inarray: np.ndarray) -> CoordsLogical:
    """Generate a CoordsLogical object from a 2x1 or 3x1 numpy array
    Args:
        inarray (np.ndarray): The coordinates
    Returns:
        CoordsLogical: The object
    """
    if len(inarray) == 2:
        coord = CoordsLogical(x=inarray[0, 0], y=inarray[1, 0])
    elif len(inarray) == 3:
        coord = CoordsLogical(x=inarray[0, 0], y=inarray[1, 0], z=inarray[2, 0])
    else:
        raise ValueError("Input coords must be 2x1 or 3x1 array")
    return coord


def point(inarray: np.ndarray, text: str = "") -> Point:
    """
    Generate a Point Annotation object from a 3x1 array

    Args:
        coords (np.ndarray): The coordinate vector
        text (str): Any info o associated with this point

    Returns:
        Point: the CETS Point object
    """

    point = Point(coords=coords(inarray))
    point.description = text

    return point


def vector(start: np.ndarray, end: np.ndarray, text: str = "") -> Vector:
    """
    Get a Vector Annotation object from two point arrays

    Args:
        start (np.ndarray): The starting point
        end (np.ndarray): The ending point
        text (str): Any text to associate with this vector

    Returns:
        Vector: The CETS Vector object
    """
    if start.shape != end.shape:
        raise ValueError("Input arrays must be the same shape")
    start_point, end_point = coords(start), coords(end)
    vec = Vector(start=start_point, end=end_point)
    vec.description = text
    return vec
