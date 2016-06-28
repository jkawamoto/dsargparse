""" Package information of docstrings based argparse.
"""
from setuptools import setup
import dargparse

setup(
    name="dargparse",
    version="0.1.0",
    author="Junpei Kawamoto",
    author_email="kawamoto.junpei@gmail.com",
    description=dargparse.__doc__,
    py_modules=["dargparse"],
    test_suite="tests.suite",
    license="MIT",
    keywords="cli helper argparse",
    url="https://github.com/jkawamoto/dargparse",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Topic :: Software Development",
        "Topic :: Utilities"
    ]
)
