# -*- coding: utf-8 -*-
"""
Created on Wed May 14 15:29:34 2014

@name:          test_core.py
@vers:          0.1
@author:        dthor
@created:       Wed May 14 15:29:34 2014
@modified:      Wed May 14 15:29:34 2014
@descr:         Unit Testing for douglib.core module
"""
# ---------------------------------------------------------------------------
### Imports
# ---------------------------------------------------------------------------
# Standard Library
import os.path
import unittest
import random
import hashlib
import io
import math
from types import GeneratorType

# Third-Party
from hypothesis import given
from hypothesis import assume
from hypothesis import strategies as st
import numpy as np

# Package / Application
from .. import core


REF_DATA_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             "reference_data",
                             )


class TestEngineeringNotationKnownValues(unittest.TestCase):
    """ Known-value testing for to_ and from_engineering_notation """
    # Known Values: (engr, float)
    known_values = (("1.1y", 1.1e-24),
                    ("99.99T", 99.99e12),
                    ("2.0012m", 0.0020012),
                    ("1", 1),
                    ("27", 27),
                    ("-15.63k", -15.63e3),
                    )

    def test_to_suffix(self):
        """ Convert to suffix strings """
        for string, number in self.known_values:
            result = core.from_engineering_notation(string)
            self.assertAlmostEqual(number, result)

    def test_from_suffix(self):
        """ Convert to suffix strings """
        for string, number in self.known_values:
            result = core.to_engineering_notation(number)
            self.assertEqual(string, result)

    def test_invalid_suffix_raises_keyerror(self):
        with self.assertRaises(KeyError):
            core.from_engineering_notation('1.7q')

    def test_extreme_value(self):
        self.assertEqual(core.to_engineering_notation(6.3e28), "63000Y")
        self.assertEqual(core.to_engineering_notation(2.3e-27), "0.0023y")


class TestRoundToMultiple(unittest.TestCase):
    """ Known Value testing for round_to_multiple. """
    # (value, round_to, result)
    known_values = ((1.23456, 2, 2),
                    (1.23456, 1, 1),
                    (1.23456, 10, 0),
                    (1.23456, 0.1, 1.2),
                    (1.23456, 0.4, 1.2),
                    )

    def test_known_values(self):
        """ Known-value testing for round_to_multiple """
        for x, multiple, value in self.known_values:
            result = core.round_to_multiple(x, multiple)
            self.assertAlmostEqual(value, result)

    @given(st.floats(), st.floats())
    def test_exceptions(self, x, y):
        try:
            core.round_to_multiple(x, y)
        except (ArithmeticError, ValueError):
            return
        except Exception as err:
            err_txt = "Non-expected exception raised: {}"
            raise AssertionError(err_txt.format(err))


class TestRescale(unittest.TestCase):
    """ Unit Testing of the rescale function """
    known_values = ((5, (10, 20), (0, 1), -0.5),
                    (27, (0, 200), (0, 5), 0.675),
                    (1.5, (0, 1), (0, 10), 15),
                    (5, (10, 20), (-1, 1), -2),
                    (-5, (10, 20), (-1, 1), -4),
                    (-5, (0, 20), (-10, 10), -15),
                    (0, (12, 20), (-10, 10), -40),
                    (0.5, (3, 6), (0, 20), -16.6666667),
                    (5, (0, 10), (0, -50), -25),
                    (5, (-10, 0), (0, 50), 75),
                    )

    def test_known_values(self):
        for x, orig_range, new_range, expected_result in self.known_values:
            result = core.rescale(x, orig_range, new_range)
            self.assertAlmostEqual(expected_result, result)

    @given(st.floats(),
           st.tuples(st.floats(), st.floats()),
           st.tuples(st.floats(), st.floats()),
           )
    def test_exceptions(self, x, orig, new):
        try:
            core.rescale(x, orig, new)
        except ArithmeticError:
            return
        except Exception as err:
            err_txt = "Non-expected exception raised: {}"
            raise AssertionError(err_txt.format(err))


