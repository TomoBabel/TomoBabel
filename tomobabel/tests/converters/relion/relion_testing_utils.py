import os
import shutil
from pathlib import Path
import unittest
import tempfile

from tomobabel.tests.converters.relion import test_data


class TomoBabelRelionTest(unittest.TestCase):
    def setUp(self):
        """
        Setup test data and output directories.
        """
        self.test_data = Path(os.path.dirname(test_data.__file__))
        self.test_dir = Path(tempfile.mkdtemp(prefix="tomobabel_relion_converter"))

        # Change to test directory
        self._orig_dir = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self._orig_dir)
        if self.test_dir.is_dir():
            shutil.rmtree(self.test_dir)

    def setup_tomo_dirs(self):
        """Set up a minimal RELION project for testing"""
        jobs = {
            "Import": 1,
            "MotionCorr": 2,
            "CtfFind": 3,
            "ExcludeTiltImages": 4,
            "AlignTiltSeries": 5,
        }
        for job in jobs:
            jobdir = Path(f"{job}/job{jobs[job]:03d}")
            jobdir.mkdir(parents=True)
            for f in self.test_data.glob(f"{job}/*"):
                if f.is_dir():
                    shutil.copytree(f, jobdir / f.name)
                else:
                    shutil.copy(f, jobdir)
