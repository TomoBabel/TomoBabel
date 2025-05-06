Writing Converters
==================

When adding a new converter for a sepcific program it should be put in a directory
``tomobabel/converters/<software_name>``.

Converters must conform to the following guidelines:

#. It should create CETS data objects.

#. It should be able to be run with arguments from the command line and imported and used as a python module.

#. It should have the ability to convert an entire project to CETS format

#. It should have the ability to separately convert individual parts of a project to the CETS data format

#. Write doncumentations for the converter.  Make a folder in `docs/source/converters` with full documentation and update `docs/source/index.rst` to display it.

#. Write tests for your converter.  Make a dir in ``tomobabel/tests/converters`` and put them there.

