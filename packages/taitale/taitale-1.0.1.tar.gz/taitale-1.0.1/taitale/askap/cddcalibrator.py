from typing import Union

from taitale.utils.Parset import Parset
from taitale.utils.wrapper import parset_app


def cddcalibrator(
    parset: Union[str, Parset, None] = None,
    **kwargs,
):
    if parset is None:
        parset = Parset("Cddcalibrator")
    elif isinstance(parset, str):
        parset_obj = Parset("Cddcalibrator")
        parset_obj.read_from_file(parset)
        parset = parset_obj
    elif not isinstance(parset, Parset):
        raise TypeError("parset must be either a string path or a Parset instance")

    cddcalibrator_app = parset_app(
        name="Cddcalibrator",
        parset=parset,
        out_parset_name="taitale_cddcalibrator.in",
        cmd="Cddcalibrator -c {parset_name}",
        mpi_compartible=True,
    )

    cddcalibrator_app(**kwargs)


cddcalibrator.__doc__ = """
Taitale interface to Cddcalibrator

Parameters
----------
parset : str or Parset or None, optional
    Either a path to a parset file, a Parset instance, or None to create a new Parset.
    If None, creates a new empty Parset with prefix "Cddcalibrator".
**kwargs : dict
    Additional keyword arguments passed to the Cddcalibrator application.

Notes
-----
For further information on usage check the ASKAPsoft documentation for `Cddcalibrator <https://yandasoft.readthedocs.io/en/latest/calim/cddcalibrator.html>`_

Example
-------

>>> from taitale import taitale_env
>>> from taitale.askap import cddcalibrator
>>>
>>> env = taitale_env(runtime="container", image="csirocass/askapsoft")
>>>
>>> # Using direct arguments
>>> cddcalibrator(
...     env=env,
...     workers=6,  # Use 6 MPI workers
...     args={
...         "dataset": "observation.ms",
...         "nAnt": "36",
...         "nBeam": "36",
...         "refantenna": "1",
...         "calibaccess": "table",
...         "calibaccess.table": "ddcal.tab",
...     },
... )
>>>
>>> # Using a parset file
>>> cddcalibrator(
...     env=env,
...     workers=6,
...     parset="cddcalibrator.in",
... )
"""
