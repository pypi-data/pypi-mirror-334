from typing import Union

from taitale.utils.Parset import Parset
from taitale.utils.wrapper import parset_app


def ccalapply(
    parset: Union[str, Parset, None] = None,
    **kwargs,
):
    if parset is None:
        parset = Parset(prefix="Ccalapply")
    elif isinstance(parset, str):
        parset_obj = Parset(prefix="Ccalapply")
        parset_obj.read_from_file(parset)
        parset = parset_obj
    elif not isinstance(parset, Parset):
        raise TypeError("parset must be either a string path or a Parset instance")

    ccalapply_app = parset_app(
        name="ccalapply",
        parset=parset,
        out_parset_name="taitale_ccalapply.in",
        cmd="ccalapply -c {parset_name}",
        mpi_compartible=False,
    )

    ccalapply_app(**kwargs)


ccalapply.__doc__ = """
The purpose of ccalapply is to apply calibration parameters to Measurement Set

Parameters
----------
parset : str or Parset or None, optional
    Either a path to a parset file, a Parset instance, or None to create a new Parset.
    If None, creates a new empty Parset with prefix "Ccalapply".
**kwargs : dict
    Additional keyword arguments passed to the ccalapply application.

Notes
-----
For further information on usage check the ASKAPsoft documentation for `ccalapply <https://yandasoft.readthedocs.io/en/latest/calim/ccalapply.html>`_

Example
-------
>>> from taitale.askap import ccalapply
>>> # Using a parset file
>>> ccalapply(
...    parset="ccalapply.in",
...     args={
...         "dataset": "./1934-638_0.ms",
...         "calibaccess": "table",
...         "calibaccess.table": "1934-638_0.calib.bp",
...         "calibaccess.table.maxant": "36",
...         "calibrate.allowflag": "true"
...     }
... )

>>> # Using a Parset instance
>>> from taitale.utils.Parset import Parset
>>> parset = Parset(prefix="Ccalapply")
>>> parset.set("dataset", "./1934-638_0.ms")
>>> ccalapply(parset=parset)
"""
