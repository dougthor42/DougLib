# -*- coding: utf-8 -*-
# Disable the 'Instance/Module has no ___ member' error for pylint
# pylint: disable=E1101
"""
Created on Wed Jun 17 13:18:55 2015

@author: dthor

Contains a collection of decorators that I've created.

Decorators are supposed to have to following functionality:

    The general thought is that a decorated function should act exactly like
    an undecorated function with respect to calling function properties
    such as __name__, __doc__, __dict__, etc.

    A decorated function, method, or class has additional attributes:
    __decor__       Decorator name
    __decordoc__    Decorator docstring

    Decorators should act the same way on class methods as they
    do on functions.

    1.  decorated_function.__name__ should return the function's
        name, not the decorator name.
    2.  decorated_function.__doc__ should return the function's
        docstring, not the decorator docstring
    3.  decorated_function.__decor__ should return the decorators by name
    4.  decoracted_function.__decordoc__ should return the
        decorator docstring

Decorator names should be verbs and past-tense whenever possible:
    'Timed' not 'time'
    'Cached' not 'cache'
    'CountCalls' not 'CountCall' or 'CallCounting'
    'Logged' not 'logging' or 'log'

    <decorator> on <function> should make sense:
    @CountCalls
    def my_function()
    ----- reads like: "CountCalls on my_function" -----

    <function> is <decorator> should make sense:
    @Timed
    @Cached
    def my_function
    ----- reads like: "my_function is Timed and Cached" -----

Decorators should be classes whenever possible, and inherit from the
abstract "decorator" class
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

# Package / Application
try:
    # Imports used by unit test runners
    from . import utils
#    from . import (__project_name__,
#                   __version__,
#                   __released__,
#                   )
#    logging.debug("Imports for UnitTests")
except SystemError:
    try:
        # Imports used by Spyder
        import utils
#        from __init__ import (__project_name__,
#                              __version__,
#                              __released__,
#                              )
#        logging.debug("Imports for Spyder IDE")
    except ImportError:
         # Imports used by cx_freeze
        from douglib import utils
#        from douglib import (__project_name__,
#                             __version__,
#                             __released__,
#        logging.debug("imports for Executable")


def debug(func=None, *, prefix=''):
    if func is None:
        return functools.partial(debug, prefix=prefix)

    msg = prefix + func.__qualname__
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(msg)
        return func(*args, **kwargs)
    return wrapper


# ---------------------------------------------------------------------------
### Decorators
# ---------------------------------------------------------------------------

# TODO: When chaning to Py3, see http://dabeaz.com/py3meta/Py3Meta.pdf
# Better handling of decorator objects and metaprogramming
class Decorator(object):
    """
    Abstract Base Class: Decorator
    This stores the decorator information, such as the name (__decor__) and
    the docstring (__decordoc__)
    """

    # This is needed so that Decorator is an Abstract Base Class
    __metaclass__ = abc.ABCMeta

    def __init__(self, func, *args):
        self.func = func

        if inspect.isfunction(self.func):
            self.__name__ = self.func.__name__

        elif inspect.isclass(self.func):
            self.__name__ = self.func.__class__.__name__

        elif inspect.ismethod(self.func):
            self.__name__ = self.func.__name__

        # Create the new attributes for __decor__ and __decordoc__
        self._set_decor()
        self._set_decordoc()
        self._set_doc()

    def _set_decor(self):
        """ Sets the __decor__ attribute to the decorator name """
        # functions = methods & classes = string repr. of method/class
        self.__decor__ = self.func.__decor__ = self.__str__()

    def _set_decordoc(self):
        """ Sets the __decordoc__ attribute to the decorator docscring """
        # functions = methods & classes = string repr. of method/class
        self.__decordoc__ = self.func.__decordoc__ = self.__doc__

    def _set_doc(self):
        """ Sets the __doc__ attribute to the funcion's docstring """
        self.__doc__ = self.func.__doc__

    def __get__(self, obj, objtype):
        """ Support instance methods. """
        @functools.wraps(self.func)
        def wrapper(*args, **kwargs):
            return self.func(obj, *args, **kwargs)
        setattr(obj, self.func.__name__, wrapper)
        return wrapper

    # force child classes to have a __call__ method
    @abc.abstractmethod
    def __call__(self):
        pass

    # force child classes to have a __str__ method
    @abc.abstractmethod
    def __str__(self):
        pass


class ExampleDecorator(Decorator):
    """ ExampleDecorator docstring """
    def __init__(self, func):
        # Need to first call the parent __init__ method
        Decorator.__init__(self, func)

    def __call__(self, *args, **kwargs):
        # This is where the decorator code goes.
        return self.func(*args, **kwargs)

    def __str__(self):
        return "ExampleDecorator"


