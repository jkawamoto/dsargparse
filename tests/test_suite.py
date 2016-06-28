#! /usr/bin/env python
#
# test_suite.py
#
# Copyright (c) 2016 Junpei Kawamoto
#
# This software is released under the MIT License.
#
# http://opensource.org/licenses/mit-license.php
#
""" Test suite.
"""
import sys
import unittest

from . import dargparse_test


def suite():
    """ Returns a test suite.
    """
    loader = unittest.TestLoader()
    res = unittest.TestSuite()

    res.addTest(loader.loadTestsFromModule(dargparse_test))
    return res


def main():
    """ The main function.

    Returns:
      Status code.
    """
    try:
        res = unittest.TextTestRunner(verbosity=2).run(suite())

    except KeyboardInterrupt:
        print("Test canceled.")
        return -1

    else:
        return 0 if res.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
