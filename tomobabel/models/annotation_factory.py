import numpy as np

from tomobabel.models.annotation import Point, Vector


def point(coords: np.ndarray, text: str = "") -> Point:
    """
    Generate a Point Annotation object from a 3x1 array

    Args:
        coords (np.ndarray): The coordinate vector
        text (str): Any info o associated with this point

    Returns:
        Point: the CETS Point object
    """

    if len(coords) == 2:
        point = Point(x=coords[0, 0], y=coords[1, 0])
    elif len(coords) == 3:
        point = Point(x=coords[0, 0], y=coords[1, 0], z=coords[2, 0])
    else:
        raise ValueError("coords must be 2x1 or 3x1 array")
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

    start_point, end_point = point(start), point(end)
    vec = Vector(start=start_point, end=end_point)
    vec.description = text
    return vec