class EnterExit(Decorator):
    """ Prints entry and exit from a function """
    def __init__(self, func):
        Decorator.__init__(self, func)

    def __call__(self, *args, **kwargs):
        print("Entering {}".format(self.func.__qualname__))
        retval = self.func(*args, **kwargs)
        print("Exiting {}".format(self.func.__qualname__))
        return retval

    def __str__(self):
        return "EnterExit Decorator"


class Deprecated(Decorator):
    """
    Decorator.
    Prints out a warning that a function is deprecated.
    """
    def __init__(self, func):
        Decorator.__init__(self, func)

    def __call__(self, *args, **kwargs):
        utils.cprint("Warning: deprecated function '{}' was called.".format(
            self.func.__name__), 'y')
        print()     # needed because cprint doesn't print newline char
        return self.func(*args, **kwargs)

    def __str__(self):
        return "Deprecated"


class Obsolete(Decorator):
    """
    Decorator.
    Raises an error when an Obsolete function is called.
    """
    def __init__(self, func):
        Decorator.__init__(self, func)

    def __call__(self, *args, **kwargs):
        utils.cprint("Error: obsolete function '{}' was called!\n".format(
            self.func.__name__), 'y')
        raise utils.ObsoleteError("'{}' is obsolete!".format(self.func.__name__))

    def __str__(self):
        return "Obsolete"


class Incomplete(Decorator):
    """
    **Decorator**

    Prints out a warning that a function is incomplete - either it's not
    yet finished or it needs more bug testing or there are pending feature
    requests or something else.
    """
    def __init__(self, func):
        Decorator.__init__(self, func)

    def __call__(self, *args, **kwargs):
        utils.cprint("Warning: incomplete function '{}' was called.".format(
            self.func.__name__), 'y')
        print()     # needed because cprint doesn't print newline char
        return self.func(*args, **kwargs)

    def __str__(self):
        return "Deprecated"


class Cached(Decorator):
    """
    **Decorator**

    Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).

    Taken from https://wiki.python.org/moin/PythonDecoratorLibrary
    under the name "Memoize"
    """
    def __init__(self, func):
        Decorator.__init__(self, func)
        self.cache = {}

    def __call__(self, *args):
        if not isinstance(args, collections.Hashable):
            # uncacheable. a list, for instance.
            # better to not cache than blow up.
            return self.func(*args)
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            return value

    def __str__(self):
        return "Cached"


# Alias for Cached
Memoize = Cached


@Incomplete
class TimeCached(Decorator):
    """
    **Decorator**

    Caches a function's return value each time it's called with a timeout on
    the cached return value.
    If called later with the same arguements, but within Timeout, the cached
    value is returned - the function is not reevaluated.

    If called more than Timeout seconds later, the stored return value is
    considered stale and the function is reevaluated.

    timeout defaults to 60s
    """
    def __init__(self, timeout=60):
        self.timeout = timeout
        self.cache = {}

    def __call__(self, func):
        self.func = func
        Decorator.__init__(self, func)

        @functools.wraps(self.func)
        def timecached(*args, **kwargs):
            import datetime
            now = datetime.datetime.now()
            if not isinstance(args, collections.Hashable):
                # uncacheable. a list, for instance.
                # better to not cache than blow up.
                return self.func(*args)
            try:
                # calculate the time since original caching; raises KeyError
                # if it's never been cached before.
                tdelta = now - self.cache[args][1]
            except KeyError:
                # Key not found, so we run the function
                pass
            else:
                # Key's found, but is it stale?
                if tdelta.total_seconds() <= self.timeout:
                    return self.cache[args][0]

            # the args are not cached or the data is stale, so run the func.
            value = self.func(*args)
            self.cache[args] = (value, now)
            return value
        return timecached

    def __str__(self):
        return "Cached"


class CountCalls(Decorator):
    """
    Decorator.
    Keeps track of the number of times a function is called.
    """
    __instances = {}

    def __init__(self, func):
        Decorator.__init__(self, func)
        self.__numcalls = 0
        CountCalls.__instances[self.func] = self

    def __call__(self, *args, **kwargs):
        self.__numcalls += 1
        return self.func(*args, **kwargs)

    def count(self):
        """ Return the number of times the function f was called. """
        return CountCalls.__instances[self.func].__numcalls

    @staticmethod
    def counts():
        """
        Return a dict of {function: # of calls} for all registered functions.
        """
        return dict([(func.__name__, CountCalls.__instances[func].__numcalls)
                    for func in CountCalls.__instances])

    def __str__(self):
        return "CountCalls"


