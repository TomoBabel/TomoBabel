import argparse
import json
import sys
from pathlib import Path
from typing import Optional, List

from tomobabel.converters.relion.relion_convert_tilt_series import (
    PipelinerTiltSeriesGroupConverter,
)
from tomobabel.models.top_level import DataSet, Region, TomoImageSet


def get_tilt_series_data(
    input_file: str,
    tilt_series: Optional[List[str]],
    gain_file: Optional[str],
    defect_file: Optional[str],
) -> PipelinerTiltSeriesGroupConverter:
    """Get data about the tilt series, including movie frames

    Args:
        input_file (str): Path to the star file containing the list of tilt series
            TiltSeriesGroupMetadata node in RELION/Pipeliner
        tilt_series (Optional[List[str]]): Names of the tilt series to get data about
            if None all tilt series in the input file will be included
        gain_file (Optional[str]): Path for the gain reference file. This info can only
            be gathered automatically if the input file is for a MotionCorr job, so it
            must be specified
        defect_file (Optional[str]): Path for the detector defect file. This info can
            only be gathered automatically if the input file is for a MotionCorr job,
            so it must be specified

    """
    converter = PipelinerTiltSeriesGroupConverter(
        input_file=Path(input_file), gain_file=gain_file, defect_file=defect_file
    )
    converter.do_conversion(tilt_series_names=tilt_series)
    return converter


# TODO: currently only does tilt series, need to add tomograms, particles, averages, and
#  other data  types
def get_arguments() -> argparse.ArgumentParser:
    """Get the args for running

    --tilt_series_starfie: The TiltSeriesGroupMetadata node to operate on
    --tilt_series_names (optional): Which tilt series to operate on, if not use then
        operate on all
    --output (optional): Where to write the json file with the converted data
    --gain_reference (optional): Path to the gain reference image
    --defect_file (optional): Path to the defect file

    Returns:
        argparse.ArgumentParser: Contains the args

    """
    parser = argparse.ArgumentParser(description="RELION tilt series -> CETS converter")

    parser.add_argument(
        "--tilt_series_starfile",
        "-i",
        help="RELION tilt series group STAR file ",
        nargs="?",
        required=True,
    )
    parser.add_argument(
        "--tilt_series_names",
        "-t",
        help="Which tilt series to operate on, if blank all will be processed",
        nargs="+",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Name of the desire output file",
        nargs="?",
        metavar="Output file name",
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


def main(in_args=None) -> DataSet:
    """Do conversions and output a single czii Dataset object

    Each tilt series/tomogram is given a Region.

    Returns:
        Dataset: CETS Dataset object
    """
    if in_args is None:
        in_args = sys.argv[1:]
    parser = get_arguments()
    args = parser.parse_args(in_args)  # create the DataSet object
    regions = []

    # write the tilt series data to the Dataset
    converted_tilt_series = get_tilt_series_data(
        args.tilt_series_starfile,
        args.tilt_series_names,
        args.gain_reference,
        args.defect_file,
    )
    for tilt_series in converted_tilt_series.all_tilt_series:
        movie_stack_collections = converted_tilt_series.all_movie_collections[
            tilt_series
        ]
        tiltseries_container = TomoImageSet(raw_movies=movie_stack_collections)
        region = Region(tilt_series=[tiltseries_container])
        regions.append(region)
    dataset = DataSet(regions=regions)

    # TODO: Add the other data types to the appropriate Regions

    # write output if requested
    if args.output:
        out = Path(args.output_name)
        if out.suffix != ".json":
            out = Path(args.output_name + ".json")
        out.parent.mkdir(exist_ok=True)
        data = dataset.model_dump()
        with open(out, "w") as outfile:
            json.dump(data, outfile, indent=4)

    return dataset


if __name__ == "__main__":
    main()
