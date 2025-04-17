Developer Setup
---------------

First get ``pdm`` to manage dependencies and then install TomoBabel

.. code-block::

 pip install pdm
 pdm install

Next add the dev and docs dependencies

.. code-block::

 pdm lock -G dev
 pddm install -dG dev
 pdm lock -G docs
 pddm install -dG docs

Finally install the pre-commit hooks

.. code-block::

 pre-commit install

.. warning::

 It is important to always allow pre-commit to run before commiting to the project.
 The pre-commit hooks run scripts that keep the data model up to date.

