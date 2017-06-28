# -*- coding: utf-8 -*-
"""
Unit tests for :py:mod:`douglib.utils`.
"""
# ---------------------------------------------------------------------------
### Imports
# ---------------------------------------------------------------------------
# Standard Library
import os.path
import sys
import unittest
import time
import datetime as dt

# Third-Party
from hypothesis import given
#from hypothesis import assume
from hypothesis import strategies as st

# Package / Application
from .. import utils


class TestDougLibError(unittest.TestCase):

    def test_instantiation(self):
        try:
            utils.DougLibError()
        except Exception:
            self.fail("An exception was raised when instantiating the class")


class TestRangeError(unittest.TestCase):

    def test_instantiation(self):
        try:
            utils.RangeError(20)
        except Exception:
            self.fail("An exception was raised when instantiating the class")

    def test_instantiation_raises_with_no_arg(self):
        with self.assertRaises(TypeError):
            utils.RangeError()

    def test_str(self):
        val = 20
        re = utils.RangeError(val)
        self.assertEqual(str(val), str(re))


class TestObsoleteError(unittest.TestCase):

    def test_instantiation(self):
        try:
            utils.ObsoleteError()
        except Exception:
            self.fail("An exception was raised when instantiating the class")

    def test_str(self):
        val = 20
        re = utils.ObsoleteError(val)
        self.assertEqual(str(val), str(re))


class TestUnjoinPath(unittest.TestCase):
    """ Verifies the unjoin_path() function """
    known_values = (("C:\\Temp",
                     ["C:\\", "Temp"]),
                    (r"C:\Temp\folder\hello.txt",
                     ["C:\\", "Temp", "folder", "hello.txt"]),
                    )

    def test_sanity(self):
        for path, _ in self.known_values:
            result = os.path.join(*utils.unjoin_path(path))
            self.assertEqual(path, result)

    def test_unjoin(self):
        if sys.platform in ['linux', 'darwin']:
            print(utils.unjoin_path(self.known_values[0][0]))
            print(utils.unjoin_path(self.known_values[1][0]))
            print(utils.unjoin_path("/a/b/c/d.txt"))
            self.skipTest("Need to determine known values for linux")
        else:
            for path, expected in self.known_values:
                result = utils.unjoin_path(path)
                self.assertEqual(result, expected)


class TestTryAgain(unittest.TestCase):

    def test_try_again(self):
        expected = 3
        errors = [ValueError] * 3
        args = [1, 2, expected]
        kwargs = [None] * 3

        def func_to_test(a):
            if a == expected:
                return a
            else:
                raise ValueError

        funcs = [func_to_test] * 3
        result = utils.try_again(funcs, args, kwargs, errors)
        self.assertEqual(result, expected)

    def test_raises_type_error_when_not_all_iterable(self):
        with self.assertRaises(TypeError):
            utils.try_again("a", None, None, None)

    def test_raises_value_error_when_not_all_same_lenght(self):
        with self.assertRaises(ValueError):
            utils.try_again(["a", 'b'], [None], [None], [None])

    def test_funcs_use_kwargs(self):
        expected = 3
        errors = [ValueError] * 3
        args = [None] * 3
        kwargs = [{'a': 1}, {'a': 2}, {'a': expected}]

        def func_to_test(a):
            if a == expected:
                return a
            else:
                raise ValueError

        funcs = [func_to_test] * 3
        result = utils.try_again(funcs, args, kwargs, errors)
        self.assertEqual(result, expected)

    def test_funcs_have_star_args(self):
        expected = (7, 8, 9)
        errors = [ValueError] * 3
        args = [[1, 2, 3], [4, 5, 6], expected]
        kwargs = [None] * 3

        def func_to_test(*a):
            if a == expected:
                return a
            else:
                raise ValueError

        funcs = [func_to_test] * 3
        result = utils.try_again(funcs, args, kwargs, errors)
        self.assertEqual(result, expected)

    def test_funcs_have_star_args_and_use_kwargs(self):
        expected = 3
        errors = [ValueError] * 3
        args = [[1, 2, 3]] * 3
        kwargs = [{'b': 1}, {'b': 2}, {'b': expected}]

        def func_to_test(*a, b):
            if b == expected:
                return b
            else:
                raise ValueError

        funcs = [func_to_test] * 3
        result = utils.try_again(funcs, args, kwargs, errors)
        self.assertEqual(result, expected)

    def test_different_functions_and_errors(self):
        expected = 3
        errors = [ValueError, IndexError, KeyError]
        args = [None] * 3
        kwargs = [None] * 3
        funcs = [lambda: raise_(ValueError),
                 lambda: raise_(IndexError),
                 lambda: expected]
        result = utils.try_again(funcs, args, kwargs, errors)
        self.assertEqual(result, expected)

    def test_raises_runtime_error_if_nothing_succeeds(self):
        funcs = [lambda: raise_(ValueError)] * 5
        kwargs = args = [None] * 5
        errors = [ValueError] * 5
        with self.assertRaises(RuntimeError):
            utils.try_again(funcs, args, kwargs, errors)

    def test_raises_custom_error_if_nothing_succeeds(self):
        funcs = [lambda: raise_(ValueError)] * 5
        kwargs = args = [None] * 5
        errors = [ValueError] * 5
        custom_error = OSError
        with self.assertRaises(custom_error):
            utils.try_again(funcs, args, kwargs, errors, custom_error)


