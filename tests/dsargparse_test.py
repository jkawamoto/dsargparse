#! /usr/bin/env python
# pylint: disable=protected-access
#
# dsargparse_test.py
#
# Copyright (c) 2016 Junpei Kawamoto
#
# This software is released under the MIT License.
#
# http://opensource.org/licenses/mit-license.php
#
""" Unit tests for dsargparse module.
"""
import textwrap
import unittest

import dsargparse


class TestParser(unittest.TestCase):
    """Unit tests for _parse_doc function.
    """

    def test_full_document(self):
        """Test for a full information docstring.
        """
        ans = dsargparse._parse_doc(dsargparse._parse_doc.__doc__)

        self.assertEqual(ans["headline"], "Parse a docstring.")
        self.assertEqual(ans["description"], textwrap.dedent("""\
            Parse a docstring.

            Parse a docstring and extract three components; headline, description,
            and map of arguments to help texts.
            """))
        self.assertIn("doc", ans["args"])
        self.assertEqual(ans["args"]["doc"], "docstring.")

    def test_minimum_document(self):
        """Test for a minimum docstring.
        """
        ans = dsargparse._parse_doc(dsargparse._checker.__doc__)
        self.assertEqual(
            ans["headline"],
            "Generate a checker which tests a given value not starts with keywords.")
        self.assertEqual(
            ans["description"],
            "Generate a checker which tests a given value not starts with keywords.")
        self.assertEqual(len(ans["args"]), 0)

    def test_docstring_without_description(self):
        """ Test for a docstring which doesn't have descriptions.
        """
        ans = dsargparse._parse_doc("""Test docstring.

        Args:
          one: definition of one.
          two: definition of two.

        Returns:
          some value.
        """)
        self.assertEqual(ans["headline"], "Test docstring.")
        self.assertEqual(
            ans["description"],
            textwrap.dedent("""\
            Test docstring."""))
        self.assertIn("one", ans["args"])
        self.assertEqual(ans["args"]["one"], "definition of one.")
        self.assertIn("two", ans["args"])
        self.assertEqual(ans["args"]["two"], "definition of two.")

    def test_docstring_without_args(self):
        """ Test for a docstring which doesn't have args.
        """
        ans = dsargparse._parse_doc("""Test docstring.

        This function do something.

        Returns:
          some value.
        """)
        self.assertEqual(ans["headline"], "Test docstring.")
        self.assertEqual(
            ans["description"],
            textwrap.dedent("""\
            Test docstring.

            This function do something.
            """))
        self.assertEqual(len(ans["args"]), 0)


if __name__ == "__main__":
    unittest.main()
