
Using the Data Model
====================

The data model objects are defined in :mod:`tomobabel.models`. The models are
in pydantic V2 format.

Editing the data model
----------------------

1) You probably shouldn't without consulting with the project stakeholders
2) Seriously... Don't

If you do edit the data model
-----------------------------

``docs/scripts/draw_diagram.py`` can be used to update the graphic of the data model in
the docs.

This requires erdantic, which is most easily installed with conda

.. code-block:: shell

 conda install erdantic -c conda-forge

otherwise refer to the `erdantic documentation <https://erdantic.drivendata.org/stable/#installation>`_