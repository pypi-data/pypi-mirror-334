import argparse

from taitale.utils import CliArgs
from taitale.utils.wrapper import cli_app


def msmerge_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output-file")
    parser.add_argument("-x", "--tileNcorr")
    parser.add_argument("-c", "--tileNchan")
    parser.add_argument("-r", "--tileNrow")
    parser.add_argument("-b", "--blocksize")
    parser.add_argument("-B", "--bufferMB")
    parser.add_argument("-f", "--format")
    parser.add_argument("-odirect", action="store_true")
    parser.add_argument("-d", "--dryrun", action="store_true")
    parser.add_argument("--full", action="store_true")
    parser.add_argument("-p", "--parameter-file")
    parser.add_argument("-i", "--input-file")

    parser.add_argument("positional", nargs="+")
    return parser


def msmerge(**kwargs):
    parser = msmerge_arguments()
    cli_args = CliArgs(parser=parser)
    msmerge_app = cli_app(
        name="msmerge",
        cmd="msmerge {option}",
        cli_args=cli_args,
    )

    msmerge_app(**kwargs)


msmerge.__doc__ = """
The msmerge program is used to merge multiple measurement sets.

Parameters
----------
**kwargs : dict
    Additional keyword arguments passed to the msmerge application.

Notes
-----
For further information on usage, check the ASKAPsoft documentation for `msmerge <https://yandasoft.readthedocs.io/en/latest/utils/msmerge.html>`_

Example
-------
>>> from taitale.askap import msmerge
>>> msmerge(
...     args={
...         "output_file": "merged.ms",
...         "tileNcorr": "4",
...         "tileNchan": "54",
...         "positional": ["input1.ms", "input2.ms", "input3.ms"]
...     }
... )
"""
