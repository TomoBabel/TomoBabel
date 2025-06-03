import os
import shutil
import tempfile
import unittest
from pathlib import Path


class TomoBabelTest(unittest.TestCase):
    def setUp(self):
        """
        Setup test data and output directories.
        """
        self.test_dir = Path(tempfile.mkdtemp(prefix="tomobabl_test"))
        # Change to test directory
        self._orig_dir = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self._orig_dir)
        if self.test_dir.is_dir():
            shutil.rmtree(self.test_dir)
