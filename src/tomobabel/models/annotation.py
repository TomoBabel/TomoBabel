from __future__ import annotations

from enum import Enum
from typing import Optional, List, Union

import numpy as np
from pydantic import Field, field_validator, model_validator

from src.tomobabel.models.basemodels import (
    CoordsLogical,
    Annotation,
    AnnotationSet,
    AnnotationSetTypes,
)
from src.tomobabel.models.transformations import Transformation


# TODO: give all these helper properties like center, corners vector and etc,


class AnnotationType(str, Enum):
    point = "point"
    particle = "particle_coodinate"
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


def check_input_dims(inputs: List[Union[CoordsLogical, Point]]) -> None:
    """
    Check the dimensions of input points match

    Args:
        inputs (List[CoordsLogical]): The input CETS CoordsLogical objects

    Raises:
        ValueError: If the dimensionality of the points is not the same
    """
    if not all([x.dim == inputs[0].dim for x in inputs]):
        dims = ", ".join([str(x.dim) for x in inputs])
        raise ValueError(f"Input dimensions do not match: {dims}")


class Cone(Annotation):
    type: str = AnnotationType.cone
    vector: Vector = Field(
        default=..., description="Vector for the center line of the cone"
    )
    start_radius: float = Field(
        default=..., description="Radius of the base of the cone"
    )
    end_radius: float = Field(
        default=0.0,
        description=(
            "Radius of the end of the cone, if 0.0, the cone comes to a sharp point,"
            "otherwise it is cut off"
        ),
    )


class Cuboid(Annotation):
    """
    A cuboid (3D) or rectangular (2D) box defined by two vectors

    Vectors point to two diagonally opposite corners of the box
    """

    type: str = AnnotationType.cuboid
    v1: Vector = Field(
        default=...,
        description="A vector that points to a corner of the box from the center point",
    )
    v2: Vector = Field(
        default=None,
        description=(
            "A vector that points to the diagonally opposite corner of the box"
        ),
    )

    @model_validator(mode="after")
    def validate_inputs(self) -> Cuboid:
        check_input_dims([self.v1.start, self.v2.start])
        if not np.allclose(self.v1.start.array, self.v2.start.array):
            raise ValueError("Both corner vectors must originate at the same point")
        return self

    @property
    def center_point(self) -> np.ndarray:
        if self.v1.start.dim == 2:
            return np.array([[self.v1.start.x], [self.v1.start.y]])
        else:
            return np.array([[self.v1.start.x], [self.v1.start.y], [self.v1.start.z]])


class Cylinder(Annotation):
    type: str = AnnotationType.cylinder
    vector: Vector = Field(
        default=..., description="Vector for the center line of the cylinder"
    )
    radius: float = Field(default=..., description="The radius of the cylinder")


class FitMap(Annotation):
    """Annotation for a fitted map"""

    type: str = AnnotationType.map
    center: CoordsLogical = Field(
        default=..., description="Coords of the center of the map"
    )
    file: str = Field(default=..., description="Path to the map file")
    transformation: Optional[Transformation] = Field(
        default=None,
        description=(
            "Tranformation applied to fit the map. IE: Affine transform for rotation"
        ),
    )


class Ovoid(Annotation):
    """An 2D oval or 3D  ovoid with its widest point at 'waist_point' on the main
    vector"""

    type: str = AnnotationType.ovoid
    vector: Vector = Field(
        default=..., description="Vector that describes the center line of the ovoid"
    )
    waist_radius: float = Field(
        default=..., description="The radius of the ovoid at its widest point"
    )
    waist_point: Optional[CoordsLogical] = Field(
        default=None,
        description=(
            "Coords of the point in the center vector where the ovoid is widest"
        ),
    )

    @model_validator(mode="after")
    def check_waist_point_dim(self) -> Ovoid:
        if self.waist_point is not None:
            check_input_dims([self.waist_point, self.vector.start])
        return self

    def model_post_init(self, __context) -> None:
        # calculate the waist point if not given
        if self.waist_point is None:
            mids = (self.vector.start.array + self.vector.end.array) / 2
            self.waist_point = CoordsLogical(
                x=mids[0, 0],
                y=mids[1, 0],
                z=None if self.vector.start.dim == 2 else mids[2, 0],
            )
        # verify waist point is on the central vector
        v = self.vector.end.array - self.vector.start.array
        w = self.waist_point.array - self.vector.start.array

        v_flat = v.flatten()
        w_flat = w.flatten()

        is_colinear = np.allclose(np.cross(v_flat, w_flat), 0)

        dot_vv = np.dot(v_flat, v_flat)
        t = np.dot(w_flat, v_flat) / dot_vv
        if not (is_colinear and (0 <= t <= 1)):
            raise ValueError("Ovoid waist point is not on central vector")


class Point(Annotation):
    type: str = AnnotationType.point
    coords: CoordsLogical = Field(
        default=None, description="The coordinates of the point"
    )

    @property
    def dim(self):
        if self.coords.z:
            return 3
        else:
            return 2


class Particle(Point):
    type: str = AnnotationType.particle
    fom: Optional[float] = Field(
        default=None, description="Figure of merit for autopicking"
    )
    alignment_transformations: List[Transformation] = Field(
        default_factory=list,
        description="Transformations applied to align this particle",
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

    # TODO: Validate the cutouts overlap with the base, raise warning otherwise
    #  This will be very complicated!


class Sphere(Annotation):
    """A sphere or circle of radius 'radius' centered on a coordinate"""

    type: str = AnnotationType.sphere
    center: CoordsLogical = Field(
        default=..., description="The center point of the circle/sphere"
    )
    radius: float = Field(default=..., description="The sphere radius")

    @property
    def center_point(self):
        return self.center.array


class Spline(Annotation):
    type: str = AnnotationType.spline
    points: List[CoordsLogical] = Field(default=..., description="At least two points")

    @field_validator("points")
    def at_least_three_points(cls, value: List[CoordsLogical]) -> List[CoordsLogical]:
        if len(value) < 3:
            raise ValueError("A spline must have at least 3 points")
        return value

    @model_validator(mode="after")
    def check_waist_point_dim(self) -> Spline:
        check_input_dims(self.points)
        return self


class Vector(Annotation):
    """A vector defined by two points"""

    type: str = AnnotationType.vector
    start: CoordsLogical
    end: CoordsLogical

    @model_validator(mode="after")
    def input_dims_match(self) -> Vector:
        check_input_dims([self.start, self.end])
        return self

    @property
    def points(self) -> List[np.ndarray]:
        """
        Get the start and end points of the vector as arrays

        Returns:
            np.ndarry: the start and end point arrays
        """
        start_coords = self.start.array
        end_coords = self.end.array
        return [start_coords, end_coords]

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


class ParticleCoordinatesSet(AnnotationSet):
    """
    An AnnotationSet subclass for a set of picked particle coordinates
    """

    type: str = AnnotationSetTypes.particle_coords
    particles: List[Particle] = Field(
        default_factory=list, description="Picked particle coorindates"
    )


# TODO: Add Surface and Volume Annotation types.  Investigate the best way to do this
#  probably use the trimesh library and .stl files.

# Model rebuilds
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model

AnnotationSet.model_rebuild()
Cone.model_rebuild()
Cuboid.model_rebuild()
Cylinder.model_rebuild()
FitMap.model_rebuild()
Ovoid.model_rebuild()
Particle.model_rebuild()
ParticleCoordinatesSet.model_rebuild()
Point.model_rebuild()
Shell.model_rebuild()
Sphere.model_rebuild()
Spline.model_rebuild()
Vector.model_rebuild()
