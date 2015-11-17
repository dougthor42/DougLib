# -*- coding: utf-8 -*-
"""
@name:          new_program.py
@vers:          0.1.0
@author:        dthor
@created:       Mon Jul 07 16:54:02 2014
@descr:         Unit Testing for douglib.prompts module
"""
# ---------------------------------------------------------------------------
### Imports
# ---------------------------------------------------------------------------
# Standard Library
import unittest

# Third-Party

# Package / Application
try:
    # Imports used for unittests
    from .. import prompts
#    from . import (__project_name__,
#                   __version__,
#                   __released__,
#                   )
#    logging.debug("Imports for UnitTests")
except SystemError:
    try:
        # Imports used by Spyder
        import prompts
#        from __init__ import (__project_name__,
#                              __version__,
#                              __released__,
#                              )
#        logging.debug("Imports for Spyder IDE")
    except ImportError:
         # Imports used by cx_freeze
        from douglib import prompts
#        from douglib import (__project_name__,
#                             __version__,
#                             __released__,
#        logging.debug("imports for Executable")

__author__ = "Douglas Thor"
__version__ = "v0.1.0"


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=1)
