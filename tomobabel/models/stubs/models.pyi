from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, ConfigDict, RootModel
from enum import Enum

class ConfiguredBaseModel(BaseModel):
    model_config: ConfigDict

class LinkMLMeta(RootModel):
    root: Dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)
    def __getattr__(self, key: str): ...
    def __getitem__(self, key: str): ...
    def __setitem__(self, key: str, value): ...
    def __contains__(self, key: str) -> bool: ...

class AxisType(str, Enum):
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

class Axis(ConfiguredBaseModel):
    name: str
    axis_unit: Optional[str]
    axis_type: Optional[str]

class CoordinateSystem(ConfiguredBaseModel):
    name: str
    axes: List[Axis]

class Image2D(ConfiguredBaseModel):
    width: Optional[int]
    height: Optional[int]
    coordinate_systems: Optional[List[CoordinateSystem]]
    coordinate_transformations: Optional[List[CoordinateTransformation]]

class Image3D(ConfiguredBaseModel):
    width: Optional[int]
    height: Optional[int]
    depth: Optional[int]
    coordinate_systems: Optional[List[CoordinateSystem]]
    coordinate_transformations: Optional[List[CoordinateTransformation]]

class ImageStack2D(ConfiguredBaseModel):
    images: Optional[List[Image2D]]

class ImageStack3D(ConfiguredBaseModel):
    images: Optional[List[Image3D]]

class CoordinateTransformation(ConfiguredBaseModel):
    name: Optional[str]
    input: Optional[str]
    output: Optional[str]
    type: Optional[TransformationType]

class Identity(CoordinateTransformation):
    name: Optional[str]
    input: Optional[str]
    output: Optional[str]
    type: Optional[TransformationType]

class AxisNameMapping(ConfiguredBaseModel):
    axis1_name: Optional[str]
    axis2_name: Optional[str]

class MapAxis(CoordinateTransformation):
    name: Optional[str]
    input: Optional[str]
    output: Optional[str]
    type: Optional[TransformationType]
    mapAxis: Optional[List[AxisNameMapping]]

class Translation(CoordinateTransformation):
    name: Optional[str]
    input: Optional[str]
    output: Optional[str]
    type: Optional[TransformationType]
    translation: Optional[List[float]]

class Scale(CoordinateTransformation):
    name: Optional[str]
    input: Optional[str]
    output: Optional[str]
    type: Optional[TransformationType]
    scale: Optional[List[float]]

class Affine(CoordinateTransformation):
    name: Optional[str]
    input: Optional[str]
    output: Optional[str]
    type: Optional[TransformationType]
    affine: Optional[list[list[float]]]

class Sequence(CoordinateTransformation):
    name: Optional[str]
    input: Optional[str]
    output: Optional[str]
    type: Optional[TransformationType]
    sequence: Optional[List[CoordinateTransformation]]

class ProjectionAlignment(Sequence):
    name: Optional[str]
    input: Optional[str]
    output: Optional[str]
    type: Optional[TransformationType]
    sequence: Optional[List[Union[Affine, Translation]]]

class Alignment(ConfiguredBaseModel):
    projection_alignments: Optional[List[ProjectionAlignment]]

class CTFMetadata(ConfiguredBaseModel):
    defocus_u: Optional[float]
    defocus_v: Optional[float]
    defocus_angle: Optional[float]

class AcquisitionMetadataMixin(ConfiguredBaseModel):
    nominal_tilt_angle: Optional[float]
    accumulated_dose: Optional[float]
    ctf_metadata: Optional[CTFMetadata]

class GainFile(Image2D):
    width: Optional[int]
    height: Optional[int]
    coordinate_systems: Optional[List[CoordinateSystem]]
    coordinate_transformations: Optional[List[CoordinateTransformation]]
    path: Optional[str]

class DefectFile(Image2D):
    width: Optional[int]
    height: Optional[int]
    coordinate_systems: Optional[List[CoordinateSystem]]
    coordinate_transformations: Optional[List[CoordinateTransformation]]
    path: Optional[str]

class MovieFrame(AcquisitionMetadataMixin):
    width: Optional[int]
    height: Optional[int]
    coordinate_systems: Optional[List[CoordinateSystem]]
    coordinate_transformations: Optional[List[CoordinateTransformation]]
    nominal_tilt_angle: Optional[float]
    accumulated_dose: Optional[float]
    ctf_metadata: Optional[CTFMetadata]
    path: Optional[str]
    section: Optional[str]

class MovieStack(ConfiguredBaseModel):
    images: Optional[List[MovieFrame]]
    path: Optional[str]

class ProjectionImage(AcquisitionMetadataMixin):
    width: Optional[int]
    height: Optional[int]
    coordinate_systems: Optional[List[CoordinateSystem]]
    coordinate_transformations: Optional[List[CoordinateTransformation]]
    nominal_tilt_angle: Optional[float]
    accumulated_dose: Optional[float]
    ctf_metadata: Optional[CTFMetadata]
    path: Optional[str]
    section: Optional[str]

class MovieStackSeries(ConfiguredBaseModel):
    stacks: Optional[List[MovieStack]]

