# -*- coding: utf-8 -*-
"""
Created on Fri Jun 13 10:40:19 2014

@name:          new_program.py
@vers:          0.1
@author:        dthor
@created:       Fri Jun 13 10:40:19 2014
@modified:      Fri Jun 13 10:40:19 2014
@descr:         Unit Testing for douglib.wafer_map module
"""
# ---------------------------------------------------------------------------
### Imports
# ---------------------------------------------------------------------------
# Standard Library
import os.path
import os
import unittest

# Third-Party

# Package / Application
try:
    # Imports used by unit test runners
    pass
#    from . import (__project_name__,
#                   __version__,
#                   __released__,
#                   )
#    logging.debug("Imports for UnitTests")
except SystemError:
    try:
        # Imports used by Spyder
        pass
#        from __init__ import (__project_name__,
#                              __version__,
#                              __released__,
#                              )
#        logging.debug("Imports for Spyder IDE")
    except ImportError:
         # Imports used by cx_freeze
        pass
#        from douglib import (__project_name__,
#                             __version__,
#                             __released__,
#        logging.debug("imports for Executable")


REF_DATA_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             "reference_data",
                             )


class DrawWaferOutline(unittest.TestCase):
    """ Compare output of draw_wafer_outline to the reference image """
    ref_img_path = os.path.join(REF_DATA_PATH,
                                "ref_draw_wafer_outline.png",
                                )

    known_values = ("ref_draw_wafer_outline.png",
                    "ref_draw_wafer_outline_2.png",
                    )

#    def test_known_values(self):
#        for img in known_values


class TestPlotRCD(unittest.TestCase):
    """ Plot the RCD from a file """
    data_file = os.path.join(REF_DATA_PATH, "wafer_map.csv")

#    def test_plot_RCD(self):
#        with open(self.data_file) as ofile:
#            raw_data = [line.strip().split(',') for line in ofile.readlines()]
#        data = [(int(a[0]), int(a[1]), float(a[2])) for a in raw_data]
#        wafer_map.plot_rcd(data)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=1)
