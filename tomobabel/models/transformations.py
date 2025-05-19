from __future__ import annotations

from enum import Enum

import numpy as np
from pydantic import Field

from tomobabel.models.basemodels import ConfiguredBaseModel


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


# Model rebuilds
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model

Transformation.model_rebuild()
