.. image:: docs/source/tblogo.png
  :width: 350
  :alt: TomoBabel logo
  :align: center

==================================================================
Cryo Electron Tomography Standard (CETS) data format and TomoBabel
==================================================================

The cryo electron tomography standard (CETS) data format is designed to facilitate
transfer and reuse of cryo-electron tomography (cryoET) data through a standardized data
format

TomoBabel is a library and set of command line programs that convert data from cryoET
data processing software to the CETS and from the CETS to various software formats,
allowing interoperability between different packages.

The CETS will be adopted by both the `CZII CryoET DataPortal <https://cryoetdataportal.czscience.com/>`_
and `Electron Microscopy Public Image Archive (EMPIAR) <https://www.ebi.ac.uk/empiar/>`_.

To install:

.. code-block:: shell

 git clone https://github.com/TomoBabel/TomoBabel.git
 cd TomoBabel
 pip install .

To get the docs:

.. code-block:: shell

 pip install -e .[docs]
 cd docs
 make html

then open ``TomoBabal/docs/_build/index.html`` in your web browser