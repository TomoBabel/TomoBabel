from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from tomobabel.models.basemodels import (
    ConfiguredBaseModel,
    Image2D,
    Image3D,
    CoordsLogical,
)
from tomobabel.models.transformations import Transformation, TranslationTransform
from tomobabel.models.transformations import AffineTransform


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

    frame_images: List[MovieFrame] = Field(
        default=..., description="The movie frames in the stack"
    )
    path: str = Field(default="")


class MovieStackSet(ConfiguredBaseModel):
    """
    A group of movie stacks that belong to a single tilt series.
    """

    movie_stacks: List[MovieStack] = Field(
        default_factory=list, description="The movie stacks"
    )
    tilt_series: List[TiltSeriesMicrographStack] = Field(
        default_factory=[],
        description="Sets of tilt series micrographs from this set of movie stacks",
    )


class MovieStackCollection(ConfiguredBaseModel):
    """
    A collection of movie stacks using the same gain and defect files.
    """

    movie_stack_sets: List[MovieStackSet] = Field(
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
    Tomograms: List[TomogramSet] = Field(
        default_factory=list,
        description="Tomograms created from this set of tilt images",
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


class Tomogram(Image3D):
    """Holds a tomogram"""

    file: Optional[str] = Field(default=None, description="Path to the file")
    subtomograms: List[SubTomogramSet] = Field(
        default_factory=[],
        description="Sets of subtomograms extracted from this tomogram",
    )


class TomogramSet(ConfiguredBaseModel):
    """
    Holds a set of Tomograms
    """

    tomograms: List[Tomogram] = Field(
        default_factory=[],
        description="A set of tomograms created from these tilt series micrographs",
    )


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


class SubTomogramSet(ConfiguredBaseModel):
    """
    Holds a set of subtomograms
    """

    Subtomograms: List[SubTomogram] = Field(
        default_factory=[], description="Sets of subtomograms extracted from a tomogram"
    )
    maps: List[Map] = Field(
        default_factory=[], description="Maps derived from this set of subtomograms"
    )


class Map(ConfiguredBaseModel):
    """
    Holds a 3D map
    """

    file: str = Field(default=..., description="Path the map file")
    pixel_size: Optional[float] = Field(default=None, description="The pixel size in Å")


# Model rebuilds
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model

CTFMetadata.model_rebuild()
DefectFile.model_rebuild()
GainFile.model_rebuild()
Map.model_rebuild()
MovieFrame.model_rebuild()
MovieStack.model_rebuild()
MovieStackCollection.model_rebuild()
MovieStackSet.model_rebuild()
SubTomogram.model_rebuild()
SubTomogramSet.model_rebuild()
TiltSeriesMicrograph.model_rebuild()
TiltSeriesMicrographStack.model_rebuild()
TiltSeriesSet.model_rebuild()
Tomogram.model_rebuild()
TomogramSet.model_rebuild()
