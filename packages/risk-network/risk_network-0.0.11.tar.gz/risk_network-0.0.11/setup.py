"""
setup
~~~~~
"""

import re
from setuptools import setup, find_packages

# Leave numpy imported for package bundling
import numpy


def find_version():
    """Function to find the version string in the __init__.py file."""
    with open("risk/__init__.py", "r", encoding="utf-8") as f:
        version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M)
        if version_match:
            return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


# Setup function
setup(
    name="risk-network",
    version=find_version(),  # Dynamically fetches the version
    author="Ira Horecka",
    author_email="ira89@icloud.com",
    description="A Python package for biological network analysis",  # Updated description
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    license="GPL-3.0-or-later",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "ipywidgets",
        "leidenalg",
        "markov_clustering",
        "matplotlib",
        "networkx",
        "nltk",
        "numpy",
        "openpyxl",
        "pandas",
        "python-igraph",
        "python-louvain",
        "scikit-learn",
        "scipy",
        "statsmodels",
        "threadpoolctl",
        "tqdm",
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Development Status :: 4 - Beta",
    ],
    python_requires=">=3.8",
)
