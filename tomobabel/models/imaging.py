from __future__ import annotations

from typing import Optional
from pydantic import Field
from tomobabel.models.basemodels import ConfiguredBaseModel
from tomobabel.models.ebi_compatibility.ebi_validation import EbiLinkedBaseModel

# These models are designed to correspond with the EBI EMDB/PDB schema:
#   The fields in these models use the same names as the EBI schema
#   Fields with limited options are validated against the EBI schema, but the
#   validation raise warnings rather than errors so as not to limit allowed parameters.


class SampleSupport(EbiLinkedBaseModel):
    ebi_scheme_name: str = Field(default="em_sample_support")
    film_material: Optional[str] = Field(default=None, description="")
    grid_material: Optional[str] = Field(default=None, description="")
    grid_mesh_size: Optional[int] = Field(default=None, description="")
    pretreatment: Optional[str] = Field(default=None, description="")


class EmDetector(EbiLinkedBaseModel):
    ebi_scheme_name: str = Field(default="em_detector")
    detective_quantum_efficiency: Optional[float] = Field(default=None, description="")
    mode: Optional[str] = Field(default=None, description="")


class EmImagingParameters(EbiLinkedBaseModel):
    ebi_scheme_name: str = Field(default="em_imaging")
    microscope_model: Optional[str] = Field(default=None, description="")
    specimen_holder_type: Optional[str] = Field(default=None, description="")
    specimen_holder_model: Optional[str] = Field(default=None, description="")
    accelerating_voltage: Optional[int] = Field(default=None, description="")
    illumination_mode: Optional[str] = Field(default=None, description="")
    mode: Optional[str] = Field(default=None, description="")
    nominal_cs: Optional[float] = Field(default=None, description="")
    nominal_defocus_min: Optional[float] = Field(default=None, description="")
    nominal_defocus_max: Optional[float] = Field(default=None, description="")
    nominal_magnification: Optional[int] = Field(default=None, description="")
    electron_source: Optional[str] = Field(default=None, description="")
    temperature: Optional[float] = Field(default=None, description="")
    detector_distance: Optional[float] = Field(default=None, description="")
    alignment_procedure: Optional[str] = Field(default=None, description="")
    c2_aperture_diameter: Optional[float] = Field(default=None, description="")
    cryogen: Optional[str] = Field(default=None, description="")
    objective_aperture: Optional[float] = Field(default=None, description="")
    microscope_serial_number: Optional[str] = Field(default=None, description="")


class EmVitrification(EbiLinkedBaseModel):
    ebi_scheme_name: str = Field(default="em_vitrification")
    cryogen_name: Optional[str] = Field(default=None, description="")
    humidity: Optional[float] = Field(default=None, description="")
    temp: Optional[float] = Field(default=None, description="")
    chamber_temperature: Optional[float] = Field(default=None, description="")
    instrument: Optional[str] = Field(default=None, description="")
    method: Optional[str] = Field(default=None, description="")


class EmSampleCreation(ConfiguredBaseModel):
    """This is called SampleCreation rather than SamplePreparation so as not to overlap
    with the em_sample_preparation catefory, which covers things like buffers"""

    sample_support: Optional[SampleSupport] = Field(default=None, description="")
    vitrification: Optional[EmVitrification] = Field(default=None, description="")


class EmImaging(ConfiguredBaseModel):
    imaging: EmImagingParameters = Field(default=None, description="")
    detector: EmDetector = Field(default=None, description="")
