Developer Setup
---------------

First install TomoBabel

.. code-block::

 pip install -e .

Next install the dev dependencies

.. code-block:: shell

 pip install -e .[dev]
 pip install -e .[docs]

Finally install the pre-commit hooks

.. code-block:: shell

 pre-commit install
