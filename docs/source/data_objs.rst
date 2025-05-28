Data Objects
============

Basic models
------------
These contain the BaseModels and most basic pieces of data

.. automodule:: tomobabel.models.basemodels
    :members:
    :undoc-members:
    :show-inheritance:
    :exclude-members: model_config

EBI linked base model
---------------------
There is a sub set of the base model called an ``EbiLinkedBaseModel``. This is
used for fields of the CETS that have a direct 1:1 correspondence with fields in
the EBI data model (Used in the PDB and EMDB). These fields are validated against
the EBI schema and are used when appropriate to make it more convenient for developers
to prepare EMDB/PDB depositions.

.. automodule:: tomobabel.models.ebi_compatibility.ebi_validation
    :members:
    :undoc-members:
    :show-inheritance:
    :exclude-members: model_config


Top level data objects
----------------------
All other types of data will live in these top level types

.. automodule:: tomobabel.models.top_level
    :members:
    :undoc-members:
    :show-inheritance:
    :exclude-members: model_config

Images
------
These describe data associated with images

.. automodule:: tomobabel.models.tomo_images
    :members:
    :undoc-members:
    :show-inheritance:
    :exclude-members: model_config

Transformations
---------------
These describe transformations applied to other data objects

.. automodule:: tomobabel.models.transformations
    :members:
    :undoc-members:
    :show-inheritance:
    :exclude-members: model_config

Annotations
-----------
These describe annotations for other data objects

.. automodule:: tomobabel.models.annotation
    :members:
    :undoc-members:
    :show-inheritance:
    :exclude-members: model_config
