#! /usr/bin/env python
# pylint: disable=superfluous-parens
"""Sample command of dargparse package.

This text will be used as description of this command.
"""
import sys

import dargparse


def greeting(title, name): # pylint: disable=unused-argument
    """Print a greeting message.

    This command print "Good morning, <title> <name>.".

    Args:
      title: title of the person say greetings to.
      name: name of the person say greetings to.
    """
    print("Good morning, {title} {name}.".format(**locals()))
    return 0


def goodbye(name): # pylint: disable=unused-argument
    """Print a goodbye message.

    This command print "Goodbye, <name>.".

    Args:
      name: name of the person say goodbye to.
    """
    print("Goodbye, {name}".format(**locals()))
    return 0


## Before `dargparse`.
# import textwrap
# def main():
#     """ The main function.
#     """
#     parser = dargparse.ArgumentParser(
#       description=textwrap.dedent("""\
#         Sample command of dargparse package.
#
#         This text will be used as description of this command.
#         """))
#     subparsers = parser.add_subparsers()
#
#     greeting_cmd = subparsers.add_parser(
#         "greeting",
#         help="Print a greeting message.",
#         description=textwrap.dedent("""\
#             Print a greeting message.
#
#             This command print "Good morning, <title> <name>".
#             """))
#     greeting_cmd.add_argument(
#         "title", help="title of the person say greetings to")
#     greeting_cmd.add_argument(
#         "name", help="name of the person say greetings to.")
#     greeting_cmd.set_defaults(cmd=greeting)
#
#     goodbye_cmd = subparsers.add_parser(
#         "goodbye",
#         help="Print a goodbye message.",
#         description=textwrap.dedent("""\
#             Print a goodbye message.
#
#             This command print "Goodbye, <name>".
#             """))
#     goodbye_cmd.add_argument(
#         "name", help="name of the person say goodbye to.")
#     goodbye_cmd.set_defaults(cmd=goodbye)
#
#     args = parser.parse_args()
#     return args.cmd(**args)

# After `dargparse`.
def main():
    """ The main function.
    """
    parser = dargparse.ArgumentParser(main=main)
    subparsers = parser.add_subparsers()

    greeting_cmd = subparsers.add_parser(greeting)
    greeting_cmd.add_argument("title")
    greeting_cmd.add_argument("name")

    goodbye_cmd = subparsers.add_parser(goodbye)
    goodbye_cmd.add_argument("name")

    return parser.parse_and_run()


if __name__ == "__main__":
    sys.exit(main())
