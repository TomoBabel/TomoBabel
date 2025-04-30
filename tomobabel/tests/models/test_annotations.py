import os
import shutil
import tempfile
import unittest
from pathlib import Path

import numpy as np

from tomobabel.models.basemodels import CoordsLogical
from tomobabel.models.annotation import Point, Vector, Sphere, Ovoid
from tomobabel.tests.converters.relion import test_data

test_point1 = Point(coords=CoordsLogical(x=10.0, y=20.0, z=30))
test_point2 = Point(coords=CoordsLogical(x=110.0, y=120.0, z=130))
test_vector1 = Vector(start=test_point1, end=test_point2)


class AnnotationModelsTest(unittest.TestCase):
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

    def test_get_point_array_2D(self):
        point = Point(coords=CoordsLogical(x=10.0, y=20.0))
        assert (point.coord_array == np.array([[10.0], [20.0], [1.0]])).all()

    def test_get_point_array_3D(self):
        point = Point(coords=test_point1)
        assert (point.coord_array == np.array([[10.0], [20.0], [30.0]])).all()

    def test_get_vector_points(self):
        p1 = Point(coords=test_point1)
        p2 = Point(coords=test_point2)
        v = Vector(start=p1, end=p2)
        assert (
            v.points
            == np.array([[[10.0], [20.0], [30.0]], [[110.0], [120.0], [130.0]]])
        ).all()

    def test_get_vector(self):
        assert (test_vector1.vector == np.array([[100.0], [100.0], [100.0]])).all()

    def test_get_unit_vector(self):
        assert np.allclose(
            test_vector1.unit_vector,
            np.array([[0.57735027], [0.57735027], [0.57735027]]),
        )

    def test_get_sphere_center_point(self):
        sp = Sphere(coords=test_point1, diameter=10)
        assert (sp.coord_array == np.array([[10.0], [20.0], [30.0]])).all()

    def test_ovoid_with_defined_waist_point(self):
        ovoid = Ovoid(start=test_point1, end=test_point2, waist_size=10)
        assert np.isclose(
            ovoid.waist_point.coord_array, np.array([[60], [70], [80]])
        ).all()
