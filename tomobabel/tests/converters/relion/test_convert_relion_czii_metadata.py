import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tomobabel.converters.relion import relion_converter
from tomobabel.tests.converters.relion import test_data
from tomobabel.tests.converters.relion.relion_testing_utils import setup_tomo_dirs


class CziiConverterTest(unittest.TestCase):
    def setUp(self):
        """
        Setup test data and output directories.
        """
        self.test_data = Path(os.path.dirname(test_data.__file__))
        self.test_dir = tempfile.mkdtemp(prefix="ccpem-czii_converter")

        # Change to test directory
        self._orig_dir = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self._orig_dir)
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    # ToDo: Update this test when the other datatypes are added
    @patch("tomobabel.converters.relion.relion_convert_tilt_series.get_mrc_dims")
    def test_main_with_ctf_data(self, mockdims):
        mockdims.return_value = 2000, 2000
        setup_tomo_dirs()
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
        assert dataset.model_dump() == expected


if __name__ == "__main__":
    unittest.main()
