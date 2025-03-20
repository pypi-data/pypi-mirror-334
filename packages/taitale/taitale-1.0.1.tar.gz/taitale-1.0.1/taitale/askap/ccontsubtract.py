from typing import Union

from taitale.utils.Parset import Parset
from taitale.utils.wrapper import parset_app


def ccontsubtract(
    parset: Union[str, Parset, None] = None,
    **kwargs,
):
    if parset is None:
        parset = Parset(prefix="CContSubtract")
    elif isinstance(parset, str):
        parset_obj = Parset(prefix="CContSubtract")
        parset_obj.read_from_file(parset)
        parset = parset_obj
    elif not isinstance(parset, Parset):
        raise TypeError("parset must be either a string path or a Parset instance")

    ccontsubtract_app = parset_app(
        name="ccontsubtract",
        parset=parset,
        out_parset_name="taitale_ccontsubtract.in",
        cmd="ccontsubtract -c {parset_name}",
        mpi_compartible=True,
    )

    ccontsubtract_app(**kwargs)


ccontsubtract.__doc__ = """
The purpose of ccontsubtract is to subtract continuum from a Measurement Set

Parameters
----------
parset : str or Parset or None, optional
    Either a path to a parset file, a Parset instance, or None to create a new Parset.
    If None, creates a new empty Parset with prefix "CContSubtract".
**kwargs : dict
    Additional keyword arguments passed to the ccontsubtract application.

Notes
-----
For further information on usage check the ASKAPsoft documentation for `ccontsubtract <https://yandasoft.readthedocs.io/en/latest/calim/ccontsubtract.html>`_

Example
-------
>>> from taitale.askap import ccontsubtract
>>> # Using a parset file
>>> ccontsubtract(
...    parset="ccontsubtract.in",
...     workers=2,
...     args={
...         "dataset": "./1934-638_0.ms",
...         "datacolumn": "DATA",
...         "outputcolumn": "CORRECTED_DATA",
...         "modelcolumn": "MODEL_DATA",
...         "nterms": "2",
...         "nchannel": "16416",
...         "spw": "0:0~16415",
...         "targetspec": "0:0~16415",
...         "freqframe": "topo",
...         "reffreq": "1.42GHz"
...     }
... )

>>> # Using a Parset instance
>>> from taitale.utils.Parset import Parset
>>> parset = Parset(prefix="CContSubtract")
>>> parset.set("dataset", "./1934-638_0.ms")
>>> ccontsubtract(parset=parset, workers=2)
"""