class Timed(Decorator):
    """
    Decorator.
    Times a given function execution.
    """
    def __init__(self, func):
        """ Init instance attributes """
        Decorator.__init__(self, func)
        self.codetimer = utils.CodeTimer(self.func.__name__)

    def __call__(self, *args, **kwargs):
        """ Actually call the function """
        self.codetimer.start()
        result = self.func(*args, **kwargs)
        self.codetimer.stop()
        return result

    def __str__(self):
        return "Timed"


class Traced(Decorator):
    """
    Decorator.
    Prints out the called function with arguements.
    """
    def __init__(self, func):
        """ Init attributes """
        Decorator.__init__(self, func)

    def __call__(self, *args, **kwargs):
        print("Calling '{}' with args {}, {}".format(self.func.__name__,
                                                     args,
                                                     kwargs))
        return self.func(*args, **kwargs)

    def __str__(self):
        return "Traced"


class OSRestricted(Decorator):
    """
    Decorator.
    Restricts the function to only run on the listed operating systems.
    Returns an error if the OS used is not in the list.

    List of Systems: Windows, Java, Linux, MacOS

    Usage:
    @OSRestricted(*systems)
    @OSRestricted('Windows')                # Runs on Windows only
    @OSRestricted('Linux', 'MacOS')         # Runs on Linux and Mac only
    """

    _systems = {'Windows', 'Java', 'Linux', 'MacOS'}

    def __init__(self, *valid_systems):
        # Decorator.__init__ is moved inside __call__
        if set(valid_systems).issubset(self._systems):
            self.valid_systems = valid_systems
        else:
            raise ValueError("Invalid system name: {}".format(valid_systems))

    def __call__(self, func):
        self.func = func
        Decorator.__init__(self, func)
        import platform

        @functools.wraps(self.func)
        def os_checked(*args, **kwargs):
            if platform.system() in self.valid_systems:
                return self.func(*args, **kwargs)
            else:
                error_str = "Invalid operating system for function '{}'"
                raise OSError(error_str.format(self.func.__name__))
        return os_checked

    def __str__(self):
        return "OSType"


@OSRestricted('Linux')
class Timeout(Decorator):
    """
    Decorator.
    Aborts a function call if it takes longer than a defined time.

    Only works on Linux due to the SIGALRM signal number.

    Usage:
    @Timeout(seconds, [message])
    """
    def __init__(self, seconds, message='Function timed out'):
        self.seconds = seconds
        self.msg = message

    def __call__(self, func):
        Decorator.__init__(self, func)

        @functools.wraps(self.func)
        def timeout(*args, **kwargs):

            import signal
            signal.signal(signal.SIGALRM, self._handle_timeout())
            signal.alarm(self.seconds)
            try:
                return self.func(*args, **kwargs)
            finally:
#                signal.alarm(0)
                pass
        return timeout

    def __str__(self):
        return "Timeout"

    def _handle_timeout(self):
        """ Handle the timeout event somehow """
        print(self.message)


class MinPythonVersion(Decorator):
    """
    Decorator.
    Raises an error if the current python version is lower than the
    minimum python version.

    Uses the sys.hexversion for comparison.

    Usage:
    @MinPythonVersion(0x03040000)       # Min version 3.4.0
    func(a):
        return a
    """
    def __init__(self, min_version):
        self.min_version = min_version

    def __call__(self, func):
        self.func = func
        Decorator.__init__(self, func)
        import sys

        @functools.wraps(self.func)
        def version_checked(*args, **kwargs):
            error_str = "'{}' requires Python version {} or higher."
            py_vers = hexvers_to_str(self.min_version)
            if sys.hexversion < self.min_version:
                raise RuntimeError(error_str.format(self.func.__name__,
                                                    py_vers))
            else:
                return self.func(*args, **kwargs)
        return version_checked

    def __str__(self):
        return "MinPythonVersion"


class Skipped(Decorator):
    """
    Decorator.
    Skips the decorated function, optionally returning return_value.

    Usage:
    @Skipped()                  # Skips with no return value
    @Skipped(return_value)      # Skips and returns return_value
    """
    def __init__(self, return_value=None):
        self.return_value = return_value

    def __call__(self, func):
        self.func = func
        Decorator.__init__(self, func)

        @functools.wraps(self.func)
        def skipped(*args, **kwargs):
            print("Skipping '{}'".format(self.func.__name__))
            if self.return_value is None:
                pass
            else:
                return self.return_value
        return skipped

    def __str__(self):
        return "Skipped"


@debug(prefix="***")
def main():
    """Main Function.
    """
    pass

if __name__ == "__main__":
    main()
    print(main.__doc__)
