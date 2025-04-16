from __future__ import annotations

import re
import sys
from datetime import date, datetime, time
from decimal import Decimal
from enum import Enum
from typing import Any, ClassVar, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, RootModel, conlist, field_validator


metamodel_version = "None"
version = "0.0.1"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True,
        validate_default=True,
        extra="forbid",
        arbitrary_types_allowed=True,
        use_enum_values=True,
        strict=False,
    )
    pass


class LinkMLMeta(RootModel):
    root: Dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key: str):
        return getattr(self.root, key)

    def __getitem__(self, key: str):
        return self.root[key]

    def __setitem__(self, key: str, value):
        self.root[key] = value

    def __contains__(self, key: str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta(
    {
        "default_prefix": "entities",
        "description": "Schema for cryoET geometry",
        "id": "https://w3id.org/cetmd/entities",
        "imports": ["linkml:types", "./image_entities", "./annotation"],
        "name": "CETMDEntities",
        "prefixes": {
            "annotation": {
                "prefix_prefix": "annotation",
                "prefix_reference": "https://w3id.org/cetmd/annotation/",
            },
            "entities": {
                "prefix_prefix": "entities",
                "prefix_reference": "https://w3id.org/cetmd/entities/",
            },
            "image_entities": {
                "prefix_prefix": "image_entities",
                "prefix_reference": "https://w3id.org/cetmd/imageentities/",
            },
            "linkml": {
                "prefix_prefix": "linkml",
                "prefix_reference": "https://w3id.org/linkml/",
            },
        },
        "source_file": "data_model/entities.yaml",
    }
)


class AxisType(str, Enum):
    """
    The type of axis
    """

    # A spatial axis
    space = "space"
    # An array axis
    array = "array"


class TransformationType(str, Enum):
    # The identity transformation.
    identity = "identity"
    # Axis permutation transformation
    mapAxis = "mapAxis"
    # A translation transformation.
    translation = "translation"
    # A scaling transformation.
    scale = "scale"
    # An affine transformation
    affine = "affine"
    # A sequence of transformations
    sequence = "sequence"


class Image2D(ConfiguredBaseModel):
    """
    A 2D image.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://w3id.org/cetmd/image/"}
    )

    width: Optional[int] = Field(
        default=None,
        description="""The width of the image (x-axis) in pixels""",
        json_schema_extra={
            "linkml_meta": {"alias": "width", "domain_of": ["Image2D", "Image3D"]}
        },
    )
    height: Optional[int] = Field(
        default=None,
        description="""The height of the image (y-axis) in pixels""",
        json_schema_extra={
            "linkml_meta": {"alias": "height", "domain_of": ["Image2D", "Image3D"]}
        },
    )
    coordinate_systems: Optional[List[CoordinateSystem]] = Field(
        default=None,
        description="""Named coordinate systems for this entity""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "coordinate_systems",
                "domain_of": ["Image2D", "Image3D", "CoordMetaMixin"],
            }
        },
    )
    coordinate_transformations: Optional[List[CoordinateTransformation]] = Field(
        default=None,
        description="""Named coordinate systems for this entity""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "coordinate_transformations",
                "domain_of": ["Image2D", "Image3D", "CoordMetaMixin"],
            }
        },
    )


class Image3D(ConfiguredBaseModel):
    """
    A 3D image.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://w3id.org/cetmd/image/"}
    )

    width: Optional[int] = Field(
        default=None,
        description="""The width of the image (x-axis) in pixels""",
        json_schema_extra={
            "linkml_meta": {"alias": "width", "domain_of": ["Image2D", "Image3D"]}
        },
    )
    height: Optional[int] = Field(
        default=None,
        description="""The height of the image (y-axis) in pixels""",
        json_schema_extra={
            "linkml_meta": {"alias": "height", "domain_of": ["Image2D", "Image3D"]}
        },
    )
    depth: Optional[int] = Field(
        default=None,
        description="""The depth of the image (z-axis) in pixels""",
        json_schema_extra={"linkml_meta": {"alias": "depth", "domain_of": ["Image3D"]}},
    )
    coordinate_systems: Optional[List[CoordinateSystem]] = Field(
        default=None,
        description="""Named coordinate systems for this entity""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "coordinate_systems",
                "domain_of": ["Image2D", "Image3D", "CoordMetaMixin"],
            }
        },
    )
    coordinate_transformations: Optional[List[CoordinateTransformation]] = Field(
        default=None,
        description="""Named coordinate systems for this entity""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "coordinate_transformations",
                "domain_of": ["Image2D", "Image3D", "CoordMetaMixin"],
            }
        },
    )


class ImageStack2D(ConfiguredBaseModel):
    """
    A stack of 2D images.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://w3id.org/cetmd/image/"}
    )

    images: Optional[List[Image2D]] = Field(
        default=None,
        description="""The images in the stack""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "images",
                "domain_of": [
                    "ImageStack2D",
                    "ImageStack3D",
                    "MovieStack",
                    "TiltSeries",
                ],
            }
        },
    )


class ImageStack3D(ConfiguredBaseModel):
    """
    A stack of 3D images.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://w3id.org/cetmd/image/"}
    )

    images: Optional[List[Image3D]] = Field(
        default=None,
        description="""The images in the stack""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "images",
                "domain_of": [
                    "ImageStack2D",
                    "ImageStack3D",
                    "MovieStack",
                    "TiltSeries",
                ],
            }
        },
    )


class Axis(ConfiguredBaseModel):
    """
    An axis in a coordinate system
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://w3id.org/cetmd/coordinate_systems"}
    )

    name: str = Field(
        default=...,
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": [
                    "Axis",
                    "CoordinateSystem",
                    "CoordinateTransformation",
                    "Average",
                    "Dataset",
                ],
                "exact_mappings": ["axis_name"],
            }
        },
    )
    axis_unit: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "axis_unit",
                "domain_of": ["Axis"],
                "exact_mappings": ["axis_unit"],
            }
        },
    )
    axis_type: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "axis_type",
                "domain_of": ["Axis"],
                "exact_mappings": ["axis_type"],
            }
        },
    )


class CoordinateSystem(ConfiguredBaseModel):
    """
    A coordinate system
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://w3id.org/cetmd/coordinate_systems"}
    )

    name: str = Field(
        default=...,
        description="""The name of the coordinate system""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": [
                    "Axis",
                    "CoordinateSystem",
                    "CoordinateTransformation",
                    "Average",
                    "Dataset",
                ],
            }
        },
    )
    axes: List[Axis] = Field(
        default=...,
        description="""The axes of the coordinate system""",
        json_schema_extra={
            "linkml_meta": {"alias": "axes", "domain_of": ["CoordinateSystem"]}
        },
    )


class CoordinateTransformation(ConfiguredBaseModel):
    """
    A coordinate transformation
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://w3id.org/cetmd/coord_transforms"}
    )

    name: Optional[str] = Field(
        default=None,
        description="""The name of the coordinate transformation""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": [
                    "Axis",
                    "CoordinateSystem",
                    "CoordinateTransformation",
                    "Average",
                    "Dataset",
                ],
            }
        },
    )
    input: Optional[str] = Field(
        default=None,
        description="""The source coordinate system name""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "input",
                "domain_of": ["CoordinateTransformation", "ProjectionAlignment"],
            }
        },
    )
    output: Optional[str] = Field(
        default=None,
        description="""The target coordinate system name""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "output",
                "domain_of": ["CoordinateTransformation", "ProjectionAlignment"],
            }
        },
    )
    type: Optional[TransformationType] = Field(
        default=None,
        description="""The type of transformation""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "type",
                "domain_of": [
                    "CoordinateTransformation",
                    "Identity",
                    "MapAxis",
                    "Translation",
                    "Scale",
                    "Affine",
                    "Sequence",
                ],
            }
        },
    )


