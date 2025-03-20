from typing import Union

from taitale.utils.Parset import Parset
from taitale.utils.wrapper import parset_app


def selavy(
    parset: Union[str, Parset, None] = None,
    **kwargs,
):
    """
    The selavy program is used for source finding and characterisation
    """
    if parset is None:
        parset = Parset(prefix="Selavy")
    elif isinstance(parset, str):
        parset_obj = Parset(prefix="Selavy")
        parset_obj.read_from_file(parset)
        parset = parset_obj
    elif not isinstance(parset, Parset):
        raise TypeError("parset must be either a string path or a Parset instance")

    selavy_app = parset_app(
        name="selavy",
        parset=parset,
        out_parset_name="taitale_selavy.in",
        cmd="selavy -c {parset_name}",
        mpi_compartible=True,
    )

    selavy_app(**kwargs)


selavy.__doc__ = """
The selavy program is used for source finding and characterisation

Parameters
----------
parset : str or Parset or None, optional
    Either a path to a parset file, a Parset instance, or None to create a new Parset.
    If None, creates a new empty Parset with prefix "Selavy".
**kwargs : dict
    Additional keyword arguments passed to the selavy application.

Notes
-----
For further information on usage check the ASKAPsoft documentation for `selavy <https://yandasoft.readthedocs.io/en/latest/analysis/selavy.html>`_

Example
-------

>>> from taitale.askap import selavy
>>> # Using a parset file
>>> selavy(
...    parset="selavy.in",
...     args={
...         "image": "image.fits",
...         "snrCut": "5",
...         "flagGrowth": "true",
...         "growthThreshold": "3",
...         "flagNegative": "true",
...         "thresholdType": "sigma",
...         "verbose": "true",
...         "nsubx": "6",
...         "nsuby": "3",
...         "overlapx": "10",
...         "overlapy": "10",
...     }
... )

>>> # Using a Parset instance
>>> from taitale.utils.Parset import Parset
>>> parset = Parset(prefix="Selavy")
>>> parset.set("image", "image.fits")
>>> parset.set("snrCut", "5")
>>> parset.set("flagGrowth", "true")
>>> selavy(parset=parset)
"""
