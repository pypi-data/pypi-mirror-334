import argparse

from taitale.utils import CliArgs
from taitale.utils.wrapper import cli_app


def mslist_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--brief", action="store_true")
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--what", action="store_true")
    parser.add_argument("--how", action="store_true")
    parser.add_argument("--tables", action="store_true")
    parser.add_argument("--data", action="store_true")
    parser.add_argument("--verbose", action="store_true")

    parser.add_argument("--datacolumn")
    parser.add_argument("--field")
    parser.add_argument("--spw")
    parser.add_argument("--antennna")
    parser.add_argument("--timerange")
    parser.add_argument("--correlation")
    parser.add_argument("--scan")
    parser.add_argument("--uvrange")
    parser.add_argument("--pagerow")
    parser.add_argument("--listfile")

    parser.add_argument("positional")
    return parser


def mslist(**kwargs):
    parser = mslist_arguments()
    cli_args = CliArgs(parser=parser)
    mslist_app = cli_app(
        name="mslist",
        cmd="mslist {option}",
        cli_args=cli_args,
        pipestderr=True,
    )

    mslist_app(**kwargs)


mslist.__doc__ = """
The mslist program is used to list the contents of a measurement set.

Parameters
----------
**kwargs : dict
    Additional keyword arguments passed to the mslist application.

Notes
-----
For further information on usage, check the ASKAPsoft documentation for `mslist <https://yandasoft.readthedocs.io/en/latest/calim/mslist.html>`_

Example
-------
>>> from taitale.askap import mslist
>>> mslist(args="--brief mydata.ms")
"""
