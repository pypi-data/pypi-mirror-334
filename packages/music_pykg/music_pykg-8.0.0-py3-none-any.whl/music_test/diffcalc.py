from __future__ import annotations

from typing import Callable

import numpy as np
from music_pykg.grid import Points
from numpy.typing import NDArray

ScalarField = Callable[[Points], NDArray]


def cycle3(axis: int, shift: int) -> int:
    return (axis + shift) % 3


def cartesian_curl(
    fx: ScalarField,
    fy: ScalarField,
    fz: ScalarField,
    axis: int,
    points: Points,
    dx: float,
    dy: float,
    dz: float,
) -> NDArray:
    """Return the component `axis` of the curl of vector field (fx, fy, fz),
    for a uniform Cartesian grid with spacings (dx, dy, dz).
    """
    assert 0 <= axis < 3
    hd = 0.5 * np.array([dx, dy, dz])

    ax1 = cycle3(axis, 1)
    ax2 = cycle3(axis, 2)

    f1 = (fx, fy, fz)[ax1]
    f2 = (fx, fy, fz)[ax2]

    ell1 = (dx, dy, dz)[ax1]
    ell2 = (dx, dy, dz)[ax2]

    fL = f2(points.shifted(shift=-hd[ax1], axis=ax1))
    fR = f2(points.shifted(shift=hd[ax1], axis=ax1))

    fB = f1(points.shifted(shift=-hd[ax2], axis=ax2))
    fT = f1(points.shifted(shift=hd[ax2], axis=ax2))

    circulation = ell2 * (fR - fL) + ell1 * (fB - fT)
    dS = ell1 * ell2
    return circulation / dS
