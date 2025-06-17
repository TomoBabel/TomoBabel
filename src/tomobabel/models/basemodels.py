from enum import Enum
from typing import Optional, List, Union

import numpy as np
from pydantic import BaseModel, ConfigDict
from pydantic import Field

metamodel_version = "None"
version = "0.0.1"

basemodel_config = ConfigDict(
    validate_assignment=True,
    validate_default=True,
    extra="forbid",
    arbitrary_types_allowed=True,
    use_enum_values=True,
    strict=False,
    json_encoders={np.ndarray: lambda a: a.tolist()},
)


class Annotation(BaseModel):
    """
    BaseClass to hold annotations
    """

    model_config = basemodel_config

    type: str = "text"
    description: str = Field(
        default="", description="Free text for annotation description"
    )


class AnnotationSetTypes(str, Enum):
    """
    Types for sets of annotations
    """

    general = "annotations"
    particle_coords = "particle_coordinates"


class AnnotationSet(BaseModel):
    model_config = basemodel_config

    name: str = Field(
        default=AnnotationSetTypes.general,
        description="The name of the annotation set EG 'Membranes' or 'Ribosomes'",
    )
    annotations: List[Annotation] = Field(default=..., description="The annotations")


class ConfiguredBaseModel(BaseModel):
    """
    Base model with an annotation
    """

    model_config = basemodel_config

    annotations: List[Union[Annotation, AnnotationSet]] = Field(
        default_factory=list, description="Annotations for this Image"
    )

    def add_text_annotation(self, text: str) -> None:
        if text:
            self.annotations.append(Annotation(description=text))

    def add_annotation(self, annotation: Union[Annotation, AnnotationSet]) -> None:
        self.annotations.append(annotation)


class Image2D(ConfiguredBaseModel):
    """
    A 2D image.
    """

    width: Optional[int] = Field(
        default=None, description="""The width of the image (x-axis) in pixels"""
    )
    height: Optional[int] = Field(
        default=None, description="""The height of the image (y-axis) in pixels"""
    )
    pixel_size: Optional[float] = Field(default=None, description="The pixel size in Å")


class Image3D(ConfiguredBaseModel):
    """
    A 3D image.
    """

    width: Optional[int] = Field(
        default=None, description="""The width of the image (x-axis) in pixels"""
    )
    height: Optional[int] = Field(
        default=None, description="""The height of the image (y-axis) in pixels"""
    )
    depth: Optional[int] = Field(
        default=None, description="""The depth of the image (z-axis) in pixels"""
    )
    voxel_size: Optional[float] = Field(default=None, description="The pixel size in Å")


class CoordUnit(str, Enum):
    """
    Describes the units for a coordinate
    """

    angstrom = "Ångstrom"
    pixel = "pixel/voxel"


class CoordsPhysical(ConfiguredBaseModel):
    """
    A 3D coordinate in the physical coordinate system.  Units are in pixel/voxel,
    0,0,0 is at the upper left of the image
    """

    # TODO: Is this really the origin we want? Would lower-left be better?

    x: int = Field(default=..., description="x coord")
    y: int = Field(default=..., description="y coord")
    z: Optional[int] = Field(default=None, description="z coord")
    description: str = Field(default="", description="Any text for this coordinate")

    @property
    def dim(self) -> int:
        return 3 if self.z is not None else 2

    @property
    def array(self) -> np.ndarray:
        if self.dim == 3:
            return np.array([[self.x], [self.y], [self.z]])
        else:
            return np.array([[self.x], [self.y]])

    @property
    def hom_array(self) -> np.ndarray:
        if self.dim == 3:
            return np.array([[self.x], [self.y], [self.z], [1]])
        else:
            return np.array([[self.x], [self.y], [1]])


class CoordsLogical(ConfiguredBaseModel):
    """
    A 3D coordinate. In the logical coordinate system
    0,0,0 is at the center of the image, units are in Ångstrom
    """

    x: float = Field(default=..., description="x coord")
    y: float = Field(default=..., description="y coord")
    z: Optional[float] = Field(default=None, description="z coord")
    description: str = Field(default="", description="Any text for this coordinate")

    @property
    def dim(self) -> int:
        return 3 if self.z is not None else 2

    @property
    def array(self) -> np.ndarray:
        if self.dim == 3:
            return np.array([[self.x], [self.y], [self.z]])
        else:
            return np.array([[self.x], [self.y]])

    @property
    def hom_array(self) -> np.ndarray:
        if self.dim == 3:
            return np.array([[self.x], [self.y], [self.z], [1]])
        else:
            return np.array([[self.x], [self.y], [1]])


# Model rebuilds
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model

Annotation.model_rebuild()
CoordsLogical.model_rebuild()
CoordsPhysical.model_rebuild()
Image2D.model_rebuild()
Image3D.model_rebuild()
