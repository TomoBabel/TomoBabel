import os
import shutil
import tempfile
import unittest
from pathlib import Path

import numpy as np

from tomobabel.models.basemodels import (
    CoordsPhysical,
    CoordsLogical,
)
from tomobabel.tests.converters.relion import test_data


class BaseModelsTest(unittest.TestCase):
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

    def test_get_coords_array_physical3D(self):
        coords = CoordsPhysical(x=10, y=11, z=12)
        assert (coords.coord_array == np.array([[10], [11], [12]])).all()

    def test_get_coords_array_physical2D(self):
        coords = CoordsPhysical(x=10, y=11)
        assert (coords.coord_array == np.array([[10], [11]])).all()

    def test_get_coords_array_logical3D(self):
        coords = CoordsLogical(x=10.0, y=11.0, z=12.0)
        assert (coords.coord_array == np.array([[10.0], [11.0], [12.0]])).all()

    def test_get_coords_array_logical2D(self):
        coords = CoordsLogical(x=10.0, y=11.0)
        assert (coords.coord_array == np.array([[10.0], [11.0]])).all()
