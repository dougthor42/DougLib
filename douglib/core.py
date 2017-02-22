# -*- coding: utf-8 -*-
# pylint: disable=C0103
"""
Created on Mon Aug 26 11:02:21 2013.

A library holding common subroutines and classes that I've created.
"""
# ---------------------------------------------------------------------------
### Imports
# ---------------------------------------------------------------------------
# Standard Library
import math
import os
import random
import operator
import hashlib

# Third-Party
import numpy as np
from pyerf.pyerf import erf, erfinv

# Package / Application
from . import decorators


# ---------------------------------------------------------------------------
### Constants
# ---------------------------------------------------------------------------
# Defined by SEMI M1-0302
FLAT_LENGTHS = {50: 15.88, 75: 22.22, 100: 32.5, 125: 42.5, 150: 57.5}


# ---------------------------------------------------------------------------
### Functions
# ---------------------------------------------------------------------------
def reservoir_sampling(array, num):
    """
    Randomly selects a number of elements from array.

    Adapted from Wikipedia page on Reservoir Sampling:
    http://en.wikipedia.org/wiki/Reservoir_sampling

    Parameters
    ----------
    array : list
        The list of items to choose from
    num : int
        The number of elements to choose from ``array``

    Returns
    -------
    list_subset : list
        A random subset of ``array`` which is ``num`` items long.


    .. note::
       Timing: O(n)
    """
    list_subset = []
    if not isinstance(num, int) or num < 0:
        raise ValueError
    for index, item in enumerate(array):
        # Generate the reservoir
        if index < num:
            list_subset.append(item)
        else:
            # Randomly replace elements in the reservoir
            # with a decreasing probability.
            # Choose an integer between 0 and index (inclusive)
            random_index = random.randint(0, index)
            if random_index < num:
                list_subset[random_index] = item
    return list_subset


def round_to_multiple(x, y):
    """
    Round ``x`` to a multiple of ``y``.

    Parameters
    ----------
    x : numeric
        The value to be rounded.

    y : numeric
        The multiplier to round to.

    Returns
    -------
    rounded : numeric
        ``x`` rounded to the nearest multiple of ``y``

    Examples
    --------
    >>> round_to_multiple(1.1234, 0.1)
    1.1
    >>> round_to_multiple(4.767, 0.3)
    4.8
    >>> round_to_multiple(1.1234, 0.32)
    1.28
    >>> round_to_multiple(-1.1234, 0.06)
    -1.14
    """
    return y * round(x/y)


def sort_by_column(big_list, *args, **kwargs):
    """
    Sort a 2D list by columns defined by ``args``.

    Will sort by multiple columns if ``args`` is longer than 1 element.

    Parameters
    ----------
    big_list : list
        The list to sort.
    *args : int
        The column(s) to sort by.
    inplace : bool, optional [False]
        If ``True``, the variable sent to ``big_list`` will be modified. If
        ``False``, a copy of the list is made.

    Returns
    -------
    sorted : list
        A copy or reference to the sorted list.

    Notes
    -----
    ``sort_by_column(A, 3, 1)`` will sort by the 4th column (index 3) and then
    by 2nd column (index 1).

    ``sort_by_column(A, 1)`` is the same as ``sort_by_column(A, 1,
    inplace=False)``

    Sorting in place (``inplace=True``) means that the data for the variable
    that you entered (A) will be modified. ``inplace=False`` returns a copy
    of the 2D array and is the default.

    Examples
    --------
    >>> my_array = [[3,5],[2,4],[1,7]]
    >>> sort_by_column(my_array, 1)     # sort by column 1 (2nd col) and copy
    [[2, 4], [3, 5], [1, 7]]
    >>> sort_by_column(my_array, 1, inplace=True)   # modifies my_array
    >>> print(my_array)
    [[2, 4], [3, 5], [1, 7]]
    """
    # if inplace is not in the keyword arguements and there are more than
    # 0 elements, then that means that there must be some invalid options.
    # Raise an error.
    if 'inplace' not in kwargs and len(kwargs.keys()) > 0:
        err_txt = "Only valid keyword arg is 'inplace'. kwarg(s) found: {}"
        raise SyntaxError(err_txt.format(kwargs.keys()))

    # If the user didn't enter any kwargs, set the default.
    if 'inplace' not in kwargs:
        kwargs = {'inplace': False}

    # If the user's arguement type is not boolean, raise error.
    if type(kwargs['inplace']) is not bool:
        err_txt = "'inplace' value must be boolean; {} found."
        raise TypeError(err_txt.format(type(kwargs['inplace'])))
    else:
        inplace = kwargs['inplace']

    if inplace:
        # sort in-place
        big_list.sort(key=operator.itemgetter(*args))
    else:
        # return a copy
        return sorted(big_list, key=operator.itemgetter(*args))


def clip(x, min_max, clipval=None):
    """
    Clip the value ``x`` to x_min or x_max.

    If ``clipval`` is defined, then returns those values instead.
    ``clipval`` must be a list or tuple of length 2.

    Parameters
    ----------
    x : numeric
        The value to clip
    min_max : sequence of numerics, length 2
        The (minimum, maximum) value to return.
    clipval : sequence of length 2, any type, optional
        The items to return when x is outside of (x_min, x_max). This
        sequence can be made up of any type.

    Returns
    -------
    clipped : any

    Examples
    --------
    >>> clip(10, (0, 1))
    1
    >>> clip(10, (0, 1), clipval=("Zero", "One"))
    'One'
    >>> clip(5.23, (3.24, 8.91))
    5.23
    """
    x_min, x_max = min_max

    if clipval is None:
        clipval = (x_min, x_max)

    if not (isinstance(clipval, tuple)
            or isinstance(clipval, list)) and len(clipval) == 2:
        error_text = "clipval must be a tuple or list of length 2"
        raise TypeError(error_text)

    if x > x_max:
        return clipval[1]
    elif x < x_min:
        return clipval[0]
    else:
        return x