class Identity(CoordinateTransformation):
    """
    The identity transformation
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://w3id.org/cetmd/coord_transforms"}
    )

    type: Optional[TransformationType] = Field(
        default="identity",
        description="""The type of transformation""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "type",
                "domain_of": [
                    "CoordinateTransformation",
                    "Identity",
                    "MapAxis",
                    "Translation",
                    "Scale",
                    "Affine",
                    "Sequence",
                ],
                "ifabsent": "identity",
            }
        },
    )
    name: Optional[str] = Field(
        default=None,
        description="""The name of the coordinate transformation""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": [
                    "Axis",
                    "CoordinateSystem",
                    "CoordinateTransformation",
                    "Average",
                    "Dataset",
                ],
            }
        },
    )
    input: Optional[str] = Field(
        default=None,
        description="""The source coordinate system name""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "input",
                "domain_of": ["CoordinateTransformation", "ProjectionAlignment"],
            }
        },
    )
    output: Optional[str] = Field(
        default=None,
        description="""The target coordinate system name""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "output",
                "domain_of": ["CoordinateTransformation", "ProjectionAlignment"],
            }
        },
    )


class AxisNameMapping(ConfiguredBaseModel):
    """
    Axis name to Axis name mapping
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://w3id.org/cetmd/coord_transforms"}
    )

    axis1_name: Optional[str] = Field(
        default=None,
        description="""The type of transformation""",
        json_schema_extra={
            "linkml_meta": {"alias": "axis1_name", "domain_of": ["AxisNameMapping"]}
        },
    )
    axis2_name: Optional[str] = Field(
        default=None,
        description="""The mapping of the axis names""",
        json_schema_extra={
            "linkml_meta": {"alias": "axis2_name", "domain_of": ["AxisNameMapping"]}
        },
    )


class MapAxis(CoordinateTransformation):
    """
    Axis permutation transformation
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://w3id.org/cetmd/coord_transforms"}
    )

    type: Optional[TransformationType] = Field(
        default="mapAxis",
        description="""The type of transformation""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "type",
                "domain_of": [
                    "CoordinateTransformation",
                    "Identity",
                    "MapAxis",
                    "Translation",
                    "Scale",
                    "Affine",
                    "Sequence",
                ],
                "ifabsent": "mapAxis",
            }
        },
    )
    mapAxis: Optional[List[AxisNameMapping]] = Field(
        default=None,
        description="""The permutation of the axes""",
        json_schema_extra={
            "linkml_meta": {"alias": "mapAxis", "domain_of": ["MapAxis"]}
        },
    )
    name: Optional[str] = Field(
        default=None,
        description="""The name of the coordinate transformation""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": [
                    "Axis",
                    "CoordinateSystem",
                    "CoordinateTransformation",
                    "Average",
                    "Dataset",
                ],
            }
        },
    )
    input: Optional[str] = Field(
        default=None,
        description="""The source coordinate system name""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "input",
                "domain_of": ["CoordinateTransformation", "ProjectionAlignment"],
            }
        },
    )
    output: Optional[str] = Field(
        default=None,
        description="""The target coordinate system name""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "output",
                "domain_of": ["CoordinateTransformation", "ProjectionAlignment"],
            }
        },
    )


class Translation(CoordinateTransformation):
    """
    A translation transformation
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://w3id.org/cetmd/coord_transforms"}
    )

    type: Optional[TransformationType] = Field(
        default="translation",
        description="""The type of transformation""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "type",
                "domain_of": [
                    "CoordinateTransformation",
                    "Identity",
                    "MapAxis",
                    "Translation",
                    "Scale",
                    "Affine",
                    "Sequence",
                ],
                "ifabsent": "translation",
            }
        },
    )
    translation: Optional[List[float]] = Field(
        default=None,
        description="""The translation vector""",
        json_schema_extra={
            "linkml_meta": {"alias": "translation", "domain_of": ["Translation"]}
        },
    )
    name: Optional[str] = Field(
        default=None,
        description="""The name of the coordinate transformation""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": [
                    "Axis",
                    "CoordinateSystem",
                    "CoordinateTransformation",
                    "Average",
                    "Dataset",
                ],
            }
        },
    )
    input: Optional[str] = Field(
        default=None,
        description="""The source coordinate system name""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "input",
                "domain_of": ["CoordinateTransformation", "ProjectionAlignment"],
            }
        },
    )
    output: Optional[str] = Field(
        default=None,
        description="""The target coordinate system name""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "output",
                "domain_of": ["CoordinateTransformation", "ProjectionAlignment"],
            }
        },
    )


class Scale(CoordinateTransformation):
    """
    A scaling transformation
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://w3id.org/cetmd/coord_transforms"}
    )

    type: Optional[TransformationType] = Field(
        default="scale",
        description="""The type of transformation""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "type",
                "domain_of": [
                    "CoordinateTransformation",
                    "Identity",
                    "MapAxis",
                    "Translation",
                    "Scale",
                    "Affine",
                    "Sequence",
                ],
                "ifabsent": "scale",
            }
        },
    )
    scale: Optional[List[float]] = Field(
        default=None,
        description="""The scaling vector""",
        json_schema_extra={"linkml_meta": {"alias": "scale", "domain_of": ["Scale"]}},
    )
    name: Optional[str] = Field(
        default=None,
        description="""The name of the coordinate transformation""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": [
                    "Axis",
                    "CoordinateSystem",
                    "CoordinateTransformation",
                    "Average",
                    "Dataset",
                ],
            }
        },
    )
    input: Optional[str] = Field(
        default=None,
        description="""The source coordinate system name""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "input",
                "domain_of": ["CoordinateTransformation", "ProjectionAlignment"],
            }
        },
    )
    output: Optional[str] = Field(
        default=None,
        description="""The target coordinate system name""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "output",
                "domain_of": ["CoordinateTransformation", "ProjectionAlignment"],
            }
        },
    )


class Affine(CoordinateTransformation):
    """
    An affine transformation
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://w3id.org/cetmd/coord_transforms"}
    )

    type: Optional[TransformationType] = Field(
        default="affine",
        description="""The type of transformation""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "type",
                "domain_of": [
                    "CoordinateTransformation",
                    "Identity",
                    "MapAxis",
                    "Translation",
                    "Scale",
                    "Affine",
                    "Sequence",
                ],
                "ifabsent": "affine",
            }
        },
    )
    affine: Optional[
        conlist(
            min_length=3,
            max_length=3,
            item_type=conlist(min_length=3, max_length=3, item_type=int),
        )
    ] = Field(
        default=None,
        description="""The affine matrix""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "affine",
                "array": {
                    "dimensions": [
                        {"alias": "exact_card", "exact_cardinality": 3},
                        {"alias": "exact_card", "exact_cardinality": 3},
                    ],
                    "exact_number_dimensions": 2,
                },
                "domain_of": ["Affine"],
            }
        },
    )
    name: Optional[str] = Field(
        default=None,
        description="""The name of the coordinate transformation""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": [
                    "Axis",
                    "CoordinateSystem",
                    "CoordinateTransformation",
                    "Average",
                    "Dataset",
                ],
            }
        },
    )
    input: Optional[str] = Field(
        default=None,
        description="""The source coordinate system name""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "input",
                "domain_of": ["CoordinateTransformation", "ProjectionAlignment"],
            }
        },
    )
    output: Optional[str] = Field(
        default=None,
        description="""The target coordinate system name""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "output",
                "domain_of": ["CoordinateTransformation", "ProjectionAlignment"],
            }
        },
    )


class Sequence(CoordinateTransformation):
    """
    A sequence of transformations
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://w3id.org/cetmd/coord_transforms"}
    )

    type: Optional[TransformationType] = Field(
        default="sequence",
        description="""The type of transformation""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "type",
                "domain_of": [
                    "CoordinateTransformation",
                    "Identity",
                    "MapAxis",
                    "Translation",
                    "Scale",
                    "Affine",
                    "Sequence",
                ],
                "ifabsent": "sequence",
            }
        },
    )
    sequence: Optional[List[CoordinateTransformation]] = Field(
        default=None,
        description="""The sequence of transformations""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "sequence",
                "domain_of": ["Sequence", "ProjectionAlignment"],
            }
        },
    )
    name: Optional[str] = Field(
        default=None,
        description="""The name of the coordinate transformation""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": [
                    "Axis",
                    "CoordinateSystem",
                    "CoordinateTransformation",
                    "Average",
                    "Dataset",
                ],
            }
        },
    )
    input: Optional[str] = Field(
        default=None,
        description="""The source coordinate system name""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "input",
                "domain_of": ["CoordinateTransformation", "ProjectionAlignment"],
            }
        },
    )
    output: Optional[str] = Field(
        default=None,
        description="""The target coordinate system name""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "output",
                "domain_of": ["CoordinateTransformation", "ProjectionAlignment"],
            }
        },
    )


class ProjectionAlignment(Sequence):
    """
    The tomographic alignment for a single projection.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({"from_schema": "CETMDAlignment"})

    input: Optional[str] = Field(
        default=None,
        description="""The source coordinate system name""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "input",
                "domain_of": ["CoordinateTransformation", "ProjectionAlignment"],
            }
        },
    )
    output: Optional[str] = Field(
        default=None,
        description="""The target coordinate system name""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "output",
                "domain_of": ["CoordinateTransformation", "ProjectionAlignment"],
            }
        },
    )
    sequence: Optional[List[Union[Affine, Translation]]] = Field(
        default=None,
        description="""The sequence of transformations""",
        max_length=2,
        json_schema_extra={
            "linkml_meta": {
                "alias": "sequence",
                "any_of": [{"range": "Affine"}, {"range": "Translation"}],
                "domain_of": ["Sequence", "ProjectionAlignment"],
            }
        },
    )
    type: Optional[TransformationType] = Field(
        default="sequence",
        description="""The type of transformation""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "type",
                "domain_of": [
                    "CoordinateTransformation",
                    "Identity",
                    "MapAxis",
                    "Translation",
                    "Scale",
                    "Affine",
                    "Sequence",
                ],
                "ifabsent": "sequence",
            }
        },
    )
    name: Optional[str] = Field(
        default=None,
        description="""The name of the coordinate transformation""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": [
                    "Axis",
                    "CoordinateSystem",
                    "CoordinateTransformation",
                    "Average",
                    "Dataset",
                ],
            }
        },
    )


