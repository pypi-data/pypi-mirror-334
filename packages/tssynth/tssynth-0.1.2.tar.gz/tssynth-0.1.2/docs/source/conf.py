# Configuration file for the Sphinx documentation builder.
import os
import sys
from datetime import datetime

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(".."))

# Project information
project = "tssynth"
copyright = f"{datetime.now().year}, Your Name"
author = "Your Name"

# Read version from version.txt
with open("../../version.txt") as f:
    release = f.read().strip()
version = release

# Extensions
extensions = [
    "sphinx.ext.autodoc",  # Automatically extract docs from docstrings
    "sphinx.ext.napoleon",  # Support for Google/NumPy-style docstrings
    "sphinx.ext.doctest",  # Test code snippets in documentation
    "sphinx.ext.intersphinx",  # Link to other projects' documentation
    "sphinx.ext.viewcode",  # Add links to highlighted source code
    "sphinx.ext.coverage",  # Collect doc coverage stats
    "sphinx_rtd_theme",  # Read The Docs theme
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# The theme to use for HTML and HTML Help pages.
html_theme = "sphinx_rtd_theme"

# Theme options
html_theme_options = {
    "navigation_depth": 4,
    "titles_only": False,
}

# Add any paths that contain custom static files (such as style sheets)
html_static_path = ["_static"]

# Intersphinx mapping to common Python libraries
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
}

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_type_aliases = None

# Autodoc settings
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
}

# DocTest settings
doctest_global_setup = """
# Add any imports or setup code needed for doctests
"""

# The master toctree document
master_doc = "index"
