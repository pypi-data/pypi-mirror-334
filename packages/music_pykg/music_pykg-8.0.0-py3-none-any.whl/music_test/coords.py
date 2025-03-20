"""Coordinate transformations"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


@dataclass(frozen=True)
class RotatedFrame2D:
    """A 2D rotated frame of reference"""

    angle: float

    def frame_to_global(self, xloc: NDArray, yloc: NDArray) -> tuple[NDArray, NDArray]:
        """Transform local frame coordinates to global"""
        s, c = np.sin(self.angle), np.cos(self.angle)
        xglob = c * xloc - s * yloc
        yglob = s * xloc + c * yloc
        assert np.allclose(xglob**2 + yglob**2, xloc**2 + yloc**2)
        return xglob, yglob

    def global_to_frame(
        self, xglob: NDArray, yglob: NDArray
    ) -> tuple[NDArray, NDArray]:
        """Transform global coordinates into local frame"""
        return RotatedFrame2D(-self.angle).frame_to_global(xglob, yglob)
