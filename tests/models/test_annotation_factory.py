import numpy as np
from src.tomobabel.models.annotation import Point, Vector
from src.tomobabel.models.annotation_factory import point, vector
from tests.testing_tools import TomoBabelTest

p1 = np.array([[10.0], [20.0], [30.0]])
p2 = np.array([[40.0], [50.0], [60.0]])
p3 = np.array([[10.0], [20.0]])
p4 = np.array([[30.0], [40.0]])


class AnnotationFactoryTest(TomoBabelTest):
    def test_make_point_3D(self):
        p = point(coords=p1, text="3D point")
        assert isinstance(p, Point)
        assert p.x == 10.0
        assert p.y == 20.0
        assert p.z == 30.0
        assert p.description == "3D point"

    def test_make_point_2D(self):
        p = point(coords=p3, text="2D point")
        assert isinstance(p, Point)
        assert p.x == 10.0
        assert p.y == 20.0
        assert p.z is None
        assert p.description == "2D point"

    def test_make_vector_3D(self):
        v = vector(start=p1, end=p2, text="This is a 3D vector")
        assert isinstance(v, Vector)
        assert v.start.x == 10.0
        assert v.start.y == 20.0
        assert v.start.z == 30.0
        assert v.end.x == 40.0
        assert v.end.y == 50.0
        assert v.end.z == 60.0
        assert v.description == "This is a 3D vector"

    def test_make_vector_2D(self):
        v = vector(start=p3, end=p4, text="This is a 2D vector")
        assert isinstance(v, Vector)
        assert v.start.x == 10.0
        assert v.start.y == 20.0
        assert v.start.z is None
        assert v.end.x == 30.0
        assert v.end.y == 40.0
        assert v.end.z is None
        assert v.description == "This is a 2D vector"
