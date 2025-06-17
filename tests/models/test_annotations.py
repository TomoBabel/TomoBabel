import numpy as np

from src.tomobabel.models.annotation import (
    Point,
    Vector,
    Sphere,
    Ovoid,
    Cuboid,
    check_input_dims,
)
from tests.testing_tools import TomoBabelTest
from src.tomobabel.models.basemodels import CoordsLogical

coords1 = CoordsLogical(x=10.0, y=20.0, z=30)
coords2 = CoordsLogical(x=110.0, y=120.0, z=130)
test_point1 = Point(coords=coords1)
test_point2 = Point(coords=coords2)
test_vector1 = Vector(start=coords1, end=coords2)


class AnnotationModelsTest(TomoBabelTest):
    def test_check_input_dims(self):
        check_input_dims([test_point1, test_point2])
        with self.assertRaises(ValueError):
            check_input_dims([test_point1, CoordsLogical(x=1, y=1)])

    def test_get_point_array_2D(self):
        point = Point(coords=CoordsLogical(x=10.0, y=20.0))
        assert (point.coords.array == np.array([[10.0], [20.0]])).all()
        assert (point.coords.hom_array == np.array([[10.0], [20.0], [1.0]])).all()

    def test_get_point_array_3D(self):
        assert (test_point1.coords.array == np.array([[10.0], [20.0], [30.0]])).all()
        assert (
            test_point1.coords.hom_array == np.array([[10.0], [20.0], [30.0], [1.0]])
        ).all()

    def test_get_vector_points(self):
        assert (
            test_vector1.points
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
        sp = Sphere(center=coords1, radius=10)
        assert (sp.center_point == np.array([[10.0], [20.0], [30.0]])).all()

    def test_ovoid_with_default_waist_point(self):
        ovoid = Ovoid(vector=test_vector1, waist_radius=10)
        assert np.isclose(ovoid.waist_point.array, np.array([[60], [70], [80]])).all()

    def test_ovoid_with_defined_waist_point(self):
        ovoid = Ovoid(
            vector=test_vector1,
            waist_radius=10,
            waist_point=CoordsLogical(x=60.0, y=70.0, z=80.0),
        )
        assert np.isclose(
            ovoid.waist_point.array, np.array([[60.0], [70.0], [80.0]])
        ).all()

    def test_ovoid_with_defined_waist_point_error_not_no_vector(self):
        with self.assertRaises(ValueError):
            Ovoid(
                vector=test_vector1,
                waist_size=10,
                waist_point=CoordsLogical(x=1, y=2, z=3),
            )

    def test_create_square(self):
        sq = Cuboid(
            v1=Vector(start=CoordsLogical(x=0, y=0), end=CoordsLogical(x=1.0, y=1.0)),
            v2=Vector(start=CoordsLogical(x=0, y=0), end=CoordsLogical(x=-1.0, y=-1.0)),
        )
        assert np.allclose(sq.center_point, np.array([[0], [0]]))

    def test_create_rectangle(self):
        sq = Cuboid(
            v1=Vector(start=CoordsLogical(x=0, y=0), end=CoordsLogical(x=1.0, y=1.0)),
            v2=Vector(
                start=CoordsLogical(x=0, y=0), end=CoordsLogical(x=-10.0, y=-10.0)
            ),
        )
        assert np.allclose(sq.center_point, np.array([[0], [0]]))

    def test_create_cube(self):
        sq = Cuboid(
            v1=Vector(
                start=CoordsLogical(x=0.0, y=0.0, z=0.0),
                end=CoordsLogical(x=1.0, y=1.0, z=1.0),
            ),
            v2=Vector(
                start=CoordsLogical(x=0.0, y=0.0, z=0.0),
                end=CoordsLogical(x=-1.0, y=-1.0, z=1.0),
            ),
        )
        assert np.allclose(sq.center_point, np.array([[0], [0], [0]]))

    def test_create_cuboid(self):
        sq = Cuboid(
            v1=Vector(
                start=CoordsLogical(x=0.0, y=0.0, z=0.0),
                end=CoordsLogical(x=1.0, y=1.0, z=1.0),
            ),
            v2=Vector(
                start=CoordsLogical(x=0.0, y=0.0, z=0.0),
                end=CoordsLogical(x=-10.0, y=-10.0, z=-10.0),
            ),
        )
        assert np.allclose(sq.center_point, np.array([[0], [0], [0]]))
