from typing import Union

from taitale.utils.Parset import Parset
from taitale.utils.wrapper import parset_app


def cbpcalibrator(
    parset: Union[str, Parset, None] = None,
    **kwargs,
):
    if parset is None:
        parset = Parset(prefix="Cbpcalibrator")
    elif isinstance(parset, str):
        parset_obj = Parset(prefix="Cbpcalibrator")
        parset_obj.read_from_file(parset)
        parset = parset_obj
    elif not isinstance(parset, Parset):
        raise TypeError("parset must be either a string path or a Parset instance")

    cbpcalibrator_app = parset_app(
        name="cbpcalibrator",
        parset=parset,
        out_parset_name="taitale_cbpcalibrator.in",
        cmd="cbpcalibrator -c {parset_name}",
        mpi_compartible=False,
    )

    cbpcalibrator_app(**kwargs)


cbpcalibrator.__doc__ = """
The cbpcalibrator program is a specialised tool for bandpass calibration.

Parameters
----------
parset : str or Parset or None, optional
    Either a path to a parset file, a Parset instance, or None to create a new Parset.
    If None, creates a new empty Parset with prefix "Cbpcalibrator".
**kwargs : dict
    Additional keyword arguments passed to the cbpcalibrator application.

Notes
-----
For further information on usage check the ASKAPsoft documentation for `cbpcalibrator <https://yandasoft.readthedocs.io/en/latest/calim/cbpcalibrator.html>`_

Example
-------
>>> from taitale.askap import cbpcalibrator
>>> # Using a parset file
>>> cbpcalibrator(
...     parset="cbpcalibrator.in",
...     args = {
...         "dataset": "./1934-638_0.ms",
...         "sources.names": "['src1']",
...         "sources.cal.flux.i": "1.0",
...         "sources.cal.direction.ra": "0.003",
...         "sources.cal.direction.dec": "0.0",
...         "sources.src1.direction": "[12h30m00.000, -45.00.00.000, J2000]",
...         "sources.src1.components": "['cal']",
...         "calibaccess": "table",
...         "nChan": "28",
...         "interval": "300.0s",
...         "calibaccess.table": "1934-638_0.calib.bp",
...         "refantenna": "4",
...         "calibaccess.table.maxant": "36"
...     }
... )

>>> # Using a Parset instance
>>> from taitale.utils.Parset import Parset
>>> parset = Parset(prefix="Cbpcalibrator")
>>> parset.set("dataset", "./1934-638_0.ms")
>>> cbpcalibrator(parset=parset)
"""