class Alignment(ConfiguredBaseModel):
    """
    The tomographic alignment for a tilt series.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({"from_schema": "CETMDAlignment"})

    projection_alignments: Optional[List[ProjectionAlignment]] = Field(
        default=None,
        description="""alignment for a specific projection""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "projection_alignments",
                "domain_of": ["Alignment"],
            }
        },
    )


class CTFMetadata(ConfiguredBaseModel):
    """
    A set of CTF patameters for an image.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://w3id.org/cetmd/imageentities"}
    )

    defocus_u: Optional[float] = Field(
        default=None,
        description="""Estimated defocus U for this image in Angstrom, underfocus positive.""",
        json_schema_extra={
            "linkml_meta": {"alias": "defocus_u", "domain_of": ["CTFMetadata"]}
        },
    )
    defocus_v: Optional[float] = Field(
        default=None,
        description="""Estimated defocus V for this image in Angstrom, underfocus positive.""",
        json_schema_extra={
            "linkml_meta": {"alias": "defocus_v", "domain_of": ["CTFMetadata"]}
        },
    )
    defocus_angle: Optional[float] = Field(
        default=None,
        description="""Estimated angle of astigmatism.""",
        json_schema_extra={
            "linkml_meta": {"alias": "defocus_angle", "domain_of": ["CTFMetadata"]}
        },
    )


class AcquisitionMetadataMixin(ConfiguredBaseModel):
    """
    Metadata concerning the acquisition process.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://w3id.org/cetmd/imageentities"}
    )

    nominal_tilt_angle: Optional[float] = Field(
        default=None,
        description="""The tilt angle reported by the microscope""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "nominal_tilt_angle",
                "domain_of": ["AcquisitionMetadataMixin"],
            }
        },
    )
    accumulated_dose: Optional[float] = Field(
        default=None,
        description="""The pre-exposure up to this image in e-/A^2""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "accumulated_dose",
                "domain_of": ["AcquisitionMetadataMixin"],
            }
        },
    )
    ctf_metadata: Optional[CTFMetadata] = Field(
        default=None,
        description="""A set of CTF patameters for an image.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "ctf_metadata",
                "domain_of": ["AcquisitionMetadataMixin"],
            }
        },
    )


class GainFile(Image2D):
    """
    A gain reference file.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://w3id.org/cetmd/imageentities"}
    )

    path: Optional[str] = Field(
        default=None,
        description="""Path to a file.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "path",
                "domain_of": [
                    "GainFile",
                    "DefectFile",
                    "MovieFrame",
                    "MovieStack",
                    "ProjectionImage",
                    "TiltSeries",
                    "Tomogram",
                    "ParticleMap",
                    "Annotation",
                ],
            }
        },
    )
    width: Optional[int] = Field(
        default=None,
        description="""The width of the image (x-axis) in pixels""",
        json_schema_extra={
            "linkml_meta": {"alias": "width", "domain_of": ["Image2D", "Image3D"]}
        },
    )
    height: Optional[int] = Field(
        default=None,
        description="""The height of the image (y-axis) in pixels""",
        json_schema_extra={
            "linkml_meta": {"alias": "height", "domain_of": ["Image2D", "Image3D"]}
        },
    )
    coordinate_systems: Optional[List[CoordinateSystem]] = Field(
        default=None,
        description="""Named coordinate systems for this entity""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "coordinate_systems",
                "domain_of": ["Image2D", "Image3D", "CoordMetaMixin"],
            }
        },
    )
    coordinate_transformations: Optional[List[CoordinateTransformation]] = Field(
        default=None,
        description="""Named coordinate systems for this entity""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "coordinate_transformations",
                "domain_of": ["Image2D", "Image3D", "CoordMetaMixin"],
            }
        },
    )


class DefectFile(Image2D):
    """
    A detector defect file.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://w3id.org/cetmd/imageentities"}
    )

    path: Optional[str] = Field(
        default=None,
        description="""Path to a file.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "path",
                "domain_of": [
                    "GainFile",
                    "DefectFile",
                    "MovieFrame",
                    "MovieStack",
                    "ProjectionImage",
                    "TiltSeries",
                    "Tomogram",
                    "ParticleMap",
                    "Annotation",
                ],
            }
        },
    )
    width: Optional[int] = Field(
        default=None,
        description="""The width of the image (x-axis) in pixels""",
        json_schema_extra={
            "linkml_meta": {"alias": "width", "domain_of": ["Image2D", "Image3D"]}
        },
    )
    height: Optional[int] = Field(
        default=None,
        description="""The height of the image (y-axis) in pixels""",
        json_schema_extra={
            "linkml_meta": {"alias": "height", "domain_of": ["Image2D", "Image3D"]}
        },
    )
    coordinate_systems: Optional[List[CoordinateSystem]] = Field(
        default=None,
        description="""Named coordinate systems for this entity""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "coordinate_systems",
                "domain_of": ["Image2D", "Image3D", "CoordMetaMixin"],
            }
        },
    )
    coordinate_transformations: Optional[List[CoordinateTransformation]] = Field(
        default=None,
        description="""Named coordinate systems for this entity""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "coordinate_transformations",
                "domain_of": ["Image2D", "Image3D", "CoordMetaMixin"],
            }
        },
    )


class MovieFrame(AcquisitionMetadataMixin, Image2D):
    """
    An individual movie frame
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "https://w3id.org/cetmd/imageentities",
            "mixins": ["AcquisitionMetadataMixin"],
        }
    )

    path: Optional[str] = Field(
        default=None,
        description="""Path to a file.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "path",
                "domain_of": [
                    "GainFile",
                    "DefectFile",
                    "MovieFrame",
                    "MovieStack",
                    "ProjectionImage",
                    "TiltSeries",
                    "Tomogram",
                    "ParticleMap",
                    "Annotation",
                ],
            }
        },
    )
    section: Optional[str] = Field(
        default=None,
        description="""0-based section index to the entity inside a stack.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "section",
                "domain_of": ["MovieFrame", "ProjectionImage"],
            }
        },
    )
    nominal_tilt_angle: Optional[float] = Field(
        default=None,
        description="""The tilt angle reported by the microscope""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "nominal_tilt_angle",
                "domain_of": ["AcquisitionMetadataMixin"],
            }
        },
    )
    accumulated_dose: Optional[float] = Field(
        default=None,
        description="""The pre-exposure up to this image in e-/A^2""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "accumulated_dose",
                "domain_of": ["AcquisitionMetadataMixin"],
            }
        },
    )
    ctf_metadata: Optional[CTFMetadata] = Field(
        default=None,
        description="""A set of CTF patameters for an image.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "ctf_metadata",
                "domain_of": ["AcquisitionMetadataMixin"],
            }
        },
    )
    width: Optional[int] = Field(
        default=None,
        description="""The width of the image (x-axis) in pixels""",
        json_schema_extra={
            "linkml_meta": {"alias": "width", "domain_of": ["Image2D", "Image3D"]}
        },
    )
    height: Optional[int] = Field(
        default=None,
        description="""The height of the image (y-axis) in pixels""",
        json_schema_extra={
            "linkml_meta": {"alias": "height", "domain_of": ["Image2D", "Image3D"]}
        },
    )
    coordinate_systems: Optional[List[CoordinateSystem]] = Field(
        default=None,
        description="""Named coordinate systems for this entity""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "coordinate_systems",
                "domain_of": ["Image2D", "Image3D", "CoordMetaMixin"],
            }
        },
    )
    coordinate_transformations: Optional[List[CoordinateTransformation]] = Field(
        default=None,
        description="""Named coordinate systems for this entity""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "coordinate_transformations",
                "domain_of": ["Image2D", "Image3D", "CoordMetaMixin"],
            }
        },
    )


class MovieStack(ConfiguredBaseModel):
    """
    A stack of movie frames.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://w3id.org/cetmd/imageentities"}
    )

    images: Optional[List[MovieFrame]] = Field(
        default=None,
        description="""The movie frames in the stack""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "images",
                "domain_of": [
                    "ImageStack2D",
                    "ImageStack3D",
                    "MovieStack",
                    "TiltSeries",
                ],
            }
        },
    )
    path: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "path",
                "domain_of": [
                    "GainFile",
                    "DefectFile",
                    "MovieFrame",
                    "MovieStack",
                    "ProjectionImage",
                    "TiltSeries",
                    "Tomogram",
                    "ParticleMap",
                    "Annotation",
                ],
            }
        },
    )


class ProjectionImage(AcquisitionMetadataMixin, Image2D):
    """
    A projection image.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "https://w3id.org/cetmd/imageentities",
            "mixins": ["AcquisitionMetadataMixin"],
        }
    )

    path: Optional[str] = Field(
        default=None,
        description="""Path to a file.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "path",
                "domain_of": [
                    "GainFile",
                    "DefectFile",
                    "MovieFrame",
                    "MovieStack",
                    "ProjectionImage",
                    "TiltSeries",
                    "Tomogram",
                    "ParticleMap",
                    "Annotation",
                ],
            }
        },
    )
    section: Optional[str] = Field(
        default=None,
        description="""0-based section index to the entity inside a stack.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "section",
                "domain_of": ["MovieFrame", "ProjectionImage"],
            }
        },
    )
    nominal_tilt_angle: Optional[float] = Field(
        default=None,
        description="""The tilt angle reported by the microscope""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "nominal_tilt_angle",
                "domain_of": ["AcquisitionMetadataMixin"],
            }
        },
    )
    accumulated_dose: Optional[float] = Field(
        default=None,
        description="""The pre-exposure up to this image in e-/A^2""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "accumulated_dose",
                "domain_of": ["AcquisitionMetadataMixin"],
            }
        },
    )
    ctf_metadata: Optional[CTFMetadata] = Field(
        default=None,
        description="""A set of CTF patameters for an image.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "ctf_metadata",
                "domain_of": ["AcquisitionMetadataMixin"],
            }
        },
    )
    width: Optional[int] = Field(
        default=None,
        description="""The width of the image (x-axis) in pixels""",
        json_schema_extra={
            "linkml_meta": {"alias": "width", "domain_of": ["Image2D", "Image3D"]}
        },
    )
    height: Optional[int] = Field(
        default=None,
        description="""The height of the image (y-axis) in pixels""",
        json_schema_extra={
            "linkml_meta": {"alias": "height", "domain_of": ["Image2D", "Image3D"]}
        },
    )
    coordinate_systems: Optional[List[CoordinateSystem]] = Field(
        default=None,
        description="""Named coordinate systems for this entity""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "coordinate_systems",
                "domain_of": ["Image2D", "Image3D", "CoordMetaMixin"],
            }
        },
    )
    coordinate_transformations: Optional[List[CoordinateTransformation]] = Field(
        default=None,
        description="""Named coordinate systems for this entity""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "coordinate_transformations",
                "domain_of": ["Image2D", "Image3D", "CoordMetaMixin"],
            }
        },
    )


class MovieStackSeries(ConfiguredBaseModel):
    """
    A group of movie stacks that belong to a single tilt series.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://w3id.org/cetmd/imageentities"}
    )

    stacks: Optional[List[MovieStack]] = Field(
        default=None,
        description="""The movie stacks.""",
        json_schema_extra={
            "linkml_meta": {"alias": "stacks", "domain_of": ["MovieStackSeries"]}
        },
    )


