from typing import Union

from taitale.utils.Parset import Parset
from taitale.utils.wrapper import parset_app


def imcontsub(
    parset: Union[str, Parset, None] = None,
    **kwargs,
):
    if parset is None:
        parset = Parset(prefix="imcontsub")
    elif isinstance(parset, str):
        parset_obj = Parset(prefix="imcontsub")
        parset_obj.read_from_file(parset)
        parset = parset_obj
    elif not isinstance(parset, Parset):
        raise TypeError("parset must be either a string path or a Parset instance")

    imcontsub_app = parset_app(
        name="imcontsub",
        parset=parset,
        out_parset_name="taitale_imcontsub.in",
        cmd="imcontsub -c {parset_name}",
        mpi_compartible=True,
    )

    imcontsub_app(**kwargs)


imcontsub.__doc__ = """
The purpose of imcontsub is to subtract continuum from an image cube.
The tool processes the cube in parallel using MPI,
where each rank processes a block of Ny/Nranks x-z planes.

Parameters
----------
parset : str or Parset or None, optional
    Either a path to a parset file, a Parset instance, or None to create a new Parset.
    If None, creates a new empty Parset with prefix "imcontsub".
**kwargs : dict
    Additional keyword arguments passed to the imcontsub application.
    Common parameters include:

    - inputfitscube : str
        Image cube to work with. Must be in FITS format.
    - outputfitscube : str
        The name of the output cube. If unspecified, generated from input name
        (e.g., mycube.fits -> mycube.contsub.fits)
    - order : int
        The order of the polynomial used to fit for the continuum (default: 2)
    - threshold : float
        Threshold in robust rms units to decide which channels to include
        in the fit (default: 2.0)
    - blocksize : int
        Size of channel blocks for subtraction. Matches beamforming interval.
        0 means fit/subtract whole spectrum (default: 0)
    - shift : int
        Shift the origin of subtraction blocks left by this many channels (default: 0)
    - interleave : bool
        If true, interleave fit/subtract blocks using blocksize channels but
        subtracting only central 50% (default: false)
    - iterativeclip : bool
        If true, use iterative robust clipping to reject emission/absorption
        features (default: true)
    - imageaccess : str
        IO mode: 'collective' (default, MPI collective IO) or
        'individual' (sequential mode)
    - imageHistory : list[str]
        Lines to add to the image history

Notes
-----
For further information on usage check the ASKAPsoft documentation for `imcontsub <https://yandasoft.readthedocs.io/en/latest/calim/imcontsub.html>`_

Example
-------
>>> from taitale.askap import imcontsub
>>> # Using kwargs directly
>>> imcontsub(
...    workers=2,
...    args={
...        "inputfitscube": "mycube.fits",
...        "outputfitscube": "mycube.contsub.fits",
...        "order": "1",
...        "threshold": "2.5",
...        "blocksize": "54",
...    }
... )
"""
