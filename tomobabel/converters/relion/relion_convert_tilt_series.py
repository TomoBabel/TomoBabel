import argparse
import json
import logging
import sys
import numpy as np
from pathlib import Path
from typing import Optional, List, Dict, Tuple

from gemmi import cif

from tomobabel.models.tomo_images import (
    MovieStackCollection,
    MovieStack,
    MovieFrame,
    CTFMetadata,
    GainFile,
    DefectFile,
    TiltSeriesMicrograph,
    TiltSeriesMicrographStack,
    MovieStackSet,
)
from tomobabel.models.top_level import TomoImageSet
from tomobabel.models.tomo_images import TiltSeriesMicrographAlignment
from tomobabel.models.transformations import (
    TranslationTransform,
    MotionCorrectionTransformation,
)
from tomobabel.models.annotation import Annotation
from tomobabel.utils import get_mrc_dims, NumpyEncoder

"""Convert a RELION starfile describing a set of tomographic tilt series into CETS
metadata format.

The master tilt series starfile should have the following header format:

    data_global
    loop_
    _rlnTomoName
    _rlnTomoTiltSeriesStarFile
    _rlnVoltage
    _rlnSphericalAberration
    _rlnAmplitudeContrast
    _rlnMicrographOriginalPixelSize
    _rlnTomoHand
    _rlnOpticsGroupName

This file references a tilt_series starfile for each tilt series. Additional headers
are added to this file by each job in the tilt series processing procedure -MotionCorr
CTF, Bad tilt exclusion, and Alignment.

The headers after all steps are applied look like this:

    data_<TILTSERIES_NAME>
    loop_
    _rlnMicrographMovieName
    _rlnTomoTiltMovieFrameCount
    _rlnTomoNominalStageTiltAngle
    _rlnTomoNominalTiltAxisAngle
    _rlnMicrographPreExposure
    _rlnTomoNominalDefocus
    _rlnCtfPowerSpectrum
    _rlnMicrographNameEven
    _rlnMicrographNameOdd
    _rlnMicrographName
    _rlnMicrographMetadata
    _rlnAccumMotionTotal
    _rlnAccumMotionEarly
    _rlnAccumMotionLate
    _rlnCtfImage
    _rlnDefocusU
    _rlnDefocusV
    _rlnCtfAstigmatism
    _rlnDefocusAngle
    _rlnCtfFigureOfMerit
    _rlnCtfMaxResolution
    _rlnCtfIceRingDensity
    _rlnTomoXTilt
    _rlnTomoYTilt
    _rlnTomoZRot
    _rlnTomoXShiftAngst
    _rlnTomoYShiftAngst

The conversion is dependent on the tilt series starfiles and the files they refer to
existing at the locations in the files, otherwise many pieces of data will not be able
to be collected
"""

logger = logging.getLogger(__name__)


class RelionTiltSeriesMovie(object):
    """A movie that represents one tilt image in the tilt series

    Attributes:
        dose_per_frame (float): In e-/Å^2
        stack_file_path (Path): Path to the MRC stack with the frames
        czii_movie_frames (List[MovieFrame]): A list of the created CETS MovieFrame objs
            for each frame of the movie. Initially empty.
        tilt (float): Nominal tilt angle, in degrees.
        pre_exp (float): In e-/Å^2
        height (int): Image y dimension in px
        width (int): Image x dimension in px
        n_frames (int): Number of frames in the movie IE: Stack z dimension
        apix (float): Movie pixel size in Å/px
        czii_movie_stack (MovieStack): A CETS MovieStack object that will hold the
            MovieFrames
    """

    def __init__(
        self,
        dose_per_frame: float,
        stack_file_path: Path,
        tilt: float,
        pre_exp: float,
        n_frames: int,
        apix: float,
        czii_movie_frames: Optional[List[MovieFrame]] = None,
    ) -> None:
        self.dose_per_frame = dose_per_frame
        self.stack_file_path = str(stack_file_path)
        self.czii_movie_frames = [] if czii_movie_frames is None else czii_movie_frames
        self.tilt = tilt
        self.pre_exp = pre_exp
        try:
            dims = get_mrc_dims(stack_file_path)
        except FileNotFoundError:
            dims = None, None, None
        self.height = dims[1]
        self.width = dims[0]
        self.n_frames = n_frames
        self.apix = apix
        self.czii_movie_stack = MovieStack(frame_images=[], path=str(stack_file_path))