class TiltSeries(ConfiguredBaseModel):
    """
    A stack of projection images.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://w3id.org/cetmd/imageentities"}
    )

    images: Optional[List[ProjectionImage]] = Field(
        default=None,
        description="""The projections in the stack""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "images",
                "domain_of": [
                    "ImageStack2D",
                    "ImageStack3D",
                    "MovieStack",
                    "TiltSeries",
                ],
            }
        },
    )
    path: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "path",
                "domain_of": [
                    "GainFile",
                    "DefectFile",
                    "MovieFrame",
                    "MovieStack",
                    "ProjectionImage",
                    "TiltSeries",
                    "Tomogram",
                    "ParticleMap",
                    "Annotation",
                ],
            }
        },
    )


class SubProjectionImage(ProjectionImage):
    """
    A croppecd projection image.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://w3id.org/cetmd/imageentities"}
    )

    particle_index: Optional[int] = Field(
        default=None,
        description="""Index of a particle inside a tomogram.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "particle_index",
                "domain_of": ["SubProjectionImage"],
            }
        },
    )
    path: Optional[str] = Field(
        default=None,
        description="""Path to a file.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "path",
                "domain_of": [
                    "GainFile",
                    "DefectFile",
                    "MovieFrame",
                    "MovieStack",
                    "ProjectionImage",
                    "TiltSeries",
                    "Tomogram",
                    "ParticleMap",
                    "Annotation",
                ],
            }
        },
    )
    section: Optional[str] = Field(
        default=None,
        description="""0-based section index to the entity inside a stack.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "section",
                "domain_of": ["MovieFrame", "ProjectionImage"],
            }
        },
    )
    nominal_tilt_angle: Optional[float] = Field(
        default=None,
        description="""The tilt angle reported by the microscope""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "nominal_tilt_angle",
                "domain_of": ["AcquisitionMetadataMixin"],
            }
        },
    )
    accumulated_dose: Optional[float] = Field(
        default=None,
        description="""The pre-exposure up to this image in e-/A^2""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "accumulated_dose",
                "domain_of": ["AcquisitionMetadataMixin"],
            }
        },
    )
    ctf_metadata: Optional[CTFMetadata] = Field(
        default=None,
        description="""A set of CTF patameters for an image.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "ctf_metadata",
                "domain_of": ["AcquisitionMetadataMixin"],
            }
        },
    )
    width: Optional[int] = Field(
        default=None,
        description="""The width of the image (x-axis) in pixels""",
        json_schema_extra={
            "linkml_meta": {"alias": "width", "domain_of": ["Image2D", "Image3D"]}
        },
    )
    height: Optional[int] = Field(
        default=None,
        description="""The height of the image (y-axis) in pixels""",
        json_schema_extra={
            "linkml_meta": {"alias": "height", "domain_of": ["Image2D", "Image3D"]}
        },
    )
    coordinate_systems: Optional[List[CoordinateSystem]] = Field(
        default=None,
        description="""Named coordinate systems for this entity""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "coordinate_systems",
                "domain_of": ["Image2D", "Image3D", "CoordMetaMixin"],
            }
        },
    )
    coordinate_transformations: Optional[List[CoordinateTransformation]] = Field(
        default=None,
        description="""Named coordinate systems for this entity""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "coordinate_transformations",
                "domain_of": ["Image2D", "Image3D", "CoordMetaMixin"],
            }
        },
    )


class Tomogram(Image3D):
    """
    A 3D tomogram.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://w3id.org/cetmd/imageentities"}
    )

    path: Optional[str] = Field(
        default=None,
        description="""Path to a file.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "path",
                "domain_of": [
                    "GainFile",
                    "DefectFile",
                    "MovieFrame",
                    "MovieStack",
                    "ProjectionImage",
                    "TiltSeries",
                    "Tomogram",
                    "ParticleMap",
                    "Annotation",
                ],
            }
        },
    )
    width: Optional[int] = Field(
        default=None,
        description="""The width of the image (x-axis) in pixels""",
        json_schema_extra={
            "linkml_meta": {"alias": "width", "domain_of": ["Image2D", "Image3D"]}
        },
    )
    height: Optional[int] = Field(
        default=None,
        description="""The height of the image (y-axis) in pixels""",
        json_schema_extra={
            "linkml_meta": {"alias": "height", "domain_of": ["Image2D", "Image3D"]}
        },
    )
    depth: Optional[int] = Field(
        default=None,
        description="""The depth of the image (z-axis) in pixels""",
        json_schema_extra={"linkml_meta": {"alias": "depth", "domain_of": ["Image3D"]}},
    )
    coordinate_systems: Optional[List[CoordinateSystem]] = Field(
        default=None,
        description="""Named coordinate systems for this entity""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "coordinate_systems",
                "domain_of": ["Image2D", "Image3D", "CoordMetaMixin"],
            }
        },
    )
    coordinate_transformations: Optional[List[CoordinateTransformation]] = Field(
        default=None,
        description="""Named coordinate systems for this entity""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "coordinate_transformations",
                "domain_of": ["Image2D", "Image3D", "CoordMetaMixin"],
            }
        },
    )


class ParticleMap(Image3D):
    """
    A 3D particle density map.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://w3id.org/cetmd/imageentities"}
    )

    path: Optional[str] = Field(
        default=None,
        description="""Path to a file.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "path",
                "domain_of": [
                    "GainFile",
                    "DefectFile",
                    "MovieFrame",
                    "MovieStack",
                    "ProjectionImage",
                    "TiltSeries",
                    "Tomogram",
                    "ParticleMap",
                    "Annotation",
                ],
            }
        },
    )
    width: Optional[int] = Field(
        default=None,
        description="""The width of the image (x-axis) in pixels""",
        json_schema_extra={
            "linkml_meta": {"alias": "width", "domain_of": ["Image2D", "Image3D"]}
        },
    )
    height: Optional[int] = Field(
        default=None,
        description="""The height of the image (y-axis) in pixels""",
        json_schema_extra={
            "linkml_meta": {"alias": "height", "domain_of": ["Image2D", "Image3D"]}
        },
    )
    depth: Optional[int] = Field(
        default=None,
        description="""The depth of the image (z-axis) in pixels""",
        json_schema_extra={"linkml_meta": {"alias": "depth", "domain_of": ["Image3D"]}},
    )
    coordinate_systems: Optional[List[CoordinateSystem]] = Field(
        default=None,
        description="""Named coordinate systems for this entity""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "coordinate_systems",
                "domain_of": ["Image2D", "Image3D", "CoordMetaMixin"],
            }
        },
    )
    coordinate_transformations: Optional[List[CoordinateTransformation]] = Field(
        default=None,
        description="""Named coordinate systems for this entity""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "coordinate_transformations",
                "domain_of": ["Image2D", "Image3D", "CoordMetaMixin"],
            }
        },
    )


class CoordMetaMixin(ConfiguredBaseModel):
    """
    Coordinate system mixins for annotations.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://w3id.org/cetmd/annotation"}
    )

    coordinate_systems: Optional[List[CoordinateSystem]] = Field(
        default=None,
        description="""Named coordinate systems for this entity""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "coordinate_systems",
                "domain_of": ["Image2D", "Image3D", "CoordMetaMixin"],
            }
        },
    )
    coordinate_transformations: Optional[List[CoordinateTransformation]] = Field(
        default=None,
        description="""Named coordinate systems for this entity""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "coordinate_transformations",
                "domain_of": ["Image2D", "Image3D", "CoordMetaMixin"],
            }
        },
    )