def rescale(x, orig_scale, new_scale=(0, 1)):
    """
    Rescale x to run over a new range.

    Rescales x (which was part of scale ``original_min`` to ``original_max``)
    to run over a range (``new_min`` to ``new_max``) such
    that the value ``x`` maintains position on the new scale.
    If ``x`` is outside of xRange, then y will be outside of yRange.

    Default new scale range is 0 to 1 inclusive.

    Parameters
    ----------
    x : numeric
        The value to rescale.
    orig_scale : sequence of numerics, length 2
        The ``(min, max)`` value that ``x`` typically ranges over.
    new_scale : sequence of numerics, length 2, optional
        The new ``(min, max)`` value that the rescaled ``x`` should reference

    Returns
    -------
    result : float
        The rescaled ``x`` value

    Examples
    --------
    >>> rescale(5, (10, 20), (0, 1))
    -0.5
    >>> rescale(27, (0, 200), (0, 5))
    0.675
    >>> rescale(1.5, (0, 1), (0, 10))
    15.0

    .. seealso::

       :func:`rescale_clip`
    """
    original_min, original_max = orig_scale
    new_min, new_max = new_scale

    part_a = x * (new_max - new_min)
    part_b = original_min * new_max - original_max * new_min
    denominator = original_max - original_min
    result = (part_a - part_b)/denominator
    return result


def rescale_clip(x, orig_scale, new_scale=(0, 1)):
    """
    Same as :func:`rescale`, but also clips the new data.

    Any result that is below ``new_min`` or above ``new_max`` is return
    as ``new_min`` or ``new_max``, respectively

    Parameters
    ----------
    x : numeric
        The value to rescale.
    orig_scale : sequence of numerics, length 2
        The ``(min, max)`` value that ``x`` typically ranges over.
    new_scale : sequence of numerics, length 2, optional
        The new ``(min, max)`` value that the rescaled ``x`` should reference

    Returns
    -------
    result : float
        The rescaled ``x`` value

    Examples
    --------
    >>> rescale_clip(5, (10, 20), (0, 1))
    0
    >>> rescale_clip(15, (10, 20), (0, 1))
    0.5
    >>> rescale_clip(25, (10, 20), (0, 1))
    1

    .. seealso::

       :func:`rescale`
    """
    original_min, original_max = orig_scale
    new_min, new_max = new_scale

    result = rescale(x, (original_min, original_max), (new_min, new_max))
    if result > new_max:
        return new_max
    elif result < new_min:
        return new_min
    else:
        return result


def nearest_indicies(data, x):
    """
    Find the two array positions (indices) around x.

    Parameters
    ----------
    data : array-like
        A sequence of [x1, x2, ... xn] values
    x : numeric
        The value to to search for in ``data``

    Returns
    -------
    indices : list
        The indices which surround the value ``x``. See Notes for more
        information.


    Examples
    --------
    >>> nearest_indicies([1,4,6,8,10,15], 3)
    [0, 1]
    >>> nearest_indicies([1,4,6,8,10,15], 6)
    [2]
    >>> nearest_indicies([1,4,6,8,6,10], 7)     # only returns 1st match
    [2, 3]


    .. seealso::

       :func:`pick_x_at_y`


    .. note::

       + Timing: O(n)
       + If an exact match is found, returns a list of length 1 which contains
         the index of the element ``x``. Otherwise, returns a list of
         length 2 containing the two indices that surround ``x``.
       + If there are more than two possible locations, it only returns
         the first.
    """
    # First find the position of the nearest element.
    # The nearest element is the one where the Abs(data-x) is at a minimum.
    differences = []
    for value in data:
        differences.append(math.fabs(value - x))
    minimum = min(differences)
    i = list(position(differences, minimum))[0]
    if data[i] - x > 0:
        return [i - 1, i]
    elif data[i] - x < 0:
        return [i, i + 1]
    else:
        return [i]


def position(array, item):
    """
    Emulate Mathematica's ``Position[]`` function as best as possible.

    Only works on 1D arrays.

    Parameters
    ----------
    array : sequence
        The list of items to search through.
    item : any
        The item to search for.

    Returns
    -------
    indices : generator
        The a generator for the index(es) of item in array. Returns an
        empty generator if ``item`` is not found.

    Examples
    --------
    >>> list(position([0, 1, 2, 3, 4], 2))
    [2]
    >>> list(position(["a", "B", "C", "d"], "d"))
    [3]
    >>> list(position(['1', '1', 'a', 15, 1], '1'))
    [0, 1]

    .. note::

       Timing: O(1)
    """
    return (i for i, x in enumerate(array) if x == item)


def threshold_1d_array(array, y):
    """
    Emulate LabVIEW's ``Threshold 1D Array`` function.

    Takes a ``Y`` value and returns a fractional index for that ``Y`` value.
    If the function is not monotomically increasing, it returns the
    first value found.

    Parameters
    ----------
    array : list
        A 1D list of numeric values.
    y : numeric
        The value to search for.

    Returns
    -------
    fractional_index : float
        A fractional index representing the location of ``y``.


    .. seealso::

       :func:`interpolate_1d_array`

    .. note::

       Timing: O(n)
    """
    indicies = nearest_indicies(array, y)
    if len(indicies) == 1:
        frac_x = indicies[0]
    else:
        low = array[indicies[0]]
        high = array[indicies[1]]
        frac_x = (y - low) / float(high - low) + indicies[0]

    return frac_x


