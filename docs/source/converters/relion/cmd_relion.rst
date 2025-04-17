RELION
------

*The module currently only handles tilt series, in the future it will be expanded for*
*other data types (Tomograms, Averages, and Annotations)*

Using the converter to prepare a ``Dataset``
********************************************

``relion_converter`` creates a SDF ``Dataset`` object for an entire RELION
project.

Run it with the following arguments:

``--tilt_series_starfile``: The file that contains metadata about all the tilt series in
the project. In RELION/pipeliner it has the node type `TiltSeriesGroupMetadata`.  This
file should be drawn from latest job in the project possible.  EX: Import/job001,
MotionCorr/job002, CtfFind/job003, ExcludeTiltImages/job004, and AlignTiltSeries/job005
all produce an appropriate input file; the one from job005 should be used.

``--tilt_series_names``: (optional) Which tilt series to operate on, if not specified
all the tilt series in the input file will be processed

``--output``: (optional): Where to write the json file with the converted data. If not
specified no file will be written.  ``relion_converter`` can also be used
as a module andreturns the ``Dataset`` object.

``--gain_reference``: (optional): Path to the gain reference image.  The way the RELION
directory is structured this information is only available in MotionCorrection jobs so
it must be explicitly set unless the job used for the input file is of the
MotionCorr type.

``--defect_file``: (optional): Path to the detector defect file. The way the RELION
directory is structured this information is only available in MotionCorrection jobs so
it must be explicitly set unless the job used for the input file is of the
MotionCorr type.

*In the future additional args will be added that allow the other data types (Tomogram,
Average, Annotation) to be included in the final ``Dataset``*

.. note::
 The converter is dependent on the RELION directory structure.  Individual starfiles will
 not work in isolation as they contain cross references to each other.

Example
*******

As a script:

.. code-block::

 python3 relion_converter --tilt_series_starfile AlignTiltSeries/job005/aligned_tilt_series.star --output dataset.json --gain_reference my_gain_file.mrc --defect_file my_defect_file.mrc

This writes ``dataset.json`` containing the CZII ``Dataset`` object for the project

As a module:

.. code-block::

 from metadata_conversion import relion_converter

 czii_dataset = relion_converter.main(
    [
        "--tilt_series_starfile",
        "AlignTiltSeries/job005/aligned_tilt_series.star",
        "--gain_reference",
        "my_gain_file.mrc",
        "--defect_file",
        "my_defect_file.mrc",
    ]
 )

This returns the ``Dataset`` object

Using individual type converters
********************************
``relion_converter`` calls individual type converters for each of the
main data types, these can also be used in isolation.

.. list-table:: Type converters
   :header-rows: 1

   * - Data type
     - Converter
     - Object returned
   * - Tilt series movie frames
     - ``converters.convert_tilt_series``
     - ``PipelinerTiltSeriesGroupConverter``
   * - Tilt series
     - ``converters.convert_tilt_series``
     - ``PipelinerTiltSeriesGroupConverter``
   * - Tomograms
     - *Not written yet*
     - *n/a*
   * - Averages
     - *Not written yet*
     - *n/a*
   * - Annotations
     - *Not written yet*
     - *n/a*


**Example of using a type converter**

In this example the RELION tomography tutorial data is used.
``AlignTiltSeries/job005/aligned_tilt_series.star`` is used as in input.  This file
contains data about five tilt series called `TS_01`, `TS_03`, `TS_43`, `TS_45`, `TS_54`,

As a script:

.. code-block::

 python3 convert_tilt_series.py --input_starfile AlignTiltSeries/job005/aligned_tilt_series.star --output output_dir/ --gain_reference my_gain.mrc --defect_file my_defect.mrc

This will write the following files:

- ``output_dir/TS_01_movie_collection.json``
- ``output_dir/TS_01_tilt_series.json``
- ``output_dir/TS_03_movie_collection.json``
- ``output_dir/TS_03_tilt_series.json``
- ``output_dir/TS_43_movie_collection.json``
- ``output_dir/TS_43_tilt_series.json``
- ``output_dir/TS_45_movie_collection.json``
- ``output_dir/TS_45_tilt_series.json``
- ``output_dir/TS_54_movie_collection.json``
- ``output_dir/TS_54_tilt_series.json``

The ``_movie_collection`` files contain a CZII ``MovieStackCollection`` object for the named tilt series

The ``_tilt_series`` files contain a CZII ``TiltSeries`` object forthe named tilt series

As a module:

.. code-block::

 from metadata_conversion.converters import convert_tilt_series

 converter = convert_tilt_series.main(
    [
        "--input_starfile"
        "AlignTiltSeries/job005/aligned_tilt_series.star",
        "--gain_reference",
        "my_gain.mrc",
        "--defect_file",
        "my_defect.mrc,
    ]
 )
 >>> converter.all_movie_collections
    {
        "TS_01": MovieCollection,
        "TS_03": MovieCollection,
        "TS_35": MovieCollection,
        "TS_45": MovieCollection,
        "TS_54": MovieCollection,
    }
 >>> converter.all_tilt_series
    {
        "TS_01": TiltSeries,
        "TS_03": TiltSeries,
        "TS_35": TiltSeries,
        "TS_45": TiltSeries,
        "TS_54": TiltSeries,
    }


Documentation

.. toctree::
   :maxdepth: 1

   relion_script

.. toctree::
   :maxdepth: 1

   relion_ts_converter

