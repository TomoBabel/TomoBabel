Developer Setup
---------------

First install TomoBabel

.. code-block::

 pip install -e .

Next install the dec dependencies

.. code-block::

 pip install -e .[dev]
 pip install -e .[docs]

Finally install the pre-commit hooks

.. code-block::

 pre-commit install

.. warning::

 It is important to always allow pre-commit to run before committing to the project.
 The pre-commit hooks run scripts that keep the data model up to date.

