from typing import List
from warnings import warn
from pydantic import model_validator, Field
import re
from tomobabel.models.basemodels import ConfiguredBaseModel
from tomobabel.models.ebi_compatibility.ebi_cats import DEPOBJ_CATS


class EbiLinkedBaseModel(ConfiguredBaseModel):
    """
    A class for fields that are directly linked to EBI schema and are validated
    against them
    """

    ebi_scheme_name: str = Field(
        default="",
        description=(
            "The name of the field in the EBI schema that corresponds to this model"
            " there needs to be a 1:1 correspondance between the Fields in the model"
            " and the fields in that EBI scheme"
        ),
    )

    @model_validator(mode="after")
    def validate_ebi_limited_fields(self):
        match_ebi_linked_model_fields(self)
        validate_fields_against_ebi(self)
        return self

    @property
    def ebi_fields(self) -> List[str]:
        fields = [
            x
            for x in self.__class__.model_fields.keys()
            if x not in ("annotations", "ebi_scheme_name")
        ]
        return fields


def validate_fields_against_ebi(cets_obj: EbiLinkedBaseModel) -> None:
    """Validate a value against the allowed choices in the EBI schema

    Raises warnings rather than errors so the overall CETS data model is not limited to
    the EBI schema

    Args:
        cets_obj (ConfiguredBaseModel): The model to be checked IE `self`
        fields (List[str]): The fields to be validated against the EBI schema choices
    Raises:
        Warning: If a field's allowable values are limited in the EBI schema and the
            value is not in the list of allowed values

    """
    for attr in cets_obj.ebi_fields:
        ebi_dict = DEPOBJ_CATS[cets_obj.ebi_scheme_name]
        options = ebi_dict[attr]["options"]
        if getattr(cets_obj, attr) is not None:
            value = str(getattr(cets_obj, attr))
            if options and value not in options:
                warn(
                    f"CETS model: {cets_obj.__class__.__name__}.{attr}: The value"
                    f"{value} is not on the approved list of values in the EBI schema"
                    " for deposition in the PDB/EMDB"
                )
            elif not re.match(str(ebi_dict[attr]["regex"]), value):
                warn(
                    f"CETS model: {cets_obj.__class__.__name__}.{attr}: The value"
                    " {value} does not satisfy the validation regex for this field in"
                    " the EBI schema"
                )


def match_ebi_linked_model_fields(cets_obj: EbiLinkedBaseModel) -> None:
    """
    Check that the fields in an EbiLinkedBaseModel match the ebi schema.

    The EbiLinkedBaseModel does not have to contain every field for the EBI scheme for
    that entry, but cannot containany additional fields.  If it does a standard
    ConfiguredBaseModel should be used instead.
    """
    bad_fields = []
    for field in cets_obj.ebi_fields:
        ebi_dict = DEPOBJ_CATS.get(cets_obj.ebi_scheme_name)
        if not ebi_dict:
            raise ValueError(
                f"{cets_obj.ebi_scheme_name} is not a valid EBI data model field"
            )
        elif str(field) not in ebi_dict.keys():
            bad_fields.append(field)
    if bad_fields:
        raise ValueError(
            f"The following fields {bad_fields} are not present in the EBI schema."
            " If they are desired a ConfiguredBaseModel should be used rather than an "
            "EbiLinkedBaseModel"
        )