class PipelinerTiltSeriesGroupConverter(object):
    """An object for conversion of a pipeliner TiltSeriesGroupMetadata node into CETS
    format.

    Attributes:
        input_file (Path): The RELION tilt series starfile. TiltSeriesGroupMetadata node
            type
        all_movie_collections (Dict[str, MovieStackCollection]): The CETS
            MovieStackCollection for each tiltseries in the input file
            {tilt_series_name: MovieStackCollection}
        all_tilt_series (Dict[str, TiltSeries]): The CETS TiltSeries for each tiltseries
            in the input file.
        ts_files (Dict[str, str]): The TiltSeriesMetadata node for each tilt series in
            the input file. {tilt_series_name: file path}
        gain_file (Optional[str]): Path to a gain reference file, which must be
            explicitly defined unless the input is from a motion corr job
        defect file (Optional[str]): Path to a detector defect file, which must be
            explicitly defined unless the input is from a motion corr job
    """

    def __init__(
        self,
        input_file: Path,
        gain_file: Optional[str] = None,
        defect_file: Optional[str] = None,
        motion_correction_job: Optional[str] = None,
    ) -> None:
        self.input_file = input_file
        self.all_movie_collections: Dict[str, MovieStackCollection] = {}
        self.all_tilt_series: Dict[str, TomoImageSet] = {}
        self.ts_files: Dict[str, str] = {}
        self.gain_file = gain_file
        self.defect_file = defect_file
        self.motion_correction_job = motion_correction_job

    def get_motioncorr_transformation(self, stack_name: str, frame: int):
        """
        Placeholder function that gets the motion corr transformation for a frame
        Need to figure out how to extract this info from the eps files in
        self.motioncorrection_job...
        """
        # TODO: Replace this placeholder with actual function
        return MotionCorrectionTransformation(
            trans_matrix=np.identity(2),
            annotations=[
                Annotation(
                    description="<PLACEHOLDER FOR TRANSFORMATION DONE BY MOTIONCORR>"
                )
            ],
        )

    def get_movies_data(
        self, tilt_series_block: cif.Block
    ) -> List[RelionTiltSeriesMovie]:
        """Get a RelionTiltSeriesMovie object for each tilt image in a tilt series

        Args:
            tilt_series_block (cif.Block): The data block from the
                TiltSeriesMetadata node for a single tilt series

        Returns:
            List[RelionTiltSeriesMovie]: A RelionTiltSeriesMovie for each tilt image in
                the tilt series

        """
        movie_data = tilt_series_block.find(
            "_rln",
            [
                "MicrographMovieName",
                "TomoNominalStageTiltAngle",
                "MicrographPreExposure",
                "TomoTiltMovieFrameCount",
                "MicrographPreExposure",
                "TomoTiltMovieFrameCount",
            ],
        )

        # get pixel sizes
        ts_file = cif.read_file(str(self.input_file)).find_block("global")
        ts_loop = ts_file.find(
            prefix="_rln",
            tags=["TomoName", "MicrographOriginalPixelSize"],
        )
        pxsizes = dict(list(ts_loop))

        exposures = [float(x[2]) for x in movie_data]
        all_movs = [x[0] for x in movie_data]
        frame_counts = [int(x[3]) for x in movie_data]
        tilts = [float(x[1]) for x in movie_data]
        pre_exp = [float(x[4]) for x in movie_data]
        n_frames = [int(x[5]) for x in movie_data]
        img_dose_per_frame = {}
        for n, dose in enumerate(exposures[:-1]):
            add_dose = exposures[n + 1] - dose
            dpf = add_dose / frame_counts[n]
            img_dose_per_frame[all_movs[n]] = dpf

        # assume the last frame move has the same dose rate as prev
        img_dose_per_frame[all_movs[-1]] = img_dose_per_frame[all_movs[-2]]

        tilt_movies = []
        for mov in all_movs:
            index = all_movs.index(mov)
            tilt_movies.append(
                RelionTiltSeriesMovie(
                    stack_file_path=Path(mov),
                    dose_per_frame=img_dose_per_frame[mov],
                    tilt=tilts[index],
                    pre_exp=pre_exp[index],
                    n_frames=n_frames[index],
                    apix=float(pxsizes[tilt_series_block.name]),
                )
            )

        return tilt_movies

    @staticmethod
    def get_ctf_data(data_block: cif.Block, index: int) -> Optional[CTFMetadata]:
        """Get CTF information for a tilt series

        Args:
            tilt_series_block (cif.Block): The data block from the
                TiltSeriesMetadata node for a single tilt series
            index (int): Which tilt image to get the CTF data for

        Returns:
            Optional[CTFMetadata]: A CETS CTFMetadata for the tilt image
        """
        ctf_obj: Optional[CTFMetadata] = None

        if data_block.find("_rln", ["DefocusU"]):
            ctf_data = data_block.find(
                "_rln",
                [
                    "DefocusU",
                    "DefocusV",
                    "DefocusAngle",
                ],
            )
            ctf_obj = CTFMetadata(
                defocus_u=float(ctf_data[index][0]),
                defocus_v=float(ctf_data[index][1]),
                defocus_angle=float(ctf_data[index][2]),
            )
        return ctf_obj

    def get_gain_ref_and_defect_file(
        self,
    ) -> Tuple[Optional[GainFile], Optional[DefectFile]]:
        """Get the gain reference and defect files for a tilt series

        These are associated with MotionCorr jobs in RELION.

        These data are not in the starfile and need to be taken from the job.star
        parameters file RELION writes in the MotionCorr job directory.  If the data dir
        structure is not in the RELION format this will not be possible.

        Returns:
            Tuple[Optional[GainFile], Optional[DefectFile]]: CETS GainFile and
                DefectFile objects for the tilt series

        """
        job_dir = self.input_file.parent
        jobstar = job_dir / "job.star"
        if not jobstar.is_file():
            return None, None
        try:
            params = cif.read_file(str(jobstar))
            jobtype = params.find_block("job").find_pair("_rlnJobTypeLabel")[1]
            # if the job is a motioncorr job use it and ignore the defined files
            if jobtype.startswith("relion.motioncorr"):
                paramsblock = params.find_block("joboptions_values")
                params_loop = paramsblock.find(
                    prefix="_rln", tags=["JobOptionVariable", "JobOptionValue"]
                )
                for i in params_loop:
                    if i[0] == "fn_gain_ref":
                        self.gain_file = (
                            cif.as_string(i[1]) if cif.as_string(i[1]) else None
                        )
                    if i[0] == "fn_defect":
                        self.defect_file = (
                            cif.as_string(i[1]) if cif.as_string(i[1]) else None
                        )
            gainfile, defectfile = None, None
            if self.gain_file is not None:
                gain_height, gain_width = get_mrc_dims(Path(self.gain_file))[:2]
                gainfile = GainFile(
                    path=self.gain_file, height=gain_height, width=gain_width
                )
            if self.defect_file is not None:
                defect_height, defect_width = get_mrc_dims(Path(self.defect_file))[:2]
                defectfile = DefectFile(
                    path=self.defect_file, height=defect_height, width=defect_width
                )
            return gainfile, defectfile

        except Exception:
            return None, None

    @staticmethod
    def get_alignment_transformation_data(
        data_block: cif.Block, index: int, apix: float
    ) -> TiltSeriesMicrographAlignment:
        """Get transformation data for a single frame in a tilt series movie

        Args:
            data_block(cif.Block): From the tilt series starfile
            index (int): The index of the frame in the data_block
            apix (float): The movie pixel size

        Returns:
            Optional[Affine]: A CETS Affine object with the transformation or None if
                it couldn't be calculated.

        """
        transformation_obj = TiltSeriesMicrographAlignment()
        trans_data = data_block.find(
            "_rln",
            [
                "TomoXShiftAngst",
                "TomoYShiftAngst",
                "TomoXTilt",
                "TomoyTilt",
                "TomoZRot",
            ],
        )
        if trans_data:
            xshift, yshift, xtilt, ytilt, rot = [float(x) for x in trans_data[index]]
            xshift = xshift / apix  # TODO: make sure that this should be in pixels
            yshift = yshift / apix  # TODO: make sure that this should be in pixels
            transformation_obj.y_tilt = ytilt
            transformation_obj.x_tilt = xtilt
            transformation_obj.z_rot = rot
            transformation_obj.translation = TranslationTransform(
                trans_matrix=np.array([[xshift, 0], [0, yshift]])
            )

        return transformation_obj

    def make_movie_collections(
        self, tilt_series_block: cif.Block, section: int, mov: RelionTiltSeriesMovie
    ) -> None:
        """Make a CETS MovieStackCollection Object for each tilt series and update its
        RelionTiltSeriesMovie object

        CTF and transformation are the same for every frame in the movie

        Args:
            tilt_series_block (cif.Block): The data block from the
                TiltSeriesMetadata node for a single tilt series
            mov (RelionTiltSeriesMovie): The movie object to update
        """
        ctf_obj = self.get_ctf_data(tilt_series_block, section)
        mov.czii_movie_frames = []
        for n in range(mov.n_frames):
            mocorrxform = self.get_motioncorr_transformation(
                stack_name=mov.stack_file_path,
                frame=n,
            )
            mov.czii_movie_frames.append(
                MovieFrame(
                    path=mov.stack_file_path,
                    section=n,
                    nominal_tilt_angle=mov.tilt,
                    accumulated_dose=mov.dose_per_frame * float(n + 1) + mov.pre_exp,
                    height=mov.height,
                    width=mov.width,
                    ctf_metadata=ctf_obj,
                    motion_correction_transformations=[mocorrxform],
                )
            )

        # update the MovieStack
        mov.czii_movie_stack.frame_images = mov.czii_movie_frames

    def make_tilt_series_object(self, path, stacks) -> TiltSeriesMicrographStack:
        """Make a CETS TiltSeriesMicrographStack object for a tilt series

        Args:
            path (str): The path to the MRC file for the tilt series stack
            stacks (MovieStackSet): The CETS MovieStackSet objects that contain
                the movie frames for the tilt images in the tilt series
        Returns:
            TiltSeriesMicrographStack: A CETS tilt serie object for the tilt series
        """
        ts_obj = TiltSeriesMicrographStack(path=path, micrographs=[])
        for mss in stacks.movie_stacks:
            img = mss.frame_images[-1]
            proj_img = TiltSeriesMicrograph(
                path=img.path,
                nominal_tilt_angle=img.nominal_tilt_angle,
                total_accumulated_dose=img.accumulated_dose,
                ctf_metadata=img.ctf_metadata,
                width=img.width,
                height=img.height,
            )
            ts_obj.micrographs.append(proj_img)  # type: ignore  # always an empty list
        return ts_obj

    def get_tilt_series_files(self):
        """
        Get the names of the tilt series starfiles for all tilt series in the input

        These are TiltSeriesMetadata node type. Updates self.ts_files with a dict:
        {tilt series name: TiltSeriesMetadata star file}

        """
        infile_cif = cif.read_file(str(self.input_file))
        glob_block = infile_cif.find_block("global")
        ts_files = list(glob_block.find("_rln", ["TomoName", "TomoTiltSeriesStarFile"]))
        self.ts_files = {key: val for key, val in ts_files}

    def do_conversion(self, tilt_series_names: Optional[List[str]] = None) -> None:
        """Get the data in tilt series in CETS data model format

        Args:
            tilt_series_names (Optional[List[str]]): Which tilt series to get the data
                for.  If None operates on all tilt series in the input file.
        """
        self.get_tilt_series_files()
        # decide which tilt series to operate on, if user didn't specify any do all of
        # them
        if tilt_series_names is not None:
            ts_starfiles = {}
            errs = []
            for tilt_series in tilt_series_names:
                try:
                    ts_starfiles[tilt_series] = self.ts_files[tilt_series]
                except KeyError:
                    errs.append(tilt_series)
                self.ts_files = ts_starfiles

            if errs:
                missing = ", ".join(errs)
                raise ValueError(
                    f"Tilt series {missing} not found in tilt series group starfile"
                )

        # operate on each tilt series separately
        for ts_name in self.ts_files.keys():
            # read the starfile for that tilt series and get data
            tilt_series_sf = cif.read_file(self.ts_files[ts_name])
            tilt_series_block = tilt_series_sf.find_block(ts_name)

            # get an RelionTiltSeriesMovie object to handle each movie
            movies = self.get_movies_data(tilt_series_block)

            # make the MovieFrame Object for each frame in every movie
            for n, mov in enumerate(movies):
                self.make_movie_collections(tilt_series_block, n, mov)

            # make the MovieStackSet objects
            ms_series = MovieStackSet(
                movie_stacks=[x.czii_movie_stack for x in movies],
                annotations=[
                    Annotation(
                        description=f"Raw images for tilt series name: {ts_name}"
                    )
                ],
            )
            gainfile, defectfile = self.get_gain_ref_and_defect_file()
            collection = MovieStackCollection(
                movie_stack_sets=[ms_series],
                gain_file=gainfile,
                defect_file=defectfile,
            )
            self.all_movie_collections[str(ts_name)] = collection

            # Make a TiltSeries object for the tilt series
            ts_obj = self.make_tilt_series_object(
                path=self.ts_files[ts_name], stacks=ms_series
            )
            self.all_tilt_series[str(ts_name)] = ts_obj


