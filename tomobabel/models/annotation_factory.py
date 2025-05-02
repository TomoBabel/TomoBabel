import numpy as np

from tomobabel.models.annotation import Point


def point(coords: np.ndarray) -> Point:
    """
    Generate a Point Annotation object from a 3x1 array

    Args:
        coords (np.ndarray): The coordinate vector
    :return:
    """
    if len(coords) == 2:
        point = Point(x=coords[0, 0], y=coords[1, 0])
    elif len(coords) == 3:
        point = Point(x=coords[0, 0], y=coords[1, 0], z=coords[2, 0])
    else:
        raise ValueError("coords must be 2x1 or 3x1 array")
    return point
