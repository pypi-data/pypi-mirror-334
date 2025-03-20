import argparse

from taitale.utils import CliArgs
from taitale.utils.wrapper import cli_app


def msconcat_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output-file")

    parser.add_argument("positional", nargs="+")
    return parser


def msconcat(**kwargs):
    parser = msconcat_arguments()
    cli_args = CliArgs(parser=parser)
    msconcat_app = cli_app(
        name="msconcat",
        cmd="msconcat {option}",
        cli_args=cli_args,
    )

    msconcat_app(**kwargs)


msconcat.__doc__ = """
The msconcat program is used to concatenate multiple measurement sets

Parameters
----------
**kwargs : dict
    Additional keyword arguments passed to the msconcat application.

Notes
-----
For further information on usage check the ASKAPsoft documentation for `msconcat <https://yandasoft.readthedocs.io/en/latest/utils/msconcat.html>`_

Example
-------
>>> from taitale.askap import msconcat
>>> msconcat(args="-o output.ms input1.ms input2.ms input3.ms")
"""