def get_arguments() -> argparse.ArgumentParser:
    """Get the args for running

    --input_starfie: The TiltSeriesGroupMetadata node to operate on
    --tilt_series (optional): Which tilt series to operate on, if not use then operate
        on all
    --output (optional): Where to write the json file with the converted data

    Returns:
        argparse.ArgumentParser: Contains the args

    """
    parser = argparse.ArgumentParser(description="RELION tilt series -> CETS converter")

    parser.add_argument(
        "--input_starfile",
        "-i",
        help="RELION tiltseries group STAR file ",
        nargs="?",
        required=True,
    )
    parser.add_argument(
        "--tilt_series",
        "-t",
        help="Which tilt series to operate on, if blank all will be processed",
        nargs="+",
    )
    parser.add_argument(
        "--output",
        "-o",
        help=(
            "Output prefix. Files will be named {output_prefix}_tilt_series.json and"
            " {output_prefix}_movie_collections.json.  A dir name can be part of the"
            " prefix, it will be created as necessary. If just a dir name is provided"
            " the files will be called tilt_series.json and movie_collections.json."
        ),
        nargs="?",
        metavar="Output prefix",
    )

    parser.add_argument(
        "--gain_reference",
        help="Path to a gain reference file for the micrographs",
        nargs="?",
        required=False,
        metavar="Gain reference",
    )

    parser.add_argument(
        "--defect_file",
        help="Path to a defect file for the detector",
        nargs="?",
        required=False,
        metavar="Defect file",
    )

    return parser