class TestBorg(unittest.TestCase):

    def test_instantiation(self):
        try:
            utils.Borg()
        except Exception:
            self.fail("An exception was raised when instantiating the class")

    def test_all_instances_have_different_id(self):
        a = utils.Borg()
        b = utils.Borg()
        self.assertNotEqual(id(a), id(b))

    def test_all_instances_have_same_data(self):
        a = utils.Borg()
        b = utils.Borg()
        a.value = 5
        self.assertEqual(a.value, b.value)


class TestSingleton(unittest.TestCase):

    def test_instantiation(self):
        try:
            utils.Singleton()
        except Exception:
            self.fail("An exception was raised when instantiating the class")

    def test_all_instances_have_same_id(self):
        a = utils.Singleton()
        b = utils.Singleton()
        self.assertEqual(id(a), id(b))

    def test_all_instances_have_same_data(self):
        a = utils.Singleton()
        b = utils.Singleton()
        a.value = 5
        self.assertEqual(a.value, b.value)


class TestCodeTimer(unittest.TestCase):

    def test_instantiation(self):
        try:
            utils.CodeTimer()
        except Exception:
            self.fail("An exception was raised when instantiating the class")

    def test_instantiation_with_label(self):
        try:
            utils.CodeTimer("Some Timer")
        except Exception:
            self.fail("An exception was raised when instantiating the class")

    def test_str(self):
        ct = utils.CodeTimer()
        self.assertIn("Timer:", str(ct))

    def test_start(self):
        ct = utils.CodeTimer()
        ct.start()
        self.assertIsNotNone(ct.start_t)
        self.assertIsNotNone(ct.prev_t)
        self.assertIsNone(ct.diff)
        self.assertIsNone(ct.stop_t)
        self.assertTrue(ct.running)

    def test_stop(self):
        ct = utils.CodeTimer()
        ct.start()
        retval = ct.stop()
        self.assertIsInstance(ct.stop_t, dt.datetime)
        self.assertIsInstance(ct.diff, dt.timedelta)
        self.assertFalse(ct.running)
        self.assertIsInstance(retval, dt.timedelta)

    def test_stop_with_label(self):
        ct = utils.CodeTimer("My Label")
        ct.start()
        ct.stop()

    def test_stop_with_label_override(self):
        ct = utils.CodeTimer("My Label")
        ct.start()
        ct.stop("label override")

    def test_reset(self):
        ct = utils.CodeTimer()
        ct.start()
        self.assertTrue(ct.running)
        ct.reset()
        self.assertTrue(ct.running)
        self.assertIsNone(ct.diff)
        self.assertIsNone(ct.stop_t)

    def test_lap(self):
        ct = utils.CodeTimer()
        ct.start()
        time.sleep(1)
        diff = ct.lap()
        self.assertAlmostEqual(diff.total_seconds(), 1, delta=0.6)
        self.assertIsInstance(ct.stop_t, dt.datetime)
        time.sleep(1)
        diff = ct.lap()
        self.assertAlmostEqual(diff.total_seconds(), 2, delta=0.6)
        self.assertIsInstance(ct.stop_t, dt.datetime)

    def test_lap_with_label(self):
        ct = utils.CodeTimer("My Label")
        ct.start()
        ct.lap()

    def test_lap_with_label_override(self):
        ct = utils.CodeTimer("My Label")
        ct.start()
        ct.lap("label override")

    def test_delta(self):
        ct = utils.CodeTimer()
        ct.start()
        time.sleep(1)
        diff = ct.delta()
        self.assertAlmostEqual(diff.total_seconds(), 1, delta=0.6)
        self.assertIsInstance(ct.stop_t, dt.datetime)
        time.sleep(1)
        diff = ct.delta()
        self.assertAlmostEqual(diff.total_seconds(), 1, delta=0.6)
        self.assertIsInstance(ct.stop_t, dt.datetime)

    def test_delta_with_label(self):
        ct = utils.CodeTimer("My Label")
        ct.start()
        ct.delta()

    def test_delta_with_label_override(self):
        ct = utils.CodeTimer("My Label")
        ct.start()
        ct.delta("label override")

    def test_stopping_timer_before_its_started_raises_runtime_error(self):
        ct = utils.CodeTimer("My Label")
        with self.assertRaises(RuntimeError):
            ct.stop()

    def test_lapping_timer_before_its_started_raises_runtime_error(self):
        ct = utils.CodeTimer("My Label")
        with self.assertRaises(RuntimeError):
            ct.lap()

    def test_deltaing_timer_before_its_started_raises_runtime_error(self):
        ct = utils.CodeTimer("My Label")
        with self.assertRaises(RuntimeError):
            ct.delta()


