import os
import shutil
import tempfile
import unittest
from pathlib import Path

import numpy as np

from tomobabel.models.transform_factory import (
    flip_transform,
    scale_transform,
    rotation_transform_from_eulers,
    translation,
)
from tomobabel.tests.converters.relion import test_data


class TransformFactoryTest(unittest.TestCase):
    def setUp(self):
        """
        Setup test data and output directories.
        """
        self.test_data = Path(os.path.dirname(test_data.__file__))
        self.test_dir = tempfile.mkdtemp(prefix="tomobabl_test")

        # Change to test directory
        self._orig_dir = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self._orig_dir)
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_flip_transform_x(self):
        xform = flip_transform(["x"])
        assert (
            xform.trans_matrix
            == np.array(
                [[-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
            )
        ).all()

    def test_flip_transform_y(self):
        xform = flip_transform(["y"])
        assert (
            xform.trans_matrix
            == np.array(
                [[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
            )
        ).all()

    def test_flip_transform_z(self):
        xform = flip_transform(["z"])
        assert (
            xform.trans_matrix
            == np.array(
                [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]],
            )
        ).all()

    def test_flip_transform_xy(self):
        xform = flip_transform(["x", "y"])
        assert (
            xform.trans_matrix
            == np.array(
                [[-1, 0, 0, 0], [0, -1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
            )
        ).all()

    def test_scale_transform(self):
        xform = scale_transform(2.5)
        assert (
            xform.trans_matrix
            == np.array(
                [[2.5, 0, 0, 0], [0, 2.5, 0, 0], [0, 0, 2.5, 0], [0, 0, 0, 1]],
            )
        ).all()

    def test_rotation_from_eluers_no_rotation(self):
        xform = rotation_transform_from_eulers("zyz", 0, 0, 0)
        assert (xform.trans_matrix == np.identity(3)).all()

    def test_translation(self):
        xform = translation(x_shift=2.5, y_shift=3.5, z_shift=4.5)
        assert (
            xform.trans_matrix
            == np.array([[1, 0, 0, 2.5], [0, 1, 0, 3.5], [0, 0, 1, 4.5], [0, 0, 0, 1]])
        ).all()
