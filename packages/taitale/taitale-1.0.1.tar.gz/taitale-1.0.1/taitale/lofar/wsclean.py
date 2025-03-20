from taitale.utils import CliArgs
from taitale.utils.wrapper import cli_app


def wsclean(**kwargs):
    cli_args = CliArgs()
    wsclean_app = cli_app(
        name="wsclean",
        cmd="wsclean {option}",
        cli_args=cli_args,
    )

    wsclean_app(**kwargs)


# TODO: Add doc strings

wsclean.__doc__ = """
Taitale interface to wsclean.

Notes
-----

For further information on usage check the WSClean documentation for `wsclean <https://wsclean.readthedocs.io/en/latest/getting_started.html>`_

Example
-------

>>> from taitale.lofar import wsclean
>>> wsclean(
...     args="wsclean -no-update-model-required -verbose -reorder \\
...         -size 4096 4096 -scale 2arcsec -pol QU -mgain 0.85 -niter 50000 \\
...         -auto-threshold 3 -join-polarizations -squared-channel-joining -log-time \\
...         -no-mf-weighting -name output input.ms"
... )
"""