class Annotation(ConfiguredBaseModel):
    """
    A primitive annotation.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://w3id.org/cetmd/annotation"}
    )

    path: Optional[str] = Field(
        default=None,
        description="""Path to a file.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "path",
                "domain_of": [
                    "GainFile",
                    "DefectFile",
                    "MovieFrame",
                    "MovieStack",
                    "ProjectionImage",
                    "TiltSeries",
                    "Tomogram",
                    "ParticleMap",
                    "Annotation",
                ],
            }
        },
    )


class SegmentationMask2D(Annotation, Image2D):
    """
    An annotation image with categorical labels.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://w3id.org/cetmd/annotation", "mixins": ["Image2D"]}
    )

    width: Optional[int] = Field(
        default=None,
        description="""The width of the image (x-axis) in pixels""",
        json_schema_extra={
            "linkml_meta": {"alias": "width", "domain_of": ["Image2D", "Image3D"]}
        },
    )
    height: Optional[int] = Field(
        default=None,
        description="""The height of the image (y-axis) in pixels""",
        json_schema_extra={
            "linkml_meta": {"alias": "height", "domain_of": ["Image2D", "Image3D"]}
        },
    )
    coordinate_systems: Optional[List[CoordinateSystem]] = Field(
        default=None,
        description="""Named coordinate systems for this entity""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "coordinate_systems",
                "domain_of": ["Image2D", "Image3D", "CoordMetaMixin"],
            }
        },
    )
    coordinate_transformations: Optional[List[CoordinateTransformation]] = Field(
        default=None,
        description="""Named coordinate systems for this entity""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "coordinate_transformations",
                "domain_of": ["Image2D", "Image3D", "CoordMetaMixin"],
            }
        },
    )
    path: Optional[str] = Field(
        default=None,
        description="""Path to a file.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "path",
                "domain_of": [
                    "GainFile",
                    "DefectFile",
                    "MovieFrame",
                    "MovieStack",
                    "ProjectionImage",
                    "TiltSeries",
                    "Tomogram",
                    "ParticleMap",
                    "Annotation",
                ],
            }
        },
    )


