===============
TomoBabel
===============

TomoBabel  is designed to facilitate transfer and reuse of cryo-electron tomography
(cryoET) data through a standardized data format (CETS).  The library and command line programs
convert data to and from cryoET data processing software to CETS allowing interoperability between different packages.

CETS will be adopted by both the `CZII CryoET DataPortal <https://cryoetdataportal.czscience.com/>`_
and `Electron Microscopy Public Image Archive (EMPIAR) <https://www.ebi.ac.uk/empiar/>`_.

General info and installation
-----------------------------

To install:

.. code-block:: shell

 git clone https://github.com/TomoBabel/TomoBabel.git
 cd TomoBabel
 pip install .

The CETS Data Model
---------------------------

.. toctree::
   :maxdepth: 1

   source/datamodel_explained

.. toctree::
   :maxdepth: 1

   source/data_objs

Converters - current
--------------------

.. toctree::
   :maxdepth: 1

   source/converters/relion/cmd_relion

Converters - planned
--------------------

.. toctree::
   :maxdepth: 1

   source/converters/cmd_dynamo

.. toctree::
   :maxdepth: 1

   source/converters/cmd_eman2

.. toctree::
   :maxdepth: 1

   source/converters/cmd_scipion

.. toctree::
   :maxdepth: 1

   source/converters/cmd_warpm

For developers
--------------

.. toctree::
   :maxdepth: 1

   source/dev/setup

.. toctree::
   :maxdepth: 1

   source/dev/writing_converters

.. toctree::
   :maxdepth: 1

   source/dev/dev_data_model


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
