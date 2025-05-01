import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path, PosixPath
from unittest.mock import patch

import numpy as np
from gemmi import cif

from tomobabel.converters.relion.relion_convert_tilt_series import (
    RelionTiltSeriesMovie,
    PipelinerTiltSeriesGroupConverter,
    main as tilt_series_main,
)
from tomobabel.models.tilt_series import (
    MovieStack,
    CTFMetadata,
    MovieFrame,
    GainFile,
    DefectFile,
)
from tomobabel.models.transformations import AffineTransform
from tomobabel.tests.converters.relion import test_data
from tomobabel.tests.converters.relion.relion_testing_utils import setup_tomo_dirs


@unittest.skip("these tests need to be updated for the new model")
class CziiTiltSeriesConverterTest(unittest.TestCase):
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

    @patch("tomobabel.converters.relion.relion_convert_tilt_series.get_mrc_dims")
    def test_instantiate_relion_tilt_series_movie_object(self, mock_dims):
        mock_dims.return_value = (2000, 2000)
        mov = RelionTiltSeriesMovie(
            stack_file_path=Path("my_stackfile.mrc"),
            dose_per_frame=3.0,
            tilt=15.0,
            pre_exp=3.0,
            n_frames=8,
            apix=0.675,
        )
        assert mov.__dict__ == {
            "dose_per_frame": 3.0,
            "stack_file_path": "my_stackfile.mrc",
            "czii_movie_frames": [],
            "tilt": 15.0,
            "height": 2000,
            "width": 2000,
            "n_frames": 8,
            "czii_movie_stack": MovieStack(images=None, path="my_stackfile.mrc"),
            "pre_exp": 3.0,
            "apix": 0.675,
        }

    def test_instantiate_PipelinerTiltSeriesGroupConverter(self):
        converter = PipelinerTiltSeriesGroupConverter(
            input_file=Path("Import/job001/tilt_series.star")
        )
        assert converter.__dict__ == {
            "input_file": PosixPath("Import/job001/tilt_series.star"),
            "all_movie_collections": {},
            "all_tilt_series": {},
            "ts_files": {},
            "defect_file": None,
            "gain_file": None,
        }

    def test_converter_get_tilt_series_dict(self):
        setup_tomo_dirs()
        converter = PipelinerTiltSeriesGroupConverter(
            input_file=Path("Import/job001/tilt_series.star")
        )
        converter.get_tilt_series_files()
        assert converter.ts_files == {
            "TS_01": "Import/job001/tilt_series/TS_01.star",
            "TS_03": "Import/job001/tilt_series/TS_03.star",
            "TS_43": "Import/job001/tilt_series/TS_43.star",
            "TS_45": "Import/job001/tilt_series/TS_45.star",
            "TS_54": "Import/job001/tilt_series/TS_54.star",
        }

    @patch("tomobabel.converters.relion.relion_convert_tilt_series.get_mrc_dims")
    def test_converter_get_movies_data(self, mockmrc):
        """Gets the move object for each movie, without frame data"""
        mockmrc.return_value = 2000, 2000
        setup_tomo_dirs()
        converter = PipelinerTiltSeriesGroupConverter(
            input_file=Path("Import/job001/tilt_series.star")
        )
        tilt_series = cif.read_file("Import/job001/tilt_series/TS_01.star")
        ts_block = tilt_series.find_block("TS_01")
        ts_movies = converter.get_movies_data(ts_block)
        assert all([isinstance(x, RelionTiltSeriesMovie) for x in ts_movies])
        assert len(ts_movies) == 41, len(ts_movies)
        assert ts_movies[0].__dict__ == {
            "dose_per_frame": 0.375,
            "stack_file_path": "frames/TS_01_000_0.0.mrc",
            "czii_movie_frames": [],
            "tilt": 0.001,
            "pre_exp": 0.0,
            "height": 2000,
            "width": 2000,
            "n_frames": 8,
            "apix": 0.675,
            "czii_movie_stack": MovieStack(
                images=None, path="frames/TS_01_000_0.0.mrc"
            ),
        }

    def test_converter_get_ctf_data(self):
        setup_tomo_dirs()
        ts = cif.read_file("CtfFind/job003/tilt_series/TS_01.star")
        block = ts.find_block("TS_01")
        converter = PipelinerTiltSeriesGroupConverter(
            input_file=Path("CtfFind/job003/tilt_series_ctf.star")
        )
        ctfdata = converter.get_ctf_data(block, 0)
        assert isinstance(ctfdata, CTFMetadata)
        assert ctfdata.model_dump() == {
            "defocus_u": 38855.828125,
            "defocus_v": 38750.828125,
            "defocus_angle": 35.154533,
        }

    @patch(
        "tomobabel.converters.relion.relion_convert_tilt_series.generate_affine_matrix"
    )
    def test_converter_get_transformation_data(self, mock_matrix):
        mock_matrix.return_value = np.zeros((3, 3), dtype=float)
        setup_tomo_dirs()
        ts = cif.read_file("AlignTiltSeries/job005/tilt_series/TS_01.star")
        block = ts.find_block("TS_01")
        converter = PipelinerTiltSeriesGroupConverter(
            input_file=Path("CtfFind/job003/corrected_tilt_series.star")
        )
        transdata = converter.get_transformation_data(block, 0, 0.675)
        assert isinstance(transdata, AffineTransform)
        assert transdata.model_dump() == {
            "name": None,
            "input": None,
            "output": None,
            "type": "affine",
            "affine": [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
        }

    @patch("tomobabel.converters.relion.relion_convert_tilt_series.get_mrc_dims")
    def test_converter_get_gain_and_defect_files(self, mockdims):
        setup_tomo_dirs()
        mockdims.return_value = 2000, 2000, 1

        converter = PipelinerTiltSeriesGroupConverter(
            input_file=Path("MotionCorr/job002/tilt_series.star")
        )
        gain, defect = converter.get_gain_ref_and_defect_file()
        assert gain == GainFile(path="my_gain_file.mrc", height=2000, width=2000)
        assert defect == DefectFile(path="my_defect_file.mrc", height=2000, width=2000)

    def test_converter_make_movie_collections_data(self):
        setup_tomo_dirs()
        ts = cif.read_file("Import/job001/tilt_series/TS_01.star")
        block = ts.find_block("TS_01")
        converter = PipelinerTiltSeriesGroupConverter(
            input_file=Path("Import/job001/tilt_series.star")
        )
        mov = RelionTiltSeriesMovie(
            dose_per_frame=1.0,
            stack_file_path=Path("my_stack.mrc"),
            tilt=3.5,
            pre_exp=1.5,
            n_frames=10,
            czii_movie_frames=None,
            apix=0.675,
        )
        converter.make_movie_collections(block, 0, mov)
        assert mov.czii_movie_frames == [
            MovieFrame(
                width=None,
                height=None,
                coordinate_systems=None,
                coordinate_transformations=None,
                nominal_tilt_angle=3.5,
                accumulated_dose=2.5,
                ctf_metadata=None,
                path="my_stack.mrc",
                section="0",
            ),
            MovieFrame(
                width=None,
                height=None,
                coordinate_systems=None,
                coordinate_transformations=None,
                nominal_tilt_angle=3.5,
                accumulated_dose=3.5,
                ctf_metadata=None,
                path="my_stack.mrc",
                section="1",
            ),
            MovieFrame(
                width=None,
                height=None,
                coordinate_systems=None,
                coordinate_transformations=None,
                nominal_tilt_angle=3.5,
                accumulated_dose=4.5,
                ctf_metadata=None,
                path="my_stack.mrc",
                section="2",
            ),
            MovieFrame(
                width=None,
                height=None,
                coordinate_systems=None,
                coordinate_transformations=None,
                nominal_tilt_angle=3.5,
                accumulated_dose=5.5,
                ctf_metadata=None,
                path="my_stack.mrc",
                section="3",
            ),
            MovieFrame(
                width=None,
                height=None,
                coordinate_systems=None,
                coordinate_transformations=None,
                nominal_tilt_angle=3.5,
                accumulated_dose=6.5,
                ctf_metadata=None,
                path="my_stack.mrc",
                section="4",
            ),
            MovieFrame(
                width=None,
                height=None,
                coordinate_systems=None,
                coordinate_transformations=None,
                nominal_tilt_angle=3.5,
                accumulated_dose=7.5,
                ctf_metadata=None,
                path="my_stack.mrc",
                section="5",
            ),
            MovieFrame(
                width=None,
                height=None,
                coordinate_systems=None,
                coordinate_transformations=None,
                nominal_tilt_angle=3.5,
                accumulated_dose=8.5,
                ctf_metadata=None,
                path="my_stack.mrc",
                section="6",
            ),
            MovieFrame(
                width=None,
                height=None,
                coordinate_systems=None,
                coordinate_transformations=None,
                nominal_tilt_angle=3.5,
                accumulated_dose=9.5,
                ctf_metadata=None,
                path="my_stack.mrc",
                section="7",
            ),
            MovieFrame(
                width=None,
                height=None,
                coordinate_systems=None,
                coordinate_transformations=None,
                nominal_tilt_angle=3.5,
                accumulated_dose=10.5,
                ctf_metadata=None,
                path="my_stack.mrc",
                section="8",
            ),
            MovieFrame(
                width=None,
                height=None,
                coordinate_systems=None,
                coordinate_transformations=None,
                nominal_tilt_angle=3.5,
                accumulated_dose=11.5,
                ctf_metadata=None,
                path="my_stack.mrc",
                section="9",
            ),
        ]

    @patch("tomobabel.converters.relion.relion_convert_tilt_series.get_mrc_dims")
    def test_converter_do_conversion_import_job(self, mockmrc):
        mockmrc.return_value = 2000, 2000
        setup_tomo_dirs()
        converter = PipelinerTiltSeriesGroupConverter(
            input_file=Path("Import/job001/tilt_series.star")
        )
        converter.get_tilt_series_files()
        converter.do_conversion()

        amc_dict = {}
        for i in converter.all_movie_collections:
            amc_dict[i] = converter.all_movie_collections[i].model_dump()
        with open(self.test_data / "import_all_movie_cols.json") as amc:
            amc_actual = json.load(amc)
        assert amc_dict == amc_actual

        ats_dict = {}
        for i in converter.all_tilt_series:
            ats_dict[i] = converter.all_tilt_series[i].model_dump()
        with open(self.test_data / "import_all_tilt_series.json") as ats:
            ats_actual = json.load(ats)
        assert ats_dict == ats_actual

    @patch("tomobabel.converters.relion.relion_convert_tilt_series.get_mrc_dims")
    def test_converter_do_conversion_with_CTF_job(self, mockmrc):
        mockmrc.return_value = 2000, 2000
        setup_tomo_dirs()
        converter = PipelinerTiltSeriesGroupConverter(
            input_file=Path("CtfFind/job003/tilt_series_ctf.star")
        )
        converter.get_tilt_series_files()
        converter.do_conversion()

        amc_dict = {}
        for i in converter.all_movie_collections:
            amc_dict[i] = converter.all_movie_collections[i].model_dump()
        with open(self.test_data / "ctf_all_movie_cols.json") as amc:
            amc_actual = json.load(amc)
        assert amc_dict == amc_actual

        ats_dict = {}
        for i in converter.all_tilt_series:
            ats_dict[i] = converter.all_tilt_series[i].model_dump()
        with open(self.test_data / "ctf_all_tilt_series.json") as ats:
            ats_actual = json.load(ats)
        assert ats_dict == ats_actual

    @patch("tomobabel.converters.relion.relion_convert_tilt_series.get_mrc_dims")
    def test_converter_do_conversion_with_CTF_job_with_gain_and_defect(self, mockmrc):
        """Output should contain gain ref and defect file info, when provided"""
        mockmrc.return_value = 2000, 2000
        setup_tomo_dirs()
        converter = PipelinerTiltSeriesGroupConverter(
            input_file=Path("CtfFind/job003/tilt_series_ctf.star"),
            gain_file="my_gain_file.mrc",
            defect_file="my_defect_file.mrc",
        )
        converter.get_tilt_series_files()
        converter.do_conversion()

        amc_dict = {}
        for i in converter.all_movie_collections:
            amc_dict[i] = converter.all_movie_collections[i].model_dump()
        with open(self.test_data / "ctf_all_movie_cols_gain_defect.json") as amc:
            amc_actual = json.load(amc)
        assert amc_dict == amc_actual

        ats_dict = {}
        for i in converter.all_tilt_series:
            ats_dict[i] = converter.all_tilt_series[i].model_dump()
        with open(self.test_data / "ctf_all_tilt_series.json") as ats:
            ats_actual = json.load(ats)
        assert ats_dict == ats_actual

    @patch("tomobabel.converters.relion.relion_convert_tilt_series.get_mrc_dims")
    def test_converter_do_conversion_with_MotionCorr_job(self, mockmrc):
        """This one will have gain ref a defect file info"""
        mockmrc.return_value = 2000, 2000
        setup_tomo_dirs()
        converter = PipelinerTiltSeriesGroupConverter(
            input_file=Path("MotionCorr/job002/corrected_tilt_series.star")
        )
        converter.get_tilt_series_files()
        converter.do_conversion()

        amc_dict = {}
        for i in converter.all_movie_collections:
            amc_dict[i] = converter.all_movie_collections[i].model_dump()
        with open(self.test_data / "mocorr_all_movie_cols.json") as amc:
            amc_actual = json.load(amc)
        assert amc_dict == amc_actual

        ats_dict = {}
        for i in converter.all_tilt_series:
            ats_dict[i] = converter.all_tilt_series[i].model_dump()
        with open(self.test_data / "mocorr_all_tilt_series.json") as ats:
            ats_actual = json.load(ats)
        assert ats_dict == ats_actual

    @unittest.skip("Need to fix Affine missing fields in model_dump()")
    @patch("tomobabel.converters.relion.relion_convert_tilt_series.get_mrc_dims")
    def test_converter_do_conversion_align_job(self, mockmrc):
        mockmrc.return_value = 2000, 2000
        setup_tomo_dirs()
        converter = PipelinerTiltSeriesGroupConverter(
            input_file=Path("AlignTiltSeries/job005/aligned_tilt_series.star")
        )
        converter.get_tilt_series_files()
        converter.do_conversion()

        amc_dict = {}
        for i in converter.all_movie_collections:
            amc_dict[i] = converter.all_movie_collections[i].model_dump()
        with open(self.test_data / "import_all_movie_cols.json") as amc:
            amc_actual = json.load(amc)
        assert amc_dict == amc_actual

        ats_dict = {}
        for i in converter.all_tilt_series:
            ats_dict[i] = converter.all_tilt_series[i].model_dump()
        with open(self.test_data / "import_all_tilt_series.json") as ats:
            ats_actual = json.load(ats)
        assert ats_dict == ats_actual

    @patch("tomobabel.converters.relion.relion_convert_tilt_series.get_mrc_dims")
    def test_main_with_outputs_dir(self, mockdims):
        mockdims.return_value = 2000, 2000
        setup_tomo_dirs()
        tilt_series_main(
            in_args=[
                "--input_starfile",
                "CtfFind/job003/tilt_series_ctf.star",
                "--output",
                "outdir/",
                "--gain_reference",
                "my_gain_file.mrc",
                "--defect_file",
                "my_defect_file.mrc",
            ]
        )
        wrote_files = list(Path("outdir").glob("*.json"))
        for f in [
            "TS_01_movie_collection.json",
            "TS_01_tilt_series.json",
            "TS_03_movie_collection.json",
            "TS_03_tilt_series.json",
            "TS_43_movie_collection.json",
            "TS_43_tilt_series.json",
            "TS_45_movie_collection.json",
            "TS_45_tilt_series.json",
            "TS_54_movie_collection.json",
            "TS_54_tilt_series.json",
        ]:
            assert Path("outdir") / f in wrote_files, Path(f)
        # check one movies file
        with open("outdir/TS_01_movie_collection.json") as wrote:
            wrote_data = json.load(wrote)
        with open(self.test_data / "TS_01_movie_collections.json") as exp:
            expected = json.load(exp)
        assert wrote_data == expected

        # check one tilt series file
        with open("outdir/TS_01_tilt_series.json") as wrote:
            wrote_data = json.load(wrote)
        with open(self.test_data / "TS_01_tilt_series.json") as exp:
            expected = json.load(exp)
        assert wrote_data == expected

    @unittest.skip("Need to fix Affine missing fields in model_dump()")
    def test_tilt_series_converter_main(self):
        pass


if __name__ == "__main__":
    unittest.main()