def interpolate_1d_array(array, x):
    """
    Emulate LabVIEW's ``Interpolate 1D Array`` function.

    Takes a fractional index value ``x`` and returns an interpolated
    ``Y`` value.

    Parameters
    ----------
    array : list
        A 1D list of numeric values.
    x : numeric
        The fractional index to inerpolate to.

    Returns
    -------
    y : float
        The interpolated value.

    Notes
    -----
    This function only performs linear interpolation.

    .. seealso::

       :func:`threshold_1d_array`

    .. note::
       Timing: O(1)
    """
    i = int(math.floor(x))
    j = int(math.ceil(x))
    inter_y = (array[j] - array[i]) * (x - i) + array[i]
    return inter_y


def pick_x_at_y(xy_array, y):
    """
    Manual linear interpolation at a POI.

    Parameters
    ----------
    xy_array : list
        A list in the format ``[(x1,y1), (x2,y2), ...]``

    y : numeric
        The y value to look for.

    Returns
    -------
    x : numeric
        The ``x`` value for the given ``y``.
    """
    y_array = [row[1] for row in xy_array]
    indicies = nearest_indicies(y_array, y)
    if len(indicies) == 2:
        # the POI between the two data points
        x1 = float(xy_array[indicies[0]][0])
        x2 = float(xy_array[indicies[1]][0])
        y1 = float(xy_array[indicies[0]][1])
        y2 = float(xy_array[indicies[1]][1])
        slope = (y2 - y1) / (x2 - x1)
        x = (y - y1) / slope + x1
    else:
        # The POI lands directly on a data point
        x = xy_array[indicies[0]][0]
    return x


@decorators.Obsolete
def nanpercentile(a, percentile):
    """
    Perform numpy.percentile(a, percentile) while ignoring NaN values.

    Parameters
    ----------
    a : array
        A 1D list or 1D numpy array

    percentile : float in range [0,100]
        Percentile to compute which must be between 0 and 100 inclusive.

    Returns
    -------
    pcntile : ndarray
        A new array holding the result.

    Only works on a 1D array.
    """
    if type(a) != np.ndarray:
        a = np.array(a)
    return np.percentile(a[np.logical_not(np.isnan(a))], percentile)


def max_dist(center, size):
    """
    Calculate the distance to the farthest corner of a rectangle.

    Assumes that the orgin is at ``(0, 0)``.

    If the rectangle's center is in Q1, then the upper-right corner is
    the farthest away from the origin. If in Q2, then the upper-left corner
    is farthest away. Etc.

    Returns the magnitude of the largest distance.

    Used primarily for calculating if a die has any part outside of wafer's
    edge exclusion.

    Parameters
    ----------
    center : tuple of length 2, numerics
        ``(x, y)`` tuple defining the rectangle's center coordinates

    size : tuple of length 2
        ``(x, y)`` tuple that defines the size of the rectangle.

    Returns
    -------
    dist : numeric
        The distance from the origin (0, 0) to the farthest corner of the
        rectangle.


    .. seealso::

       :func:`max_dist_sqrd`
    """
    dist = math.sqrt(max_dist_sqrd(center, size))
    return dist


def max_dist_sqrd(center, size):
    """
    Calculate the squared distance to the farthest corner of a rectangle.

    Assumes that the orgin is at ``(0, 0)``.

    **Does not take the square of the distance for the sake of speed.**

    If the rectangle's center is in the Q1, then the upper-right corner is
    the farthest away from the origin. If in Q2, then the upper-left corner
    is farthest away. Etc.

    Returns the squared magnitude of the largest distance.

    Used primarily for calculating if a die has any part outside of wafer's
    edge exclusion.

    Parameters
    ----------
    center : tuple of length 2, numerics
        ``(x, y)`` tuple defining the rectangle's center coordinates

    size : tuple of length 2
        ``(x, y)`` tuple that defines the size of the rectangle.

    Returns
    -------
    dist : float
        The distance from the origin (0, 0) to the farthest corner of the
        rectangle.


    .. seealso::

       :func:`max_dist`
    """
    half_x = size[0]/2.
    half_y = size[1]/2.
    if center[0] < 0:
        half_x = -half_x
    if center[1] < 0:
        half_y = -half_y
    dist = (center[0] + half_x)**2 + (center[1] + half_y)**2
    return dist


def rc_to_radius(rc_coord, die_xy, center_rc):
    """
    Convert a die RC coordinate to a radius.

    Parameters
    ----------
    rc_coord : sequence of ints, length 2
        The ``(row, column)`` grid coordinate die
    die_xy : sequence of numerics, length 2
        The die ``(x, y)`` size. Typically in units of mm.
    center_rc : sequence of numerics, length 2
        The grid ``(row, column)`` coordinate which defines the origin (center
        of the wafer).

    Returns
    -------
    radius : float
        The radius of the *center* of the die in question.


    .. seealso::

       :func:`rc_to_radius_sqrd`
    """
    return math.sqrt(rc_to_radius_sqrd(rc_coord, die_xy, center_rc))


