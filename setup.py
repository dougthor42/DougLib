# -*- coding: utf-8 -*-

#from distutils.core import setup
# ---------------------------------------------------------------------------
### Imports
# ---------------------------------------------------------------------------
# Standard Library
from setuptools import setup, find_packages
import logging

# Third Party

# Package / Application
from douglib import (__version__,
                     __project_url__,
                     __project_name__,
                     )

# turn off logging if we're going to build a distribution
logging.disable(logging.CRITICAL)

setup(
    name=__project_name__,
#    packages=["douglib"],
    packages=find_packages(),
    version=__version__,
    description="Doug's Standard Library",
    author="Douglas Thor",
    author_email="doug.thor@gmail.com",
    url=__project_url__,
    classifiers=[
#        "Development Status :: 5 - Production/Stable",
#        "Intended Audience :: Manufacturing",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        ],
    requires=["wxPython"],
    long_description="""
=========
douglib
=========

A collection of functions, classes, utilities, and other items that I've
created over the years.
""",
    )

