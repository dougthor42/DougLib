# -*- coding: utf-8 -*-
"""
Unit tests for :py:mod:`douglib.decorators`.

Things I want to be true:
Classes:
    temp.__str__()                 = __str__() for TestClass
    temp.__repr__                  = __repr__() for TestClass"
    temp.__doc__                   = docsctring of TestClass
    temp.__decor__                 = the decorators for the class
    temp.__decordoc__              = class's decorator docstrings
Class Methods:
    temp.temp_method.__name__      = "temp_method"
    temp.temp_method.__doc__       = " temp_method docstring "
    temp.temp_method.__decor__     = "ExampleDecorator"
    temp.temp_method.__decordoc__  = " ExampleDecorator docstring "
Functions:
    temp_func.__name__             = "temp_func"
    temp_func.__doc__              = " docstring for temp_func "
    temp_func.__decor__            = "ExampleDecorator"
    temp_func.__decordoc__         = " ExampleDecorator docstring "

Some decorators should make aspects of them public, such as the Cached
decorator: the user should be able to call Cached.cache and get a dict
of the cached values.
"""

# ---------------------------------------------------------------------------
### Imports
# ---------------------------------------------------------------------------
# Standard Library
import platform
import unittest
import sys

# Third-Party

# Package / Application
from .. import decorators as dec
from .. import utils


# ---------------------------------------------------------------------------
### Dummy Functions and Classes used by tests
# ---------------------------------------------------------------------------
@dec.EnterExit
def temp_func(a):
    """ docstring for temp_func """
    return a


class TempClass(object):
    """
    Decorator testing
    """
    def __init__(self, n):
        self.n = n

    @dec.EnterExit
    def temp_method(self):
        """ temp_method docstring """
        a = b = 1
        result = []
        for _ in range(self.n):
            result.append(a)
            a, b = b, a + b
        return result


@dec.EnterExit
class TempClass2(object):
    """ TempClass2 docstring """
    def __init__(self, n):
        self.n = n

    def another_method(self):
        """ docstring for another_method """
        a = b = 1
        result = []
        for _ in range(self.n):
            result.append(a)
            a, b = b, a + b
        return result

    def __str__(self):
        return "str representation of TempClass2"

    def __repr__(self):
        return "repr for TempClass2"


# ---------------------------------------------------------------------------
### Unit Tests
# ---------------------------------------------------------------------------
class TestFunctionDecorator(unittest.TestCase):
    """
    Make sure that test_func.__name__, .__doc__, .__decor__, .__decordoc__
    are working as expected:

        temp_func.__name__             = "temp_func"
        temp_func.__doc__              = " docstring for temp_func "
        temp_func.__decor__            = "ExampleDecorator"
        temp_func.__decordoc__         = " ExampleDecorator docstring "
    """
    def test_funcion(self):
        """ Check that the function actually runs """
        self.assertEqual(temp_func(5), 5)

    def test_name(self):
        """ Check that temp_func.__name__ returns correctly """
        self.assertEqual(temp_func.__name__,
                         "temp_func")

    def test_doc(self):
        """ Check that temp_func.__doc__ returns correctly """
        self.assertEqual(temp_func.__doc__,
                         " docstring for temp_func ")

    def test_decor(self):
        """ Check that temp_func.__decor__ returns correctly """
        self.assertEqual(temp_func.__decor__,
                         "EnterExit Decorator")

    def test_decordoc(self):
        """ Check that temp_func.__decordoc__ returns correctly """
        self.assertEqual(temp_func.__decordoc__,
                         " Prints entry and exit from a function ")


class TestMethodDecorator(unittest.TestCase):
    """
    Make sure that temp_method.__name__, .__doc__, .__decor__, .__decordoc__
    are working as expected:

        my_class.temp_method.__name__      = "temp_method"
        my_class.temp_method.__doc__       = " temp_method docstring "
        my_class.temp_method.__decor__     = "ExampleDecorator"
        my_class.temp_method.__decordoc__  = " ExampleDecorator docstring "
    """

    def setUp(self):        # pylint: disable=C0103
        """ setUp the TestCase by instancing the class """
        self.my_class = TempClass(250)
        self.my_class.temp_method()

    def test_name(self):
        """ Check that temp_method.__name__ returns correctly """
        self.assertEqual(self.my_class.temp_method.__name__,
                         "temp_method")

    def test_doc(self):
        """ Check that temp_method.__doc__ returns correctly """
        self.assertEqual(self.my_class.temp_method.__doc__,
                         " temp_method docstring ")

    def test_decor(self):
        """ Check that temp_method.__decor__ returns correctly """
        self.assertEqual(self.my_class.temp_method.__decor__,
                         "EnterExit Decorator")

    def test_decordoc(self):
        """ Check that temp_method.__decordoc__ returns correctly """
        self.assertEqual(self.my_class.temp_method.__decordoc__,
                         " Prints entry and exit from a function ")


