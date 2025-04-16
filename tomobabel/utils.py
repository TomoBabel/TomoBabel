from pathlib import Path
from typing import Tuple, Optional

import mrcfile
import numpy as np


def generate_affine_matrix(
    xshift: float,
    yshift: float,
    xtilt: float,
    ytilt: float,
    rot: float,
    euler_conv: str,
) -> np.ndarray:
    """Placeholder for function that will generate an affine matrix"""
    return np.zeros((3, 3))


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
