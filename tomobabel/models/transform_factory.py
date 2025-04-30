from typing import List, Literal
import numpy as np
from scipy.spatial.transform import Rotation as R

from tomobabel.models.transformations import (
    FlipTransform,
    ScaleTransform,
    AffineTransform,
    TranslationTransform,
    RotationTransform,
)


def flip_transform(axes: List[Literal["x", "y", "z"]]) -> FlipTransform:
    """Flip over one or more axes

    Args:
        axes (List[Literal["x", "y", "z"]]): Axes to flip over

    Returns:
        FlipTransform: The Transform object


    """
    matrix = np.identity(4)
    axis_map = {"x": 0, "y": 1, "z": 2}
    for axis in axes:
        i = axis_map[axis.lower()]
        matrix[i, i] = -1
    return FlipTransform(trans_matrix=matrix)


def scale_transform(factor: float) -> ScaleTransform:
    """Uniform scale transformation

    Args:
        factor (float): The factor to scale by

    Returns:
        ScaleTransform: The Transform object
    """
    matrix = np.array(
        [
            [factor, 0.0, 0.0, 0.0],
            [0.0, factor, 0.0, 0.0],
            [0.0, 0.0, factor, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ]
    )
    return ScaleTransform(trans_matrix=matrix)


def rotation_transform_from_eulers(
    convention: str, phi: float, psi: float, theta: float
) -> AffineTransform:
    rotation = R.from_euler(convention, [phi, theta, psi], degrees=True)
    return RotationTransform(trans_matrix=rotation.as_matrix())


def translation(
    x_shift: float = 0, y_shift: float = 0, z_shift: float = 0
) -> TranslationTransform:
    """A translation in x, y, and/or z

    Args:
        x_shift (float): Shift in x
        y_shift (float): Shift in y
        z_shift (float): Shift in z

    Returns:
        AffineTransformation: The transformation object
    """
    matrix = np.identity(4)
    matrix[0, 3] = x_shift
    matrix[1, 3] = y_shift
    matrix[2, 3] = z_shift
    return AffineTransform(trans_matrix=matrix)
