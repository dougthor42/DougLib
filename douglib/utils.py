# -*- coding: utf-8 -*-
# Disable the 'Instance/Module has no ___ member' error for pylint
# pylint: disable=E1101
"""
douglib.utils
=============

Created on Thu 2014-07-10 at 09:51:32 PDT

Contains non-math-related utilities used by douglib such as
decorators, colored terminal printing, code timing and
progress bars.
"""
# ---------------------------------------------------------------------------
### Imports
# ---------------------------------------------------------------------------
# Standard Library
import time
import datetime
import os.path

# Third-Party
import colorama

# Package / Application

# ---------------------------------------------------------------------------
### Custom Exceptions
# ---------------------------------------------------------------------------
class DougLibError(Exception):
    """ Generic Exception Class for douglib """
    pass


class RangeError(ValueError):
    """ A custom exception for reporting out-of-range errors """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class ObsoleteError(RuntimeError):
    """ Custom error for reporting obsolete functions """
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return repr(self.value)


class NewError(DougLibError):
    """ Temporary new error for testing """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


# ---------------------------------------------------------------------------
### Classes
# ---------------------------------------------------------------------------
class CodeTimer(object):
    """
    A Simple code execution timer.

    My attempt at making a simple code timer. The idea is that a user can
    just call this simple thing, once to start and once again to stop. Upon
    stopping, it prints out the time delta.

    Stop times are printed in Red, while lap times are printed in Cyan. Time
    differences, as provided by the ``delta()`` method, are printed in Yellow.

    Parameters
    ----------
    label : string
        An optional label for the timer. Will be displayed upon stopping or
        lapping the timer.

    Attributes
    ----------
    label : string
        The label for the timer instance.
    running : bool
        Returns ``True`` if the timer is currently running.
    start_t : datetime.datetime object
        The time, in seconds, that the timer was last started, as reported
        by the built-in time.clock() function. Returns ``None`` if the
        timer has never been started.
    stop_t : datetime.datetime object
        The time, in seconds, that the timer was last stopped, as reported
        by the built-in time.clock() function. Returns ``None`` if the
        timer has never been stopped.
    diff : float
        The time between the the last lap or stop event and the start event.
        Returns ``None`` if the timer has never been lapped or stopped.
    prev_t : datetime.datetime object
        The timestamp of the previous lap, start, or delta event. Returns
        ``None`` if the timer has never been started.

    Methods
    -------
    start(self)
        Start the timer.
    stop(self, override_label=None)
        Stops the timer and prints out the elapsed time, optionally
        overriding the label temporarily. Returns the elapsed time as a
        datetime.timedelta object.
    reset(self)
        Resets the timer and clears the last start_t, stop_t, and diff values.
    lap(self, override_label=None)
        Prints out the current elapsed time, optionally overrideing the
        label temporarily. Returns the elapsed time as a
        datetime.timedelta object.
    delta(self, override_label=None)
        Prints out the time delta between this call and the previous call
        of ``delta``, ``lap``, or ``start``. Returns the value as a
        datetime.timedelta object.

    Examples
    --------
    Basic Usage:

    >>> ct = CodeTimer("my_label")
    >>> ct.start()
    >>> # code to time
    >>> ct.stop()           # doctest: +SKIP
    my_label: 13.2725267063 seconds.

    Printing out lap times:

    >>> ct = CodeTimer()
    >>> ct.start()
    >>> for _i in range(3):
    ...     ct.lap()        # doctest: +SKIP
    Current Exec: 6.99158129829 seconds.
    Current Exec: 6.9916975028 seconds.
    Current Exec: 6.99176305405 seconds.
    >>> ct.stop()           # doctest: +SKIP
    Exec time: 18.8153060201 seconds.
    """
    def __init__(self, label=None):
        """ __init__(self, label: string = None) -> CodeTimer """
        # Initialize class attributes
        self.label = label
        self.temp_label = None
        self.running = False
        self.start_t = None
        self.stop_t = None
        self.diff = None
        self.prev_t = None

    def __str__(self):
        return "Timer: {}".format(self.label)

    def start(self):
        """ Start the timer """
        self.start_t = datetime.datetime.utcnow()
        self.prev_t = self.start_t
        self.running = True

    def stop(self, override_label=None):
        """ Stop the timer and return and print the delta with label. """
        if override_label is None:
            # Use the class label for the timer
            self.temp_label = self.label
        else:
            # Use the temporary override label for the timer
            self.temp_label = override_label
        if not self.running:
            raise RuntimeError("Timer not started.")

        self.running = False
        self.stop_t = datetime.datetime.utcnow()
        self.diff = self.stop_t - self.start_t
        if self.temp_label is None:
            print_red("Exec time: {diff}".format(diff=self.diff))
