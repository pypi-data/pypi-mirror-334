# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
# with inspiration from https://gitlab.mpcdf.mpg.de/struphy/struphy/-/blob/devel/doc/conf.py

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here.

import sys
import subprocess
import logging
import os
from pathlib import Path

sys.path.append(str(Path(__file__).parent / "generators"))  # docs/generators
from generate_parameter_list import format_parameter_list


# -- Project information -----------------------------------------------------

project = "GVEC"
copyright = "2025 GVEC Contributors | Max Planck Institute for Plasma Physics"
author = "Florian Hindenlang et al."

try:
    p = subprocess.run(
        ["git", "describe", "--tags", "--dirty", "--always"], capture_output=True
    )
    version = p.stdout.decode().strip()
except Exception as e:
    logging.error(f"Could not get git version: {e}")
    version = "unknown"
release = version

# generate parameter lists, generators/parameters-*md
genpath = Path(__file__).parent / "generators"
for category, expr in [
    ("minimizer", "'minimizer' in 'category'"),
    ("initialization", "'initialization' in 'category'"),
    ("discretization", "'discretization' in 'category'"),
    ("profiles", "'profiles' in 'category'"),
    ("bcs", "'boundary' in 'category' or 'axis' in 'category'"),
    ("hmap", "'hmap' in 'category'"),
    ("visualization", "'visualization' in 'category'"),
]:
    format_parameter_list(
        genpath / "parameters.yaml",
        output_file=genpath / f"parameters-{category}.md",
        filter_expr=expr,
        formatting="markdown",
        open_all=False,
    )
    print(f"generated parameters-{category}.md")


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "myst_parser",  # "a rich and extensible flavour of Markdown for authoring technical and scientific documentation."
    "sphinx_design",  # proveides Grids, Cards, Dropdowns & more
    "sphinx.ext.napoleon",  # preprocessor for NumPy and Google style docstrings
    "sphinx.ext.autodoc",  # automatically generated API documentation from docstrings
    "sphinxcontrib.bibtex",  # bibtex citation with :cite:`refname`
    "sphinx_math_dollar",
    "sphinx.ext.mathjax",  # mathjax
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["templates"]

bibtex_bibfiles = ["generators/references.bib"]

# -- Options for LaTeX output --------------------------------------------
mathjax3_config = {
    "loader": {"load": ["[tex]/physics"]},
    "options": {"processHtmlClass": "tex2jax_process|mathjax_process|math|output_area"},
    "tex": {
        "packages": {"[+]": ["physics", "amsmath", "amssymb"]},
        "macros": {
            "vec": [r"\mathbf{#1}", 1],
            "Jac": r"\mathcal{J}",
            "rint": r"\int\limits_0^{1}\!",
            "dblint": r"\int\limits_0^{2\pi}\!\int\limits_0^{2\pi}",
            "thet": r"\vartheta",
            "erho": r"\vec{e}_{\rho}",
            "ethet": r"\vec{e}_{\rho}",
            "ezeta": r"\vec{e}_{\zeta}",
            "submin": r"_\mathrm{min}",
            "submax": r"_\mathrm{max}",
            "R": r"\mathbb{R}",
            "nfp": r"N_{FP}",
            "rbasis": r"\mathcal{N}",
            "fbasis": r"\mathcal{F}",
            "Btavg": r"\langle{B_\thet}\rangle",
            "Bzavg": r"\langle{B_\zeta}\rangle",
            "el": r"\ell",
            "elp": r"\el^{\prime}",
            "elpp": r"\el^{\prime\prime}",
            "X": r"\vec{X}_0",
            "Xp": r"\X^{\prime}",
            "Xpp": r"\X^{\prime\prime}",
            "Xppp": r"\X^{\prime\prime\prime}",
            "ttilde": r"{\vec{\tilde{T}}_q}",
        },
    },
}


# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["ford/ford.md", "ford/static/index.md", "generators"]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "pydata_sphinx_theme"

html_theme_options = {
    # "sidebarwidth": 270,
    "show_toc_level": 2,  # number of levels always visible in the (right) toc
    # "show_nav_level": ?,
    # "navigation_depth": ?,
    "back_to_top_button": True,
    # --- footer --- #
    "footer_start": ["version", "last-updated"],
    "footer_center": ["copyright"],
    "footer_end": ["sphinx-version", "theme-version"],
    # --- header --- #
    # "header_links_before_dropdown": ?,
    "external_links": [
        {
            # external section of the documentation, built with FORD
            "name": "Fortran Code Documentation",
            # important to use an absolute path, denoted with a starting "/"
            # prefix with the FORD_PREFIX environment variable (e.g. set to "/gvec" on GitLab Pages)
            "url": f"{os.environ.get('FORD_PREFIX', ' ')}/ford/index.html",
        },
    ],
    "gitlab_url": "https://gitlab.mpcdf.mpg.de/gvec-group/gvec",
    "icon_links": [
        {
            "name": "Issues",
            "url": "https://gitlab.mpcdf.mpg.de/gvec-group/gvec/issues",
            "icon": "fa-solid fa-bug",
        },
        # {
        #     "name": "PyPI",
        #     "url": "https://pypi.org/project/gvec",
        #     "icon": "fa-custom fa-pypi",
        # },
    ],
}

html_title = "GVEC Documentation"
html_last_updated_fmt = "%Y-%m-%d"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# The content with the given paths is copied to the _static directory of the build directory.
html_static_path = ["static"]
# Add any paths that contain extra files (such as robots.txt, .htaccess or static html files) here
# extra/ford is generated by FORD
html_extra_path = ["extra"]

html_css_files = [
    "custom.css",
]

# --- markdown parsing with myst --- #
myst_enable_extensions = [
    "amsmath",
    "attrs_inline",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]

myst_dmath_allow_labels = True
myst_heading_anchors = 3
