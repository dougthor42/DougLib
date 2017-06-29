# -*- coding: utf-8 -*-
"""
@name:          new_program.py
@vers:          0.1.0
@author:        dthor
@created:       Mon Jul 07 16:54:02 2014
@descr:         Unit Testing for douglib.prompts module
"""
# ---------------------------------------------------------------------------
### Imports
# ---------------------------------------------------------------------------
# Standard Library
import unittest
from unittest.mock import patch

# Third-Party

# Package / Application
from .. import prompts


class TestDieSize(unittest.TestCase):

    def test_good_input(self):
        with patch('builtins.input', side_effect=['4.8', '7.3']):
            self.assertEqual((4.8, 7.3), prompts.die_size())

    def test_loops_on_invalid_input(self):

        values = [
            'dew',
            '-1.1',
            '1062.3',
            '2.7',              # 1st good value, saved as X
            'apple',
            '-163',
            '23096',
            '3.4',              # 2nd good value, saved as Y
        ]

        with patch('builtins.input', side_effect=values):
            self.assertEqual((2.7, 3.4), prompts.die_size())


class TestWaferSize(unittest.TestCase):

    def test_good_input(self):
        with patch('builtins.input', return_value='100'):
            self.assertEqual(100, prompts.wafer_size())

    def test_loops_on_invalid_input(self):
        with patch('builtins.input', side_effect=['dew', '-1.1', '650',
                                                  '150']):
            self.assertEqual(150, prompts.wafer_size())

    def test_uses_default_on_empty_input(self):
        with patch('builtins.input', return_value=''):
            self.assertEqual(150, prompts.wafer_size())

    def test_raises_on_none_input(self):
        with patch('builtins.input', return_value=None):
            with self.assertRaises(TypeError):
                prompts.wafer_size()


class TestExclusionSize(unittest.TestCase):

    def test_good_input(self):
        with patch('builtins.input', return_value='7'):
            self.assertEqual(7, prompts.exclusion_size())

    def test_loops_on_invalid_input(self):
        with patch('builtins.input', side_effect=['dew', '-1.1', '8.13']):
            self.assertEqual(8.13, prompts.exclusion_size())

    def test_uses_default_on_empty_input(self):
        with patch('builtins.input', return_value=''):
            self.assertEqual(5.0, prompts.exclusion_size())

    def test_raises_on_none_input(self):
        with patch('builtins.input', return_value=None):
            with self.assertRaises(TypeError):
                prompts.exclusion_size()


class TestFssExclusion(unittest.TestCase):

    def test_good_input(self):
        with patch('builtins.input', return_value='7'):
            self.assertEqual(7, prompts.fss_exclusion())

    def test_loops_on_invalid_input(self):
        with patch('builtins.input', side_effect=['dew', '-1.1', '8.13']):
            self.assertEqual(8.13, prompts.fss_exclusion())

    def test_uses_default_on_empty_input(self):
        with patch('builtins.input', return_value=''):
            self.assertEqual(5.0, prompts.fss_exclusion())

    def test_raises_on_none_input(self):
        with patch('builtins.input', return_value=None):
            with self.assertRaises(TypeError):
                prompts.fss_exclusion()


class TestPlot(unittest.TestCase):

    def test_true_inputs(self):
        with patch('builtins.input', side_effect=['y', 'Y', 'yes', 'YES']):
            self.assertTrue(prompts.plot())

    def test_false_inputs(self):
        with patch('builtins.input', side_effect=['', 'n', 'N', 'NO', 'no']):
            self.assertFalse(prompts.plot())

    def test_invalid_input(self):
        with patch('builtins.input', side_effect=['7', 'yuppers', '']):
            self.assertFalse(prompts.plot())


class TestYesNo(unittest.TestCase):

    def test_true_inputs(self):
        with patch('builtins.input', side_effect=['y', 'Y', 'yes', 'YES']):
            self.assertTrue(prompts.y_n("Some Prompt"))

    def test_false_inputs(self):
        with patch('builtins.input', side_effect=['', 'n', 'N', 'NO', 'no']):
            self.assertFalse(prompts.y_n("Some Prompt"))

    def test_invalid_input(self):
        with patch('builtins.input', side_effect=['7', 'yuppers', '']):
            self.assertFalse(prompts.y_n("Some Prompt"))

    def test_missing_prompt_raises_error(self):
        with self.assertRaises(TypeError):
            prompts.y_n()


class TestUsername(unittest.TestCase):

    def test_username(self):
        with patch('builtins.input', side_effect=['', 'dew']):
            actual = prompts.username()
            self.assertEqual('dew', actual)


class TestPassword(unittest.TestCase):

    def test_password(self):
        with patch('getpass.getpass', return_value='dew'):
            actual = prompts.password()
            self.assertEqual('dew', actual)


class TestDiePatternId(unittest.TestCase):

    def test_die_pattern_id(self):
        with patch('builtins.input', return_value='7'):
            actual = prompts.die_pattern_id()
            self.assertEqual(7, actual)

    def test_die_pattern_id_loops_on_non_int_input(self):
        with patch('builtins.input', side_effect=['', 'dew', '8']):
            actual = prompts.die_pattern_id()
            self.assertEqual(8, actual)


class TestWaferInfo(unittest.TestCase):

    def test_good_inputs(self):
        inputs = [
            '2.3', '3.6',       # Die Size
            '150',              # Wafer Size
            '5',                # Exclusion
            '4.5',              # Front-side Scribe Exclusion
        ]
        expected = ((2.3, 3.6), 150, 5, 4.5)
        with patch('builtins.input', side_effect=inputs):
            self.assertEqual(expected, prompts.wafer_info())
