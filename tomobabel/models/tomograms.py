from __future__ import annotations

from typing import Optional

from tomobabel.models.basemodels import Image3D, ConfiguredBaseModel, CoordsLogical
from tomobabel.models.transformations import AffineTransform
from tomobabel.models.tilt_series import CTFMetadata
from pydantic import Field


class Tomogram(Image3D):
    file: Optional[str] = Field(default=None, description="Path to the file")


class SubTomogram(Image3D):
    """
    Holds a sub tomogram
    """

    alignment_transformation: Optional[AffineTransform] = Field(
        default=None, description="The transformation applied to align this subtomo"
    )
    ctf_metadata: Optional[CTFMetadata] = Field(
        default=None, description="CTF metadata for this subtomo"
    )
    coordinates: Optional[CoordsLogical] = Field(
        default=None,
        description="The location of the center of the subtomo in the parent tomogram",
    )


class Map(ConfiguredBaseModel):
    """
    Holds a 3D map
    """

    file: str = Field(default=..., description="Path the map file")
    pixel_size: Optional[float] = Field(default=None, description="The pixel size in Å")
