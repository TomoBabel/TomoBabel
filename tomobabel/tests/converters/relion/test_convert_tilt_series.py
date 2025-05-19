import json
import unittest
from deepdiff import DeepDiff
from pathlib import Path, PosixPath
from unittest.mock import patch
from numpy import array
import numpy as np
from gemmi import cif

from tomobabel.converters.relion.relion_convert_tilt_series import (
    RelionTiltSeriesMovie,
    PipelinerTiltSeriesGroupConverter,
    main as tilt_series_main,
)
from tomobabel.models.tomo_images import (
    MovieStack,
    CTFMetadata,
    MovieFrame,
    GainFile,
    DefectFile,
    TiltSeriesMicrographAlignment,
)
from tomobabel.models.transformations import Transformation
from tomobabel.models.basemodels import Annotation
from tomobabel.tests.converters.relion.relion_testing_utils import TomoBabelRelionTest
from tomobabel.utils import clean_dict


class CziiTiltSeriesConverterTest(TomoBabelRelionTest):

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
            "czii_movie_stack": MovieStack(frame_images=[], path="my_stackfile.mrc"),
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
            "motion_correction_job": None,
        }

    def test_converter_get_tilt_series_dict(self):
        self.setup_tomo_dirs()
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
        self.setup_tomo_dirs()
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
                frame_images=[], path="frames/TS_01_000_0.0.mrc"
            ),
        }

    def test_converter_get_ctf_data(self):
        self.setup_tomo_dirs()
        ts = cif.read_file("CtfFind/job003/tilt_series/TS_01.star")
        block = ts.find_block("TS_01")
        converter = PipelinerTiltSeriesGroupConverter(
            input_file=Path("CtfFind/job003/tilt_series_ctf.star")
        )
        ctfdata = converter.get_ctf_data(block, 0)
        assert isinstance(ctfdata, CTFMetadata)
        assert ctfdata.model_dump(mode="json") == {
            "defocus_u": 38855.828125,
            "defocus_v": 38750.828125,
            "defocus_angle": 35.154533,
            "defocus_handedness": -1,
            "annotations": [],
        }

    def test_converter_get_transformation_data(self):
        self.setup_tomo_dirs()
        ts = cif.read_file("AlignTiltSeries/job005/tilt_series/TS_01.star")
        block = ts.find_block("TS_01")
        converter = PipelinerTiltSeriesGroupConverter(
            input_file=Path("CtfFind/job003/corrected_tilt_series.star")
        )
        transdata = converter.get_alignment_transformation_data(
            data_block=block, index=0, apix=0.675
        )
        assert isinstance(transdata, TiltSeriesMicrographAlignment)
        assert np.allclose(
            transdata.translation.trans_matrix,
            array([[51.62312741, 0.0], [0.0, 160.73987704]]),
        )
        assert transdata.x_tilt == 0.0
        assert transdata.y_tilt == -57.0
        assert transdata.z_rot == 85.032958

    @patch("tomobabel.converters.relion.relion_convert_tilt_series.get_mrc_dims")
    def test_converter_get_gain_and_defect_files(self, mockdims):
        self.setup_tomo_dirs()
        mockdims.return_value = 2000, 2000, 1

        converter = PipelinerTiltSeriesGroupConverter(
            input_file=Path("MotionCorr/job002/tilt_series.star")
        )
        gain, defect = converter.get_gain_ref_and_defect_file()
        assert gain == GainFile(path="my_gain_file.mrc", height=2000, width=2000)
        assert defect == DefectFile(path="my_defect_file.mrc", height=2000, width=2000)

    def test_converter_make_movie_collections_data(self):
        self.setup_tomo_dirs()
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
        expected = [
            MovieFrame(
                annotations=[],
                width=None,
                height=None,
                pixel_size=None,
                path="my_stack.mrc",
                section=0,
                nominal_tilt_angle=3.5,
                accumulated_dose=2.5,
                ctf_metadata=None,
                motion_correction_transformations=[
                    Transformation(
                        annotations=[
                            Annotation(
                                type="text",
                                description="<PLACEHOLDER>",
                            )
                        ],
                        transform_type="translation",
                        trans_matrix=array([[1.0, 0.0], [0.0, 1.0]]),
                    )
                ],
            ),
            MovieFrame(
                annotations=[],
                width=None,
                height=None,
                pixel_size=None,
                path="my_stack.mrc",
                section=1,
                nominal_tilt_angle=3.5,
                accumulated_dose=3.5,
                ctf_metadata=None,
                motion_correction_transformations=[
                    Transformation(
                        annotations=[
                            Annotation(
                                type="text",
                                description="<PLACEHOLDER>",
                            )
                        ],
                        transform_type="translation",
                        trans_matrix=array([[1.0, 0.0], [0.0, 1.0]]),
                    )
                ],
            ),
            MovieFrame(
                annotations=[],
                width=None,
                height=None,
                pixel_size=None,
                path="my_stack.mrc",
                section=2,
                nominal_tilt_angle=3.5,
                accumulated_dose=4.5,
                ctf_metadata=None,
                motion_correction_transformations=[
                    Transformation(
                        annotations=[
                            Annotation(
                                type="text",
                                description="<PLACEHOLDER>",
                            )
                        ],
                        transform_type="translation",
                        trans_matrix=array([[1.0, 0.0], [0.0, 1.0]]),
                    )
                ],
            ),
            MovieFrame(
                annotations=[],
                width=None,
                height=None,
                pixel_size=None,
                path="my_stack.mrc",
                section=3,
                nominal_tilt_angle=3.5,
                accumulated_dose=5.5,
                ctf_metadata=None,
                motion_correction_transformations=[
                    Transformation(
                        annotations=[
                            Annotation(
                                type="text",
                                description="<PLACEHOLDER>",
                            )
                        ],
                        transform_type="translation",
                        trans_matrix=array([[1.0, 0.0], [0.0, 1.0]]),
                    )
                ],
            ),
            MovieFrame(
                annotations=[],
                width=None,
                height=None,
                pixel_size=None,
                path="my_stack.mrc",
                section=4,
                nominal_tilt_angle=3.5,
                accumulated_dose=6.5,
                ctf_metadata=None,
                motion_correction_transformations=[
                    Transformation(
                        annotations=[
                            Annotation(
                                type="text",
                                description="<PLACEHOLDER>",
                            )
                        ],
                        transform_type="translation",
                        trans_matrix=array([[1.0, 0.0], [0.0, 1.0]]),
                    )
                ],
            ),
            MovieFrame(
                annotations=[],
                width=None,
                height=None,
                pixel_size=None,
                path="my_stack.mrc",
                section=5,
                nominal_tilt_angle=3.5,
                accumulated_dose=7.5,
                ctf_metadata=None,
                motion_correction_transformations=[
                    Transformation(
                        annotations=[
                            Annotation(
                                type="text",
                                description="<PLACEHOLDER>",
                            )
                        ],
                        transform_type="translation",
                        trans_matrix=array([[1.0, 0.0], [0.0, 1.0]]),
                    )
                ],
            ),
            MovieFrame(
                annotations=[],
                width=None,
                height=None,
                pixel_size=None,
                path="my_stack.mrc",
                section=6,
                nominal_tilt_angle=3.5,
                accumulated_dose=8.5,
                ctf_metadata=None,
                motion_correction_transformations=[
                    Transformation(
                        annotations=[
                            Annotation(
                                type="text",
                                description="<PLACEHOLDER>",
                            )
                        ],
                        transform_type="translation",
                        trans_matrix=array([[1.0, 0.0], [0.0, 1.0]]),
                    )
                ],
            ),
            MovieFrame(
                annotations=[],
                width=None,
                height=None,
                pixel_size=None,
                path="my_stack.mrc",
                section=7,
                nominal_tilt_angle=3.5,
                accumulated_dose=9.5,
                ctf_metadata=None,
                motion_correction_transformations=[
                    Transformation(
                        annotations=[
                            Annotation(
                                type="text",
                                description="<PLACEHOLDER>",
                            )
                        ],
                        transform_type="translation",
                        trans_matrix=array([[1.0, 0.0], [0.0, 1.0]]),
                    )
                ],
            ),
            MovieFrame(
                annotations=[],
                width=None,
                height=None,
                pixel_size=None,
                path="my_stack.mrc",
                section=8,
                nominal_tilt_angle=3.5,
                accumulated_dose=10.5,
                ctf_metadata=None,
                motion_correction_transformations=[
                    Transformation(
                        annotations=[
                            Annotation(
                                type="text",
                                description="<PLACEHOLDER>",
                            )
                        ],
                        transform_type="translation",
                        trans_matrix=array([[1.0, 0.0], [0.0, 1.0]]),
                    )
                ],
            ),
            MovieFrame(
                annotations=[],
                width=None,
                height=None,
                pixel_size=None,
                path="my_stack.mrc",
                section=9,
                nominal_tilt_angle=3.5,
                accumulated_dose=11.5,
                ctf_metadata=None,
                motion_correction_transformations=[
                    Transformation(
                        annotations=[
                            Annotation(
                                type="text",
                                description="<PLACEHOLDER>",
                            )
                        ],
                        transform_type="translation",
                        trans_matrix=array([[1.0, 0.0], [0.0, 1.0]]),
                    )
                ],
            ),
        ]
        for n, x in enumerate(mov.czii_movie_frames):
            assert x.annotations == expected[n].annotations
            assert x.width == expected[n].width
            assert x.height == expected[n].height
            assert x.pixel_size == expected[n].pixel_size
            assert x.path == expected[n].path
            assert x.section == expected[n].section
            assert x.nominal_tilt_angle == expected[n].nominal_tilt_angle
            assert x.accumulated_dose == expected[n].accumulated_dose
            assert x.ctf_metadata == expected[n].ctf_metadata
            assert np.allclose(
                x.motion_correction_transformations[0].trans_matrix,
                expected[n].motion_correction_transformations[0].trans_matrix,
            )

    @patch("tomobabel.converters.relion.relion_convert_tilt_series.get_mrc_dims")
    def test_converter_do_conversion_import_job(self, mockmrc):
        mockmrc.return_value = 2000, 2000
        self.setup_tomo_dirs()
        converter = PipelinerTiltSeriesGroupConverter(
            input_file=Path("Import/job001/tilt_series.star")
        )
        converter.get_tilt_series_files()
        converter.do_conversion()

        amc_dict = {}
        for i in converter.all_movie_collections:
            amc_dict[i] = converter.all_movie_collections[i].model_dump(mode="json")
        with open(self.test_data / "import_all_movie_cols.json") as amc:
            amc_actual = json.load(amc)
        assert not DeepDiff(clean_dict(amc_dict), amc_actual, ignore_order=True)
        ats_dict = {}
        for i in converter.all_tilt_series:
            ats_dict[i] = converter.all_tilt_series[i].model_dump(mode="json")
        with open(self.test_data / "import_all_tilt_series.json") as ats:
            ats_actual = json.load(ats)
        assert not DeepDiff(clean_dict(ats_dict), ats_actual, ignore_order=True)

    @patch("tomobabel.converters.relion.relion_convert_tilt_series.get_mrc_dims")
    def test_converter_do_conversion_with_CTF_job(self, mockmrc):
        mockmrc.return_value = 2000, 2000
        self.setup_tomo_dirs()
        converter = PipelinerTiltSeriesGroupConverter(
            input_file=Path("CtfFind/job003/tilt_series_ctf.star")
        )
        converter.get_tilt_series_files()
        converter.do_conversion()

        amc_dict = {}
        for i in converter.all_movie_collections:
            amc_dict[i] = converter.all_movie_collections[i].model_dump(mode="json")
        with open(self.test_data / "ctf_all_movie_cols.json") as amc:
            amc_actual = json.load(amc)
        assert not DeepDiff(clean_dict(amc_dict), amc_actual, ignore_order=True)

        ats_dict = {}
        for i in converter.all_tilt_series:
            ats_dict[i] = converter.all_tilt_series[i].model_dump(mode="json")
        with open(self.test_data / "ctf_all_tilt_series.json") as ats:
            ats_actual = json.load(ats)
        assert not DeepDiff(clean_dict(ats_dict), ats_actual, ignore_order=True)

    @patch("tomobabel.converters.relion.relion_convert_tilt_series.get_mrc_dims")
    def test_converter_do_conversion_with_CTF_job_with_gain_and_defect(self, mockmrc):
        """Output should contain gain ref and defect file info, when provided"""
        mockmrc.return_value = 2000, 2000
        self.setup_tomo_dirs()
        converter = PipelinerTiltSeriesGroupConverter(
            input_file=Path("CtfFind/job003/tilt_series_ctf.star"),
            gain_file="my_gain_file.mrc",
            defect_file="my_defect_file.mrc",
        )
        converter.get_tilt_series_files()
        converter.do_conversion()

        amc_dict = {}
        for i in converter.all_movie_collections:
            amc_dict[i] = converter.all_movie_collections[i].model_dump(mode="json")
        with open(self.test_data / "ctf_all_movie_cols_gain_defect.json") as amc:
            amc_actual = json.load(amc)
        assert not DeepDiff(clean_dict(amc_dict), amc_actual, ignore_order=True)

        ats_dict = {}
        for i in converter.all_tilt_series:
            ats_dict[i] = converter.all_tilt_series[i].model_dump(mode="json")
        with open(self.test_data / "ctf_all_tilt_series.json") as ats:
            ats_actual = json.load(ats)
        assert not DeepDiff(clean_dict(ats_dict), ats_actual, ignore_order=True)

    @patch("tomobabel.converters.relion.relion_convert_tilt_series.get_mrc_dims")
    def test_converter_do_conversion_with_MotionCorr_job(self, mockmrc):
        """This one will have gain ref a defect file info"""
        mockmrc.return_value = 2000, 2000
        self.setup_tomo_dirs()
        converter = PipelinerTiltSeriesGroupConverter(
            input_file=Path("MotionCorr/job002/corrected_tilt_series.star")
        )
        converter.get_tilt_series_files()
        converter.do_conversion()

        amc_dict = {}
        for i in converter.all_movie_collections:
            amc_dict[i] = converter.all_movie_collections[i].model_dump(mode="json")
        with open(self.test_data / "mocorr_all_movie_cols.json") as amc:
            amc_actual = json.load(amc)
        assert not DeepDiff(clean_dict(amc_dict), amc_actual, ignore_order=True)

        ats_dict = {}
        for i in converter.all_tilt_series:
            ats_dict[i] = converter.all_tilt_series[i].model_dump(mode="json")
        with open(self.test_data / "mocorr_all_tilt_series.json") as ats:
            ats_actual = json.load(ats)
        assert not DeepDiff(clean_dict(ats_dict), ats_actual, ignore_order=True)

    @patch("tomobabel.converters.relion.relion_convert_tilt_series.get_mrc_dims")
    def test_converter_do_conversion_align_job(self, mockmrc):
        mockmrc.return_value = 2000, 2000
        self.setup_tomo_dirs()
        converter = PipelinerTiltSeriesGroupConverter(
            input_file=Path("AlignTiltSeries/job005/aligned_tilt_series.star")
        )
        converter.get_tilt_series_files()
        converter.do_conversion()

        amc_dict = {}
        for i in converter.all_movie_collections:
            amc_dict[i] = converter.all_movie_collections[i].model_dump(mode="json")
        with open(self.test_data / "aligned_ts_all_movie_cols.json") as amc:
            amc_actual = json.load(amc)
        assert not DeepDiff(clean_dict(amc_dict), amc_actual, ignore_order=True)

        ats_dict = {}
        for i in converter.all_tilt_series:
            ats_dict[i] = converter.all_tilt_series[i].model_dump(mode="json")
        with open(self.test_data / "aligned_ts_all_tilt_series.json") as ats:
            ats_actual = json.load(ats)
        assert not DeepDiff(clean_dict(ats_dict), ats_actual, ignore_order=True)

    @patch("tomobabel.converters.relion.relion_convert_tilt_series.get_mrc_dims")
    def test_main_with_outputs_dir(self, mockdims):
        mockdims.return_value = 2000, 2000
        self.setup_tomo_dirs()
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


if __name__ == "__main__":
    unittest.main()
