# -*- coding: utf-8 -*-
"""
plotting.py

Part of douglib. Used for general data plotting.

Created on Tue June 06 08:44:12 2014
@author: dthor
"""
# ---------------------------------------------------------------------------
### Imports
# ---------------------------------------------------------------------------
# Standard Library


# Third-Party
import matplotlib.pyplot as pyplot

# Package / Application
from .core import rc_to_radius


def radius_plot(rcd_list, die_xy, center_rc):
    """ Plots up data by radius """
#    rc_to_radius

    x_data = []
    y_data = []
    for rcd in rcd_list:
        x_data.append(rc_to_radius((rcd[0], rcd[1]), die_xy, center_rc))
        y_data.append(rcd[2])

    pyplot.figure()
    pyplot.plot(x_data, y_data, 'bo')
    pyplot.xlabel("Radius")
    pyplot.ylabel("Value")
    pyplot.show()


def main():
    """
    Runs only when module is called directly. Runs a quick sanity
    check on some of the functions in this module.
    """
    import random

    die_xy = (2.43, 3.3)
    center_rc = (24, 31.5)
    fake_rcd_list = []
    for row in range(30):
        for col in range(54):
            value = (random.normalvariate(10, 5) +
                     rc_to_radius((row, col), die_xy, center_rc))
            fake_rcd_list.append([row, col, value])

    radius_plot(fake_rcd_list, die_xy, center_rc)
#    random.gauss()


if __name__ == "__main__":
    main()
