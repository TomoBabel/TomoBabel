from __future__ import annotations

from enum import Enum
from typing import Optional, List, Union

import numpy as np
from pydantic import Field, field_validator, model_validator

from tomobabel.models.basemodels import ConfiguredBaseModel, CoordsLogical, Annotation
from tomobabel.models.transformations import AffineTransform


# TODO: give all these helper properties like center, corners vector and etc,


def check_input_dims(inputs: List[object]):
    if not all([isinstance(x, type(inputs[0])) for x in inputs]):
        raise ValueError("Input dimensions do not match")


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


class Cone(Annotation):
    type: str = AnnotationType.cone
    vector: Vector = Field(
        default=..., description="Vector for the center line of the cylinder"
    )
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


class Cuboid(Annotation):
    """A cuboidal box defined by two or three vectors"""

    type: str = AnnotationType.cuboid
    center: Point = Field(default=..., description="The center of the box")
    v1: Vector = Field(
        default=...,
        description="A vector that points to a face of the box from the center point",
    )
    v2: Optional[Vector] = Field(
        default=None,
        description=(
            "A vector that points to the 2nd face of the box, if None it will be set "
            "as 90° from v1 to make a square/cube"
        ),
    )
    v3: Optional[Vector] = Field(
        default=None,
        description=(
            "A vector that points to the 3nd face of the box, if None it will be set as"
            "90° from v2 to make a square/cube"
        ),
    )

    # TODO: write function that calculates V2 and V3 automatically for a cube


class Cylinder(Annotation):
    type: str = AnnotationType.cylinder
    vector: Vector = Field(
        default=..., description="Vector for the center line of the cylinder"
    )
    diameter: float = Field(default=..., description="The diameter of the cylinder")


class FitMap(Annotation):
    """Annotation for a fitted map"""

    type: str = AnnotationType.map
    center: Point = Field(default=..., description="Coords of the center of the map")
    file: str = Field(default=..., description="Path to the map file")
    transformation: AffineTransform = Field(
        default=AffineTransform(),
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
    waist_size: float = Field(
        default=..., description="The length across the ovoid at its widest point"
    )
    waist_point: Optional[Point] = Field(
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
            mids = (self.vector.start.coord_array + self.vector.end.coord_array) / 2
            self.waist_point = Point(
                x=mids[0, 0],
                y=mids[1, 0],
                z=None if self.vector.start.dim == 2 else mids[2, 0],
            )
        # verify waist point is on the central vector
        v = self.vector.end.coord_array - self.vector.start.coord_array
        w = self.waist_point.coord_array - self.vector.start.coord_array

        v_flat = v.flatten()
        w_flat = w.flatten()

        is_colinear = np.allclose(np.cross(v_flat, w_flat), 0)

        dot_vv = np.dot(v_flat, v_flat)
        t = np.dot(w_flat, v_flat) / dot_vv
        if not (is_colinear and (0 <= t <= 1)):
            raise ValueError("Ovoid waist point is not on central vector")


class Point(CoordsLogical):
    type: str = AnnotationType.point


class Particle(Point):
    type: str = AnnotationType.particle
    fom: Optional[float] = Field(
        default=None, description="Figure of merit for autopicking"
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


class Sphere(Annotation):
    """A sphere or circle of radius 'radius' centered on a coordinate"""

    type: str = AnnotationType.sphere
    center: Point = Field(
        default=..., description="The center point of the circle/sphere"
    )
    radius: float = Field(default=..., description="The sphere diameter")

    @property
    def coord_array(self):
        return self.center.coord_array


class Spline(Annotation):
    type: str = AnnotationType.spline
    points: List[Point] = Field(default=..., description="At least two points")

    @field_validator("points")
    def at_least_three_points(cls, value: List[Point]) -> List[Point]:
        if len(value) < 3:
            raise ValueError("A spline must have at least 3 points")
        return value


class Vector(Annotation):
    """A defined by two points"""

    type: str = AnnotationType.vector
    start: Point
    end: Point

    @model_validator(mode="after")
    def input_dims_match(self) -> Vector:
        check_input_dims([self.start, self.end])
        return self

    @property
    def points(self) -> np.ndarray:
        """
        Get the start and end points of the vector as arrays

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


class AnnotationSetTypes(str, Enum):
    """
    Types for sets of annotations
    """

    general = "annotations"
    particle_coords = "particle_coordinates"


class AnnotationSet(ConfiguredBaseModel):
    name: str = Field(
        default=AnnotationSetTypes.general,
        description="The name of the annotation set EG 'Membranes' or 'Ribosomes'",
    )
    annotations: List[Annotation] = Field(default=..., description="The annotations")


class ParticleCoordinatesSet(AnnotationSet):
    type: str = AnnotationSetTypes.particle_coords
    particles: List[Particle] = Field(
        default_factory=[], description="Picked particle coorindates"
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
