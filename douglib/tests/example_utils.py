# -*- coding: utf-8 -*-
"""
@name:          new_program.py
@vers:          0.1.0
@author:        dthor
@created:       Fri Jul 25 09:44:25 2014
@descr:         A new file

Usage:
    new_program.py

Options:
    -h --help           # Show this screen.
    --version           # Show version.
"""
# ---------------------------------------------------------------------------
### Imports
# ---------------------------------------------------------------------------
# Standard Library
import unittest

# Third-Party
import numpy as np
import scipy.stats as scipystats
from docopt import docopt

# Package / Application
try:
    # Imports used by unit test runners
    from . import utils
    from . import decorators
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


class TestClass(object):
    """
    A class with slow methods for testing the @Timed decorator.
    """
    def __init__(self, n):
        self.n = n

#    @utils.TestDecorator
    def test_method(self):
        """ test_method docstring """
        a = b = 1
        result = []
        for i in range(self.n):
            result.append(a)
            a, b = b, a + b
        return result


@decorators.TestDecorator
def test_func(a):
    """ docstring for test_func """
    return a


@decorators.Deprecated
def some_old_function(x, y):
    return x + y


class SomeClass:
    @decorators.Deprecated
    def some_old_method(self, x, y):
        return x + y


@decorators.contextmanager
def ignored(*exceptions):
    try:
        yield
    except exceptions:
        pass


@decorators.CountCalls
def hello():
    return 1


@decorators.CountCalls
def goodbye():
    return 1


@decorators.Timed
def count_example():
    """ docstring for count_example """
    print("Counting Example:")
    for i in range(5):
        hello()
        if i >= 2:
            goodbye()

    print("hello.count = {} (should be 5).".format(hello.count()))
    print("{} should be 5 and 3.".format(utils.CountCalls.counts()))
    print()


@decorators.Timed
@decorators.Cached
def fib(n):
    a = b = 1
    for i in range(n):
        yield a
        a, b = b, a + b


@decorators.Timed
@decorators.Cached
def fibslow(n):
    a = b = 1
    result = []
    for i in range(n):
        result.append(a)
        a, b = b, a + b
    return result


def deprecated_example(a=5):
    """ docstring """
    print("Deprecated notification example:")
    some_old_function(2, 2)
    someclass = SomeClass()
    someclass.some_old_method(2, 2)
    print()


def main():
    """ Main Code """
    docopt(__doc__, version=__version__)

    print()
    count_example()
    print()
    a = fibslow(50000)
    b = fibslow(50000)
    if a == b:
        print("Match")

    print()
    print("Printing the count_example.__name__:")
    print(count_example.__name__)

    temp = TestClass(25000)
    temp.test_method()
    test_func(5)
    print(deprecated_example.__name__)
    print(deprecated_example.__doc__)

#    Things I want to be true:
#    Classes:
#        temp.__str__                   returns "TestClass"
#        temp.__repr__                  returns whatever the repr def is.
#        temp.__decor__                 returns the decorators for the class
#        temp.__decordoc__              returns class's decorator docstrings
#    Class Methods:
#        temp.test_method.__name__      returns "test_method"
#        temp.test_method.__doc__       returns " test_method docstring "
#        temp.test_method.__decor__     returns "TestDecorator"
#        temp.test_method.__decordoc__  returns " TestDecorator docstring "
#    Functions:
#        test_func.__name__             returns "test_func"
#        test_func.__doc__              returns " docstring for test_func "
#        test_func.__decor__            returns "TestDecorator"
#        test_func.__decordoc__         returns " TestDecorator docstring "
#
#    Some decorators should make aspects of them public, such as the Cached
#    decorator: the user should be able to call Cached.cache and get a dict
#    of the cached values.


if __name__ == "__main__":
    main()
