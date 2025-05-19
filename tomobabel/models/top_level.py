from __future__ import annotations

from typing import List, Optional, Union

from pydantic import Field

from tomobabel.models.basemodels import ConfiguredBaseModel, Image2D, Image3D
from tomobabel.models.tomo_images import MovieStackSet


class DataSet(ConfiguredBaseModel):
    """
    Top-level container for the entire dataset
    """

    name: str = Field(default="", description="Name for this dataset")
    regions: List[Region] = Field(
        default_factory=list, description="All regions in the dataset"
    )


class Region(ConfiguredBaseModel):
    """
    Data from a single region of a specimen.
    Tilt series and their derived data and non-tomographic images
    """

    tomo_imaging: List[TomoImageSet] = Field(
        default_factory=list, description="Tilt series associated with the region"
    )
    non_tomo_imaging: List[NonTomoImageSet] = Field(
        default_factory=list,
        description="Non-tilt series images associated with the region, EG: CLEM",
    )


class TomoImageSet(ConfiguredBaseModel):
    raw_movies: Optional[MovieStackSet] = Field(
        default=None, description="Raw movies associated with this tilt series"
    )


class NonTomoImageSet(ConfiguredBaseModel):
    """A set of images that are not part of a tomographic tiltseries or tomogram"""

    images: List[Union[Image3D, Image2D]] = Field(
        default_factory=list, description="A list of non-tomographic images"
    )


# Model rebuilds
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model

DataSet.model_rebuild()
NonTomoImageSet.model_rebuild()
Region.model_rebuild()
TomoImageSet.model_rebuild()
