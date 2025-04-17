
Using the Data Model
====================

Using the data model objects
----------------------------

The data model objects are defined in :mod:`tomobabel.models.models`.

.. warning::
 DO NOT EDIT THIS MODULE, EVER. FOR ANY REASON!


Editing the data model
----------------------

1) You probably shouldn't without consulting with the project stakeholders
2) Seriously... Don't

data_model yaml files
---------------------
These files in the toplevel ``TomoBabel/data_model`` dir define the model.

If any changes are made to these filesa pre-commit hook will run scripts that
update :mod:`tomobabel.models.models` and :file:`tomobabel/model/stubs/models.pyi`