def rc_to_radius_sqrd(rc_coord, die_xy, center_rc):
    """
    Convert a die RC coordinate to a radius.

    Returns the squared radius for the sake of speed.

    Parameters
    ----------
    rc_coord : sequence of ints, length 2
        The ``(row, column)`` grid coordinate die
    die_xy : sequence of numerics, length 2
        The die ``(x, y)`` size. Typically in units of mm.
    center_rc : sequence of numerics, length 2
        The grid ``(row, column)`` coordinate which defines the origin (center
        of the wafer).

    Returns
    -------
    radius : float
        The squared radius of the *center* of the die in question.


    .. seealso::

       :func:`rc_to_radius`
    """
    x_dist = (die_xy[0] * (rc_coord[1] - center_rc[1]))**2
    y_dist = (die_xy[1] * (rc_coord[0] - center_rc[0]))**2
    return x_dist + y_dist


def frange(start, stop, step):
    """
    Generator that creates an arbitrary-stepsize range.

    Creates a list generator that returns ``[start, start + step,
    start + step * 2, ..., stop)``

    Note that the interval is closed-open ``[)``. The ``stop`` value is
    not supposed to be part of the returned list generator.

    Parameters
    ----------
    start : numeric
        The number to start at

    stop : numeric
        The number to end at

    step : numeric
        The delta between points

    Returns
    -------
    frange : generator
        A generator that returns the numbers in the range on demand.

    .. note::

       This function does not accout for floating-point math errors.
       This means that there's a possibliity that rounding the last point
       to the ``step`` precision will equal ``stop``. See examples.

    Examples
    --------
    >>> list(frange(1.5, 6.5, 0.5))
    [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0]

    Floating Point Error:

    >>> list(frange(1.2, 1.8, 0.2))
    [1.2, 1.4, 1.5999999999999999, 1.7999999999999998]

    """
    r = start
    while r < stop:
        yield r
        r += step


@decorators.Deprecated
def unit_prefix_str_to_num(string):
    """
    Convert a number string with unit prefix to a floating point number.

    For example, "1.23m" becomes 0.00123 and "4.5k" becomes 4500.0

    .. warning::

       Deprecated by :func:`from_engineering_notation`
    """
    prefixes = {"y": 1e-24,
                "z": 1e-21,
                "a": 1e-18,
                "f": 1e-15,
                "p": 1e-12,
                "n": 1e-9,
                "u": 1e-6,
                "m": 1e-3,
                "c": 1e-2,
                "d": 1e-1,
                "da": 1e1,
                "": 1e0,
                "h": 1e2,
                "k": 1e3,
                "M": 1e6,
                "G": 1e9,
                "T": 1e12,
                "P": 1e15,
                "E": 1e18,
                "Z": 1e21,
                "Y": 1e24}
    try:
        if string[-1] in prefixes:
            return float(string[:-1]) * prefixes[string[-1]]
        else:
            raise KeyError
    except KeyError as err:
        raise KeyError(str(err) + "Invalid unit prefix in: '%s'." % string)


def from_engineering_notation(string):
    """
    Convert a number string with order-of-magnitude suffix to a float.

    Parameters
    ----------
    string : string
        The string to convert.

    Returns
    -------
    number : float
        The numerical equivalent of ``string``.

    Examples
    --------
    >>> from_engineering_notation("1.23m")
    0.00123
    >>> from_engineering_notation("4.5k")
    4500.0
    >>> from_engineering_notation("-6.84u")
    -6.84e-06

    .. seealso::

       :func:`to_engineering_notation`
    """
    numbers = {str(i) for i in range(10)}
    prefixes = {"y": 1e-24,
                "z": 1e-21,
                "a": 1e-18,
                "f": 1e-15,
                "p": 1e-12,
                "n": 1e-9,
                "u": 1e-6,
                "m": 1e-3,
                "c": 1e-2,
                "d": 1e-1,
                "da": 1e1,
                "": 1e0,
                "h": 1e2,
                "k": 1e3,
                "M": 1e6,
                "G": 1e9,
                "T": 1e12,
                "P": 1e15,
                "E": 1e18,
                "Z": 1e21,
                "Y": 1e24}
    try:
        if string[-1] in prefixes and string[-1] not in numbers:
            return float(string[:-1]) * prefixes[string[-1]]
        elif string[-1] in numbers:
            return float(string)
        else:
            raise KeyError
    except KeyError as err:
        raise KeyError(str(err) + "Invalid unit prefix in: '%s'." % string)


@decorators.Deprecated
def num_to_unit_prefix_str(number, num_dec=5):
    """
    Convert a number to a string with a unit prefix appended.

    Always uses smaller of two options:

    >>> number_to_unit_prefix_string(123456)
    "123.456k"
    >>> number_to_unit_prefix_string(1000036, 2)
    "1.000036M"

    .. warning::

       Deprecated by :func:`to_engineering_notation`
    """
    prefixes = {-24: "y",
                -21: "z",
                -18: "a",
                -15: "f",
                -12: "p",
                -9: "n",
                -6: "u",
                -3: "m",
                -2: "c",
                -1: "d",
                0: "",
                1: "da",
                2: "h",
                3: "k",
                6: "M",
                9: "G",
                12: "T",
                15: "P",
                18: "E",
                21: "Z",
                24: "Y"}

    exp = math.floor(math.log10(abs(number)))
    if exp in prefixes:
        prefix = prefixes[exp]
    elif exp > 24:
        exp = 24
    elif exp < -24:
        exp = -24
    else:
        for key in sorted(prefixes.keys())[::-1]:
            if key < exp:
                exp = key
                break
    prefix = prefixes[exp]
    format_str = "{:.%dg}{:s}" % num_dec
    return_str = format_str.format(number * (10**-exp), prefix)
    return return_str


