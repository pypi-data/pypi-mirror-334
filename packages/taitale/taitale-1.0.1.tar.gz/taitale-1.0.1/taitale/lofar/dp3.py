from typing import Union

from taitale.utils.Parset import Parset
from taitale.utils.wrapper import parset_app


def dp3(
    parset: Union[str, Parset, None] = None,
    **kwargs,
):
    if parset is None:
        parset = Parset()
    elif isinstance(parset, str):
        parset_obj = Parset()
        parset_obj.read_from_file(parset)
        parset = parset_obj
    elif not isinstance(parset, Parset):
        raise TypeError("parset must be either a string path or a Parset instance")

    dp3_app = parset_app(
        name="DP3",
        parset=parset,
        out_parset_name="taitale_dp3.in",
        cmd="DP3 -c {parset_name}",
        mpi_compartible=False,
    )

    dp3_app(**kwargs)


dp3.__doc__ = """
Taitale interface to DP3

Parameters
----------
parset : str or Parset or None, optional
    Either a path to a parset file, a Parset instance, or None to create a new Parset.
    If None, creates a new empty Parset.
**kwargs : dict
    Additional keyword arguments passed to the DP3 application.

Notes
-----
For further information on usage check the LOFARsoft documentation for `DP3 <https://dp3.readthedocs.io/>`_

Example
-------

>>> from taitale.lofar import dp3
>>> # Using a parset file
>>> dp3(
...     parset="dp3.in",
...     args={
...         "msin": "MWA-1052736496-averaged.ms",
...         "steps": "[average]",
...         "average.type": "averager",
...         "average.timestep": "8",
...         "msout": "MWA-1052736496-averaged-averaged.MS",
...         "msout.datacolumn": "DATA",
...     },
... )

>>> # Using a Parset instance
>>> from taitale.utils.Parset import Parset
>>> parset = Parset()
>>> parset.set("msin", "MWA-1052736496-averaged.ms")
>>> parset.set("steps", "[]")
>>> parset.set("msout", "MWA-1052736496-averaged-copy.MS")
>>> dp3(parset=parset)
"""