class TestClassDecorator(unittest.TestCase):
    """
    Make sure that MyClass.__str__, .__repr__, .__decor__, .__decordoc__
    are working as expected:

        MyClass.__str__                   = "TestClass"
        MyClass.__repr__                  = whatever the repr def is.
        MyClass.__decor__                 = the decorators for the class
        MyClass.__decordoc__              = class's decorator docstrings
    """

    def setUp(self):        # pylint: disable=C0103
        self.my_class = TempClass2(5)
#        self.my_class.another_method()             # calls __get__

    def test_str(self):
        """ Check that my_class.__str__() returns correctly """
        self.assertEqual(self.my_class.__str__(),
                         "str representation of TempClass2")

    def test_doc(self):
        """ Check that my_class.__doc__ returns correctly """
        self.assertEqual(self.my_class.__doc__,
                         " TempClass2 docstring ")

    def test_decor(self):
        """ Check that my_class.__decor__ returns correctly """
        self.assertEqual(self.my_class.__decor__,
                         "EnterExit Decorator")

    def test_decordoc(self):
        """ Check that my_class.__decordoc__ returns correctly """
        self.assertEqual(self.my_class.__decordoc__,
                         " Prints entry and exit from a function ")

    def test_repr(self):
        """ Check that the __repr__() returns correctly """
        self.assertEqual(self.my_class.__repr__(),
                         "repr for TempClass2")


class TestMultipleFunctionDecorators(unittest.TestCase):
    """
    Verifies that a function can have an arbitrary number of decorators.
    """
    def test_1_decorator(self):
        try:
            @dec.Timed
            def _1_decor():
                pass
        except:
            self.fail("1 decorator caused an exception to be raised!")

    def test_2_decorator(self):
        try:
            @dec.Timed
            @dec.Traced
            def _2_decor():
                pass
        except:
            self.fail("2 decorators caused an exception to be raised!")

    @unittest.skip("Need to figure out why this is failing.")
    def test_3_decorator(self):
        try:
            @dec.Timed
            @dec.Traced
            @dec.EnterExit
            def _3_decor():
                pass
        except:
            self.fail("3 decorators caused an exception to be raised!")

    @unittest.skip("Need to figure out why this is failing.")
    def test_4_decorator(self):
        try:
            @dec.Timed
            @dec.Traced
            @dec.EnterExit
            @dec.CountCalls
            def _4_decor():
                pass
        except:
            self.fail("4 decorators caused an exception to be raised!")


class TestDecorator(unittest.TestCase):

    def test_instantiation_on_function(self):
        try:
            @dec.Decorator
            def dummy():
                pass
        except Exception:
            self.fail("An exception was raised when instantiating the class")

    def test_instantiation_on_class(self):
        try:
            @dec.Decorator
            class A(object):
                pass
        except Exception:
            self.fail("An exception was raised when instantiating the class")

    def test_instantiation_on_method(self):
        try:
            class A(object):
                @dec.Decorator
                def dummy():
                    pass
        except Exception:
            self.fail("An exception was raised when instantiating the class")

    def test_docstring(self):
        @dec.Decorator
        def dummy():
            """Function docstring"""
            pass
        self.assertEqual(dummy.__doc__, "Function docstring")

    def test_name(self):
        @dec.Decorator
        def dummy():
            """Function docstring"""
            pass
        self.assertEqual(dummy.__name__, "dummy")


class TestEnterExit(unittest.TestCase):

    def test_instantiation(self):
        try:
            @dec.EnterExit
            def dummy():
                pass
        except Exception:
            self.fail("An exception was raised when instantiating the class")

    def test_calling(self):
        @dec.EnterExit
        def dummy():
            pass
        try:
            dummy()
        except Exception:
            self.fail("An exception was raised when calling the decorated"
                      " function")