def to_engineering_notation(number, num_digits=5):
    """
    Convert a float to string with an SI order-of-magnitude suffix.

    .. caution::

       This function can reduce significant digits.

    .. note::

       + Only uses suffixes that are multiples of 3.
       + Always uses smaller of two options.

    Parameters
    ----------
    number : numeric
        The number to convert.
    num_digits : int, optional
        The maximum number of digits to display in ``string``.

    Returns
    -------
    engr_string : string
        An engineering-formatted string representation of ``number``.

    Examples
    --------
    >>> to_engineering_notation(123456)
    '123.46k'
    >>> to_engineering_notation(-0.003216)
    '-3.216m'

    Using ``num_digits``:

    >>> to_engineering_notation(1000036, 2)
    '1M'
    >>> to_engineering_notation(1000036, 6)
    '1.00004M'

    >>> to_engineering_notation(-0.003216, 1)
    '-3m'
    >>> to_engineering_notation(-0.003216, 3)
    '-3.22m'

    >>> to_engineering_notation(32165, 1)
    '3e+01k'
    >>> to_engineering_notation(32165, 2)
    '32k'
    >>> to_engineering_notation(32165, 3)
    '32.2k'
    >>> to_engineering_notation(32165, 4)
    '32.16k'
    """
    # FIXME: change num_digits to num_dec and only affect decimal places
    # FIXME: to_engineering_notation(32165, 1) should return '30k'
    prefixes = {-24: "y",
                -21: "z",
                -18: "a",
                -15: "f",
                -12: "p",
                -9: "n",
                -6: "u",
                -3: "m",
                0: "",
                3: "k",
                6: "M",
                9: "G",
                12: "T",
                15: "P",
                18: "E",
                21: "Z",
                24: "Y"}

    exp = math.floor(math.log10(abs(number)))
    if exp in prefixes:
        prefix = prefixes[exp]
    elif exp > 24:
        exp = 24
    elif exp < -24:
        exp = -24
    else:
        for key in sorted(prefixes.keys())[::-1]:
            if key < exp:
                exp = key
                break
    prefix = prefixes[exp]
    format_str = "{:.%dg}{:s}" % num_digits
    return_str = format_str.format(number * (10**-exp), prefix)
    return return_str


@decorators.Obsolete
def cei_ink_map(probe_list, bad_xy):
    """
    Generate a txt file that is readable by CEI for pick-and-place.

    Currently only uses a single bin. Plans to add more bins are coming.
    bad_xy is a list of tuples. For now.
    """
    bad_xy = [(1, 1),
              (5, 4),
              (27, 58),
              ]
    probe_list1 = [list(i) for i in probe_list]

    bins = {'probe': '1',
            'wafer': '.',
            'flat': '.',
            'excl': 'e',
            'flatExcl': 'f',
            'B': 'B'}

    # First we'll go through and replace the bincode in probe list with
    # any bad die
    n = 0
    for die in probe_list1:
        if tuple([die[0], die[1]]) in bad_xy:
            probe_list1[n] = [die[0], die[1], die[2], die[3], "B"]
            print(probe_list1[n])
        n += 1

    # now let's try making the "map"
    # first, split the list into rows
    max_x = max([i[0] for i in probe_list1])
    max_y = max([i[1] for i in probe_list1])

    die_map = [[0] * max_y] * max_x
    print("Len(die_map) = %d" % len(die_map))
    print("Len(die_map) = %d" % len(die_map[0]))

    sort_by_column(probe_list1, 1, 0)
    temp_map = [bins[x[4]] for x in [y for y in probe_list1]]
    #pprint.pprint(probe_list1)
    die_map = zip(*[iter(temp_map)] * max_x)
    for line in die_map:
        print("".join(line))
    print()

    # create and open file
    file_name = "CEI"
    path = os.path.join("X:\\WinPython27\\programs\\tests\\data",
                        file_name + ".txt")
    print("Saving CEI file data to:")
    print(path)

    #"""
    #WAFER_MAP = {
    #WAFER_ID = "122"
    #MAP_TYPE = "Ascii"
    #NULL_BIN = "."
    #ROWS =  70
    #COLUMNS =  104
    #FLAT_NOTCH = 0
    #SUPPLIER_NAME = "GCS"
    #LOT_ID = "BPG133406M"
    #X_SIZE = 0.950
    #Y_SIZE = 1.360
    #REF_DIES = 1
    #REF_DIE = 0 0
    #BIN  = "1" 4329 "Pass" ""
    #BIN  = "B" 52 "Fail" ""
    #BIN  = "N" 1456 "Not_Used" ""
    #MAP = {
    #"""

    f = open(path, 'w')
    for line in die_map:
        f.write("".join(line) + "\n")
    f.close()


def rcd_to_2d_array(data, missing=0):
    """
    Convert an array of tuples to a 2D array (matrix-like).

    Takes an array of tuples of (Row (y), column (x), data) and converts
    it to a 2D array where the element index is the row and column value.

    Parameters
    ----------
    data : list of tuples
        The data to convert, in the format ``[(x1, y1, d1),
        (x2, y2, d2), ...]``
    missing : any, optional
        The value to replace use for missing points.

    Returns
    -------
    array : list
        The matrix-like array.

    Example
    -------
    >>> data = [[0, 0, 'a'], [0, 1, 'b'], [0, 2, 'c'],
    ...         [1, 0, 'd'], [1, 1, 'e'], [1, 2, 'f'],
    ...         [2, 0, 'g'], [2, 2, 'i'],
    ...         ]
    >>> rcd_to_2d_array(data, 'X')
    [['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'X', 'i']]

    .. warning::

        ``data`` must be sorted by Row (y) then by Column (x) values.
    """
    #sort_by_column(data, 1)
    max_x = max([i[1] for i in data])   # note that x = column, y = row
    max_y = max([i[0] for i in data])

    # Initialize the array.
    # Might be slow for large arrays
    data_2d = [[missing for _x in range(max_x + 1)]
               for _y in range(max_y + 1)]
    for line in data:
        try:
            data_2d[line[0]][line[1]] = line[2]
        except IndexError as err:
            print("IndexError Occured for line {l}.".format(l=line))
            print(err)
            raise
    #for line in data_2d:
    #    print("".join([str(i)[0] for i in line]))
    return data_2d


