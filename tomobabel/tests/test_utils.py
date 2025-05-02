import os
import shutil
import tempfile
import unittest
from pathlib import Path

from tomobabel.tests.converters.relion import test_data


class TomoBabelUtilsTest(unittest.TestCase):
    def setUp(self):
        """
        Setup test data and output directories.
        """
        self.test_data = Path(os.path.dirname(test_data.__file__))
        self.test_dir = tempfile.mkdtemp(prefix="tomobabl_test")

        # Change to test directory
        self._orig_dir = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self._orig_dir)
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
