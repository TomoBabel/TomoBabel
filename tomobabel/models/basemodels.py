import numpy as np
from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from pydantic import Field, model_validator
from enum import Enum

metamodel_version = "None"
version = "0.0.1"


class AnnotationModel(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True,
        validate_default=True,
        extra="forbid",
        arbitrary_types_allowed=True,
        use_enum_values=True,
        strict=False,
    )


class Annotation(AnnotationModel):
    type: str = "text"
    text: str = Field(default="", description="Free text for annotation description")


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True,
        validate_default=True,
        extra="forbid",
        arbitrary_types_allowed=True,
        use_enum_values=True,
        strict=False,
    )
    annotations: List[Annotation] = Field(
        default_factory=list, description="Annotations for this Image"
    )


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


class AxisOrigin(str, Enum):
    """
    Describes the origin of an axis
    most common cases for a 2D image:
        x is bottom and y is bottom:  0,0 is the bottom left of the image
        x is bottom and y is top:  0,0 is at the top left of the image
        x is center, y is center: 0,0 is at the center of the image
    """

    # 0 is at the low end of the axis, all values for coords on an image will be
    # positive
    bottom = "bottom"
    # 0 is at the center, values for coords on an image can be positive or negative
    centerpoint = "center"
    # 0 is at the high end of the axis, all values in an image will be negative
    # IE origin is at the bottom
    top = "top"


class CoordUnit(str, Enum):
    """
    Describes the units for a coordinate
    """

    angstrom = "Ångstrom"
    pixel = "pixel/voxel"


class CoordinateLogical(ConfiguredBaseModel):
    axis_origin: str = AxisOrigin.centerpoint
    unit: str = CoordUnit.angstrom
    value: float = Field(default=..., description="The coordinate value")


class CoordinatePhysical(ConfiguredBaseModel):
    axis_origin: str = AxisOrigin.top
    unit: str = CoordUnit.pixel
    value: int = Field(default=..., description="The coordinate value")


class CoordsPhysical(ConfiguredBaseModel):
    """
    A 3D coordinate
    """

    x: CoordinatePhysical = Field(default=..., description="x coord")
    y: CoordinatePhysical = Field(default=..., description="y coord")
    z: Optional[CoordinatePhysical] = Field(default=None, description="z coord")

    @model_validator(mode="after")
    def units_match(self):
        vals = [self.x, self.y]
        if self.z:
            vals.append(self.z)
        if not (v.unit == vals[0].unit for v in vals):
            raise ValueError("Coordinate axes must have the same units")
        return self

    @property
    def coord_array(self) -> np.ndarray:
        if not self.z:
            # pad 2D coords if necessary
            return np.array([[self.x.value], [self.y.value], [1.0]])
        else:
            return np.array([[self.x.value], [self.y.value], [self.z.value]])


class CoordsLogical(ConfiguredBaseModel):
    """
    A 3D coordinate. In the logical coordinate system
    0,0,0 is at the center of the image, units are in Ångstrom
    """

    x: CoordinateLogical = Field(default=..., description="x coord")
    y: CoordinateLogical = Field(default=..., description="y coord")
    z: Optional[CoordinateLogical] = Field(default=None, description="z coord")

    @property
    def coord_array(self) -> np.ndarray:
        if not self.z:
            # pad 2D coords if necessary
            return np.array([[self.x], [self.y], 1])
        else:
            return np.array([[self.x], [self.y], [self.z]])


# Model rebuilds
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model

Annotation.model_rebuild()
CoordinateLogical.model_rebuild()
CoordsLogical.model_rebuild()
CoordinatePhysical.model_rebuild()
CoordsPhysical.model_rebuild()
Image2D.model_rebuild()
Image3D.model_rebuild()