#            print()
        else:
            print_red("{lbl}: {diff}".format(lbl=self.temp_label,
                                             diff=self.diff))
#            print()
        return self.diff

    def reset(self):
        """ Reset the timer. """
        self.start_t = None
        self.stop_t = None
        self.diff = None
        self.prev_t = None
        self.start()

    def lap(self, override_label=None):
        """ Returns and prints out the current timer value. """
        if override_label is None:
            # Use the class label for the timer
            self.temp_label = self.label
        else:
            # Use the temporary override label for the timer
            self.temp_label = override_label
        if not self.running:
            raise RuntimeError("Timer not started.")

        self.running = True
        self.stop_t = datetime.datetime.utcnow()
        self.prev_t = self.stop_t
        self.diff = self.stop_t - self.start_t
        if self.temp_label is None:
            cprint("Current Exec: {diff}".format(diff=self.diff),
                   'c')
#            print()
        else:
            cprint("{lbl}: {diff}".format(lbl=self.temp_label,
                                          diff=self.diff),
                   'c')
#            print()
        return self.diff

    def delta(self, override_label=None):
        """
        Prints out the time delta between this call and the previous
        call of ``delta``, ``lap`` or ``start``. Returns the value
        as a datetime.timedelta object.
        """
        if override_label is None:
            # Use the class label for the timer
            self.temp_label = self.label
        else:
            # Use the temporary override label for the timer
            self.temp_label = override_label
        if not self.running:
            raise RuntimeError("Timer not started.")

        self.running - True
        self.stop_t = datetime.datetime.utcnow()
        self.diff = self.stop_t - self.prev_t
        self.prev_t = self.stop_t
        if self.temp_label is None:
            cprint("Delta: {diff}".format(diff=self.diff),
                   'y')
            print()
        else:
            cprint("{lbl}: {diff}".format(lbl=self.temp_label,
                                          diff=self.diff),
                   'y')
            print()
        return self.diff


class Borg(object):
    """
    Inheritable class.

    Having a class that inherits from Borg will allow the class to be
    instances an arbitrary number of times, with each instance always
    having the same data.

    Any change to a single instance will also change the data in other
    instances.

    Examples
    --------
    >>> a = Borg()
    >>> b = Borg()
    >>> repr(a)             # doctest: +ELLIPSIS
    '<utils.Borg object at 0x...>'
    >>> repr(b)             # doctest: +ELLIPSIS
    '<utils.Borg object at 0x...>'
    >>> a.value = 5
    >>> a.value
    5
    >>> b.value
    5

    **Resistance is futile.**
    """

    _state = {}

    def __new__(cls, *args, **kwargs):
        self = object.__new__(cls)
        self.__dict__ = cls._state
        return self


