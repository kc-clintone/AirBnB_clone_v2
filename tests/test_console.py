#!/usr/bin/python3
"""
Tests for the console class
"""

import console
import inspect
import pep8
import unittest
HBNBCommand = console.HBNBCommand


class TestConsoleDocs(unittest.TestCase):
    """
    This class is for testing documentation of
    the console
    """
    def test_that_pep8_conforms_the_console(self):
        """ Test if the console.py conforms to PEP8."""
        p8 = pep8.StyleGuide(quiet=True)
        res = p8.check_files(['console.py'])
        self.assertEqual(res.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_that_pep8_conforms_test_console(self):
        """
        Test if the tests/test_console.py conforms to PEP8
        """
        p8 = pep8.StyleGuide(quiet=True)
        res = p8.check_files(['tests/test_console.py'])
        self.assertEqual(res.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_the_console_module_docstring(self):
        """
        Testing for the console.py module docstring
        """
        self.assertIsNot(console.__doc__, None,
                         "console.py needs a docstring")
        self.assertTrue(len(console.__doc__) >= 1,
                        "console.py needs a docstring")

    def test_the_HBNBCommand_class_docstring(self):
        """
        Test for the HBNBCommand class docstring
        """
        self.assertIsNot(HBNBCommand.__doc__, None,
                         "HBNBCommand class needs a docstring")
        self.assertTrue(len(HBNBCommand.__doc__) >= 1,
                        "HBNBCommand class needs a docstring")
