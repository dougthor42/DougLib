# -*- coding: utf-8 -*-
"""
@name:          misc_re.py
@vers:          0.1.0
@author:        dthor
@created:       Mon Feb 09 16:32:09 2015
@descr:         A new file

Usage:
    new_program.py

Options:
    -h --help           # Show this screen.
    --version           # Show version.

Description:
    Miscellaneious regex that I've come up with and want to keep for
    some reason.
"""

# ---------------------------------------------------------------------------
### Imports
# ---------------------------------------------------------------------------
# Standard Library
import re


# Matches stuff inside the parentheses (including them) for any class
# or function definition.
re1 = re.compile("""
(?:\s*class|def)            # look for 'class' or 'def, but don't capture it.
\s*\w+\s*                   # the function name
(?P<classdef>\(.*?)         # the full string of function parameters
(?:\s*:)                    # non-capturing group for the whitespace and :
""", re.DOTALL | re.VERBOSE)


# Matches stuff inside the parentheses (*not* including them) for any class
# or function definition.
re2 = re.compile("""
(?:\s*class|def)            # look for 'class' or 'def, but don't capture it.
\s*\w+\s*\(                 # the function name, whitespace, and (
(?P<classdef>.*?)           # the full string of function parameters
(?:\)\s*:)                  # non-capturing group for ) and whitespace and :
""", re.DOTALL | re.VERBOSE)
