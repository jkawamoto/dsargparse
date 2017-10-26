dsargparse: docstring based argparse
======================================
.. raw:: html

   <div class="addthis_inline_share_toolbox"></div>

.. figure:: https://jkawamoto.github.io/dsargparse/_static/dsargparse.png
  :alt: dsargparse

  dsargparse

``dsargparse`` is a wrapper of argparse library which prepares helps and descriptions
from docstrings. It also sets up functions to be run for each sub command,
and provides a helper function which parses args and run a selected command.

Using this library, you don't need to write same texts in docstrings, help,
and description.

Install
---------
Use ``pip`` to install from `PyPi <https://pypi.python.org/pypi?:action=display&name=dsargparse>`_.

.. code-block:: sh

   $ pip install -U dsargparse

Example
--------

.. toctree::
   :maxdepth: 1

   example

Usage
------
``dsargparse`` is a simple wrapper of the original `argparse <https://docs.python.org/3/library/argparse.html>`_.
To use it, install this package and just adding *ds* to your import command
i.e. from ``import argparse`` to ``import dsargparse``.

In addition to all API ``argparse`` has, ``dsargparse`` updates three functions;

- constructor of :ref:`ArgumentParser <dsargparse-argumentparser>` object,
- :ref:`ArgumentParser.add_argument <add_argument>`,
- :ref:`add_parser` method of the action class made by `ArgumentParser.add_subparsers <https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_subparsers>`_,

and give one new method :ref:`ArgumentParser.parse_and_run <parse_and_run>`.


.. _dsargparse-argumentparser:

dsargparse.ArgumentParser
............................
In addition to the keyword arguments `argparse.ArgumentParser <https://docs.python.org/3/library/argparse.html#argumentparser-objects>`_ takes,
this constructor has keyword argument ``main`` which takes the main function.

If you give the main function, you don't need to set ``description``, and
``formatter_class`` also will be set automatically.


.. _add_argument:

add_argument
...............
This method adds a new argument to the current parser. The function is
same as `argparse.ArgumentParser.add_argument <https://docs.python.org/3/library/argparse.html#the-add-argument-method>`_. But, this method
tries to determine help messages for the adding argument from some
docstrings.

If the new arguments belong to some subcommand, the docstring
of a function implements behavior of the subcommand has ``Args:`` section,
and defines same name variable, this function sets such
definition to the help message.


.. _add_parser:

add_parser
.............
After constructing subparsers by ``subparsers = parser.add_subparsers()``,
you may call ``subparsers.add_parser`` to add a new subcommand.

The add_parser has a new positional argument ``func`` which takes a function
to be called in order to run the subcommand. The ``func`` will be used
to determine the name, help, and description of this subcommand. The
function ``func`` will also be set as a default value of ``cmd`` attribute.

The add_parser also has as same keyword arguments as ``add_parser`` of ``argparse``
library.


.. _parse_and_run:

ArgumentParser.parse_and_run
..............................
This method parses arguments and run the selected command. It returns a value
which the selected command returns. This function takes as same arguments as
`ArgumentParser.parse_args <https://docs.python.org/3/library/argparse.html#the-parse-args-method>`_.


API References
---------------

.. toctree::
   :maxdepth: 2

   modules/dsargparse


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

License
=========
This software is released under the MIT License.
