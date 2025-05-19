import json
import unittest
from unittest.mock import patch

from tomobabel.converters.relion import relion_converter
from tomobabel.tests.converters.relion.relion_testing_utils import TomoBabelRelionTest


class CziiConverterTest(TomoBabelRelionTest):

    # ToDo: Update this test when the other datatypes are added
    @patch("tomobabel.converters.relion.relion_convert_tilt_series.get_mrc_dims")
    def test_main_with_ctf_data(self, mockdims):
        mockdims.return_value = 2000, 2000
        self.setup_tomo_dirs()
        dataset = relion_converter.main(
            [
                "--tilt_series_starfile",
                "CtfFind/job003/tilt_series_ctf.star",
                "--gain_reference",
                "my_gain_file.mrc",
                "--defect_file",
                "my_defect_file.mrc",
            ]
        )
        with open(self.test_data / "ctf_dataset.json") as exp:
            expected = json.load(exp)
        assert dataset.model_dump(mode="json") == expected


if __name__ == "__main__":
    unittest.main()