class TestHexversToStr(unittest.TestCase):

    known_values = (
        (34014960, '2.7.6.f0'),
        (50660080, '3.5.2.f0'),
    )

    def test_known_values(self):
        for hexvers, expected in self.known_values:
            with self.subTest(hexvers=hexvers, expected=expected):
                self.assertEqual(expected, utils.hexvers_to_str(hexvers))

    def test_result_is_str(self):
        self.assertIsInstance(utils.hexvers_to_str(), str)


class TestPrintRed(unittest.TestCase):

    @given(st.text(st.characters()))
    def test_no_exceptions(self, val):
        try:
            utils.print_red(val)
        except Exception as err:
            err_txt = "Non-expected exception raised: {}"
            raise AssertionError(err_txt.format(err))


class TestCprint(unittest.TestCase):

    @given(st.text(st.characters()))
    def test_exceptions(self, val):
        try:
            utils.cprint(val, 'r')
        except Exception as err:
            err_txt = "Non-expected exception raised: {}"
            raise AssertionError(err_txt.format(err))


class TestPrintSection(unittest.TestCase):

    @given(st.text(st.characters()), st.integers())
    def test_exceptions(self, text, style):
        try:
            utils.print_section(text, style)
        except ValueError:
            pass
        except Exception as err:
            err_txt = "Non-expected exception raised: {}"
            raise AssertionError(err_txt.format(err))

    @given(st.text(st.characters()))
    def test_styles(self, text):
        for style in [1, 2, 3]:
            try:
                utils.print_section(text, style)
            except Exception as err:
                err_txt = "Non-expected exception raised: {}"
                raise AssertionError(err_txt.format(err))


class TestPrintInput(unittest.TestCase):

    @given(st.text(st.characters()))
    def test_exceptions(self, text):
        try:
            utils.print_input(text)
        except Exception as err:
            err_txt = "Non-expected exception raised: {}"
            raise AssertionError(err_txt.format(err))


class TestProgressBar(unittest.TestCase):

    def test_exceptions(self):
        try:
            utils.progress_bar(10, 10, 10)
        except Exception as err:
            err_txt = "Non-expected exception raised: {}"
            raise AssertionError(err_txt.format(err))


def raise_(exception):
    """ Used only in the lambda functions for testing ``try_again``. """
    raise exception