class TiltSeries(ConfiguredBaseModel):
    images: Optional[List[ProjectionImage]]
    path: Optional[str]

class SubProjectionImage(ProjectionImage):
    width: Optional[int]
    height: Optional[int]
    coordinate_systems: Optional[List[CoordinateSystem]]
    coordinate_transformations: Optional[List[CoordinateTransformation]]
    nominal_tilt_angle: Optional[float]
    accumulated_dose: Optional[float]
    ctf_metadata: Optional[CTFMetadata]
    path: Optional[str]
    section: Optional[str]
    particle_index: Optional[int]

class Tomogram(Image3D):
    width: Optional[int]
    height: Optional[int]
    depth: Optional[int]
    coordinate_systems: Optional[List[CoordinateSystem]]
    coordinate_transformations: Optional[List[CoordinateTransformation]]
    path: Optional[str]

class ParticleMap(Image3D):
    width: Optional[int]
    height: Optional[int]
    depth: Optional[int]
    coordinate_systems: Optional[List[CoordinateSystem]]
    coordinate_transformations: Optional[List[CoordinateTransformation]]
    path: Optional[str]

class CoordMetaMixin(ConfiguredBaseModel):
    coordinate_systems: Optional[List[CoordinateSystem]]
    coordinate_transformations: Optional[List[CoordinateTransformation]]

class Annotation(ConfiguredBaseModel):
    path: Optional[str]

class SegmentationMask2D(Annotation):
    width: Optional[int]
    height: Optional[int]
    coordinate_systems: Optional[List[CoordinateSystem]]
    coordinate_transformations: Optional[List[CoordinateTransformation]]
    path: Optional[str]

class SegmentationMask3D(Annotation):
    width: Optional[int]
    height: Optional[int]
    depth: Optional[int]
    coordinate_systems: Optional[List[CoordinateSystem]]
    coordinate_transformations: Optional[List[CoordinateTransformation]]
    path: Optional[str]

class ProbabilityMap2D(Annotation):
    width: Optional[int]
    height: Optional[int]
    coordinate_systems: Optional[List[CoordinateSystem]]
    coordinate_transformations: Optional[List[CoordinateTransformation]]
    path: Optional[str]

class ProbabilityMap3D(Annotation):
    width: Optional[int]
    height: Optional[int]
    depth: Optional[int]
    coordinate_systems: Optional[List[CoordinateSystem]]
    coordinate_transformations: Optional[List[CoordinateTransformation]]
    path: Optional[str]

class PointSet2D(Annotation):
    coordinate_systems: Optional[List[CoordinateSystem]]
    coordinate_transformations: Optional[List[CoordinateTransformation]]
    path: Optional[str]
    origin2D: Optional[list[list[float]]]

class PointSet3D(Annotation):
    coordinate_systems: Optional[List[CoordinateSystem]]
    coordinate_transformations: Optional[List[CoordinateTransformation]]
    path: Optional[str]
    origin3D: Optional[list[list[float]]]

class PointVectorSet2D(Annotation):
    coordinate_systems: Optional[List[CoordinateSystem]]
    coordinate_transformations: Optional[List[CoordinateTransformation]]
    path: Optional[str]
    origin2D: Optional[list[list[float]]]
    vector2D: Optional[list[list[float]]]

class PointVectorSet3D(Annotation):
    coordinate_systems: Optional[List[CoordinateSystem]]
    coordinate_transformations: Optional[List[CoordinateTransformation]]
    path: Optional[str]
    origin3D: Optional[list[list[float]]]
    vector3D: Optional[list[list[float]]]

class PointMatrixSet2D(Annotation):
    coordinate_systems: Optional[List[CoordinateSystem]]
    coordinate_transformations: Optional[List[CoordinateTransformation]]
    path: Optional[str]
    origin2D: Optional[list[list[float]]]
    matrix2D: Optional[list[list[list[float]]]]

class PointMatrixSet3D(Annotation):
    coordinate_systems: Optional[List[CoordinateSystem]]
    coordinate_transformations: Optional[List[CoordinateTransformation]]
    path: Optional[str]
    origin3D: Optional[list[list[float]]]
    matrix3D: Optional[list[list[list[float]]]]

class TriMesh(Annotation):
    coordinate_systems: Optional[List[CoordinateSystem]]
    coordinate_transformations: Optional[List[CoordinateTransformation]]
    path: Optional[str]

class Region(ConfiguredBaseModel):
    movie_stack_collections: Optional[List[MovieStackCollection]]
    tilt_series: Optional[List[TiltSeries]]
    alignments: Optional[List[Alignment]]
    tomograms: Optional[List[Tomogram]]
    annotations: Optional[List[Annotation]]

class Average(ConfiguredBaseModel):
    name: Optional[str]
    particle_maps: Optional[List[ParticleMap]]
    annotations: Optional[List[Annotation]]

class MovieStackCollection(ConfiguredBaseModel):
    movie_stacks: Optional[List[MovieStackSeries]]
    gain_file: Optional[GainFile]
    defect_file: Optional[DefectFile]

class Dataset(ConfiguredBaseModel):
    name: Optional[str]
    regions: Optional[List[Region]]
    averages: Optional[List[Average]]
