from pydantic import Field
import warnings
from tests.testing_tools import TomoBabelTest
from src.tomobabel.models.imaging import EmImagingParameters


class EbiValidationTests(TomoBabelTest):
    def test_instantiate_EBI_linked_model(self):
        model = EmImagingParameters()
        assert model.ebi_fields == [
            "microscope_model",
            "specimen_holder_type",
            "specimen_holder_model",
            "accelerating_voltage",
            "illumination_mode",
            "mode",
            "nominal_cs",
            "nominal_defocus_min",
            "nominal_defocus_max",
            "nominal_magnification",
            "electron_source",
            "temperature",
            "detector_distance",
            "alignment_procedure",
            "c2_aperture_diameter",
            "cryogen",
            "objective_aperture",
            "microscope_serial_number",
        ]

    def test_EBI_linked_model_bad_field(self):
        class BadModel(EmImagingParameters):
            bad_field: str = Field(default="")

        with self.assertRaises(ValueError):
            BadModel()

    def test_warnings_raised_if_fields_values_dont_validate_options(self):
        with warnings.catch_warnings(record=True) as w:
            EmImagingParameters(microscope_model="BAD")
        assert str(w[0].message).startswith(
            "CETS model: EmImagingParameters.microscope_model: The value BAD is not"
        )
