#
# setup.py
#
# Copyright (c) 2016-2017 Junpei Kawamoto
#
# This software is released under the MIT License.
#
# http://opensource.org/licenses/mit-license.php
#
"""Package information of docstrings based argparse.
"""
from os import path
from setuptools import setup
import dsargparse


def read(fname):
    """Read a file.
    """
    return open(path.join(path.dirname(__file__), fname)).read()

setup(
    name="dsargparse",
    version="0.3.2",
    author="Junpei Kawamoto",
    author_email="kawamoto.junpei@gmail.com",
    description=dsargparse.__doc__,
    long_description=read("README.rst"),
    py_modules=["dsargparse"],
    test_suite="tests.suite",
    license="MIT",
    keywords="cli helper argparse",
    url="https://github.com/jkawamoto/dsargparse",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Topic :: Software Development",
        "Topic :: Utilities"
    ]
)