class TestDeprecated(unittest.TestCase):

    def test_instantiation(self):
        try:
            @dec.Deprecated
            def dummy():
                pass
        except Exception:
            self.fail("An exception was raised when instantiating the class")

    def test_calling(self):
        @dec.Deprecated
        def dummy():
            pass
        try:
            dummy()
        except Exception:
            self.fail("An exception was raised when calling the decorated"
                      " function")


class TestObsolete(unittest.TestCase):

    def test_instantiation(self):
        try:
            @dec.Obsolete
            def dummy():
                pass
        except utils.ObsoleteError:
            pass
        except Exception:
            self.fail("An exception was raised when instantiating the class")

    def test_calling(self):
        @dec.Obsolete
        def dummy():
            pass
        try:
            dummy()
        except utils.ObsoleteError:
            pass
        except Exception:
            self.fail("An exception was raised when calling the decorated"
                      " function")


class TestIncomplete(unittest.TestCase):

    def test_instantiation(self):
        try:
            @dec.Incomplete
            def duummy():
                pass
        except Exception:
            self.fail("An exception was raised when instantiating the class")

    def test_calling(self):
        @dec.Incomplete
        def dummy():
            pass
        try:
            dummy()
        except Exception:
            self.fail("An exception was raised when calling the decorated"
                      " function")


class TestCached(unittest.TestCase):

    def test_instantiation(self):
        try:
            @dec.Cached
            def dummy():
                pass
        except Exception:
            self.fail("An exception was raised when instantiating the class")

    def test_calling(self):
        @dec.Cached
        def dummy():
            pass
        try:
            dummy()
        except Exception:
            self.fail("An exception was raised when calling the decorated"
                      " function")

    def test_unhashable_arg(self):
        @dec.Cached
        def dummy(a):
            pass
        try:
            dummy([1, 2, 3])
        except Exception:
            self.fail("An exception was raised when calling the decorated"
                      " function")

    def test_caching(self):
        @dec.Cached
        def dummy(a):
            pass
        try:
            dummy(1)
            dummy(1)
        except Exception:
            self.fail("An exception was raised when calling the decorated"
                      " function")


class TestTimeCached(unittest.TestCase):

    def test_instantiation(self):
        try:
            @dec.TimeCached(60)
            def dummy():
                pass
        except Exception:
            self.fail("An exception was raised when instantiating the class")

    def test_calling(self):
        @dec.TimeCached(60)
        def dummy():
            pass
        try:
            dummy()
        except Exception:
            self.fail("An exception was raised when calling the decorated"
                      " function")

    def test_unhashable_arg(self):
        @dec.TimeCached(60)
        def dummy(a):
            pass
        try:
            dummy([1, 2, 3])
        except Exception:
            self.fail("An exception was raised when calling the decorated"
                      " function")

    def test_caching(self):
        @dec.TimeCached(60)
        def dummy(a):
            pass
        try:
            dummy(1)
            dummy(1)
        except Exception:
            self.fail("An exception was raised when calling the decorated"
                      " function")


class TestCountCalls(unittest.TestCase):

    def test_instantiation(self):
        try:
            @dec.CountCalls
            def dummy():
                pass
        except Exception:
            self.fail("An exception was raised when instantiating the class")

    def test_calling(self):
        @dec.CountCalls
        def dummy():
            pass
        try:
            dummy()
        except Exception:
            self.fail("An exception was raised when calling the decorated"
                      " function")

    def test_action(self):
        @dec.CountCalls
        def dummy():
            pass
        for n in range(1, 5):
            dummy()
            self.assertEqual(dummy.count(), n)

    def test_counts_static_method(self):
        # We need to force a clear of the decorated function instance cache
        # or else we'll be getting values from the other unit tests.
        try:
            dec.CountCalls._CountCalls__instances = {}
        except Exception as err:
            raise err

        @dec.CountCalls
        def dummy2():
            return 1

        @dec.CountCalls
        def other_dummy():
            return 2

        dummy2()
        other_dummy()
        dummy2()
        dummy2()
        other_dummy()

        expected = {'dummy2': 3, 'other_dummy': 2}
        self.assertEqual(dec.CountCalls.counts(), expected)


