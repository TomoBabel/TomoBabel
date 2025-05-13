import unittest

import numpy as np
from tomobabel.models.transform_factory import (
    flip_transform,
    scale_transform,
    rotation_from_eulers,
    translation,
)
from tomobabel.tests.testing_tools import TomoBabelTest


class TransformFactoryTest(TomoBabelTest):

    def test_flip_transform_x(self):
        xform = flip_transform(["x"])
        assert (
            xform.trans_matrix
            == np.array(
                [[-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
            )
        ).all()

    def test_flip_transform_x_2d(self):
        xform = flip_transform(["x"], dim=2)
        assert (
            xform.trans_matrix == np.array([[-1, 0, 0], [0, 1, 0], [0, 0, 1]])
        ).all()

    def test_flip_transform_y(self):
        xform = flip_transform(["y"])
        assert (
            xform.trans_matrix
            == np.array(
                [[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
            )
        ).all()

    def test_flip_transform_y_2d(self):
        xform = flip_transform(["y"], dim=2)
        assert (
            xform.trans_matrix == np.array([[1, 0, 0], [0, -1, 0], [0, 0, 1]])
        ).all()

    def test_flip_transform_z(self):
        xform = flip_transform(["z"])
        assert (
            xform.trans_matrix
            == np.array(
                [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]],
            )
        ).all()

    def test_flip_transform_z_2d_error(self):
        with self.assertRaises(ValueError):
            flip_transform(["z"], dim=2)

    def test_flip_transform_xy(self):
        xform = flip_transform(["x", "y"])
        assert (
            xform.trans_matrix
            == np.array(
                [[-1, 0, 0, 0], [0, -1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
            )
        ).all()

    def test_flip_transform_xy_2d(self):
        xform = flip_transform(["x", "y"], dim=2)
        assert (
            xform.trans_matrix == np.array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]])
        ).all()

    def test_scale_transform(self):
        xform = scale_transform(2.5)
        assert (
            xform.trans_matrix
            == np.array(
                [[2.5, 0, 0, 0], [0, 2.5, 0, 0], [0, 0, 2.5, 0], [0, 0, 0, 1]],
            )
        ).all()

    def test_scale_transform_2d(self):
        xform = scale_transform(2.5, dim=2)
        assert (
            xform.trans_matrix == np.array([[2.5, 0, 0], [0, 2.5, 0], [0, 0, 1]])
        ).all()

    def test_rotation_from_eluers_no_rotation(self):
        xform = rotation_from_eulers("zyz", 0, 0, 0)
        assert (xform.trans_matrix == np.identity(3)).all()

    unittest.skip("Need to get a ground truth to test this against")

    def test_rotation_from_eulers(self):
        pass

    def test_translation(self):
        xform = translation(x_shift=2.5, y_shift=3.5, z_shift=4.5)
        assert (
            xform.trans_matrix
            == np.array([[1, 0, 0, 2.5], [0, 1, 0, 3.5], [0, 0, 1, 4.5], [0, 0, 0, 1]])
        ).all()

    def test_translation_2d(self):
        xform = translation(x_shift=2.5, y_shift=3.5, dim=2)
        assert (
            xform.trans_matrix == np.array([[1, 0, 2.5], [0, 1, 3.5], [0, 0, 1]])
        ).all()
