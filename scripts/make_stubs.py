#!/usr/bin/env python3

"""mypy does not play nice with the type annotations in the model file, so .pyi stubs
are needed.
"""

import ast
from tomobabel.models import models
from typing import get_type_hints, Dict, List


class TomoBabelModelClass(object):
    def __init__(self, name: str, type: str, attrs: Dict[str, str]):
        self.name = name
        self.type = type
        self.attrs = attrs


def get_classes_from_file() -> List[str]:
    with open("tomobabel/models/models.py") as f:
        node = ast.parse(f.read(), filename="tomobabel/models/models.py")

    class_names = [n.name for n in node.body if isinstance(n, ast.ClassDef)]
    return class_names


def get_class_attrs() -> List[TomoBabelModelClass]:
    classes = []
    attrs = {}
    for class_name in get_classes_from_file():
        if class_name in (
            "LinkMLMeta",
            "ConfiguredBaseModel",
            "AxisType",
            "TransformationType",
            "Axis",
            "CoordinateSystem",
        ):
            continue
        cls = getattr(models, class_name, None)
        attrs[class_name] = get_type_hints(cls)
        clean_attrs = {}
        for attr in attrs[class_name].items():
            type_str = str(attr[1])
            rm_typing = type_str.replace("typing.", "")
            rm_path = rm_typing.replace("tomobabel.models.models.", "")
            clean_attrs[attr[0]] = rm_path

        if cls:
            cl_type = (
                str(cls.__bases__[0])
                .replace("<class 'tomobabel.models.models.", "")
                .replace("'>", "")
            )
        else:
            cl_type = "ERROR"
        classes.append(
            TomoBabelModelClass(name=class_name, type=str(cl_type), attrs=clean_attrs)
        )
    return classes


oddballs = """
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


"""

with open("tomobabel/models/models.pyi", "w") as outfile:
    outfile.write(oddballs)
    classes = get_class_attrs()
    for cls in classes:
        outfile.write(f"class {cls.name}({cls.type}):\n")
        for attr in cls.attrs.items():
            outfile.write(f"    {attr[0]}: {attr[1]}\n")
        outfile.write("\n\n")