def main(in_args=None) -> PipelinerTiltSeriesGroupConverter:
    if in_args is None:
        in_args = sys.argv[1:]
    parser = get_arguments()
    args = parser.parse_args(in_args)

    # get converter object and do the conversion
    converter = PipelinerTiltSeriesGroupConverter(
        Path(args.input_starfile), args.gain_reference, args.defect_file
    )
    converter.do_conversion(args.tilt_series)

    if args.output:
        out = Path(args.output)
        if bool(Path(args.output).suffix):
            raise ValueError("Output should be a prefix or dir name, not a file name")
        if args.output.endswith("/"):
            out.mkdir(parents=True, exist_ok=True)

        for tilt_series in converter.all_tilt_series:
            if out.is_dir():
                outfile = out / f"{tilt_series}_tilt_series.json"
            else:
                outfile = Path(str(out) + f"_{tilt_series}_tilt_series.json")
            ts_dict = converter.all_tilt_series[tilt_series].model_dump()
            with open(outfile, "w") as to_write:
                json.dump(ts_dict, to_write, indent=4, cls=NumpyEncoder)

        for movie_collection in converter.all_movie_collections:
            if out.is_dir():
                outfile = out / f"{movie_collection}_movie_collection.json"
            else:
                outfile = Path(str(out) + f"_{movie_collection}_movie_collection.json")
            mc_dict = converter.all_movie_collections[movie_collection].model_dump()
            with open(outfile, "w") as to_write:
                json.dump(mc_dict, to_write, indent=4, cls=NumpyEncoder)

    return converter
