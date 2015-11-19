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
import matplotlib.pyplot as pyplot

# Package / Application
try:
    # Imports used by unit test runners
    from ..core import binary_file_compare
#    from . import (__project_name__,
#                   __version__,
#                   __released__,
#                   )
#    logging.debug("Imports for UnitTests")
except SystemError:
    try:
        # Imports used by Spyder
        from .core import binary_file_compare
#        from __init__ import (__project_name__,
#                              __version__,
#                              __released__,
#                              )
#        logging.debug("Imports for Spyder IDE")
    except ImportError:
         # Imports used by cx_freeze
        from douglib.core import binary_file_compare
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
#    filepath = os.path.dirname(os.path.realpath(__file__))
#    fig = pyplot.figure(1)
#    fig.clf()
#    ax = fig.add_subplot(1, 1, 1, aspect='equal')
#    dia = 150
#    x_axis_min = -dia * 0.55
#    x_axis_max = dia * 0.55
#    y_axis_min = -dia * 0.55
#    y_axis_max = dia * 0.55
#    ax.axis([x_axis_min, x_axis_max, y_axis_min, y_axis_max])
#    wafer_map.draw_wafer_outline(ax, dia)
#    ref_img_path = os.path.join(filepath,
#                                "reference_data",
#                                "ref_draw_wafer_outline.png",
#                                )
#    tmp_img_path = os.path.join(filepath,
#                                "reference_data",
#                                "temp.png",
#                                )
#    fig.savefig(tmp_img_path, bbox_inches='tight')
#
#    match = binary_file_compare(ref_img_path, tmp_img_path, True)
#    print(match)
#
#    # Delete the tmp_data file if it matches the reference file
#    if match:
#        os.remove(tmp_img_path)

#    data_file = os.path.join(REF_DATA_PATH, "wafer_map.csv")
#
#    with open(data_file) as open_file:
#        raw_data = [line.strip().split(',') for line in open_file.readlines()]
#    data = [(int(a[0]), int(a[1]), float(a[2])) for a in raw_data]
#    wafer_map.plot_rcd(data)