class SegmentationMask3D(Annotation, Image3D):
    """
    An annotation volume with categorical labels.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://w3id.org/cetmd/annotation", "mixins": ["Image3D"]}
    )

    width: Optional[int] = Field(
        default=None,
        description="""The width of the image (x-axis) in pixels""",
        json_schema_extra={
            "linkml_meta": {"alias": "width", "domain_of": ["Image2D", "Image3D"]}
        },
    )
    height: Optional[int] = Field(
        default=None,
        description="""The height of the image (y-axis) in pixels""",
        json_schema_extra={
            "linkml_meta": {"alias": "height", "domain_of": ["Image2D", "Image3D"]}
        },
    )
    depth: Optional[int] = Field(
        default=None,
        description="""The depth of the image (z-axis) in pixels""",
        json_schema_extra={"linkml_meta": {"alias": "depth", "domain_of": ["Image3D"]}},
    )
    coordinate_systems: Optional[List[CoordinateSystem]] = Field(
        default=None,
        description="""Named coordinate systems for this entity""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "coordinate_systems",
                "domain_of": ["Image2D", "Image3D", "CoordMetaMixin"],
            }
        },
    )
    coordinate_transformations: Optional[List[CoordinateTransformation]] = Field(
        default=None,
        description="""Named coordinate systems for this entity""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "coordinate_transformations",
                "domain_of": ["Image2D", "Image3D", "CoordMetaMixin"],
            }
        },
    )
    path: Optional[str] = Field(
        default=None,
        description="""Path to a file.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "path",
                "domain_of": [
                    "GainFile",
                    "DefectFile",
                    "MovieFrame",
                    "MovieStack",
                    "ProjectionImage",
                    "TiltSeries",
                    "Tomogram",
                    "ParticleMap",
                    "Annotation",
                ],
            }
        },
    )


class ProbabilityMap2D(Annotation, Image2D):
    """
    An annotation image with real-valued labels.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://w3id.org/cetmd/annotation", "mixins": ["Image2D"]}
    )

    width: Optional[int] = Field(
        default=None,
        description="""The width of the image (x-axis) in pixels""",
        json_schema_extra={
            "linkml_meta": {"alias": "width", "domain_of": ["Image2D", "Image3D"]}
        },
    )
    height: Optional[int] = Field(
        default=None,
        description="""The height of the image (y-axis) in pixels""",
        json_schema_extra={
            "linkml_meta": {"alias": "height", "domain_of": ["Image2D", "Image3D"]}
        },
    )
    coordinate_systems: Optional[List[CoordinateSystem]] = Field(
        default=None,
        description="""Named coordinate systems for this entity""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "coordinate_systems",
                "domain_of": ["Image2D", "Image3D", "CoordMetaMixin"],
            }
        },
    )
    coordinate_transformations: Optional[List[CoordinateTransformation]] = Field(
        default=None,
        description="""Named coordinate systems for this entity""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "coordinate_transformations",
                "domain_of": ["Image2D", "Image3D", "CoordMetaMixin"],
            }
        },
    )
    path: Optional[str] = Field(
        default=None,
        description="""Path to a file.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "path",
                "domain_of": [
                    "GainFile",
                    "DefectFile",
                    "MovieFrame",
                    "MovieStack",
                    "ProjectionImage",
                    "TiltSeries",
                    "Tomogram",
                    "ParticleMap",
                    "Annotation",
                ],
            }
        },
    )


class ProbabilityMap3D(Annotation, Image3D):
    """
    An annotation volume with real-valued labels.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://w3id.org/cetmd/annotation", "mixins": ["Image3D"]}
    )

    width: Optional[int] = Field(
        default=None,
        description="""The width of the image (x-axis) in pixels""",
        json_schema_extra={
            "linkml_meta": {"alias": "width", "domain_of": ["Image2D", "Image3D"]}
        },
    )
    height: Optional[int] = Field(
        default=None,
        description="""The height of the image (y-axis) in pixels""",
        json_schema_extra={
            "linkml_meta": {"alias": "height", "domain_of": ["Image2D", "Image3D"]}
        },
    )
    depth: Optional[int] = Field(
        default=None,
        description="""The depth of the image (z-axis) in pixels""",
        json_schema_extra={"linkml_meta": {"alias": "depth", "domain_of": ["Image3D"]}},
    )
    coordinate_systems: Optional[List[CoordinateSystem]] = Field(
        default=None,
        description="""Named coordinate systems for this entity""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "coordinate_systems",
                "domain_of": ["Image2D", "Image3D", "CoordMetaMixin"],
            }
        },
    )
    coordinate_transformations: Optional[List[CoordinateTransformation]] = Field(
        default=None,
        description="""Named coordinate systems for this entity""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "coordinate_transformations",
                "domain_of": ["Image2D", "Image3D", "CoordMetaMixin"],
            }
        },
    )
    path: Optional[str] = Field(
        default=None,
        description="""Path to a file.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "path",
                "domain_of": [
                    "GainFile",
                    "DefectFile",
                    "MovieFrame",
                    "MovieStack",
                    "ProjectionImage",
                    "TiltSeries",
                    "Tomogram",
                    "ParticleMap",
                    "Annotation",
                ],
            }
        },
    )


class PointSet2D(Annotation, CoordMetaMixin):
    """
    A set of 2D point annotations.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "https://w3id.org/cetmd/annotation",
            "mixins": ["CoordMetaMixin"],
        }
    )

    origin2D: Optional[
        conlist(
            min_length=1, item_type=conlist(min_length=2, max_length=2, item_type=float)
        )
    ] = Field(
        default=None,
        description="""Location on a 2D image (Nx2).""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "origin2D",
                "array": {
                    "dimensions": [
                        {"alias": "N", "minimum_cardinality": 1},
                        {"alias": "xy", "exact_cardinality": 2},
                    ],
                    "exact_number_dimensions": 2,
                },
                "domain_of": ["PointSet2D", "PointVectorSet2D", "PointMatrixSet2D"],
            }
        },
    )
    coordinate_systems: Optional[List[CoordinateSystem]] = Field(
        default=None,
        description="""Named coordinate systems for this entity""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "coordinate_systems",
                "domain_of": ["Image2D", "Image3D", "CoordMetaMixin"],
            }
        },
    )
    coordinate_transformations: Optional[List[CoordinateTransformation]] = Field(
        default=None,
        description="""Named coordinate systems for this entity""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "coordinate_transformations",
                "domain_of": ["Image2D", "Image3D", "CoordMetaMixin"],
            }
        },
    )
    path: Optional[str] = Field(
        default=None,
        description="""Path to a file.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "path",
                "domain_of": [
                    "GainFile",
                    "DefectFile",
                    "MovieFrame",
                    "MovieStack",
                    "ProjectionImage",
                    "TiltSeries",
                    "Tomogram",
                    "ParticleMap",
                    "Annotation",
                ],
            }
        },
    )


class PointSet3D(Annotation, CoordMetaMixin):
    """
    A set of 3D point annotations.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "https://w3id.org/cetmd/annotation",
            "mixins": ["CoordMetaMixin"],
        }
    )

    origin3D: Optional[
        conlist(
            min_length=1, item_type=conlist(min_length=3, max_length=3, item_type=float)
        )
    ] = Field(
        default=None,
        description="""Location on a 3D image (Nx3).""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "origin3D",
                "array": {
                    "dimensions": [
                        {"alias": "N", "minimum_cardinality": 1},
                        {"alias": "xyz", "exact_cardinality": 3},
                    ],
                    "exact_number_dimensions": 2,
                },
                "domain_of": ["PointSet3D", "PointVectorSet3D", "PointMatrixSet3D"],
            }
        },
    )
    coordinate_systems: Optional[List[CoordinateSystem]] = Field(
        default=None,
        description="""Named coordinate systems for this entity""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "coordinate_systems",
                "domain_of": ["Image2D", "Image3D", "CoordMetaMixin"],
            }
        },
    )
    coordinate_transformations: Optional[List[CoordinateTransformation]] = Field(
        default=None,
        description="""Named coordinate systems for this entity""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "coordinate_transformations",
                "domain_of": ["Image2D", "Image3D", "CoordMetaMixin"],
            }
        },
    )
    path: Optional[str] = Field(
        default=None,
        description="""Path to a file.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "path",
                "domain_of": [
                    "GainFile",
                    "DefectFile",
                    "MovieFrame",
                    "MovieStack",
                    "ProjectionImage",
                    "TiltSeries",
                    "Tomogram",
                    "ParticleMap",
                    "Annotation",
                ],
            }
        },
    )


