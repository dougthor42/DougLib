# -*- coding: utf-8 -*-
"""
@name:          new_program.py
@vers:          0.1.0
@author:        dthor
@created:       Fri Jul 25 09:44:25 2014
@descr:         A new file
"""
# ---------------------------------------------------------------------------
### Imports
# ---------------------------------------------------------------------------
# Standard Library
import os.path
import sys
import unittest

# Third-Party

# Package / Application
try:
    # Imports used by unit test runners
    from .. import utils
    from .. import decorators
#    from . import (__project_name__,
#                   __version__,
#                   __released__,
#                   )
#    logging.debug("Imports for UnitTests")
except SystemError:
    try:
        # Imports used by Spyder
        import utils
        import decorators
#        from __init__ import (__project_name__,
#                              __version__,
#                              __released__,
#                              )
#        logging.debug("Imports for Spyder IDE")
    except ImportError:
         # Imports used by cx_freeze
        from douglib import utils
        from douglib import decorators
#        from douglib import (__project_name__,
#                             __version__,
#                             __released__,
#        logging.debug("imports for Executable")


__author__ = "Douglas Thor"
__version__ = "v0.1.0"

#    Things I want to be true:
#    Classes:
#        temp.__str__()                 = __str__() for TestClass
#        temp.__repr__                  = __repr__() for TestClass"
#        temp.__doc__                   = docsctring of TestClass
#        temp.__decor__                 = the decorators for the class
#        temp.__decordoc__              = class's decorator docstrings
#    Class Methods:
#        temp.temp_method.__name__      = "temp_method"
#        temp.temp_method.__doc__       = " temp_method docstring "
#        temp.temp_method.__decor__     = "ExampleDecorator"
#        temp.temp_method.__decordoc__  = " ExampleDecorator docstring "
#    Functions:
#        temp_func.__name__             = "temp_func"
#        temp_func.__doc__              = " docstring for temp_func "
#        temp_func.__decor__            = "ExampleDecorator"
#        temp_func.__decordoc__         = " ExampleDecorator docstring "
#
#    Some decorators should make aspects of them public, such as the Cached
#    decorator: the user should be able to call Cached.cache and get a dict
#    of the cached values.


class TempClass(object):
    """
    Decorator testing
    """
    def __init__(self, n):
        self.n = n

    @decorators.ExampleDecorator
    def temp_method(self):
        """ temp_method docstring """
        a = b = 1
        result = []
        for _ in range(self.n):
            result.append(a)
            a, b = b, a + b
        return result


@decorators.ExampleDecorator
def temp_func(a):
    """ docstring for temp_func """
    return a


@decorators.ExampleDecorator
class TestClass(object):
    """ TestClass docstring """
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
        return "str representation of TestClass"

    def __repr__(self):
        return "repr for TestClass"


class FunctionDecorator(unittest.TestCase):
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
                         "ExampleDecorator")

    def test_decordoc(self):
        """ Check that temp_func.__decordoc__ returns correctly """
        self.assertEqual(temp_func.__decordoc__,
                         " ExampleDecorator docstring ")


class MethodDecorator(unittest.TestCase):
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
                         "ExampleDecorator")

    def test_decordoc(self):
        """ Check that temp_method.__decordoc__ returns correctly """
        self.assertEqual(self.my_class.temp_method.__decordoc__,
                         " ExampleDecorator docstring ")


class ClassDecorator(unittest.TestCase):
    """
    Make sure that MyClass.__str__, .__repr__, .__decor__, .__decordoc__
    are working as expected:

        MyClass.__str__                   = "TestClass"
        MyClass.__repr__                  = whatever the repr def is.
        MyClass.__decor__                 = the decorators for the class
        MyClass.__decordoc__              = class's decorator docstrings
    """
    def setUp(self):        # pylint: disable=C0103
        self.my_class = TestClass(5)
        self.my_class.another_method()             # calls __get__

    def test_str(self):
        """ Check that my_class.__str__() returns correctly """
        self.assertEqual(self.my_class.__str__(),
                         "str representation of TestClass")

    def test_doc(self):
        """ Check that my_class.__doc__ returns correctly """
        self.assertEqual(self.my_class.__doc__,
                         " TestClass docstring ")

    def test_decor(self):
        """ Check that my_class.__decor__ returns correctly """
        self.assertEqual(self.my_class.__decor__,
                         "ExampleDecorator")

    def test_decordoc(self):
        """ Check that my_class.__decordoc__ returns correctly """
        self.assertEqual(self.my_class.__decordoc__,
                         " ExampleDecorator docstring ")

    def test_repr(self):
        """ Check that the __repr__() returns correctly """
        self.assertEqual(self.my_class.__repr__(),
                         "repr for TestClass")


class MultipleFunctionDecorators(unittest.TestCase):
    """
    Verifies that a function can have an arbitrary number of decorators.
    """
    def test_1_decorator(self):
        try:
            @decorators.Timed
            def _1_decor():
                pass
        except:
            self.fail("1 decorator caused an exception to be raised!")

    def test_2_decorator(self):
        try:
            @decorators.Timed
            @decorators.Traced
            def _2_decor():
                pass
        except:
            self.fail("2 decorators caused an exception to be raised!")

    @unittest.skip("Skipped")
    def test_3_decorator(self):
        try:
            @decorators.Timed
            @decorators.Traced
            @decorators.Deprecated
            def _3_decor():
                pass
        except:
            self.fail("3 decorators caused an exception to be raised!")

    @unittest.skip("Skipped")
    def test_4_decorator(self):
        try:
            @decorators.Timed
            @decorators.Traced
            @decorators.Deprecated
            @decorators.ExampleDecorator
            def _4_decor():
                pass
        except:
            self.fail("4 decorators caused an exception to be raised!")


class UnjoinPath(unittest.TestCase):
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


class TryAgain(unittest.TestCase):
    """
    Need to check:

    - Raise error when no args are lists, tuples, generators, or other
      non-dict iterable
    - Raise error when list items are not the same length
    - Runs func with no args when arg is None and kwargs is None
    - Runs func with 1 arg when arg is single element
    - Runs func with multiple args when arg is non-dict iterable
    - Runs func with kwarg when arg is None and kwarg is not None
    - Runs func with arg and kwargs when arg is single elem and kwarg != None
    - Runs func with args and kwargs when arg is non-dict iterable
      and kwarg is not None
    - Works with list of functions and single-elements for others
    - Works with list of args and single-elements for others
    - Works with list of kwargs and single-elements for others
    - Works with list of exceptions and single-elements for others

    """
    pass


def main():
    """
    Code to be run if module is called directly.
    Contains example usages for varoius functions.
    """
    pass


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=1)