class TestRescaleClip(unittest.TestCase):
    """ Unit Testing of the rescale function """
    known_values = ((5, (10, 20), (0, 1), 0),
                    (27, (0, 200), (0, 5), 0.675),
                    (1.5, (0, 1), (0, 10), 10),
                    (5, (10, 20), (-1, 1), -1),
                    (-5, (10, 20), (-1, 1), -1),
                    (-5, (0, 20), (-10, 10), -10),
                    (0, (12, 20), (-10, 10), -10),
                    (0.5, (3, 6), (0, 20), 0),
                    (5, (0, 10), (0, -50), -50),
                    (5, (-10, 0), (0, 50), 50),
                    )

    def test_known_values(self):
        for x, orig_range, new_range, expected_result in self.known_values:
            result = core.rescale_clip(x, orig_range, new_range)
            self.assertAlmostEqual(expected_result, result)

    @given(st.floats(),
           st.tuples(st.floats(), st.floats()),
           st.tuples(st.floats(), st.floats()),
           )
    def test_exceptions(self, x, orig, new):
        try:
            core.rescale_clip(x, orig, new)
        except ArithmeticError:
            return
        except Exception as err:
            err_txt = "Non-expected exception raised: {}"
            raise AssertionError(err_txt.format(err))

    @given(st.floats(allow_nan=False, allow_infinity=False),
           st.tuples(st.floats(), st.floats()),
           st.tuples(st.floats(), st.floats()),
           )
    def test_result_within_new_scale(self, x, orig, new):
        assume(orig[0] != orig[1])
        assume(new[0] != new[1])
        assume(new[1] > new[0])
        assume(all(abs(y) >= 1e-100 and abs(y) <= 1e100 for y in orig + new))
        assume(all(abs(y2 - y1) >= 1e-6 for y2, y1 in [orig, new]))
        res = core.rescale_clip(x, orig, new)
        self.assertGreaterEqual(res, new[0])
        self.assertLessEqual(res, new[1])


class TestClip(unittest.TestCase):
    """ Unit Testing of the clip function """
    known_values = ((5, (10, 20), (0, 1), 0),
                    (27, (0, 200), (0, 5), 27),
                    (1.5, (0, 1), (0, 10), 10),
                    (5, (10, 20), None, 10),
                    (-5, (10, 20), None, 10),
                    (-5, (0, 20), (-10, 10), -10),
                    (0, (12, 20), (-10, 10), -10),
                    (0.5, (0, 6), (0, 20), 0.5),
                    (50, (0, 10), None, 10),
                    (50, (0, 10), ("Apple", "Pear"), "Pear"),
                    )

    def test_known_values(self):
        for x, (x_min, x_max), clipval, expected in self.known_values:
            result = core.clip(x, (x_min, x_max), clipval=clipval)
            self.assertEqual(expected, result)

    @given(st.floats(),
           st.tuples(st.floats(), st.floats()),
           st.tuples(st.floats(), st.floats())
           )
    def test_exceptions(self, x, _range, clipval):
        try:
            core.clip(x, _range, clipval)
        except ArithmeticError:
            return
        except Exception as err:
            err_txt = "Non-expected exception raised: {}"
            raise AssertionError(err_txt.format(err))

    def test_invalid_clipval_type(self):
        invalid_clipvals = [
            (1, 2, 3),
            "Hello",
            {"a": 27},
        ]
        for clipval in invalid_clipvals:
            with self.subTest(clipval=clipval):
                with self.assertRaises(TypeError):
                    core.clip(0, (0, 1), clipval)


