from __future__ import annotations

import typing
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path

import numpy as np
from scipy.io import FortranFile

if typing.TYPE_CHECKING:
    from numpy.typing import NDArray


@dataclass(frozen=True)
class GravityFile:
    """Gravity profiles, read and/or written by the code

    See gravitation.f90
    """

    path: Path

    @cached_property
    def data(self) -> NDArray[np.float64]:
        with FortranFile(self.path, mode="r") as ff:
            nr_tot = ff.read_record(np.int32).item()
            grav = ff.read_record(np.float64)
        if not grav.size == nr_tot:
            raise RuntimeError(f"Inconsistent gravity shape in {self.path}")
        return grav


def write_gravity(filepath: Path, grav: NDArray[np.floating]) -> None:
    """Write gravity file with given profile."""
    if not grav.ndim == 1:
        raise ValueError("Gravity profile should be a 1D array.")
    with FortranFile(filepath, "w") as ff:
        ff.write_record(np.array(grav.shape, dtype=np.int32))
        ff.write_record(grav.astype(np.float64))
