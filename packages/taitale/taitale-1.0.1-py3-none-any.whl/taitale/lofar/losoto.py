from typing import Union

from taitale.utils.Parset import Parset
from taitale.utils.wrapper import parset_app


def losoto(
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

    # Pop h5parm from kwargs
    h5parm = kwargs.pop("h5parm", None)
    if h5parm is None:
        raise ValueError("h5parm parameter is required")

    losoto_app = parset_app(
        name="LoSoTo",
        parset=parset,
        out_parset_name="taitale_losoto.parset",
        cmd="losoto " + h5parm + " {parset_name}",
        mpi_compartible=False,
    )

    losoto_app(**kwargs)


losoto.__doc__ = """
Taitale interface to LoSoTo (LOFAR Solution Tool)

Parameters
----------
parset : str or Parset or None, optional
    Either a path to a parset file, a Parset instance, or None to create a new Parset.
    If None, creates a new empty Parset.
h5parm : str
    Path to the H5Parm file containing the solutions to process. This is a required parameter.
**kwargs : dict
    Additional keyword arguments passed to the LoSoTo application.

Notes
-----
For further information on usage check:
- LoSoTo GitHub repository: `<https://github.com/revoltek/losoto>`_
- LOFAR Imaging Cookbook: `<https://support.astron.nl/LOFARImagingCookbook/losoto.html>`_

Example
-------

>>> from taitale.lofar import losoto
>>> # Using a parset file
>>> losoto(
...     parset="losoto.parset",
...     h5parm="solutions.h5",
...     args={
...         "soltab": "sol000/amplitude000",
...         "operation": "PLOT",
...         "axisInTable": "time",
...         "axisInCol": "ant",
...         "plotFlag": "True",
...         "prefix": "amp_",
...     },
... )

>>> # Using a Parset instance
>>> from taitale.utils.Parset import Parset
>>> parset = Parset()
>>> parset.set("soltab", "sol000/amplitude000")
>>> parset.set("operation", "SMOOTH")
>>> parset.set("axisToSmooth", "time")
>>> parset.set("windowSize", "3600")
>>> losoto(parset=parset, h5parm="solutions.h5")
"""
