from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from tomobabel.models.basemodels import ConfiguredBaseModel, Image2D
from tomobabel.models.transformations import Transformation, TranslationTransform


class GainFile(Image2D):
    """
    A gain reference file.
    """

    path: str = Field(default="")
    width: Optional[int] = Field(
        default=None, description="The width of the image (x-axis) in pixels"
    )
    height: Optional[int] = Field(
        default=None, description="The height of the image (y-axis) in pixels"
    )
    transformations: List[Transformation] = Field(
        default_factory=list,
        description=(
            "Any transformation applied to the file before applying, usually a flip"
        ),
    )


class DefectFile(Image2D):
    """
    A detector defect file.
    """

    path: str = Field(default="")
    width: Optional[int] = Field(
        default=None, description="The width of the image (x-axis) in pixels"
    )
    height: Optional[int] = Field(
        default=None, description="The height of the image (y-axis) in pixels"
    )
    transformations: List[Transformation] = Field(
        default_factory=list,
        description=(
            "Any trasformation applied to the file before applying, usually a flip"
        ),
    )


class CTFMetadata(ConfiguredBaseModel):
    """
    A set of CTF parameters for an image.
    """

    defocus_u: Optional[float] = Field(
        default=None,
        description=(
            "Estimated defocus U for this image in Angstrom, underfocus positive."
        ),
    )
    defocus_v: Optional[float] = Field(
        default=None,
        description=(
            "Estimated defocus V for this image in Angstrom, underfocus positive."
        ),
    )
    defocus_angle: Optional[float] = Field(
        default=None, description="Estimated angle of astigmatism."
    )
    # TODO: write better description for this
    defocus_handedness: Optional[int] = Field(
        default=-1,
        description=(
            "Which direction is positive for defocus angle. Using RELION convention"
        ),
    )


class MovieFrame(Image2D):
    """
    An individual movie frame
    """

    path: str = Field(default="")
    section: Optional[int] = Field(
        default=None,
        description="0-based section index to the entity inside a stack.",
    )
    nominal_tilt_angle: Optional[float] = Field(
        default=None, description="The tilt angle reported by the microscope in degrees"
    )
    accumulated_dose: Optional[float] = Field(
        default=None, description="The pre-exposure up to this image in e-/A^2"
    )
    ctf_metadata: Optional[CTFMetadata] = Field(
        default=None, description="A set of CTF patameters for an image."
    )
    width: Optional[int] = Field(
        default=None, description="The width of the image (x-axis) in pixels"
    )
    height: Optional[int] = Field(
        default=None, description="The height of the image (y-axis) in pixels"
    )
    motion_correction_transformations: List[Transformation] = Field(
        default_factory=list,
        description="Transformations applied during motion correction",
    )


class MovieStack(ConfiguredBaseModel):
    """
    A stack of movie frames.
    """

    images: List[MovieFrame] = Field(
        default=..., description="The movie frames in the stack"
    )
    path: str = Field(default="")


class MovieStackSeries(ConfiguredBaseModel):
    """
    A group of movie stacks that belong to a single tilt series.
    """

    movie_stacks: List[MovieStack] = Field(
        default_factory=list, description="The movie stacks"
    )


class MovieStackCollection(ConfiguredBaseModel):
    """
    A collection of movie stacks using the same gain and defect files.
    """

    movie_stacks: List[MovieStackSeries] = Field(
        default_factory=list, description="The movie stacks in the collection"
    )
    gain_file: Optional[GainFile] = Field(
        default=None, description="The gain file for the movie stacks"
    )
    defect_file: Optional[DefectFile] = Field(
        default=None, description="The defect file for the movie stacks"
    )


class TiltSeriesMicrographAlignment(ConfiguredBaseModel):
    """
    Describes the transformations to align a micrograph in a tilt series
    """

    translation: TranslationTransform = Field(
        default=TranslationTransform(),
        description="Matrix that describes the translations for alignment",
    )
    x_tilt: float = Field(default=0.0, description="Tilt in x in degrees")
    y_tilt: float = Field(default=0.0, description="Tilt in y in degrees")
    z_rot: float = Field(default=0.0, description="Rotation around z in degrees")


class TiltSeriesMicrograph(Image2D):
    """
    A merged micrograph generated from a movie stack
    """

    ctf_metadata: Optional[CTFMetadata] = Field(
        default=None, description="A set of CTF patameters for an image."
    )
    total_accumulated_dose: Optional[float] = Field(
        default=None, description="The total dose in e-/A^2"
    )
    nominal_tilt_angle: Optional[float] = Field(
        default=None, description="The tilt angle reported by the microscope in degrees"
    )
    refined_tilt_angle: Optional[float] = Field(
        default=None, description="The tilt angle after refinement in degrees"
    )
    alignment_transformations: TiltSeriesMicrographAlignment = Field(
        default=TiltSeriesMicrographAlignment(),
        description="Transformations applied for tilt series alignment",
    )
    path: str = Field(
        default="",
        description=(
            "Path to the image file.  Can be a file path or an index to a frame of a "
            "stack EG: 001@stack_name.mrc"
        ),
    )


class TiltSeriesMicrographStack(ConfiguredBaseModel):
    """
    A set of aligned micrographs for a tilt series
    """

    micrographs: List[TiltSeriesMicrograph] = Field(
        default_factory=list,
        description="The micrographs that make up this tilt series",
    )
    path: str = Field(default="")


class TiltSeriesSet(ConfiguredBaseModel):
    """
    A container for the aligned tilt series associated with a region
    """

    tilt_series: List[TiltSeriesMicrographStack] = Field(
        default=...,
        description="The TiltSeriesMicrographStacks associated with this Region",
    )


# Model rebuilds
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model

CTFMetadata.model_rebuild()
DefectFile.model_rebuild()
GainFile.model_rebuild()
MovieFrame.model_rebuild()
MovieStack.model_rebuild()
MovieStackCollection.model_rebuild()
MovieStackSeries.model_rebuild()
TiltSeriesMicrograph.model_rebuild()
TiltSeriesMicrographStack.model_rebuild()
TiltSeriesSet.model_rebuild()
