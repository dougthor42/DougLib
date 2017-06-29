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

substrate_id = re.compile("""
# Older 4" SiC style substrate IDs
([A-Z]{2}[0-9]{4}-[0-9]{2}(-EV)?(X*|(-[1-9]))?)
|
((\w{5,10})?T[PX]H?[0-9]{3,4})
|
(K[0-9]{6})
|
((F5L07G)[0-9]{2}-[0-9]{5}-[0-9]{2})
|
([0-9]{5}-[0-9])
""",
re.DOTALL | re.VERBOSE)

growth_id = re.compile("""
((0[1-9]|[01][0-9])
(0[1-9]|1[012])
(0[1-9]|[12][0-9]|3[01])
[A-G][HGM]?[A-Z](-[A-C])?(-[1-9])?)
|
([0-9]{5}-[0-9])
""",
re.DOTALL | re.VERBOSE)

yymmdd = re.compile("""
(0[0-9]|[12][0-9])          # YY: 00 - 29
(0[1-9]|1[012])             # MM: 01 - 12
(0[1-9]|[12][0-9]|3[01])    # DD: 01 - 31
""",
re.VERBOSE)

REGEX_YEAR = r"(0[1-9]|[012][0-9])"
REGEX_MONTH = r"(0[1-9]|1[012])"
REGEX_DAY = r"(0[1-9]|[12][0-9]|3[01])"
REGEX_RUN = r"[A-Z][A-Z](-[1-6])"
REGEX_GROWTH = re.compile(REGEX_YEAR + REGEX_MONTH + REGEX_DAY + REGEX_RUN)
REGEX_SUBSTRATE = re.compile(r"(\w{5})?TPH?[0-9]{3,4}")


re.compile(r"""
(0?7G[0-9]{2})          # Aizu
|
(M[DE]H[0-9]{2})        # Goleta Prod
|
(MCAP[0-9])             # MCAP
|
(SHAD[O0-9])            # Shadowmask
""",
re.VERBOSE)

re.compile(r"""
(0[1-9]G[0-9]{2})      # Aizu
|(M[DE]H[0-9]{2})      # Goleta
|(MCAP[0-9E])          # Goleta MCAP
|(SHAD[O1-9])          # Goleta Shadowmask
|(ECM[0-9][0-9])       # Emode Contact Mask
|(MVBD[1-9])           # Goleta VBD mask
|(R[0-9]{4})           # IR silicon FET
""",
re.VERBOSE)
