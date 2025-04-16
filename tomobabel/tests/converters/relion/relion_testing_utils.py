import os
import shutil
from pathlib import Path

from tomobabel.tests.converters.relion import test_data

test_data_dir = Path(os.path.dirname(test_data.__file__))


def setup_tomo_dirs():
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
        for f in test_data_dir.glob(f"{job}/*"):
            if f.is_dir():
                shutil.copytree(f, jobdir / f.name)
            else:
                shutil.copy(f, jobdir)
