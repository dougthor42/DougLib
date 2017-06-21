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
import math

# Third-Party
from hypothesis import given
from hypothesis import strategies as st

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
        """ Verifies the known-value test """
#        for name, rc in self.known_values:
#            result = core.reedholm_die_to_rc(name)
#            self.assertEqual(result, rc)
        self.assertEqual(True,
                         generic_test_equal('core.reedholm_die_to_rc',
                                            self.known_values),
                         )


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


def generic_test_equal(function, known_values):
    """ Generic known-value testing of assertNotEqual """
    for params in known_values:
        expected_result = params[-1]
        inputs = params[:-1]
        eval_str = function + "("
        for item in inputs:
            if type(item) is str:
                eval_str += "'" + item + "'" + ', '
            else:
                eval_str += str(item) + ', '
        eval_str += ")"
        result = eval(eval_str)
        return result == expected_result


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=1)
