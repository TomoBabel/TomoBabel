from __future__ import annotations

import numpy as np
from enum import Enum
from pydantic import Field, model_validator, field_validator
from typing import Optional, List, Union
from math import sqrt

from tomobabel.models.basemodels import ConfiguredBaseModel, CoordsLogical, Annotation
from tomobabel.models.transformations import AffineTransform

# TODO: give all these helper properties like center, corners vector and etc,


class AnnotationType(str, Enum):
    point = "point"
    sphere = "sphere"
    cuboid = "cuboid"
    vector = "vector"
    ovoid = "ovoid"
    box = "box"
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
        return self.coords.coord_array


class Vector(Annotation):
    """A defined by two points"""

    type: str = AnnotationType.vector
    start: Point
    end: Point

    def points(self):
        start_coords = self.start.coord_array
        end_coords = self.end.coord_array
        return np.ndarray([start_coords, end_coords])

    def vector(self):
        p1, p2 = self.points
        return p2 - p1

    def unit_vector(self):
        return np.linalg.norm(self.vector)


class Sphere(Point):
    """A sphere of diameter 'diameter' centered on x,y,(z) coordinate"""

    type: str = AnnotationType.sphere
    diameter = float = Field(default=..., description="The sphere diameter")


class Ovoid(Vector):
    """An 2D oval or 3D  ovoid with its widest point 'waist_size'along the vector at
    'waist_distance' from the start point"""

    type: str = AnnotationType.ovoid
    waist_size: float = Field(
        default=..., description="The length across the ovoid at its widest point"
    )
    waist_distace: Optional[float] = Field(
        default=None,
        description=(
            "The distance from the start point for the widest point of the ovoid"
        ),
    )

    @model_validator(mode="after")
    def find_center(self):
        """If waist distance is None put it at the middle of the center vector"""
        if self.waist_distance:
            return self
        mid_x = (self.start.x + self.end.x) / 2
        mid_y = (self.start.y + self.end.y) / 2
        xd = self.start.x - mid_x
        yd = self.start.y - mid_y
        if not self.start.y:
            self.waist_distace = sqrt(xd**2 + yd**2)
        if self.start_z:
            mid_z = (self.start.z + self.end.z) / 2
            zd = self.start.z - mid_z
            self.waist_distace = sqrt(xd**2 + yd**2 + zd**2)
        return self


class Cuboid(Vector):
    """A cuboidal box defined by two vectors"""

    type: str = AnnotationType.cuboid
    center: Point
    v1: Vector
    v2: Vector


class Box(Annotation):
    """An irregular bounding volume defined a center point and 3 vectors"""

    type: str = AnnotationType.box
    center: Point
    v1: Vector
    v2: Vector
    v3: Vector


class Spline(Annotation):
    type: str = AnnotationType.spline
    points: List[Point] = Field(default=..., description="At least two points")

    @field_validator("points")
    def at_least_three_points(cls, value=List[Point]) -> List[Point]:
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
    base: Union[Sphere, Cuboid, Ovoid, Cylinder, Box, Cone] = Field(
        default=..., description="The base volume the cutouts will be subtracted from"
    )
    cut_outs: List[Union[Sphere, Cuboid, Ovoid, Cylinder, Box, Cone]] = Field(
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
Box.model_rebuild()
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
