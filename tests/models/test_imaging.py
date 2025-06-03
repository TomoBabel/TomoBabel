from tests.testing_tools import TomoBabelTest
from src.tomobabel.models.imaging import (
    EmImagingParameters,
    EmVitrification,
    EmDetector,
    EmSampleCreation,
)


class ImagingModelsTest(TomoBabelTest):
    def test_all_imaging_EBI_linked_models_are_valid(self):
        for model in [
            EmImagingParameters,
            EmVitrification,
            EmDetector,
            EmSampleCreation,
        ]:
            model()
