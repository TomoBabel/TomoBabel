from __future__ import annotations

import numpy as np
from tomobabel.models.basemodels import ConfiguredBaseModel
from pydantic import Field
from enum import Enum


class TransformationType(str, Enum):
    identity = "identity"
    flip = "flip"
    translation = "translation"
    scale = "scale"
    rotation = "rotate"
    affine = "affine"


class Transformation(ConfiguredBaseModel):
    """
    A generic superclass for transformations
    """

    transform_type: str = TransformationType.identity
    trans_matrix: np.ndarray = Field(
        default=np.identity(4),
        description="The matrix used to apply the transformation",
    )


class AffineTransform(Transformation):
    """
    An affine transformation
    """

    transform_type: str = TransformationType.affine


class ScaleTransform(Transformation):
    """
    An scale transformation
    """

    transform_type: str = TransformationType.scale


class RotationTransform(Transformation):
    """
    A rotation
    """

    transform_type: str = TransformationType.rotation


class TranslationTransform(Transformation):
    """
    A translation
    """

    transform_type: str = TransformationType.translation


class MotionCorrectionTransformation(TranslationTransform):
    """
    A transformation applied to a movie frame during motion correction. Currently, a
    whole frame translation, maybe a more complex deformation in the future.
    """

    transform_type: str = TransformationType.translation


class FlipTransform(Transformation):
    """
    A flip over one or more axes
    """

    transform_type: str = TransformationType.flip


# Model rebuilds
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model

AffineTransform.model_rebuild()
FlipTransform.model_rebuild()
MotionCorrectionTransformation.model_rebuild()
RotationTransform.model_rebuild()
ScaleTransform.model_rebuild()
Transformation.model_rebuild()
TranslationTransform.model_rebuild()
