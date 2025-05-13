import numpy as np

from tomobabel.models.basemodels import (
    CoordsPhysical,
    CoordsLogical,
)
from tomobabel.tests.testing_tools import TomoBabelTest


class BaseModelsTest(TomoBabelTest):

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
