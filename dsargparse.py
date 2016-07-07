#
# dsargparse.py
#
# Copyright (c) 2016 Junpei Kawamoto
#
# This software is released under the MIT License.
#
# http://opensource.org/licenses/mit-license.php
#
"""dsargparse: docstring based argparse.

dsargparse is a wrapper of argparse library which prepares helps and descriptions
from docstrings. It also sets up functions to be run for each sub command,
and provides a helper function which parses args and run a selected command.
"""
import argparse
import itertools
import inspect
import textwrap

# Load objects defined in argparse.
for name in argparse.__all__:
    if name != "ArgumentParser":
        globals()[name] = getattr(argparse, name)
__all__ = argparse.__all__


_HELP = "help"
_DESCRIPTION = "description"
_FORMAT_CLASS = "formatter_class"

_KEYWORDS_ARGS = ("Args:",)
_KEYWORDS_OTHERS = ("Returns:", "Raises:", "Yields:")
_KEYWORDS = _KEYWORDS_ARGS + _KEYWORDS_OTHERS


def _checker(keywords):
    """Generate a checker which tests a given value not starts with keywords."""
    def _(v):
        """Check a given value matches to keywords."""
        for k in keywords:
            if k in v:
                return False
        return True
    return _


def _parse_doc(doc):
    """Parse a docstring.

    Parse a docstring and extract three components; headline, description,
    and map of arguments to help texts.

    Args:
      doc: docstring.

    Returns:
      a dictionary.
    """
    lines = doc.split("\n")
    descriptions = list(itertools.takewhile(_checker(_KEYWORDS), lines))

    if len(descriptions) < 3:
        description = lines[0]
    else:
        description = "{0}\n\n{1}".format(
            lines[0], textwrap.dedent("\n".join(descriptions[2:])))

    args = list(itertools.takewhile(
        _checker(_KEYWORDS_OTHERS),
        itertools.dropwhile(_checker(_KEYWORDS_ARGS), lines)))
    argmap = {}
    if len(args) > 1:
        for pair in args[1:]:
            kv = [v.strip() for v in pair.split(":")]
            if len(kv) >= 2:
                argmap[kv[0]] = kv[1]

    return dict(headline=descriptions[0], description=description, args=argmap)


class _SubparsersWrapper(object):
    """Wrapper of the action object made by argparse.ArgumentParser.add_subparsers.

    To create an instance, the constructor takes a reference to an instance of
    the action class.
    """
    __slots__ = ("__delegate")

    def __init__(self, delegate):
        self.__delegate = delegate

    def add_parser(self, func, name=None, **kwargs):
        """Add parser.

        This method makes a new sub command parser. It takes same arguments
        as add_parser() of the action class made by
        argparse.ArgumentParser.add_subparsers.

        In addition to, it takes one positional argument `func`, which is the
        function implements process of this sub command. The `func` will be used
        to determine the name, help, and description of this sub command. The
        function `func` will also be set as a default value of `cmd` attribute.

        If you want to choose name of this sub command, use keyword argument
        `name`.

        Args:
          func: function implements the process of this command.
          name: name of this command. If not give, the function name is used.

        Returns:
          new ArgumentParser object.

        Raises:
          ValueError: if the given function does not have docstrings.
        """
        if not func.__doc__:
            raise ValueError("No docstrings given in {0}".format(func.__name__))

        info = _parse_doc(func.__doc__)
        if _HELP not in kwargs or not kwargs[_HELP]:
            kwargs[_HELP] = info["headline"]
        if _DESCRIPTION not in kwargs or not kwargs[_DESCRIPTION]:
            kwargs[_DESCRIPTION] = info["description"]
        if _FORMAT_CLASS not in kwargs or not kwargs[_FORMAT_CLASS]:
            kwargs[_FORMAT_CLASS] = argparse.RawTextHelpFormatter

        if not name:
            name = func.__name__ if hasattr(func, "__name__") else func

        res = self.__delegate.add_parser(name, argmap=info["args"], **kwargs)
        res.set_defaults(cmd=func)
        return res

    def __repr__(self):
        return self.__delegate.__repr__()


class ArgumentParser(argparse.ArgumentParser):
    """Customized ArgumentParser.

    This customized ArgumentParser will add help and description automatically
    based on docstrings of main module and functions implements processes of
    each command. It also provides `parse_and_run` method which helps parsing
    arguments and executing functions.

    This class takes same arguments as argparse.ArgumentParser to construct
    a new instance. Additionally, it has a positional argument `main`,
    which takes the main function of the script `dsargparse` library called.
    From the main function, it extracts doctstings to set command descriptions.
    """

    def __init__(self, main=None, argmap=None, *args, **kwargs):
        if main:
            if _DESCRIPTION not in kwargs or not kwargs[_DESCRIPTION]:
                kwargs[_DESCRIPTION] = inspect.getmodule(main).__doc__
            if _FORMAT_CLASS not in kwargs or not kwargs[_FORMAT_CLASS]:
                kwargs[_FORMAT_CLASS] = argparse.RawTextHelpFormatter
        self.__argmap = argmap if argmap else {}

        super(ArgumentParser, self).__init__(*args, **kwargs)

    def add_subparsers(self, **kwargs):
        """Add subparsers.

        Args:
          kwargs: same keywords arguments as
            argparse.ArgumentParser.add_subparsers.

        Returns:
          an instance of action class which is used to add sub parsers.
        """
        return _SubparsersWrapper(
            super(ArgumentParser, self).add_subparsers(**kwargs))

    def add_argument(self, *args, **kwargs):
        """Add an argument.

        This method adds a new argument to the current parser. The function is
        same as argparse.ArgumentParser.add_argument. However, this method
        tries to determine help messages for the adding argument from some
        docstrings.

        If the new arguments belong to some sub commands, the docstring
        of a function implements behavior of the sub command has `Args:` section,
        and defines same name variable, this function sets such
        definition to the help message.

        Args:
          *args: same positional arguments as argparse.ArgumentParser.add_argument.
          **kwargs: same keywards arguments as argparse.ArgumentParser.add_argument.
        """
        if _HELP not in kwargs:
            for name in args:
                name = name.replace("-", "")
                if name in self.__argmap:
                    kwargs[_HELP] = self.__argmap[name]
                    break
        return super(ArgumentParser, self).add_argument(*args, **kwargs)

    def parse_and_run(self, **kwargs):
        """Parse arguments and run the selected command.

        Args:
          kwargs: same keywords arguments as argparse.ArgumentParser.parse_args.

        Returns:
          any value the selected command returns. It could be None.
        """
        return self._dispatch(**vars(self.parse_args(**kwargs)))

    @staticmethod
    def _dispatch(cmd, **kwargs):
        """Dispatch parsed arguments to a command to be run.
        """
        return cmd(**kwargs)
