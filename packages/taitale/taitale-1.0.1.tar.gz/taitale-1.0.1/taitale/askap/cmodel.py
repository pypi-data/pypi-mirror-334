from typing import Union

from taitale.utils.Parset import Parset
from taitale.utils.wrapper import parset_app


def cmodel(
    parset: Union[str, Parset, None] = None,
    **kwargs,
):
    if parset is None:
        parset = Parset(prefix="Cmodel")
    elif isinstance(parset, str):
        parset_obj = Parset(prefix="Cmodel")
        parset_obj.read_from_file(parset)
        parset = parset_obj
    elif not isinstance(parset, Parset):
        raise TypeError("parset must be either a string path or a Parset instance")

    cmodel_app = parset_app(
        name="cmodel",
        parset=parset,
        out_parset_name="taitale_cmodel.in",
        cmd="cmodel -c {parset_name}",
        mpi_compartible=True,
    )

    cmodel_app(**kwargs)


cmodel.__doc__ = """
The cmodel program is used to generate model visibilities

Parameters
----------
parset : str or Parset or None, optional
    Either a path to a parset file, a Parset instance, or None to create a new Parset.
    If None, creates a new empty Parset with prefix "Cmodel".
**kwargs : dict
    Additional keyword arguments passed to the cmodel application.

Notes
-----
For further information on usage check the ASKAPsoft documentation for `cmodel <https://yandasoft.readthedocs.io/en/latest/calim/cmodel.html>`_

Example
-------
>>> from taitale.askap import cmodel
>>> # Using a parset file
>>> cmodel(
...    parset="cmodel.in",
...     workers=2,
...     args={
...         "dataset": "./1934-638_0.ms",
...         "modelimage": "1934-638.model",
...         "nchan": "16416",
...         "singleoutputms": "true",
...         "useweightsderived": "true",
...         "visweightcutoff": "1e-4"
...     }
... )

>>> # Using a Parset instance
>>> from taitale.utils.Parset import Parset
>>> parset = Parset(prefix="Cmodel")
>>> parset.set("dataset", "./1934-638_0.ms")
>>> cmodel(parset=parset, workers=2)
"""
