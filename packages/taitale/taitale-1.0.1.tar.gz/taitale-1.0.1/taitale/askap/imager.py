from typing import Union

from taitale.utils.Parset import Parset
from taitale.utils.wrapper import parset_app


def imager(
    parset: Union[str, Parset, None] = None,
    **kwargs,
):
    if parset is None:
        parset = Parset(prefix="Cimager")
    elif isinstance(parset, str):
        parset_obj = Parset(prefix="Cimager")
        parset_obj.read_from_file(parset)
        parset = parset_obj
    elif not isinstance(parset, Parset):
        raise TypeError("parset must be either a string path or a Parset instance")

    imager_app = parset_app(
        name="imager",
        parset=parset,
        out_parset_name="taitale_cimager.in",
        cmd="imager -c {parset_name}",
        mpi_compartible=True,
    )

    imager_app(**kwargs)


imager.__doc__ = """

Perform imaging in a parallel/distributed environment or on a single computer system.

Parameters
----------
parset : str or Parset or None, optional
    Either a path to a parset file, a Parset instance, or None to create a new Parset.
    If None, creates a new empty Parset with prefix "Cimager".
**kwargs : dict
    Additional keyword arguments passed to the imager application.

Notes
-----
For further information on usage check the ASKAPsoft documentation for `imager <https://yandasoft.readthedocs.io/en/latest/calim/imager.html>`_

Example
-------
>>> from taitale.askap import imager
>>> # Using a parset file
>>> imager(
...    parset="cimager.in",
...     workers=4,
...     args = {
...         "dataset": "./1934-638_0.ms",
...         "Images.Names": "image.i.1934-638_0",
...         "Images.shape":[2048, 2048],
...         "Images.cellsize":['2arcsec', '2arcsec'],
...         "Images.image.1924-638.direction":"[19h39m25.0342, -63.42.45.623, J2000]",
...         "restore":"true",
...         "restore.beam":"fit",
...         "restore.beam.cutoff": "0.5"
...     }
... )

>>> # Using a Parset instance
>>> from taitale.utils.Parset import Parset
>>> parset = Parset(prefix="Cimager")
>>> parset.set("dataset", "./1934-638_0.ms")
>>> imager(parset=parset, workers=4)
"""
