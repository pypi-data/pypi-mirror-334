"""Mudag setup script."""

from setuptools import find_packages, setup

# Import version from package
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from mudag import __version__

# Read the long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mudag",
    version=__version__,
    description="A tool for analyzing research software repositories with focus on workflow languages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Aaron Strachardt",
    url="https://github.com/aaronstrachardt/mudag",
    project_urls={
        "Bug Tracker": "https://github.com/aaronstrachardt/mudag/issues",
    },
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "mudag=mudag.cli.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Quality Assurance",
    ],
)
