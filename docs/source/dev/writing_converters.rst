Writing Converters
==================

When adding a new converter for a specific program it should be put in a directory
``tomobabel/converters/<software_name>``.

Converters should conform to the following guidelines:

#. It should create CETS data objects.

#. It should be able to be run with arguments from the command line and imported and
   used as a python module.

#. It should have the ability to convert an entire project to CETS format returning a
   CETS ``DataSet``

#. It should have the ability to separately convert individual parts of a project to the
   appropriate CETS data format objects.

#. Write documentation for the converter.  Make a folder in ``docs/source/converters``
   with full documentation and update ``docs/source/index.rst`` to display it.

#. Write tests for your converter.  Make a dir in ``tomobabel/tests/converters`` and
   put them there.

#. Use the existing testing framework. See the ``TomoBabelTest`` object in
   ``tomobabel/tests/testing_tools.py`` and its ``TomoBabelRelionTest`` subclass in
   ``tomobabel/tests/converters/relion/relion_testing_utils.py``


