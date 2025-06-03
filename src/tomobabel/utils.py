from pathlib import Path
from typing import Tuple, Optional, Dict

import mrcfile
import numpy as np
import json

# from scipy.spatial.transform import Rotation


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


def clean_dict(input_dict) -> Dict[str, object]:
    """Converts any np.ndarrys in the dict to lists

    Args:
        input_dict (Dict[str, object]): The dict to operate on

    Returns:
        Dict[str, object]: The dict with all np.ndarrays in list form

    """
    json_str = json.dumps(input_dict, cls=NumpyEncoder)
    result_dict = json.loads(json_str)
    return result_dict


# TODO: Make sure this is the correct way to go about this
#  neither of these functions seem precise enough

# def tilt_series_micrograph_alignment_matrix(
#     x_shift, y_shift, x_tilt, y_tilt, z_rotation
# ):
#     """
#     Create a 3x3 affine transformation matrix to align an image in a tilt series
#
#     Arguments:
#         x_shift (float): x translation in px,
#         y_shift (float): y translation in px,
#         x_tilt (float): x tilt in degrees
#         y_tilt (float): y tilt in degrees
#         z_rotation: rotation around z in degrees
#
#     Returns:
#     numpy.ndarray: 3x3 affine matrix for alignment
#     """
#
#     # Step 1: Rotation around Z axis (in 2D plane)
#     rot = Rotation.from_euler("z", z_rotation, degrees=True)
#     rot_matrix = rot.as_matrix()[:2, :2]  # extract 2D part
#
#     # Step 2: Shear (tilt)
#     shear_matrix = np.array([[1, x_tilt], [y_tilt, 1]])
#
#     # Step 3: Combine rotation and shear
#     linear_transform = rot_matrix @ shear_matrix
#
#     # Step 4: Construct full 3x3 affine matrix
#     affine_matrix = np.eye(3)
#     affine_matrix[:2, :2] = linear_transform
#     affine_matrix[:2, 2] = [x_shift, y_shift]
#
#     return affine_matrix
#
#
# def decompose_tilt_series_micrograph_alignment_matrix(matrix, pixel_size_ang=1.0):
#     """
#     Decomposes a 3x3 affine matrix into:
#     x_shift_ang, y_shift_ang (translation in Angstroms),
#     x_tilt, y_tilt (shear), and z_rotation_deg (rotation in degrees).
#
#     Args:
#     - matrix: A 3x3 affine matrix (numpy array).
#     - pixel_size_ang: Pixel size in Angstroms per pixel.
#
#     Returns:
#     - dict: Contains x_shift_ang, y_shift_ang, x_tilt, y_tilt, z_rotation_deg.
#     """
#
#     # Ensure it's a 3x3 matrix
#     matrix = np.array(matrix, dtype=np.float64)
#     if matrix.shape == (2, 3):
#         matrix = np.vstack([matrix, [0, 0, 1]])
#
#     # Step 1: Extract translation (from last column)
#     t = matrix[:2, 2]  # Last column for x and y shift (translation)
#     x_shift_ang = t[0] * pixel_size_ang
#     y_shift_ang = t[1] * pixel_size_ang
#
#     # Step 2: Extract the 2x2 linear transformation part (rotation + shear)
#     A = matrix[:2, :2]
#
#     # Step 3: Calculate rotation angle
#     # We assume the rotation matrix has form:
#     # [ cos(theta)  -sin(theta) ]
#     # [ sin(theta)   cos(theta) ]
#     # The rotation angle is computed using arctangent of the elements.
#     rotation_angle_rad = np.arctan2(A[1, 0], A[0, 0])  # Rotation angle
#     rotation_angle_deg = np.rad2deg(rotation_angle_rad)
#
#     # Step 4: Shear extraction: The off-diagonal elements represent shear.
#     # The shear values are normalized by the rotation component.
#     # We use a simple method to extract shear.
#     x_tilt = A[0, 1] / np.cos(rotation_angle_rad)  # Horizontal shear
#     y_tilt = A[1, 0] / np.sin(rotation_angle_rad)  # Vertical shear
#
#     return {
#         "x_shift_ang": np.float64(x_shift_ang),
#         "y_shift_ang": np.float64(y_shift_ang),
#         "x_tilt": np.float64(x_tilt),
#         "y_tilt": np.float64(y_tilt),
#         "z_rotation_deg": np.float64(rotation_angle_deg),
#     }


def get_mrc_dims(
    mrc_file: Optional[Path],
) -> Tuple[Optional[int], Optional[int], Optional[int]]:
    """Get the dimensions of an MRC file

    Args:
        mrc_file (Optional[Path]): The file to check

    Returns:
         Tuple[Optional[int], Optional[int], Optional[int]]: The dimensions in pixels
            or (None, None, None) if the file was not found.
    """
    if mrc_file is None:
        return None, None, None
    try:
        with mrcfile.open(mrc_file, permissive=True) as mrc:
            return mrc.header.nx, mrc.header.ny, mrc.header.nz
    except FileNotFoundError:
        return None, None, None
