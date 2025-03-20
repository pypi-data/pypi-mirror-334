from typing import Union

from taitale.utils.Parset import Parset
from taitale.utils.wrapper import parset_app


def mssplit(
    parset: Union[str, Parset, None] = None,
    **kwargs,
):
    """
    The mssplit program is used to split measurement sets
    """
    if parset is None:
        parset = Parset()
    elif isinstance(parset, str):
        parset_obj = Parset()
        parset_obj.read_from_file(parset)
        parset = parset_obj
    elif not isinstance(parset, Parset):
        raise TypeError("parset must be either a string path or a Parset instance")

    mssplit_app = parset_app(
        name="mssplit",
        parset=parset,
        out_parset_name="taitale_mssplit.in",
        cmd="mssplit -c {parset_name}",
        mpi_compartible=False,
    )

    mssplit_app(**kwargs)


mssplit.__doc__ = """
The mssplit program is used to split measurement sets

Parameters
----------
parset : str or Parset or None, optional
    Either a path to a parset file, a Parset instance, or None to create a new Parset.
    If None, creates a new empty Parset.
**kwargs : dict
    Additional keyword arguments passed to the mssplit application.

Notes
-----
For further information on usage check the ASKAPsoft documentation for `mssplit <https://yandasoft.readthedocs.io/en/latest/calim/mssplit.html>`_

Example
-------

>>> from taitale.askap import mssplit
>>> # Using a parset file
>>> mssplit(
...     parset="mssplit.in",
...     args={
...         "vis": "input.ms",
...         "outputvis": "output.ms",
...         "beams": "[0,1,2]",
...         "channel": "1-300",
...         "width": "1",
...         "column": "DATA",
...         "timebegin": "2010/12/25/00:00:00",
...         "timeend": "2010/12/26/00:00:00",
...         "rows": "0-1000"
...     }
... )

>>> # Using a Parset instance
>>> from taitale.utils.Parset import Parset
>>> parset = Parset()
>>> parset.set("vis", "input.ms")
>>> parset.set("outputvis", "output.ms")
>>> parset.set("beams", "[0,1,2]")
>>> mssplit(parset=parset)
"""
