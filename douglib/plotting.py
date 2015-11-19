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
import abc
import functools
import collections
import inspect

# Third-Party
import matplotlib.pyplot as pyplot

# Package / Application
try:
    # Imports used by unit test runners
    from .core import rc_to_radius
#    from . import (__project_name__,
#                   __version__,
#                   __released__,
#                   )
#    logging.debug("Imports for UnitTests")
except SystemError:
    try:
        # Imports used by Spyder
#        import utils
        from core import rc_to_radius
#        from __init__ import (__project_name__,
#                              __version__,
#                              __released__,
#                              )
#        logging.debug("Imports for Spyder IDE")
    except ImportError:
         # Imports used by cx_freeze
        from douglib.core import rc_to_radius
#        from douglib import (__project_name__,
#                             __version__,
#                             __released__,
#        logging.debug("imports for Executable")


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

# This is Brian's code.
def main1():
    import urllib, StringIO, glob, sys, os, csv
    from numpy import *#recfromcsv
    import matplotlib.pyplot as plt
    from matplotlib import gridspec
    import mpl_toolkits.mplot3d.axes3d as p3
    from scipy.interpolate import griddata
    import numpy as np
    from matplotlib  import cm
    #from pylab import *

    #os.system('cls')

    if len(sys.argv)==1: sys.argv+=['\\\\HYDROGEN\\Shared\\Engineering\\Power\\AP Data\\SHAD2\\1502-5\\40072-1-04 W1\\1mm-A, 700V Vert_po_breakdown_dl_s_140714-105846.00.csv']

    vCur = 600
    iCur = 1e-6
    psize = (14,10)

    if len(sys.argv)>1:
        fd = sys.argv[1:]
    else:
        #sys.exit()
        fd = [raw_input('WaferMap: ')]

    mz = range(len(fd))
    for i in range(len(fd)):
        plt.figure(fd[i].split('\\')[-2],figsize=(10,10))
        fig = plt.subplot2grid(psize, (0,0), colspan=9, rowspan=8)
        plt.axvline(x=600)
        plt.axhline(y=1e-5)
        plt.ylim(1e-9, 1e-3)
        plt.xlim(0, 700)

        lol = open(fd[i],'r').read().split('\nAtt1\n')
        header = lol[0]
        rawdata = lol[1:]

        wfrdata = []
        cen = (16.5,16)
        d600 = np.ones((len(rawdata),1),np.float)*1e-3
        r600 = np.ones((len(rawdata),1),np.float)*1e-3
        neg_Flag = False
        for d in rawdata:
            attr = d[:d.find('\nEnd')].split('\n')
            data = d[d.find('Test_parm1'):d.find('End Test_parm1')].split('\n')[1:-1]
            data2 = np.array([d2.split(',') for d2 in data], np.float32)

            if not data2.any(): continue
            data2 = data2[abs(data2[:,0])<>60]#remove bad data point at 60v

            wfrdata += [[attr, data2, []]]
            if data2[np.abs(data2[:,0])==600,1].any():# and abs(data2[np.abs(data2[:,0])==100,1])[0] > 2e-9:
                d600[len(wfrdata)-1] = np.abs(data2[np.abs(data2[:,0])==600,1])
                #r600[len(wfrdata)-1] = np.abs(np.sqrt(((int(attr[0])-cen[0])*5.0)**2 + ((int(attr[1])-cen[1])*5.0)**2))
                if max(np.abs(data2[:,0])) <> max(data2[:,0]): neg_Flag = True

            plt.semilogy(np.abs(data2[:,0]),np.abs(data2[:,1]))


        plt.title(fd[i].split('\\')[-2])
        if neg_Flag:plt.title(fd[i].split('\\')[-2]+' Reverse')

        fig = plt.subplot2grid(psize, (9,6), colspan=4, rowspan=5)
        x,y,z = ([int(a[0][1]) for a in wfrdata],[int(a[0][0]) for a in wfrdata], \
                 [((abs(a[1][np.abs(a[1][:,0])==600,1][0])) if abs(a[1][-1,0])>=600 else 1e-3) for a in wfrdata])
        plt.scatter(x,y,s=80,c=log10(z), marker = 'o', cmap = cm.jet )
        mymap = plt.get_cmap()
        plt.ylim(max(y),0)
        plt.xlim(0, max(x))
        plt.axis('equal')

        r = [np.abs(np.sqrt((((int(a[0][0])-cen[0])*5.0)**2 + ((int(a[0][1])-cen[1])*5.0)**2))) for a in wfrdata]
        fig = plt.subplot2grid(psize, (9,0), colspan=5, rowspan=5)
        plt.scatter(r, z,s=50,c=log10(z),edgecolors='None', cmap = mymap )
        fig.set_yscale('log')
        plt.xlim(0, 75)
        plt.ylim(min(d600)*0.9,max(d600[d600 < 9e-4])*1.1 if min(d600) < 1e-3 else 1e-3)
        plt.axhline(y=1e-5)

        fig = plt.subplot2grid(psize, (0,9), rowspan=8)
        plt.boxplot(np.log10(d600[d600.nonzero()[0]]))
        fig.axes.get_xaxis().set_ticklabels([600])
        plt.axhline(y=-5)
        fig.axes.get_xaxis().set_visible(False)
        fig.axes.get_yaxis().set_ticklabels([])
        plt.ylim(-9, -3)

    plt.show()



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
    main1()
