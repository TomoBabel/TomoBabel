# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys

sys.path.insert(0, os.path.abspath("../"))


# -- Project information -----------------------------------------------------

project = "TomoBabel"
copyright = "2025, Science and Technology Facilities Council"  # @ReservedAssignment
author = "Matthew G Iadanza, Utz Ermel"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx_autodoc_typehints",
    "sphinxarg.ext",
]

autodoc_typehints = "description"

# sphinx-autodoc-pydantic configuration
autodoc_pydantic_model_show_signature = False
autodoc_pydantic_model_show_json = False
autodoc_pydantic_model_show_field_summary = True
autodoc_pydantic_model_show_field_constraints = True
autodoc_pydantic_model_show_config_summary = True
autodoc_pydantic_model_show_config_member = False

# intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "gemmi": ("https://gemmi.readthedocs.io/en/stable", "gemmi.inv"),
    "numpy": ("https://numpy.org/doc/stable/", None),
}


# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ["_static"]


# Temporary fix for CI failure caused by a bug in python 3.8:
# https://github.com/sphinx-doc/sphinx/issues/8237
# Also ignoring plotly Figure object, because it was causing problems in sphinx:
# py:class reference target not found: plotly.graph_objs._figure.Figure

nitpick_ignore = [
    ("py:class", "NoneType"),
]
