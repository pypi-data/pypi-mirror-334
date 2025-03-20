from typing import Union

from taitale.utils.Parset import Parset
from taitale.utils.wrapper import parset_app


def ccalibrator(
    parset: Union[str, Parset, None] = None,
    **kwargs,
):
    if parset is None:
        parset = Parset(prefix="Ccalibrator")
    elif isinstance(parset, str):
        parset_obj = Parset(prefix="Ccalibrator")
        parset_obj.read_from_file(parset)
        parset = parset_obj
    elif not isinstance(parset, Parset):
        raise TypeError("parset must be either a string path or a Parset instance")

    ccalibrator_app = parset_app(
        name="ccalibrator",
        parset=parset,
        out_parset_name="taitale_ccalibrator.in",
        cmd="ccalibrator -c {parset_name}",
        mpi_compartible=True,
    )

    ccalibrator_app(**kwargs)


ccalibrator.__doc__ = """
The ccalibrator program performs calibration in a parallel/distributed environment or on a single computer system.

Parameters
----------
parset : str or Parset or None, optional
    Either a path to a parset file, a Parset instance, or None to create a new Parset.
    If None, creates a new empty Parset with prefix "Ccalibrator".
**kwargs : dict
    Additional keyword arguments passed to the ccalibrator application.

Notes
-----
For further information on usage check the ASKAPsoft documentation for `ccalibrator <https://yandasoft.readthedocs.io/en/latest/calim/ccalibrator.html>`_

Example
-------
>>> from taitale.askap import ccalibrator
>>> # Using a parset file
>>> ccalibrator(
...    parset="ccalibrator.in",
...     args = {
...         "dataset": "1934-638_0.ms",
...         "nAnt": "36",
...         "nBeam": "1",
...         "solve": "antennagains",
...         "solver": "SVD",
...         "calibaccess": "table",
...         "calibaccess.table": "1934-638.calib",
...         "calibaccess.table.maxant": "36",
...         "sources.names": "['1934-638']",
...         "sources.1934-638.direction": "[19h39m25.027, -63.42.45.61, J2000]",
...         "sources.1934-638.model": "1934-638.model"
...     }
... )

>>> # Using a Parset instance
>>> from taitale.utils.Parset import Parset
>>> parset = Parset(prefix="Ccalibrator")
>>> parset.set("dataset", "1934-638_0.ms")
>>> ccalibrator(parset=parset, workers=4)
"""
