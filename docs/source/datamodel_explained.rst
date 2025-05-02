The CETS data model explained
=============================

The data model is based on geometry standards discussed at the April 2024 CZII/EBI
tomography standards meeting. (Cambridge, UK).

The full description is available in the
forthcoming :download:`whitepaper (draft) <../files/GeometryStandards.pdf>`

Data Hierarchy
--------------
The top level object is a ``DataSet``; all the data live here.

A ``DataSet`` contains multiple ``Region`` objects.  Each ``Region`` contains information
about part of a sample that was imaged.

Each ``Region`` contains a ``TomoImageSet`` with data about tomographic imaging
of that part of the sample and a ``NonTomoImageSet`` that contains any other imaging of
the region (EG: CLEM images or overview micrographs)

Inside ``TomoImageSet``
---------------------

**Raw Data**

The first layer is ``MovieStackCollection`` which contains info that applies to all the
subsequent images such as the gain file, defect file, and microscope/imaging info

Inside that are ``MovieStackSeries`` objects each corresponding to a tilt series. These
contain a ``MovieStack`` for each tilt image. Each ``MovieStack`` contains a ``MovieFrame``
for each frame in the movie.

**Aligned tilt series**

Aligned tilt series are stored in ``TiltSeriesSet`` containing ``TiltSeriesMicrographStack``
objects that contain a ``TiltSeriesMicrograph`` for each image (Merged movie for that tilt)

**Reconstructed Tomograms**

Any tomograms created from the data in this ``Region`` are stored in the ``TomogramSet``
object containing (you guessed it!) ``Tomogram`` objects

Inside each ``Tomogram`` object are ``SubTomogramSet`` and ``MapSet`` objects that
contain ``SubTomogram`` and ``Map`` objects associated with that tomogram.

**Annotations**

Every data object in the heierarchy has an ``annotations`` attribute that contains any
number of ``Annotation`` objects.  Which can contain anything from text or coordinates, to
a 3D mesh surface.

So...

- a ``Region`` could have a ``Text`` ``Annotation``:  'The nucleus'

- a ``TiltSeriesMicrographStack`` could have a list of ``Point`` ``Annotation`` objects
  labelled 'picked particles'

- a ``Tomogram`` could have ``FitMap`` object in the ``annotations`` which contains the
  path to a map and the matrix that transforms it to align it in the tomogram

Tree
----

.. code-block:: text

 DataSet
 |- Region
    |- MovieStackCollection
    |  |- GainFile
    |  |- DefectFile
    |  |- MovieStackSeries
    |     |- MovieStack
    |        |- Movieframe
    |        |- CTFMetadata
    |
    |  |- TiltSeriesSet
    |     |- TiltSeriesMicrographStack
    |        |- TiltSeriesMicrograph
    |           |- CTFMetadata
    |
    |- TomogramSet
    |  |- Tomogram
    |     |- MapSet
    |        |- Map
    |     |- SubTomgramSet
    |        |- SubTomogram