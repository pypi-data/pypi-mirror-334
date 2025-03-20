from typing import Union

from taitale.utils.Parset import Parset
from taitale.utils.wrapper import parset_app


def linmos(
    parset: Union[str, Parset, None] = None,
    **kwargs,
):
    if parset is None:
        parset = Parset(prefix="linmos")
    elif isinstance(parset, str):
        parset_obj = Parset(prefix="linmos")
        parset_obj.read_from_file(parset)
        parset = parset_obj
    elif not isinstance(parset, Parset):
        raise TypeError("parset must be either a string path or a Parset instance")

    linmos_app = parset_app(
        name="linmos",
        parset=parset,
        out_parset_name="taitale_linmos.in",
        cmd="linmos -c {parset_name}",
        mpi_compartible=False,
    )

    linmos_app(**kwargs)


linmos.__doc__ = """
The linmos program is used to mosaic images together

Parameters
----------
parset : str or Parset or None, optional
    Either a path to a parset file, a Parset instance, or None to create a new Parset.
    If None, creates a new empty Parset with prefix "linmos".
**kwargs : dict
    Additional keyword arguments passed to the linmos application.

Notes
-----
For further information on usage check the ASKAPsoft documentation for `linmos <https://yandasoft.readthedocs.io/en/latest/calim/linmos.html>`_

Example
-------
>>> from taitale.askap import linmos
>>> # Using a parset file
>>> linmos(
...    parset="linmos.in",
...     args={
...         "names": "['image.0', 'image.1', 'image.2']",
...         "weights": "['weight.0', 'weight.1', 'weight.2']",
...         "outname": "mosaic",
...         "outweight": "weight",
...         "weighttype": "FromWeightImages",
...         "weightstate": "Inherent",
...         "nterms": "2",
...     }
... )

>>> # Using a Parset instance
>>> from taitale.utils.Parset import Parset
>>> parset = Parset(prefix="linmos")
>>> parset.set("names", "['image.0', 'image.1']")
>>> linmos(parset=parset)
"""
