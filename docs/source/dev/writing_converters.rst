Writing Converters
==================

When adding a new converter for a sepcific program it should be put in a directory
``tomobabel/converters/<software_name>``.

Converters must conform to the following guidelines:

#. It should create SDF data objects and use ``model_dump()`` on them to return a dict in the SDF format.

#. It should be able to be run with arguments from the command line and imported and used as a python module.


