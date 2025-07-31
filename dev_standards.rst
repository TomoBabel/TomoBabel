===========================================================
Proposed Development Standards for CryoET Standards Project
===========================================================

*rev 0.1 - MGI - 20250729*

As this is intended to be a library that will be used in a variety of settings
and by many different developers, we should try to maintain strict best practices
for the quality of the code.

General
-------

- **Python:** I propose we use python 3.11
- **Syntax and style:** The code should conform to `PEP8 <https://peps.python.org/pep-0008/>`_
  as much as is possible
- **Linting:** ``Ruff 0.11.12``
- **Type checking:** ``mypy 1.8.0``

Dev Dependencies
----------------

The following in ``pyproject.toml``:

.. code-block:: toml

 optional-dependencies.dev = [
     "mypy==1.8.0",  # this version should match the one in .pre-commit-config.yaml
     "pre-commit",
     "pytest",
     "pytest-cov",
     "types-setuptools",
     "ruff==0.11.12", # this version should match the one in .pre-commit-config.yaml
 ]

 [tool.mypy]
 files = ["tomobabel", "tests"]
 python_version = "3.11"
 warn_unused_configs = true

Precommit hooks
---------------

.. code-block:: yaml

 repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    # Ruff version.
    rev: v0.11.12
    hooks:
      # Run the linter.
      - id: ruff
        args: [ --fix ]
      # Run the formatter.
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-setuptools]

Typing
------

- All functions should be strictly typed.
- When file names are used as arguments ``os.PathLike`` should be used
  rather than ``str``.
- Empty string defaults should be ``""`` all other empty defaults should be
  ``Optional[<type>]``

Test coverage
-------------

We should aim for high (80%) test coverage.  When A CI pipeline is established
I propose pytest is run with ``--cov-fail-under=80``.

Library suggestions
-------------------

These are my personal preferences, we can discuss...

- ``pathlib`` for handling paths rather than ``os.path``.
- ``gemmi 0.7.4`` for reading/writing .mmcif/.star files. Do not use ``starfile``
  as although it writes files that are fine for RELION, the star files it writes
  can have errors and don't strictly conform to the file definition.
- ``numpy`` and ``scipy``: We will all probably be using these so we should agree on
  specific version.