class PointVectorSet2D(Annotation, CoordMetaMixin):
    """
    A set of 2D points with an associated direction vector.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "https://w3id.org/cetmd/annotation",
            "mixins": ["CoordMetaMixin"],
        }
    )

    origin2D: Optional[
        conlist(
            min_length=1, item_type=conlist(min_length=2, max_length=2, item_type=float)
        )
    ] = Field(
        default=None,
        description="""Location on a 2D image (Nx2).""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "origin2D",
                "array": {
                    "dimensions": [
                        {"alias": "N", "minimum_cardinality": 1},
                        {"alias": "xy", "exact_cardinality": 2},
                    ],
                    "exact_number_dimensions": 2,
                },
                "domain_of": ["PointSet2D", "PointVectorSet2D", "PointMatrixSet2D"],
            }
        },
    )
    vector2D: Optional[
        conlist(
            min_length=1, item_type=conlist(min_length=2, max_length=2, item_type=float)
        )
    ] = Field(
        default=None,
        description="""Orientation vector associated with a point on a 2D image (Nx2).""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "vector2D",
                "array": {
                    "dimensions": [
                        {"alias": "N", "minimum_cardinality": 1},
                        {"alias": "xy", "exact_cardinality": 2},
                    ],
                    "exact_number_dimensions": 2,
                },
                "domain_of": ["PointVectorSet2D"],
            }
        },
    )
    coordinate_systems: Optional[List[CoordinateSystem]] = Field(
        default=None,
        description="""Named coordinate systems for this entity""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "coordinate_systems",
                "domain_of": ["Image2D", "Image3D", "CoordMetaMixin"],
            }
        },
    )
    coordinate_transformations: Optional[List[CoordinateTransformation]] = Field(
        default=None,
        description="""Named coordinate systems for this entity""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "coordinate_transformations",
                "domain_of": ["Image2D", "Image3D", "CoordMetaMixin"],
            }
        },
    )
    path: Optional[str] = Field(
        default=None,
        description="""Path to a file.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "path",
                "domain_of": [
                    "GainFile",
                    "DefectFile",
                    "MovieFrame",
                    "MovieStack",
                    "ProjectionImage",
                    "TiltSeries",
                    "Tomogram",
                    "ParticleMap",
                    "Annotation",
                ],
            }
        },
    )


class PointVectorSet3D(Annotation, CoordMetaMixin):
    """
    A set of 3D points with an associated direction vector.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "https://w3id.org/cetmd/annotation",
            "mixins": ["CoordMetaMixin"],
        }
    )

    origin3D: Optional[
        conlist(
            min_length=1, item_type=conlist(min_length=3, max_length=3, item_type=float)
        )
    ] = Field(
        default=None,
        description="""Location on a 3D image (Nx3).""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "origin3D",
                "array": {
                    "dimensions": [
                        {"alias": "N", "minimum_cardinality": 1},
                        {"alias": "xyz", "exact_cardinality": 3},
                    ],
                    "exact_number_dimensions": 2,
                },
                "domain_of": ["PointSet3D", "PointVectorSet3D", "PointMatrixSet3D"],
            }
        },
    )
    vector3D: Optional[
        conlist(
            min_length=1, item_type=conlist(min_length=3, max_length=3, item_type=float)
        )
    ] = Field(
        default=None,
        description="""Orientation vector associated with a point on a 3D image (Nx3).""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "vector3D",
                "array": {
                    "dimensions": [
                        {"alias": "N", "minimum_cardinality": 1},
                        {"alias": "xyz", "exact_cardinality": 3},
                    ],
                    "exact_number_dimensions": 2,
                },
                "domain_of": ["PointVectorSet3D"],
            }
        },
    )
    coordinate_systems: Optional[List[CoordinateSystem]] = Field(
        default=None,
        description="""Named coordinate systems for this entity""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "coordinate_systems",
                "domain_of": ["Image2D", "Image3D", "CoordMetaMixin"],
            }
        },
    )
    coordinate_transformations: Optional[List[CoordinateTransformation]] = Field(
        default=None,
        description="""Named coordinate systems for this entity""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "coordinate_transformations",
                "domain_of": ["Image2D", "Image3D", "CoordMetaMixin"],
            }
        },
    )
    path: Optional[str] = Field(
        default=None,
        description="""Path to a file.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "path",
                "domain_of": [
                    "GainFile",
                    "DefectFile",
                    "MovieFrame",
                    "MovieStack",
                    "ProjectionImage",
                    "TiltSeries",
                    "Tomogram",
                    "ParticleMap",
                    "Annotation",
                ],
            }
        },
    )


class PointMatrixSet2D(Annotation, CoordMetaMixin):
    """
    A set of 2D points with an associated rotation matrix.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "https://w3id.org/cetmd/annotation",
            "mixins": ["CoordMetaMixin"],
        }
    )

    origin2D: Optional[
        conlist(
            min_length=1, item_type=conlist(min_length=2, max_length=2, item_type=float)
        )
    ] = Field(
        default=None,
        description="""Location on a 2D image (Nx2).""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "origin2D",
                "array": {
                    "dimensions": [
                        {"alias": "N", "minimum_cardinality": 1},
                        {"alias": "xy", "exact_cardinality": 2},
                    ],
                    "exact_number_dimensions": 2,
                },
                "domain_of": ["PointSet2D", "PointVectorSet2D", "PointMatrixSet2D"],
            }
        },
    )
    matrix2D: Optional[
        conlist(
            min_length=1,
            item_type=conlist(
                min_length=2,
                max_length=2,
                item_type=conlist(min_length=2, max_length=2, item_type=float),
            ),
        )
    ] = Field(
        default=None,
        description="""Rotation matrix associated with a point on a 2D image (Nx2x2).""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "matrix2D",
                "array": {
                    "dimensions": [
                        {"alias": "N", "minimum_cardinality": 1},
                        {"alias": "xy", "exact_cardinality": 2},
                        {"alias": "xy", "exact_cardinality": 2},
                    ],
                    "exact_number_dimensions": 3,
                },
                "domain_of": ["PointMatrixSet2D"],
            }
        },
    )
    coordinate_systems: Optional[List[CoordinateSystem]] = Field(
        default=None,
        description="""Named coordinate systems for this entity""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "coordinate_systems",
                "domain_of": ["Image2D", "Image3D", "CoordMetaMixin"],
            }
        },
    )
    coordinate_transformations: Optional[List[CoordinateTransformation]] = Field(
        default=None,
        description="""Named coordinate systems for this entity""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "coordinate_transformations",
                "domain_of": ["Image2D", "Image3D", "CoordMetaMixin"],
            }
        },
    )
    path: Optional[str] = Field(
        default=None,
        description="""Path to a file.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "path",
                "domain_of": [
                    "GainFile",
                    "DefectFile",
                    "MovieFrame",
                    "MovieStack",
                    "ProjectionImage",
                    "TiltSeries",
                    "Tomogram",
                    "ParticleMap",
                    "Annotation",
                ],
            }
        },
    )


