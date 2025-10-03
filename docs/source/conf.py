"""
Configuration file for the Sphinx documentation builder.

For the full list of built-in configuration values, see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html

-- Project information -----------------------------------------------------
https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

"""

import sys
from pathlib import Path

SRC = str(Path(__file__).resolve().parents[2] / "src")
sys.path.insert(0, SRC)

project = "pypc_utils"
copyright = "2025, Philip Cogswell"
author = "Philip Cogswell"
release = "0.1.4"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon", "sphinx_autodoc_typehints"]

templates_path = ["_templates"]
myst_enable_extensions = ["deflist", "html_image"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
