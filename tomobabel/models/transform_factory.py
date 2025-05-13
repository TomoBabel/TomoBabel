from typing import List, Literal

import numpy as np
from scipy.spatial.transform import Rotation as R

from tomobabel.models.transformations import (
    FlipTransform,
    ScaleTransform,
    TranslationTransform,
    RotationTransform,
)


def check_dim(dim: int) -> None:
    if dim not in (2, 3):
        raise ValueError("Input dimension must be 2 or 3")


def flip_transform(axes: List[Literal["x", "y", "z"]], dim: int = 3) -> FlipTransform:
    """Flip over one or more axes

    Args:
        axes (List[Literal["x", "y", "z"]]): Axes to flip over
        dim (int): Dimension of the transform matrix

    Returns:
        FlipTransform: The Transform object


    """
    check_dim(dim)
    matrix = np.identity(dim + 1)
    if dim == 2 and "z" in axes:
        raise ValueError("Can't flip 2D object in z")
    axis_map = {"x": 0, "y": 1, "z": 2}
    for axis in axes:
        i = axis_map[axis.lower()]
        matrix[i, i] = -1
    return FlipTransform(trans_matrix=matrix)


def scale_transform(factor: float, dim: int = 3) -> ScaleTransform:
    """Uniform scale transformation

    Args:
        factor (float): The factor to scale by
        dim (int): Dimension of the transform matrix

    Returns:
        ScaleTransform: The Transform object
    """
    check_dim(dim)
    l1 = [factor, 0.0, 0.0, 0.0] if dim == 3 else [factor, 0.0, 0.0]
    l2 = [0.0, factor, 0.0, 0.0] if dim == 3 else [0.0, factor, 0.0]
    l3 = [0.0, 0.0, factor, 0.0] if dim == 3 else [0.0, 0.0, 1.0]
    arr = [l1, l2, l3, [0.0, 0.0, 0.0, 1.0]] if dim == 3 else [l1, l2, l3]
    return ScaleTransform(trans_matrix=np.array(arr))


def rotation_from_eulers(
    convention: str, phi: float, psi: float, theta: float
) -> RotationTransform:
    rotation = R.from_euler(convention, [phi, theta, psi], degrees=True)
    return RotationTransform(trans_matrix=rotation.as_matrix())


def rotation_2d(rotation: float) -> RotationTransform:
    """
    A 2D rotation matrix

    Args:
        rotation (float): The anticlockwise rotation angle in degrees

    Returns:
        RotationTransform: The CETS Transformation object
    """
    angle_radians = np.deg2rad(rotation)
    cos_a = np.cos(angle_radians)
    sin_a = np.sin(angle_radians)
    return RotationTransform(matrix=np.array([[cos_a, -sin_a], [sin_a, cos_a]]))


def translation(
    x_shift: float = 0, y_shift: float = 0, z_shift: float = 0, dim: int = 3
) -> TranslationTransform:
    """A translation in x, y, and/or z

    Args:
        x_shift (float): Shift in x
        y_shift (float): Shift in y
        z_shift (float): Shift in z
        dim (int): Dimension of the transform matrix

    Returns:
        TranslationTransform: The transformation object
    """
    matrix = np.identity(dim + 1)
    matrix[0, dim] = x_shift
    matrix[1, dim] = y_shift
    matrix[2, dim] = z_shift if dim == 3 else 1
    return TranslationTransform(trans_matrix=matrix)
