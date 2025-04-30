from __future__ import annotations

import numpy as np
from enum import Enum
from pydantic import Field, field_validator
from typing import Optional, List, Union

from tomobabel.models.basemodels import ConfiguredBaseModel, CoordsLogical, Annotation
from tomobabel.models.transformations import AffineTransform

# TODO: give all these helper properties like center, corners vector and etc,


class AnnotationType(str, Enum):
    point = "point"
    sphere = "sphere"
    cuboid = "cuboid"
    vector = "vector"
    ovoid = "ovoid"
    shell = "shell"
    spline = "spline"
    cylinder = "cylinder"
    cone = "cone"
    surface = "surface"
    volumne = "volume"
    map = "fit_map"
    text = "text"


class Point(Annotation):
    type: str = AnnotationType.point
    coords: CoordsLogical = Field(
        default=..., description="Coords for the point center"
    )

    @property
    def coord_array(self) -> np.ndarray:
        """Returns the coordinates as a numpy array

        Returns:
            np.ndarray: The coordinate array in a 3x1 array [[x], [y], [z]] if the
            coords are 2D the array is padded with the [2,1] index as 1

        """
        return self.coords.coord_array


class Vector(Annotation):
    """A defined by two points"""

    type: str = AnnotationType.vector
    start: Point
    end: Point

    @property
    def points(self) -> np.ndarray:
        """
        Get the start and end points of the vector as a 3x2 array

        Returns:
            np.ndarry: the start and end point arrays
        """
        start_coords = self.start.coord_array
        end_coords = self.end.coord_array
        return np.array([start_coords, end_coords])

    @property
    def vector(self) -> np.ndarray:
        """
        Get the vector as a 3x1 array

        Returns:
            np.ndarray: the vector array
        """
        p1, p2 = self.points
        return p2 - p1

    @property
    def unit_vector(self) -> np.ndarray:
        """
        Get the unit vector as a 3x1 array

        Returns:
            np.ndarray: the unit vector array
        """
        norm = np.linalg.norm(self.vector)
        return self.vector / norm


class Sphere(Point):
    """A sphere of diameter 'diameter' centered on x,y,(z) coordinate"""

    type: str = AnnotationType.sphere
    diameter: float = Field(default=..., description="The sphere diameter")


class Ovoid(Vector):
    """An 2D oval or 3D  ovoid with its widest point at 'waist_point' on the main
    vector"""

    type: str = AnnotationType.ovoid
    waist_size: float = Field(
        default=..., description="The length across the ovoid at its widest point"
    )
    waist_point: Optional[Point] = Field(
        default=None,
        description=(
            "Coords of the point in the center vector where the ovoid is widest"
        ),
    )

    def model_post_init(self, __context) -> None:
        # calculate the waist point if not given
        if not self.waist_point:
            mids = (self.start.coord_array + self.end.coord_array) / 2
            self.waist_point = Point(
                coords=CoordsLogical(x=mids[0, 0], y=mids[1, 0], z=mids[2, 0])
            )
        # verify waist point is on the central vector
        v = self.end.coord_array - self.start.coord_array
        w = self.waist_point.coord_array - self.start.coord_array

        v_flat = v.flatten()
        w_flat = w.flatten()

        is_colinear = np.allclose(np.cross(v_flat, w_flat), 0)

        dot_vv = np.dot(v_flat, v_flat)
        t = np.dot(w_flat, v_flat) / dot_vv
        if not (is_colinear and (0 <= t <= 1)):
            raise ValueError("Ovoid waist point is not on central vector")


class Cuboid(Vector):
    """A cuboidal box defined by two or three vectors"""

    type: str = AnnotationType.cuboid
    center: Point
    v1: Vector
    v2: Vector
    v3: Optional[Vector]


class Spline(Annotation):
    type: str = AnnotationType.spline
    points: List[Point] = Field(default=..., description="At least two points")

    @field_validator("points")
    def at_least_three_points(cls, value: List[Point]) -> List[Point]:
        if len(value) < 3:
            raise ValueError("A spline must have at least 3 points")
        return value


class Cylinder(Vector):
    type: str = AnnotationType.cylinder
    diameter: float = Field(default=..., description="The diameter of the cylinder")


class Cone(Vector):
    type: str = AnnotationType.cone
    start_diameter: float = Field(
        default=..., description="Diameter of the base of the cone"
    )
    end_diameter: float = Field(
        default=0.0,
        description=(
            "Diameter of the end of the cone, if 0.0, the cone comes to a sharp point,"
            "otherwise it is cut off"
        ),
    )


class Shell(Annotation):
    """A shell created by subtracting one or more volume annotations from a starting
    volume"""

    type: str = AnnotationType.shell
    base: Union[Sphere, Cuboid, Ovoid, Cylinder, Cone] = Field(
        default=..., description="The base volume the cutouts will be subtracted from"
    )
    cut_outs: List[Union[Sphere, Cuboid, Ovoid, Cylinder, Cone]] = Field(
        default=..., description="These volumes will be subtracted from the base volume"
    )


class FitMap(Point):
    """Annotation for a fitted map"""

    type: str = AnnotationType.map
    file: str = Field(default=..., description="Path to the map file")
    transformation: AffineTransform = Field(
        default=AffineTransform(),
        description=(
            "Tranformation that fits the map. IE: Affine transform for rotation"
        ),
    )


class AnnotationSet(ConfiguredBaseModel):
    name: Optional[str] = Field(
        default="Annotations",
        description="The name of the annotation set EG 'Membranes' or 'Ribosomes'",
    )
    annotations: List[Annotation] = Field(default=..., description="The annotations")


# Model rebuilds
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model

AnnotationSet.model_rebuild()
Cone.model_rebuild()
Cuboid.model_rebuild()
Cylinder.model_rebuild()
FitMap.model_rebuild()
Ovoid.model_rebuild()
Point.model_rebuild()
Shell.model_rebuild()
Sphere.model_rebuild()
Spline.model_rebuild()
Vector.model_rebuild()
