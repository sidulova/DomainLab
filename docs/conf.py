# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/stable/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

# Incase the project was not installed
import os
import sys
from datetime import datetime

import sphinx_material

sys.path.insert(0, os.path.abspath(".."))

# -- Project information -----------------------------------------------------

project = "domainlab"  # @FIXME
copyright = f"2021-{datetime.now().year}, Marr Lab." ""

author = "Xudong Sun, et.al."

# The short X.Y version
# version = libdg.__version__.split("+")[0]   # @FIXME
# The full version, including alpha/beta/rc tags
# release = version  # @FIXME


# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    # "recommonmark",  # conflict with myst_parser
    "myst_parser",
    "sphinx.ext.autosummary",
    "sphinx.ext.autodoc",
    "sphinx.ext.githubpages",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.extlinks",
    "sphinx.ext.todo",
    "sphinx_material",
    "nbsphinx",
    "nbsphinx_link",
    "IPython.sphinxext.ipython_console_highlighting",
]

# myst_all_links_external = True
myst_heading_anchors = 3
myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "html_admonition",
    "html_image",
    "linkify",
    "replacements",
    "smartquotes",
    "substitution",
]

# autosummary_generate = True
# napoleon_google_docstring = False
# napoleon_use_param = False
# napoleon_use_ivar = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:

### conflict with MySt
# source_parsers = {
#        '.md': 'recommonmark.parser.CommonMarkParser',
# }

source_suffix = [".rst", ".md"]
source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "markdown",
    ".md": "markdown",
}

# The master toctree document.
master_doc = "index"

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path .
exclude_patterns = [
    "setup.py",
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "**.ipynb_checkpoints",
]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "default"
nbsphinx_codecell_lexer = "python"
highlight_language = "none"

# -- Options for HTML output -------------------------------------------------
# -- HTML theme settings ------------------------------------------------
html_short_title = "domainlab"  # @FIXME
html_show_sourcelink = False
html_sidebars = {
    "**": ["logo-text.html", "globaltoc.html", "localtoc.html", "searchbox.html"]
}

html_theme_path = sphinx_material.html_theme_path()
html_context = sphinx_material.get_html_context()
html_theme = "sphinx_material"

# material theme options (see theme.conf for more information)
html_theme_options = {
    # "base_url": "http://bashtage.github.io/sphinx-material/",
    "repo_url": "https://github.com/marrlab/DomainLab",
    "repo_name": "DomainLab",
    # "google_analytics_account": "",
    "html_minify": False,
    "html_prettify": False,
    "css_minify": False,
    "logo_icon": "school",
    "repo_type": "github",
    "globaltoc_depth": 2,
    "color_primary": "teal",
    "color_accent": "cyan",
    "touch_icon": "images/apple-icon-152x152.png",
    "theme_color": "#2196f3",
    "master_doc": False,
    "nav_title": "DomainLab",
    "nav_links": [
        {"href": "readme_link", "internal": True, "title": "Introduction"},
        {"href": "doc_tasks", "internal": True, "title": "Task Specification"},
        {
            "href": "doc_custom_nn",
            "internal": True,
            "title": "Specify neural network in commandline",
        },
        {
            "href": "doc_MNIST_classification",
            "internal": True,
            "title": "Examples with MNIST",
        },
        {
            "href": "doc_examples",
            "internal": True,
            "title": "More commandline examples",
        },
        {"href": "doc_benchmark", "internal": True, "title": "Benchmarks tutorial"},
        {"href": "doc_output", "internal": True, "title": "Output Structure"},
        {
            "href": "doc_extend_contribute",
            "internal": True,
            "title": "Specify custom model in commandline",
        },
        # {
        #     "href": "https://squidfunk.github.io/mkdocs-material/",
        #     "internal": False,
        #     "title": "Material for MkDocs",
        # },
    ],
    "heroes": {
        "index": "DomainLab for modular domain generalization in deep learning",
        "customization": "Configuration options to personalize your site.",
    },
    "version_dropdown": False,
    # "version_json": "_static/versions.json",
    # "version_info": {
    #     "Release": "https://bashtage.github.io/sphinx-material/",
    #     "Development": "https://bashtage.github.io/sphinx-material/devel/",
    #     "Release (rel)": "/sphinx-material/",
    #     "Development (rel)": "/sphinx-material/devel/",
    # },
    "table_classes": ["plain"],
}


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "domainlab"  # @FIXME


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',
    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (
        master_doc,
        "domainlab.tex",
    ),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, "domainlab", "domainlab", [author], 1)]  # @FIXME


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "domainlab",
        "DomainLab Documentation",
        author,
        "domainlab",
        "A pytorch platform of modular domain generalization for deep learning",
        "Miscellaneous",
    ),
]


# -- Extension configuration -------------------------------------------------

# html_static_path = ["_static"]
# html_css_files = [
#   "custom.css",
# ]
# html_js_files = []