def xyd_to_2d_array(data, missing=0):
    """
    Convert an array of tuples to a 2D array (matrix-like).

    Takes an array of ``(x, y, data)`` tuples and converts
    it to a 2D array where the element index is the Y and X value.

    Parameters
    ----------
    data : list of tuples
        The data to convert, in the format ``[(x1, y1, d1),
        (x2, y2, d2), ...]``
    missing : any, optional
        The value to replace use for missing points.

    Returns
    -------
    array : list
        The matrix-like array.

    Example
    -------
    >>> data = [[0, 0, 'a'], [0, 1, 'b'], [0, 2, 'c'],
    ...         [1, 0, 'd'], [1, 1, 'e'], [1, 2, 'f'],
    ...         [2, 0, 'g'], [2, 2, 'i'],
    ...         ]
    >>> xyd_to_2d_array(data, 'X')
    [['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'X', 'i']]

    .. warning::
        ``data`` must be sorted by X then by Y values.
    """
    #sort_by_column(data, 1)
    max_x = max([i[0] for i in data])   # note that x = column, y = row
    max_y = max([i[1] for i in data])

    # Initialize the array.
    # Might be slow for large arrays
    data_2d = [[missing for y in range(max_y + 1)] for x in range(max_x + 1)]
    for line in data:
        try:
            data_2d[line[0]][line[1]] = line[2]
        except IndexError as err:
            print("IndexError Occured for line {l}.".format(l=line))
            print(err)
            raise
    return data_2d


def convert_rcd_xyd(rcd):
    """
    Convert a list of ``(a, b, data)`` to ``(b, a, data)``.

    Simply swaps the first two items in each sublist. Also sorts the new
    list by ``x`` then ``y``.

    Parameters
    ----------
    rcd : list of tuples
        The data to convert.

    Returns
    -------
    list of tuples
        A copy of ``rcd`` with sublist index 0 and 1 swapped, sorted.
    """
    return sort_by_column([(_i[1], _i[0], _i[2]) for _i in rcd], 0, 1)


def array_2d_to_str(array_2d):
    """
    Convert a 2D array to a spreadsheet string.

    Parameters
    ----------
    array_2d : list of lists
        The array to convert.

    Returns
    -------
    str
        A csv-compatible string.
    """
    output_str = ""
    for line in array_2d:
        output_str += ''.join([str(i) for i in line]) + "\n"
    return output_str


def reedholm_die_to_rc(die_name):
    """
    Convert the Reedholm die name ("x27y54") to a row-column tuple.

    Parameters
    ----------
    die_name : str
        The die name to parse.

    Returns
    -------
    tuple :
        The ``(row, column)`` grid coordinate.
    """
    split_die_name = die_name.split("y")
    if len(split_die_name[0]) == 1:
        x_col = 0
    else:
        x_col = int(split_die_name[0][1:])
    if len(split_die_name[1]) == 0:
        y_row = 0
    else:
        y_row = int(split_die_name[1])

    return (y_row, x_col)


#@decorators.Timed
def binary_file_compare(file1, file2):
    """
    Compare two files byte-by-byte.

    Parameters
    ----------
    file1 : str
        The path to the master file
    file2 : str
        The path to the 2nd file.

    Returns
    -------
    failcode : int
        A flag providing information on where the difference is located.

    Notes
    -----

    Fail codes can be:

    + 0: files match
    + 1: different sizes
    + 2: different first or last byte
    + 3: different data in statistically significant random sample
    + 4: different data in full search

    See :func:`significant_subsample` for more information on failcode ``3``.
    """
    failcode = 0
    with open(file1, 'rb') as ref:
        with open(file2, 'rb') as tmp:
            # First byte check
            if not ref.read(1) == tmp.read(1):
                failcode = 1
                return failcode

            # File Size Check
            ref.seek(-1, 2)
            tmp.seek(-1, 2)
            if not ref.tell() == tmp.tell():
                failcode = 2
                return failcode

            # Last byte check
            ref.seek(-1, 2)
            tmp.seek(-1, 2)
            if not ref.read(1) == tmp.read(1):
                failcode = 3
                return failcode

            # Check a random subset check
            # Limit the subset to a statistically significant size.
            tmp.seek(-1, 2)
            rand_bytes = significant_subsample(range(int(tmp.tell())))
            for rand_byte in rand_bytes:
                ref.seek(rand_byte)
                tmp.seek(rand_byte)
                if not ref.read(1) == tmp.read(1):
                    failcode = 4
                    return failcode

            # all else matched, so we try a full compare. Very Slow.
#            ref.seek(0, 0)
#            tmp.seek(0, 0)
#            for ref_byte, tmp_byte in zip(ref, tmp):
#                match = ref_byte == tmp_byte
#                if not match:
#                    failcode = 5
#                    return failcode

            # Full compare using checksum
            ref.seek(0, 0)
            tmp.seek(0, 0)
            ref_hash = hashlib.md5(ref.read()).hexdigest()
            tmp_hash = hashlib.md5(tmp.read()).hexdigest()
            if not ref_hash == tmp_hash:
#                if timer:
#                    ct.stop()
                failcode = 5
                return failcode

            # Full compare using checksum