class Singleton(object):
    """
    Inheritable class.

    Having a class that inherits from Singleton will allow the class to be
    instanced only once. Any subsequent instancing will actually return
    the originally instanced memory location.

    This is slighly different from Borg in that only a single memory location
    (identity) will be used. With Borg, multiple identities are allowed, but
    each identity has the same state.

    Examples
    --------
    >>> a = Singleton()
    >>> b = Singleton()
    >>> repr(a)             # doctest: +ELLIPSIS
    '<utils.Singleton object at 0x...>'
    >>> repr(b)             # doctest: +ELLIPSIS
    '<utils.Singleton object at 0x...>'
    >>> repr(a) == repr(b)
    True

    *Note how the memory location is the same.*
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


# ---------------------------------------------------------------------------
### Functions
# ---------------------------------------------------------------------------
def hexvers_to_str(hexvers=None):
    """
    Converts a sys.hexversion output to a standard version string.

    The sys.hexversion output is of the form 0x030401a5
    03 is the major
    04 is the minor
    01 is the fix
    a is the release level
    5 is the release serial

    If hexvers is not defined, then it imports sys.hexversion and runs that.

    Parameters
    ----------
    hexvers : int, optional
        The integer representation of a hex-encoded version number. Defaults
        to None, which pulls the current python version.

    Returns
    -------
    The version number representated as a string

    Examples
    --------
    >>> hexvers_to_str()            # doctest: +SKIP
    a
    >>> hexvers_to_str(34014960)
    '2.7.6.f0'
    """
    if hexvers is None:
        from sys import hexversion
        hexvers = hexversion
    hexstr = '{0:08x}'.format(hexvers)
    major = int(hexstr[:2])
    minor = int(hexstr[3:4])
    fix = int(hexstr[5:6])
    release = hexstr[6:]
    return "{}.{}.{}.{}".format(major, minor, fix, release)


def print_red(text):
    """ Prints text as bright red """
    cprint(text, 'red')


def cprint(text, color, end='\n'):
    """ Prints text as the specified color. Accepts RGB, CMYK, and White. """
    colors = {'r': colorama.Fore.RED,
              'red': colorama.Fore.RED,
              'g': colorama.Fore.GREEN,
              'green': colorama.Fore.GREEN,
              'b': colorama.Fore.BLUE,
              'blue': colorama.Fore.BLUE,
              'c': colorama.Fore.CYAN,
              'cyan': colorama.Fore.CYAN,
              'y': colorama.Fore.YELLOW,
              'yellow': colorama.Fore.YELLOW,
              'm': colorama.Fore.MAGENTA,
              'magenta': colorama.Fore.MAGENTA,
              'k': colorama.Fore.BLACK,
              'black': colorama.Fore.BLACK,
              'w': colorama.Fore.WHITE,
              'white': colorama.Fore.WHITE}
    colorama.init(strip=False)      # for Spyder: don't strip format chars
    print(colors[color.lower()] + colorama.Style.BRIGHT + text, end=end)
    print(colorama.Style.RESET_ALL, end='')
    colorama.deinit()


def progress_bar(count, size, bar_size=10):
    """
    A simple terminal progress bar.

    Insert into the loop that you want to monitor progrss on and once after
    the loop is completed (with count = size)

    Parameters
    ----------
    count : int
        ieration that you want to display.
    size : int
        maximum number of iterations that the loop will go through
    barLen : int
        Length of the progress bar.

    Notes
    -----
    1.  If count = length, then the bar display will be persistant
    2.  I'd like for it to only update if percent_complete changes, but
        I'm not quite sure how to do that yet.
    3.  Does not like to work properly in Spyder. This is because the Spyder
        terminal doesn't recognize the ``\\r`` special character.

    Example
    -------

    ::

        size = 1000
        n = 0
        bar_size = 17
        for item in range(size):
            time.sleep(0.02)
            progress_bar(n, size, bar_size)
            n += 1
        progress_bar(n, size, bar_size)
    """
#    fill = int(math.floor(count * bar_size / float(size)))
    fill = count * bar_size // size
    percent_complete = max(0, min(fill, bar_size))
    hash_fill = "#" * percent_complete
    space_fill = " " * (bar_size - percent_complete)
    bar_str = "[{fill}{spaces}] {n}/{size}"
    if count == size:
        end = "\n"
    else:
        end = "\r"
    print(bar_str.format(fill=hash_fill,
                         spaces=space_fill,
                         n=count,
                         size=size),
          end=end,
          )


def unjoin_path(path):
    """
    Returns a list of all folders that make up PATH. This is
    the inverse of os.path.join().

    ``os.path.join(*unjoin_path(path)) == path``

    *Note the "splat" (list unpacking) operator (asterisk)*

    Examples
    --------
    >>> path = "C:\path1\path2\hello.txt"
    >>> my_split_path = unjoin_path(path)
    >>> my_split_path
    ['C:\\\\', 'path1', 'path2', 'hello.txt']
    >>> path == os.path.join(*my_split_path)
    True
    """
    rest, tail = os.path.split(path)
    if tail == '':
        return [rest]
    return unjoin_path(rest) + [tail]


def print_section(text, style=3):
    """
    Prints out a line in varoius section header styles. Automatically
    prepends newline char(s) to text for sections and major sections

    Notes
    -----
    0:
        subsubsection, denoted by ``--- subsubsection ---`` in magenta.
    1:
        subsection, denoted by ``----- subsection -----`` in cyan.
    2:
        section, denoted by ``---------- section ----------`` in yellow
    3:
        major section, denoted by ``========== MAJOR SECTION ==========`` in
        green. Text is forced to uppercase.

    """
    if style == 0:
        color = 'm'
        prepend = "--- "
        append = " ---"
    elif style == 1:
        color = 'c'
        prepend = "----- "
        append = " -----"
    elif style == 2:
        color = 'y'
        prepend = "\n---------- "
        append = " ----------"
    elif style == 3:
        text = text.upper()
        color = 'g'
        prepend = "\n\n========== "
        append = " =========="
    else:
        raise ValueError("Invalid style code.")

    output = "{}{}{}".format(prepend, text, append)
    cprint(output, color)


def print_input(text):
    """
    Prints text formatted as a python input by putting ">>> " in front
    and making sure that a newline is at the end. Also colors red.
    """
    prepend = ">>> "
#    if type(text) is not str:
#        raise TypeError("Input must be a string.")
    if text[-1] != "\n":
        text = "{}\n".format(text)

    cprint("{}{}".format(prepend, text), 'r', end='')


def print_and_exec(code):
    """
    Prints out a formatted code line and executes it.
    WARNING: UNSAFE
    """
    print_input(code)
    print(eval(code))


# TODO: Possibly rename...
def try_again(funcs, args, kwargs, errors, raise_error=None):
    """
    Trys multiple functions, arguements, or exceptions until one succeeds.
    Returns the value of the succeeding function.

    Parameters
    ----------
    funcs : list of functions
        List of functions to try, in order.

    args : list of arguments
        List of arguments for each function.

    kwargs : list of dicts
        Dictionary of keyword arguments for each function.

    errors : list of exceptions
        List of errors to catch in the Except clause. If a list of tuples,
        then the tuple of errors will be caught for a given iteration.

    raise_error : exception, optional
        The exception to raise if no attempt passes. If None, then raises
        the most recent exception as RuntimeError

    Returns
    -------
    retval
        The result of whichever function succeeded.

    Notes
    -----
    `funcs`, `args`, `kwargs`, and `errors` must all have the same length.

    Examples
    --------
    >>> def my_func(a):
    ...     if a == 3:
    ...         return a
    ...     else:
    ...         raise ValueError
    >>> errors = [ValueError, ValueError, ValueError]
    >>> funcs = [my_func] * 3
    >>> args = [1, 2, 3]
    >>> kwargs = [None] * 3
    >>> try_again(funcs, args, kwargs, errors, OSError("something"))
    3
    """
    # Check that all inputs are lists.
    for item in (funcs, args, kwargs, errors):
        if not isinstance(item, list):
            raise TypeError("All args must be lists")

    # and that all of the lists are the same length.
    length = len(funcs)
    if not all(len(x) == length for x in (funcs, args, kwargs, errors)):
        raise ValueError("All iterables must be the same length.")

    # Execute each item in turn
    # TODO: there's gotta be a better way to do this...
    #       Why doesn't func(*arg, **kwarg) work?
    final_error = None
    for func, arg, kwarg, error in zip(funcs, args, kwargs, errors):
        try:
            if arg is None and kwarg is None:
                retval = func()
            elif arg is None and kwarg is not None:
                retval = func(**kwarg)
            elif not hasattr(arg, '__iter__') and kwarg is None:
                retval = func(arg)
            elif not hasattr(arg, '__iter__') and kwarg is not None:
                retval = func(arg, **kwarg)
            elif hasattr(arg, '__iter__') and kwarg is None:
                retval = func(*arg)
            elif hasattr(arg, '__iter__') and kwarg is not None:
                retval = func(*arg, **kwarg)
            else:
                raise SyntaxError("Unknown run case")
            break
        except error as err:
            final_error = err
            continue
    else:
        if raise_error is None:
            err_text = "No attemps succeeded. Error = `{}`"
            raise RuntimeError(err_text.format(repr(final_error)))
        else:
            raise raise_error

    return retval


# ---------------------------------------------------------------------------
### main() and examples
# ---------------------------------------------------------------------------
def main():
    """ Contains examples of some functions """
    section_level = 0

    # CodeTimer
    print_section("CodeTimer", section_level)
    codetimer = CodeTimer("Main Label")
    codetimer.start()
    import random

    for _x in range(5):
        time.sleep(random.random())
        if _x >= 3:
            codetimer.lap()
        else:
            codetimer.lap("Lap {}".format(_x))
    print("<Ending Label>  ", end='')
    codetimer.stop()


    # Borg
    print_section("Borg", section_level)
    class testBorg(Borg):
        def __init__(self):
            self.a = 5

    borg1 = testBorg()
    borg2 = testBorg()
    print("Two instances of Borg share the same data value but are different")
    print("memory locations:")
    print("id(borg1): {}".format(id(borg1)), end='\t\t')
    print("id(borg2): {}".format(id(borg2)))
    print("borg1.a is: {}".format(borg1.a), end='\t\t')
    print("borg2.a is now: {}".format(borg2.a))
    print("Setting borg1.a to 15")
    borg1.a = 15
    print("borg1.a is now: {}".format(borg1.a), end='\t\t')
    print("borg2.a is now: {}".format(borg2.a))

    # Singleton
    print_section("Singleton", section_level)
    class testSingleton(Singleton):
        def __init__(self):
            self.a = 1

    singleton1 = testSingleton()
    singleton2 = testSingleton()
    print("Only one instance of a singleton is ever created:")
    print("id(singleton1): {}".format(id(singleton1)), end='\t')
    print("id(singleton2): {}".format(id(singleton2)))
    print("singleton1.a is {}".format(singleton1.a), end='\t\t')
    print("singleton2.a is {}".format(singleton2.a))
    print("Setting singleton1.a to 15")
    singleton1.a = 15
    print("singleton1.a is {}".format(singleton1.a), end='\t\t')
    print("singleton2.a is {}".format(singleton2.a))


    # hexvers_to_str
    print_section("hexvers_to_str", section_level)
    print(hexvers_to_str(0x03040000))

    # print_red
    print_section("print_red", section_level)
    print_red("Red Text")

    # cprint
    print_section("cprint", section_level)
    cprint("cprint Cyan", 'c')
    cprint("cprint Blue", 'b')

    # unjoin_path
    print_section("unjoin_path", section_level)
    path = "C:\\Temp\\my_file.txt"
    print("Spliting a Path: `{}`".format(path))
    unjoined = unjoin_path(path)
    print(unjoined)
    joined = os.path.join(*unjoined)
    print("and rejoining it: `{}`".format(joined))

    # print_section
    print_section("print_section", section_level)
    print_section("major section, lvl 3", 3)
    print_section("section, lvl 2", 2)
    print_section("sub section, lvl 1", 1)
    print_section("sub sub section, lvl 0", 0)

    # print_input
    print_section("print_input", section_level)
    print_input("range(5)")

    # print_and_exec
    print_section("print_and_exec", section_level)
    print_and_exec("range(5)")

    # try_again
    def make_trouble(a=0):
        print("a = `{}`   {}".format(a, datetime.datetime.now()))
        if a > 10:
            return a
        else:
            raise ValueError("oh no!")


    errors = [ValueError] * 5
    args = [1, 2, 9, 11, 12]
    funcs = [make_trouble] * 5
    a = try_again(funcs, args, [None] * 5, errors)
    print(a)