class TestMaxDistSqrd(unittest.TestCase):

    known_values = (
        ((0, 0), (1, 1), 0.5),
        ((1, 1), (1, 1), 4.5),
        ((10, 15), (2, 3), 393.25),
    )

    def test_known_values(self):
        for center, size, expected in self.known_values:
            with self.subTest(center=center, size=size, expected=expected):
                result = core.max_dist_sqrd(center, size)
                self.assertAlmostEqual(expected, result)

    @given(st.tuples(st.floats(), st.floats()),
           st.tuples(st.floats(), st.floats()))
    def test_all_results_are_positive(self, center, size):
        assume(all(abs(x) <= 1e20 for x in center + size))
        result = core.max_dist_sqrd(center, size)
        self.assertGreaterEqual(result, 0)


class TestMaxDist(unittest.TestCase):

    known_values = (
        ((0, 0), (1, 1), 0.7071067811865476),
        ((1, 1), (1, 1), 2.1213203435596424),
        ((10, 15), (2, 3), 19.83053201505194),
    )

    def test_known_values(self):
        for center, size, expected in self.known_values:
            with self.subTest(center=center, size=size, expected=expected):
                result = core.max_dist(center, size)
                self.assertEqual(expected, result)


class TestRCDto2DArray(unittest.TestCase):

    known_values = (
        ([[0, 0, 'a'], [0, 1, 'b'], [0, 2, 'c'],
          [1, 0, 'd'], [1, 1, 'e'], [1, 2, 'f'],
          [2, 0, 'g'], [2, 2, 'i']],
         0,
         [['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 0, 'i']]
         ),
    )

    def test_known_values(self):
        for data, missing, expected in self.known_values:
            with self.subTest(data=data, missing=missing, expected=expected):
                result = core.rcd_to_2d_array(data, missing)
                self.assertEqual(expected, result)


class TestXYDto2DArray(unittest.TestCase):

    known_values = (
        ([[0, 0, 'a'], [0, 1, 'b'], [0, 2, 'c'],
          [1, 0, 'd'], [1, 1, 'e'], [1, 2, 'f'],
          [2, 0, 'g'], [2, 2, 'i']],
         0,
         [['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 0, 'i']]
         ),
    )

    def test_known_values(self):
        for data, missing, expected in self.known_values:
            with self.subTest(data=data, missing=missing, expected=expected):
                result = core.xyd_to_2d_array(data, missing)
                self.assertEqual(expected, result)


class TestFrange(unittest.TestCase):

    known_values = (
        (0, 1, 0.5, [0, 0.5]),
        (0, 2, 0.5, [0, 0.5, 1, 1.5]),
    )

    def test_known_values(self):
        for start, stop, step, expected in self.known_values:
            with self.subTest(start=start, stop=stop, step=step,
                              expected=expected):
                result = list(core.frange(start, stop, step))
                self.assertEqual(expected, result)

    @given(st.floats(), st.floats(), st.floats())
    def test_return_type(self, start, stop, step):
        self.assertIsInstance(core.frange(start, stop, step), GeneratorType)


class TestArray2dToStr(unittest.TestCase):

    known_values = (
        ([[1, 2], [3, 4]], ',', "1,2\n3,4\n"),
        ([[1, 2], [3, 4]], '', "12\n34\n"),
    )

    def test_known_values(self):
        for array, delim, expected in self.known_values:
            with self.subTest(array=array, delim=delim, expected=expected):
                result = core.array_2d_to_str(array, delim)
                self.assertEqual(expected, result)


class TestThreshold1DArray(unittest.TestCase):
    """ Unit Testing of the threshold_1d_array function """
    list1 = range(8)
    list2 = [x*2 for x in range(10)]

    known_values = ((5, list1, 5),
                    (3, list2, 1.5),
                    (16.25, list2, 8.125),
                    (5.3, list1, 5.3),
                    )

    def test_known_values(self):
        for y, array, expected_result in self.known_values:
            result = core.threshold_1d_array(array, y)
            self.assertAlmostEqual(expected_result, result)

    @given(st.lists(st.floats()), st.floats())
    def test_exceptions(self, array, y):
        allowed_exceptions = (ValueError, IndexError, ZeroDivisionError)
        try:
            core.threshold_1d_array(array, y)
        except allowed_exceptions:
            return
        except Exception as err:
            err_txt = "Non-expected exception raised: {}"
            raise AssertionError(err_txt.format(err))

    def test_empty_array_raises_index_error(self):
        with self.assertRaises(ValueError):
            core.threshold_1d_array([], 0)


class TestInterpolate1DArray(unittest.TestCase):

    @given(st.lists(st.floats()), st.floats())
    def test_exceptions(self, array, x):
        allowed_exceptions = (ValueError, IndexError, OverflowError)
        try:
            core.interpolate_1d_array(array, x)
        except allowed_exceptions:
            return
        except Exception as err:
            err_txt = "Non-expected exception raised: {}"
            raise AssertionError(err_txt.format(err))

    def test_empty_array_raises_index_error(self):
        with self.assertRaises(IndexError):
            core.interpolate_1d_array([], 0)

    @given(st.lists(st.floats(), min_size=2))
    def test_x_inf_raises_overflow_error(self, array):
        with self.assertRaises(OverflowError):
            core.interpolate_1d_array(array, math.inf)


class TestPickXatY(unittest.TestCase):
    """ Unit Testing of the pick_x_at_y function """
    xy_array1 = [(0, 0), (1, 1), (2, 2), (3, 3)]
    xy_array2 = [(0, 0), (1, 2), (2, 4), (3, 9)]

    # array, y, expected_x
    known_values = ((xy_array1, 0.5, 0.5),
                    (xy_array1, 1, 1),
                    (xy_array1, 2.75, 2.75),
                    (xy_array1, -1, -1),
                    (xy_array1, 0, 0),
                    (xy_array2, 1, 0.5),
                    (xy_array2, 3, 1.5),
                    (xy_array2, 5, 2.2),
                    )

    def test_known_values(self):
        for xy_array, y, expected_result in self.known_values:
            result = core.pick_x_at_y(xy_array, y)
            self.assertAlmostEqual(expected_result, result)

    @given(st.lists(st.tuples(st.floats(), st.floats())), st.floats())
    def test_exceptions(self, xy_array, y):
        allowed_exceptions = (ValueError, IndexError, ZeroDivisionError)
        try:
            core.pick_x_at_y(xy_array, y)
        except allowed_exceptions:
            pass
        except Exception as err:
            err_txt = "Non-expected exception raised: {}"
            raise AssertionError(err_txt.format(err))


class TestHashFile(unittest.TestCase):

    def test_return_type(self):

        h = hashlib.sha256()
        f = io.StringIO("Some test data")
        self.assertIsInstance(core.hash_file(f, h), bytes)


class Test_Integrate(unittest.TestCase):

    known_values = (
        (lambda x: x*2, 0, 2, 4),
        (lambda x: x**2, -1, 2, 3),
        (lambda x: x**3, 1, 3, 20),
        (lambda x: 2 * np.sin(x) + 1, 1, 3, 5.0606),
    )

    def test_integrate(self):
        for func, start, stop, expected in self.known_values:
            with self.subTest(func=func, start=start, stop=stop,
                              expected=expected):
                result = core._integrate(func, start, stop)
                self.assertAlmostEqual(expected, result, places=3)


class TestNormalCDF(unittest.TestCase):

    # (input, rounding value, expected)
    known_values = (
        (1.96, 3, 0.975),
        (1.6448536269514722, 3, 0.95),
        (2.5758293035489004, 3, 0.995),
        (0, 3, 0.5),
        (-1, 3, 0.159),
    )

    def test_known_values(self):
        for x, round_to, expected in self.known_values:
            with self.subTest(x=x, round_to=round_to, expected=expected):
                result = round(core.normal_cdf(x), round_to)
                self.assertEqual(expected, result)

    @given(st.floats())
    def test_all_floats_are_valid_inputs(self, x):
        try:
            core.normal_cdf(x)
        except Exception as err:
            err_txt = "Non-expected exception raised: {}"
            raise AssertionError(err_txt.format(err))


class TestProbit(unittest.TestCase):

    known_values = (
        (0.025, 2, -1.96),
        (0.975, 2, 1.96),
        (0.5, 2, 0.0),
        (0.95, 12, 1.644853626951),
    )

    def test_known_values(self):
        for x, round_to, expected in self.known_values:
            with self.subTest(x=x, round_to=round_to, expected=expected):
                result = round(core.probit(x), round_to)
                self.assertEqual(expected, result)

    @given(st.floats())
    def test_exceptions(self, x):
        try:
            core.probit(x)
        except ValueError:
            pass
        except Exception as err:
            err_txt = "Non-expected exception raised: {}"
            raise AssertionError(err_txt.format(err))


class TestReservoirSampling(unittest.TestCase):
    """ Tests for the Reservior Sampling function """
    dataset = range(100)
    good_lengths = [0, 1, 10, 34, 127]
    bad_lengths = [-162, -13.27, -12, -1, 52.6, "a", None, "1"]

    def setUp(self):
        """ Gets run before every test """
        pass

    def tearDown(self):
        """ Runs after the tests if and only if setUp succeeded. """
        pass

    def test_subset(self):
        """ Check that all chosen elements are part of the original set """
        for length in self.good_lengths:
            subset = set(core.reservoir_sampling(self.dataset, length))
            self.assertTrue(subset.issubset(set(self.dataset)))

    def test_good_length(self):
        """ Check that we have n or all of the original data set """
        for length in self.good_lengths:
            subset = core.reservoir_sampling(self.dataset, length)
            if length > len(self.dataset):
                length = len(self.dataset)
            self.assertEqual(len(subset), length)

    def test_bad_length(self):
        """ Checks that invalid lenght args raise a ValueError """
        for length in self.bad_lengths:
            self.assertRaises(ValueError,
                              core.reservoir_sampling,
                              self.dataset,
                              length,
                              )

    def test_seeded_value(self):
        random.seed(12345)
        expected = [53, 94, 2, 23, 40, 82, 95, 96, 25, 38]
        result = core.reservoir_sampling(self.dataset, 10)
        self.assertEqual(result, expected)


class TestReedholmDieNameToRC(unittest.TestCase):
    """ Tests the reedholm_die_to_rc function """
    # (Reedholm Die Name, (row, column))
    known_values = (("x0y0", (0, 0)),
                    ("x1y1", (1, 1)),
                    ("x24y81", (81, 24)),
                    ("x-10y-99", (-99, -10)),
                    ("x1001y786", (786, 1001)),
                    ("xy90", (90, 0)),
                    ("x123y", (0, 123)),
                    )

    def test_known_values(self):
        for val, expected in self.known_values:
            with self.subTest(val=val, expected=expected):
                self.assertEqual(core.reedholm_die_to_rc(val), expected)


class TestRCtoRadius(unittest.TestCase):
    """ Tests the rc_to_radius function """
    # ((r_coord, c_coord), (die_x, die_y), (center_x, center_y), expected)
    known_values = (((5, 2), (2.43, 3.3), (18, 4), 43.17440909),
                    )

    def test_known_values(self):
        for rc_coord, die_size, center_xy, expected in self.known_values:
            result = core.rc_to_radius(rc_coord, die_size, center_xy)
            self.assertAlmostEqual(expected, result)


#@unittest.skip("Skipped")
class TestBinaryFileCompare(unittest.TestCase):
    """ Tests the binary_file_compare function """
    ref_file = "ref_BinaryFileCompare.csv"
    bad_file = ("ref_BinaryFileCompare_start_diff.csv",
                "ref_BinaryFileCompare_size_diff.csv",
                "ref_BinaryFileCompare_end_diff.csv",
                "ref_BinaryFileCompare_allbyte_diff.csv",
                "ref_BinaryFileCompare_1byte_diff.csv",
                "ref_BinaryFileCompare_2nd_to_last_diff.csv",
#                "ref_BinaryFileCompare_large.csv",
                )
    ref_file_path = os.path.join(REF_DATA_PATH, ref_file)

    def test_equal(self):
        match = core.binary_file_compare(self.ref_file_path,
                                         self.ref_file_path)
        self.assertEqual(match, 0)

    def test_unequal(self):
        for name in self.bad_file:
            path = os.path.join(REF_DATA_PATH, name)
            match = core.binary_file_compare(self.ref_file_path,
                                             path)
            self.assertNotEqual(match, 0)


class TestSignificantSampleSize(unittest.TestCase):
    """ Significant Sample Size """
    # ((population, Z(CI), margin of Error, response_dist), sample_size)
    known_values = (((10000, 0.95, 0.02, 0.5), 1936),
                    ((1234, 0.95, 0.02, 0.5), 815),
                    ((3214, 0.95, 0.02, 0.5), 1374),
                    ((3214, 0.95, 0.05, 0.5), 343),
                    ((10000, 0.95, 0.05, 0.5), 369),
                    ((10000, 0.95, 0.10, 0.5), 95),
                    ((10000, 0.99, 0.02, 0.5), 2931),
                    )

    def test_known_values(self):
        """ known value testing for sample size """
        for (N, ci, E, p), expected in self.known_values:
            result = core.significant_sample_size(N, E=E, p=p, CI=ci)
            self.assertEqual(expected, result)

    def test_mutually_exclusive_args_raises_runtime_error(self):
        with self.assertRaises(RuntimeError):
            core.significant_sample_size(100, E=0.95, p=0.2, CI=0.5, Z=1.96)


class TestSortByColumn(unittest.TestCase):
    """ sort_by_column """
    # the array to be sorted
    array = [[3, 5, 10], [2, 4, 1], [1, 7, 5]]

    # (arguements, expected result)
    known_values = (((0), [[1, 7, 5], [2, 4, 1], [3, 5, 10]]),
                    ((1), [[2, 4, 1], [3, 5, 10], [1, 7, 5]]),
                    ((2), [[2, 4, 1], [1, 7, 5], [3, 5, 10]]),
                    )

    def test_known_values(self):
        """ kvt for sort_by_column """
        for args, expected in self.known_values:
            result = core.sort_by_column(self.array, args, inplace=False)
            self.assertEqual(expected, result)

    def test_invalid_type(self):
        """ Ensure that invalid types for inplace raise a TypeError """
        types = (1, 'a', [1, 2, 3], 1.33)
        for _type in types:
            with self.assertRaises(TypeError):
                core.sort_by_column(self.array, 0, inplace=_type)

    def test_invalid_args(self):
        """ Ensure that invalid kwargs for sot_by_column raise SyntaxErrors """
        with self.assertRaises(SyntaxError):
            core.sort_by_column(self.array, 0, hello=True)
        with self.assertRaises(SyntaxError):
            core.sort_by_column(self.array, 0, hello=True, aaa=False)

    def test_sort_inplace(self):
        array = [[3, 5, 10], [2, 4, 1], [1, 7, 5]]
        expected = [[1, 7, 5], [2, 4, 1], [3, 5, 10]]
        result = core.sort_by_column(array, 0, inplace=True)
        self.assertEqual(array, expected)
        self.assertIsNone(result)


class TestConvertRcdXyd(unittest.TestCase):

    known_values = (
        ([(1, 2, "a"), (3, 4, "b"), (5, 6, "c")],
         [(2, 1, "a"), (4, 3, "b"), (6, 5, "c")]),
    )

    def test_known_values(self):
        for rcd, expected in self.known_values:
            with self.subTest(rcd=rcd, expected=expected):
                result = core.convert_rcd_xyd(rcd)
                self.assertEqual(expected, result)