#            ref_hash = hash_file(ref, hashlib.md5())
#            tmp_hash = hash_file(ref, hashlib.md5())
#            if not ref_hash == tmp_hash:
#                failcode = 5
#                return failcode

    # if we magically exit that loop without hitting one of the return
    # statements, then the file's good
    return failcode


def hash_file(file_object, hasher, blocksize=65536):
    """
    Hash a file using a given hashing type.

    Parameters
    ----------
    file_object : io.IOBase object
        The stream to hash.
    hasher : hashlib.HASH object
        The hasher to use.
    blocksize : int, optional
        The block size to read from ``file_object``.

    Returns
    -------
    digest :
        The hash digest of the stream.


    .. note::

       ``file_object`` must already be opened.

    .. hint::

       Examples of valid hashers are ``hashlib.md5()``, ``hashlib.sha256()``,
       etc.
    """
    buf = file_object.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = file_object.read(blocksize)
    return hasher.digest()


def significant_subsample(array, CI=0.95, E=0.02, p=0.5):
    """
    Return a subarray that is a statictically significant sampling.

    Assumes the original array is the entire population.

    See docstring for the significant_sample_size function for more
    information.

    Parameters
    ----------
    array : sequence
        The array to create a subset of.

    CI : float [0.95]
        The desired confidence interval. Must be between 0 and 1 inclusive.

    E : float [0.02]
        The desired margin of error. Must be between 0 and 1 inclusive.

    p : float [0.5]
        Response distribution. This is what the expected response rate is.
        If you aren't sure, use 0.5 as that results in the largest sample
        size. Must be between 0 and 1 inclusive.

    Returns
    -------
    subarray : sequence
        A random subset of ``array`` that is ``N`` items long, where ``N``
        is defined by the input parameters.


    .. seealso::

       :func:`significant_sample_size`, :func:`reservoir_sampling`

    .. note::

       + Timing: O(n)
    """
    n = significant_sample_size(len(array), CI=CI, E=E, p=p)
    return reservoir_sampling(array, n)


def _integrate(f, a, b, N=200):
    """
    Integrate function ``f`` from ``a`` to ``b`` using ``N`` itertions.

    Parameters
    ----------
    f : function
        The function to integrate. Must take a single numeric argument (or
        more if args 2 through n are optional).
    a : float
    b : float
        The limits of the integral
    N : int, optional
        The number of samples to use. Higher numbers yield more accurate
        values but cost more processing power and memory.

    Returns
    -------
    area : float
        The area under the function.

    See Also
    --------
    https://helloacm.com/how-to-compute-numerical-integration-in-numpy-python/

    Examples
    --------
    >>> _integrate(np.sin, 0, np.pi/2, 100)
    1.0000102809119051
    """
    x = np.linspace(
        a + (b - a) / (2*N),
        b - (b - a) / (2*N),
        N
    )
    fx = f(x)
    area = np.sum(fx)*(b-a)/N
    return area


def normal_cdf(x):
    """
    Return the probability for a z-score of ``x``.

    Parameters
    ----------
    x : float
        The value to.. stuff and things.

    Returns
    -------
    float
        The probability that a value below ``x`` will occur.

    References
    ----------
    https://en.wikipedia.org/wiki/Normal_distribution#Cumulative_distribution_function

    Examples
    --------
    >>> round(normal_cdf(1.96), 3)
    0.975
    >>> round(normal_cdf(1.6448536269514722), 3)
    0.95
    >>> round(normal_cdf(2.5758293035489004), 3)
    0.995
    >>> round(normal_cdf(0), 3)
    0.5
    >>> round(normal_cdf(-1), 3)
    0.159

    # 68-95-99.7 rule
    >>> round(normal_cdf(1) - normal_cdf(-1), 2)
    0.68
    >>> round(normal_cdf(2) - normal_cdf(-2), 2)
    0.95
    >>> round(normal_cdf(3) - normal_cdf(-3), 3)
    0.997

    # The probit function should be the inverse of this
    >>> round(probit(normal_cdf(1)), 2)
    1.0
    >>> round(probit(normal_cdf(2)), 2)
    2.0
    """
    return 0.5 * (1 + erf(x / math.sqrt(2)))


def probit(p):
    """
    Return the probit function at probability ``p``.

    Parameters
    ----------
    p : float
        Probability that a value will be drawn from the returned range.
        Must be between 0 and 1 inclusive.

    Returns
    -------
    float
        The value of the probit function at ``p``.

    Notes
    -----
    This was shamelessly taken from the Scipy source code. I don't want to
    deal with getting a scipy requirement working for this project and I only
    use this bit from it so... I figured I'd make it myself.

    Examples
    --------
    >>> round(probit(0.025), 2)
    -1.96
    >>> round(probit(0.975), 2)
    1.96
    >>> probit(0.5)
    0.0
    >>> round(probit(0.95), 12)
    1.644853626951
    """
    if p < 0 or p > 1:
        raise ValueError("prob must be between 0 and 1 inclusive")

    return math.sqrt(2) * erfinv(2 * p - 1)


def z_score_from_confidence_interval(ci):
    """
    Return a Z-score for a given confidence interval.

    Parameters
    ----------
    ci : float
        The confidence intervalue to use. Must be beween 0 and 1 inclusive.

    Returns
    -------
    float
        The z-score (the number of standard deviations from the mean) for
        a symmetric interval.

    Examples
    --------
    >>> round(z_score_from_confidence_interval(0.95), 12)
    1.95996398454
    >>> round(z_score_from_confidence_interval(0.90), 12)
    1.644853626951
    >>> round(z_score_from_confidence_interval(0.975), 12)
    2.241402727605
    """
    p = (ci + 1) / 2
    return probit(p)


