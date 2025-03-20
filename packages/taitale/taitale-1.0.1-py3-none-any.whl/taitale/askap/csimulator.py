from typing import Union

from taitale.utils.Parset import Parset
from taitale.utils.wrapper import parset_app


def csimulator(
    parset: Union[str, Parset, None] = None,
    **kwargs,
):
    if parset is None:
        parset = Parset(prefix="Csimulator")
    elif isinstance(parset, str):
        parset_obj = Parset(prefix="Csimulator")
        parset_obj.read_from_file(parset)
        parset = parset_obj
    elif not isinstance(parset, Parset):
        raise TypeError("parset must be either a string path or a Parset instance")

    csimulator_app = parset_app(
        name="csimulator",
        parset=parset,
        out_parset_name="taitale_csimulator.in",
        cmd="csimulator -c {parset_name}",
        mpi_compartible=False,
    )

    csimulator_app(**kwargs)


csimulator.__doc__ = """
The csimulator program is used to generate a measurement set from a model sky.

Parameters
----------
parset : str or Parset or None, optional
    Either a path to a parset file, a Parset instance, or None to create a new Parset.
    If None, creates a new empty Parset with prefix "Csimulator".
out_parset_name : str, optional
    The name of the output parset file. Defaults to "taitale_csimulator.in".
**kwargs : dict
    Additional keyword arguments passed to the csimulator application.

Notes
-----
For further information on usage check the ASKAPsoft documentation for `csimulator <https://yandasoft.readthedocs.io/en/latest/calim/csimulator.html>`_

Example
-------
>>> from taitale.askap import csimulator
>>> # Using a parset file
>>> csimulator(
...    parset="csimulator.in",
...     workers=4,
...     args = {
...         "dataset": "test.ms",
...         "antennas": "./parsets/ASKAP36.antpos.in",
...         "feeds": "./parsets/ASKAP1feeds.in",
...         "duration": {
...             "from": "-2h",
...             "to": "2h"
...         },
...         "spw": '[48, 1.420GHz, 1MHz, "XX YY XY YX"]'
...     }
... )

>>> # Using a Parset instance
>>> from taitale.utils.Parset import Parset
>>> parset = Parset(prefix="Csimulator")
>>> parset.set("dataset", "test.ms")
>>> csimulator(parset=parset, workers=4)
"""
