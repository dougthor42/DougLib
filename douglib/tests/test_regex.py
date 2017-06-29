# -*- coding: utf-8 -*-
"""
Unit tests for :py:mod:`douglib.regex`.
"""
# ---------------------------------------------------------------------------
### Imports
# ---------------------------------------------------------------------------
# Standard Library
import unittest

# Third-Party

# Package / Application
from .. import regex


class TestRe1(unittest.TestCase):

    known_values = (
        ("""
         class MyClass(object):
             pass
         """,
         "(object)"),
        ("""
         def some_function(a, b, c):
             pass
         """,
         "(a, b, c)"),
    )

    def test_known_values(self):
        for text, expected in self.known_values:
            with self.subTest(text=text, expected=expected):
                expr = regex.re1
                self.assertRegex(text, expr)
                result = expr.search(text).group('classdef')
                self.assertEqual(result, expected)


class TestRe2(unittest.TestCase):

    known_values = (
        ("""
         class MyClass(object):
             pass
         """,
         "object"),
        ("""
         def some_function(a, b, c):
             pass
         """,
         "a, b, c"),
    )

    def test_known_values(self):
        for text, expected in self.known_values:
            with self.subTest(text=text, expected=expected):
                expr = regex.re2
                self.assertRegex(text, expr)
                result = expr.search(text).group('classdef')
                self.assertEqual(result, expected)