def significant_sample_size(N, **kwargs):
    r"""
    Return the significant sample size.

    The significant sample size is the sample size needed to provide a given
    z-score. (or confidence interval) and margin of error from a population
    of size ``N`` and response distribution ``p``. Assumes a normal
    distribution.

    Parameters
    ----------
    N : int
        The population size.
    Z : float, optional [1.96]
        The Z-score for the desired confidence interval. If given, ``CI``
        must not be given. Defaults to a confidence interval of 95%.
    CI : float, optional [0.95]
        The desired confidence interval. Must be between 0 and 1 inclusive.
        If given, ``Z`` must not be given. Defaults to a Z-score of 1.96.
    E : float, optional [0.02]
        The desired margin of error. Must be between 0 and 1 inclusive.
    p : float, optional [0.5]
        Response distribution. This is what the expected response rate is.
        If you aren't sure, use 0.5 as that results in the largest sample
        size. Must be between 0 and 1 inclusive.

    Returns
    -------
    n : int
        The number of samples needed.

    Examples
    --------
    >>> significant_sample_size(1000)
    706
    >>> significant_sample_size(1000, Z=1.6448, E=0.05)
    213
    >>> significant_sample_size(1000, Z=1.6448, E=0.1)
    63
    >>> significant_sample_size(1000, Z=1.6448, E=0.1, p=0.3)
    53
    >>> significant_sample_size(10000)
    1936
    >>> significant_sample_size(1000, CI=0.95, E=0.02)
    706
    >>> significant_sample_size(1000, CI=0.96, E=0.02)
    725
    >>> significant_sample_size(1000, CI=0.95, E=0.03)
    516

    Notes
    -----
    The sample size for the statistically significant random sample is given
    by:

    .. math::
        n = \frac{N \times Z^2 \times p(1-p)}
                 {(N-1) E^2 +(Z^2 \times p(1-p))}

    - n = sample size
    - N = population size
    - Z = z-score for a given confidence interval
    - E = margin of error
    - p = is the response distribution (what the expected response rate is)

    Info from http://www.raosoft.com/samplesize.html which provides the
    following equations:

    .. math ::
        x = Z^2 \times p(1-p)

    .. math ::
        n = \frac{(N \times x)}{((N-1) \times E^2 + x)}

    .. math ::
        E^2 = \frac{(N - n) \times x}{n(N-1)}

    Note that on the website: :math:`Z(c)^2`, where :math:`Z` is
    a function of :math:`c`.

    Typical Z-scrore / confidence interval values are:

    - Z = 1.6448536269514722 -> 90%
    - Z = 1.959963984540054 -> 95%
    - Z = 2.5758293035489004 -> 99%

    and I have no idea how to calculate them.

    For a given population size, the margin of error ``E`` typically
    has a much stronger effect on ``n`` than the confidence interval does.

    Example:

    >>> # Given a population of 1000, a CI of 95%, and a MoE of 2%:
    >>> significant_sample_size(1000, CI=0.95, E=0.02)
    706
    >>> # a 1% change in CI means a 2.5% change in sample size:
    >>> significant_sample_size(1000, CI=0.94, E=0.02)  # 1% change in CI
    688
    >>> # a 1% change in margin of error means a 27% change in sample size:
    >>> significant_sample_size(1000, CI=0.95, E=0.03)  # 1% change in error
    516


    .. seealso::

       :func:`significant_subsample`
    """
    # Error if both the Confidence Interval and the Z-score are given
    if "CI" in kwargs and "Z" in kwargs:
        raise RuntimeError("Arguments `CI` and `Z` are mutually exclusive.")

    # Set the defaults
    Z = 1.96 if "Z" not in kwargs.keys() else kwargs['Z']
    E = 0.02 if "E" not in kwargs.keys() else kwargs['E']
    p = 0.50 if "p" not in kwargs.keys() else kwargs['p']
    if "CI" in kwargs:
        Z = z_score_from_confidence_interval(kwargs["CI"])

    return int(N * Z**2 * p*(1-p) / ((N - 1) * E**2 + (Z**2 * p*(1-p))))


@decorators.Obsolete
def significant_sample_size_ci(N, CI=0.95, E=0.02, p=0.5):
    """
    Same as significant_sample_size.

    Allows the user to enter in a confidence interval directly rather than
    using the Z-score.

    See docstring for the significant_sample_size function for more
    information.

    Uses the scipy.stats.norm.interval method to calculate the Z-score based
    on the confidence interval.

    Parameters
    ----------
    N : int
        The population size.

    CI : float [0.95]
        The desired confidence interval. Must be between 0 and 1 inclusive.

    E : float [0.02]
        The desired margin of error. Must be between 0 and 1 inclusive.

    p : float [0.5]
        Response distribution. This is what the expected response rate is.
        If you aren't sure, use 0.5 as that results in the largest sample
        size. Must be between 0 and 1 inclusive.

    Returns
    -------
    n : int
        The number of samples needed.

    Examples
    --------
    >>> significant_sample_size_ci(10000)
    1936
    >>> significant_sample_size_ci(1000, 0.95, 0.02)
    706
    >>> significant_sample_size_ci(1000, 0.96, 0.02)
    725
    >>> significant_sample_size_ci(1000, 0.95, 0.03)
    516

    See Also
    --------
    significant_sample_size :
        Returns the sample size needed to provide a given z-score
        and margin of error from a population of size ``N`` and response
        distribution ``p``. Assumes a normal distribution.
    """
    Z = probit(CI)
    return significant_sample_size(N, Z, E, p)