class PointMatrixSet3D(Annotation, CoordMetaMixin):
    """
    A set of 3D points with an associated rotation matrix.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "https://w3id.org/cetmd/annotation",
            "mixins": ["CoordMetaMixin"],
        }
    )

    origin3D: Optional[
        conlist(
            min_length=1, item_type=conlist(min_length=3, max_length=3, item_type=float)
        )
    ] = Field(
        default=None,
        description="""Location on a 3D image (Nx3).""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "origin3D",
                "array": {
                    "dimensions": [
                        {"alias": "N", "minimum_cardinality": 1},
                        {"alias": "xyz", "exact_cardinality": 3},
                    ],
                    "exact_number_dimensions": 2,
                },
                "domain_of": ["PointSet3D", "PointVectorSet3D", "PointMatrixSet3D"],
            }
        },
    )
    matrix3D: Optional[
        conlist(
            min_length=1,
            item_type=conlist(
                min_length=3,
                max_length=3,
                item_type=conlist(min_length=3, max_length=3, item_type=float),
            ),
        )
    ] = Field(
        default=None,
        description="""Rotation matrix associated with a point on a 3D image (Nx3x3).""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "matrix3D",
                "array": {
                    "dimensions": [
                        {"alias": "N", "minimum_cardinality": 1},
                        {"alias": "xyz", "exact_cardinality": 3},
                        {"alias": "xyz", "exact_cardinality": 3},
                    ],
                    "exact_number_dimensions": 3,
                },
                "domain_of": ["PointMatrixSet3D"],
            }
        },
    )
    coordinate_systems: Optional[List[CoordinateSystem]] = Field(
        default=None,
        description="""Named coordinate systems for this entity""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "coordinate_systems",
                "domain_of": ["Image2D", "Image3D", "CoordMetaMixin"],
            }
        },
    )
    coordinate_transformations: Optional[List[CoordinateTransformation]] = Field(
        default=None,
        description="""Named coordinate systems for this entity""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "coordinate_transformations",
                "domain_of": ["Image2D", "Image3D", "CoordMetaMixin"],
            }
        },
    )
    path: Optional[str] = Field(
        default=None,
        description="""Path to a file.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "path",
                "domain_of": [
                    "GainFile",
                    "DefectFile",
                    "MovieFrame",
                    "MovieStack",
                    "ProjectionImage",
                    "TiltSeries",
                    "Tomogram",
                    "ParticleMap",
                    "Annotation",
                ],
            }
        },
    )


class TriMesh(Annotation, CoordMetaMixin):
    """
    A mesh annotation.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "https://w3id.org/cetmd/annotation",
            "mixins": ["CoordMetaMixin"],
        }
    )

    coordinate_systems: Optional[List[CoordinateSystem]] = Field(
        default=None,
        description="""Named coordinate systems for this entity""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "coordinate_systems",
                "domain_of": ["Image2D", "Image3D", "CoordMetaMixin"],
            }
        },
    )
    coordinate_transformations: Optional[List[CoordinateTransformation]] = Field(
        default=None,
        description="""Named coordinate systems for this entity""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "coordinate_transformations",
                "domain_of": ["Image2D", "Image3D", "CoordMetaMixin"],
            }
        },
    )
    path: Optional[str] = Field(
        default=None,
        description="""Path to a file.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "path",
                "domain_of": [
                    "GainFile",
                    "DefectFile",
                    "MovieFrame",
                    "MovieStack",
                    "ProjectionImage",
                    "TiltSeries",
                    "Tomogram",
                    "ParticleMap",
                    "Annotation",
                ],
            }
        },
    )


class Region(ConfiguredBaseModel):
    """
    Raw data (movie stacks) and derived data (tilt series, tomograms, annotations) from a single region of a specimen.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://w3id.org/cetmd/entities"}
    )

    movie_stack_collections: Optional[List[MovieStackCollection]] = Field(
        default=None,
        description="""The movie stack""",
        json_schema_extra={
            "linkml_meta": {"alias": "movie_stack_collections", "domain_of": ["Region"]}
        },
    )
    tilt_series: Optional[List[TiltSeries]] = Field(
        default=None,
        description="""The tilt series""",
        json_schema_extra={
            "linkml_meta": {"alias": "tilt_series", "domain_of": ["Region"]}
        },
    )
    alignments: Optional[List[Alignment]] = Field(
        default=None,
        description="""The alignments""",
        json_schema_extra={
            "linkml_meta": {"alias": "alignments", "domain_of": ["Region"]}
        },
    )
    tomograms: Optional[List[Tomogram]] = Field(
        default=None,
        description="""The tomograms""",
        json_schema_extra={
            "linkml_meta": {"alias": "tomograms", "domain_of": ["Region"]}
        },
    )
    annotations: Optional[List[Annotation]] = Field(
        default=None,
        description="""The annotations for this region""",
        json_schema_extra={
            "linkml_meta": {"alias": "annotations", "domain_of": ["Region", "Average"]}
        },
    )


class Average(ConfiguredBaseModel):
    """
    A particle averaging experiment.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://w3id.org/cetmd/entities"}
    )

    name: Optional[str] = Field(
        default=None,
        description="""The name of the averaging experiment.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": [
                    "Axis",
                    "CoordinateSystem",
                    "CoordinateTransformation",
                    "Average",
                    "Dataset",
                ],
            }
        },
    )
    particle_maps: Optional[List[ParticleMap]] = Field(
        default=None,
        description="""The particle maps""",
        json_schema_extra={
            "linkml_meta": {"alias": "particle_maps", "domain_of": ["Average"]}
        },
    )
    annotations: Optional[List[Annotation]] = Field(
        default=None,
        description="""The annotations""",
        json_schema_extra={
            "linkml_meta": {"alias": "annotations", "domain_of": ["Region", "Average"]}
        },
    )


class MovieStackCollection(ConfiguredBaseModel):
    """
    A collection of movie stacks using the same gain and defect files.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://w3id.org/cetmd/entities"}
    )

    movie_stacks: Optional[List[MovieStackSeries]] = Field(
        default=None,
        description="""The movie stacks in the collection""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "movie_stacks",
                "domain_of": ["MovieStackCollection"],
            }
        },
    )
    GainFile: Optional[GainFile] = Field(
        default=None,
        description="""The gain file for the movie stacks""",
        json_schema_extra={
            "linkml_meta": {"alias": "GainFile", "domain_of": ["MovieStackCollection"]}
        },
    )
    DefectFile: Optional[DefectFile] = Field(
        default=None,
        description="""The defect file for the movie stacks""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "DefectFile",
                "domain_of": ["MovieStackCollection"],
            }
        },
    )


class Dataset(ConfiguredBaseModel):
    """
    A dataset
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://w3id.org/cetmd/entities"}
    )

    name: Optional[str] = Field(
        default=None,
        description="""The name of the dataset""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": [
                    "Axis",
                    "CoordinateSystem",
                    "CoordinateTransformation",
                    "Average",
                    "Dataset",
                ],
            }
        },
    )
    regions: Optional[List[Region]] = Field(
        default=None,
        description="""The regions in the dataset""",
        json_schema_extra={
            "linkml_meta": {"alias": "regions", "domain_of": ["Dataset"]}
        },
    )
    averages: Optional[List[Average]] = Field(
        default=None,
        description="""The averages in the dataset""",
        json_schema_extra={
            "linkml_meta": {"alias": "averages", "domain_of": ["Dataset"]}
        },
    )


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
Image2D.model_rebuild()
Image3D.model_rebuild()
ImageStack2D.model_rebuild()
ImageStack3D.model_rebuild()
Axis.model_rebuild()
CoordinateSystem.model_rebuild()
CoordinateTransformation.model_rebuild()
Identity.model_rebuild()
AxisNameMapping.model_rebuild()
MapAxis.model_rebuild()
Translation.model_rebuild()
Scale.model_rebuild()
Affine.model_rebuild()
Sequence.model_rebuild()
ProjectionAlignment.model_rebuild()
Alignment.model_rebuild()
CTFMetadata.model_rebuild()
AcquisitionMetadataMixin.model_rebuild()
GainFile.model_rebuild()
DefectFile.model_rebuild()
MovieFrame.model_rebuild()
MovieStack.model_rebuild()
ProjectionImage.model_rebuild()
MovieStackSeries.model_rebuild()
TiltSeries.model_rebuild()
SubProjectionImage.model_rebuild()
Tomogram.model_rebuild()
ParticleMap.model_rebuild()
CoordMetaMixin.model_rebuild()
Annotation.model_rebuild()
SegmentationMask2D.model_rebuild()
SegmentationMask3D.model_rebuild()
ProbabilityMap2D.model_rebuild()
ProbabilityMap3D.model_rebuild()
PointSet2D.model_rebuild()
PointSet3D.model_rebuild()
PointVectorSet2D.model_rebuild()
PointVectorSet3D.model_rebuild()
PointMatrixSet2D.model_rebuild()
PointMatrixSet3D.model_rebuild()
TriMesh.model_rebuild()
Region.model_rebuild()
Average.model_rebuild()
MovieStackCollection.model_rebuild()
Dataset.model_rebuild()