class TestTimed(unittest.TestCase):

    def test_instantiation(self):
        try:
            @dec.Timed
            def dummy():
                pass
        except Exception:
            self.fail("An exception was raised when instantiating the class")

    def test_calling(self):
        @dec.Timed
        def dummy():
            pass
        try:
            dummy()
        except Exception:
            self.fail("An exception was raised when calling the decorated"
                      " function")


class TestTraced(unittest.TestCase):

    def test_instantiation(self):
        try:
            @dec.Traced
            def dummy():
                pass
        except Exception:
            self.fail("An exception was raised when instantiating the class")

    def test_calling(self):
        @dec.Traced
        def dummy():
            pass
        try:
            dummy()
        except Exception:
            self.fail("An exception was raised when calling the decorated"
                      " function")


class TestOSRestricted(unittest.TestCase):

    def test_instantiation(self):
        try:
            @dec.OSRestricted('Windows')
            def dummy():
                pass
        except Exception:
            self.fail("An exception was raised when instantiating the class")

    @unittest.expectedFailure
    def test_instantiation_with_empty_arg_raises_type_error(self):
        with self.assertRaises(TypeError):
            @dec.OSRestricted()
            def dummy():
                pass

    def test_instantiation_with_invalid_arg_raises_value_error(self):
        with self.assertRaises(ValueError):
            @dec.OSRestricted("some invalid string")
            def dummy():
                pass

    def test_calling(self):
        valid = platform.system()
        @dec.OSRestricted(valid)
        def dummy():
            pass
        try:
            dummy()
        except Exception:
            self.fail("An exception was raised when calling the decorated"
                      " function")

    def test_invalid_os_raises_os_error(self):
        invalid = 'Windows' if platform.system() == 'Java' else 'Java'

        @dec.OSRestricted(invalid)
        def dummy():
            pass
        with self.assertRaises(OSError):
            dummy()


@unittest.skipIf(platform.system not in ['Linux', 'MaxOS'],
                 "'Timeout' decorator requires a linux-based OS.")
class TestTimeout(unittest.TestCase):

    def test_instantiation(self):
        try:
            @dec.Timeout(60)
            def dummy():
                pass
        except Exception:
            self.fail("An exception was raised when instantiating the class")

    def test_calling(self):
        @dec.Timeout(60)
        def dummy():
            pass
        try:
            dummy()
        except Exception:
            self.fail("An exception was raised when calling the decorated"
                      " function")


class TestMinPythonVersion(unittest.TestCase):

    def test_instantiation(self):
        try:
            @dec.MinPythonVersion(0x03040000)
            def dummy():
                pass
        except Exception:
            self.fail("An exception was raised when instantiating the class")

    def test_instantiation_with_empty_args_raises_type_error(self):
        with self.assertRaises(TypeError):
            @dec.MinPythonVersion()
            def dummy():
                pass

    def test_calling(self):
        @dec.MinPythonVersion(0x03040000)
        def dummy():
            pass
        try:
            dummy()
        except Exception:
            self.fail("An exception was raised when calling the decorated"
                      " function")

    def test_old_python_version_raises_runtime_error(self):
        next_vers = sys.hexversion + 0x01000000

        @dec.MinPythonVersion(next_vers)
        def dummy():
            pass
        with self.assertRaises(RuntimeError):
            dummy()


class TestSkipped(unittest.TestCase):

    def test_instantiation(self):
        try:
            @dec.Skipped
            def dummy():
                pass
        except Exception:
            self.fail("An exception was raised when instantiating the class")

    def test_instantiation_with_empty_arg(self):
        try:
            @dec.Skipped()
            def dummy():
                pass
        except Exception:
            self.fail("An exception was raised when instantiating the class")

    def test_instantiation_with_arg(self):
        try:
            @dec.Skipped(17)
            def dummy():
                pass
        except Exception:
            self.fail("An exception was raised when instantiating the class")

    def test_calling(self):
        expected = 1.234

        @dec.Skipped(expected)
        def dummy():
            return "Hello"
        self.assertEqual(dummy(), expected)

    def test_calling_with_none_return_value(self):
        @dec.Skipped(None)
        def dummy():
            return 2
        self.assertIsNone(dummy())
