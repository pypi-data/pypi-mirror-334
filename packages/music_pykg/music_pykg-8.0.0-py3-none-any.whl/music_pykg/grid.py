from __future__ import annotations

import typing
from dataclasses import dataclass
from functools import cached_property

import numpy as np

if typing.TYPE_CHECKING:
    from numpy.typing import NDArray

    from .format2 import Header


@dataclass(frozen=True)
class Nodes:
    staggered_along_ax: tuple[bool, bool, bool]
    slices: tuple[slice, slice, slice]

    def __hash__(self) -> int:
        # because slices are not hashable
        return hash((self.staggered_along_ax, str(self.slices)))

    def is_staggered_along(self, axis: int, ndim: int) -> bool:
        assert 1 <= ndim <= 3
        assert 0 <= axis <= 2
        last_axis = ndim - 1
        if axis > last_axis:
            # A node is never staggered along a non-existing dimension
            return False
        else:
            return self.staggered_along_ax[axis]

    def slice_along(self, axis: int, ndim: int) -> slice:
        assert 1 <= ndim <= 3
        assert 0 <= axis <= 2
        last_axis = ndim - 1
        if axis > last_axis:
            # a non-existing dimension has only one point, we need to take it
            return slice(None)
        else:
            return self.slices[axis]

    def num_staggered_axes(self, ndim: int) -> int:
        assert 1 <= ndim <= 3
        return sum(self.staggered_along_ax[:ndim])


# Define some nodes
NODES_CENTER = Nodes(
    staggered_along_ax=(False, False, False),
    slices=(slice(None), slice(None), slice(None)),
)

NODES_FACE_1 = Nodes(
    staggered_along_ax=(True, False, False),
    slices=(slice(-1), slice(None), slice(None)),
)
NODES_FACE_2 = Nodes(
    staggered_along_ax=(False, True, False),
    slices=(slice(None), slice(-1), slice(None)),
)
NODES_FACE_3 = Nodes(
    staggered_along_ax=(False, False, True),
    slices=(slice(None), slice(None), slice(-1)),
)


@dataclass(frozen=True)
class Points:
    x1: NDArray
    x2: NDArray
    x3: NDArray

    def __post_init__(self) -> None:
        if not (self.x1.shape == self.x2.shape == self.x3.shape):
            raise ValueError(
                f"inconsistent shapes {self.x1.shape}, {self.x2.shape}, {self.x3.shape}"
            )

    @property
    def shape(self) -> tuple[int, ...]:
        return self.x1.shape

    def zeros(self) -> NDArray:
        return np.zeros_like(self.x1)

    def ones(self) -> NDArray:
        return np.ones_like(self.x1)

    def full(self, value: float) -> NDArray:
        return np.full_like(self.x1, value)

    def shifted(self, shift: float, axis: int) -> Points:
        face_arrs = (self.x1, self.x2, self.x3)
        shifted_faces = tuple(
            faces + shift if ax == axis else faces
            for (ax, faces) in enumerate(face_arrs)
        )
        return Points(x1=shifted_faces[0], x2=shifted_faces[1], x3=shifted_faces[2])


@dataclass(frozen=True)
class Grid:
    faces_along_axis: tuple[NDArray, NDArray, NDArray]
    spherical: bool = False

    def __post_init__(self) -> None:
        for axis, faces in enumerate(self.faces_along_axis):
            if faces.ndim != 1 or faces.size < 2:
                raise ValueError(
                    f"faces_along_axis[{axis}] has an invalid shape {faces.shape}"
                )

    @staticmethod
    def from_faces_loc(
        x0_faces: NDArray,
        x1_faces: NDArray,
        x2_faces: NDArray | None = None,
        spherical: bool = False,
    ) -> Grid:
        if x2_faces is None:
            x2_faces = np.array([0.0, 2 * np.pi]) if spherical else np.array([0.0, 1.0])
        return Grid(
            faces_along_axis=(x0_faces, x1_faces, x2_faces), spherical=spherical
        )

    @staticmethod
    def from_header(header: Header) -> Grid:
        return Grid.from_faces_loc(
            header.face_loc_1,
            header.face_loc_2,
            header.face_loc_3,
            spherical=header.spherical,
        )

    @cached_property
    def centers_along_axis(self) -> tuple[NDArray, NDArray, NDArray]:
        return tuple((faces[:-1] + faces[1:]) / 2 for faces in self.faces_along_axis)  # type: ignore

    @property
    def nfaces(self) -> tuple[int, int, int]:
        return tuple(faces.size for faces in self.faces_along_axis)  # type: ignore

    def is_2d(self) -> bool:
        return self.faces_along_axis[2].size == 2

    def points_at(self, nodes: Nodes) -> Points:
        ndim = 2 if self.is_2d() else 3

        xps = [
            faces[nodes.slice_along(axis, ndim)]
            if nodes.is_staggered_along(axis, ndim)
            else self.centers_along_axis[axis][nodes.slice_along(axis, ndim)]
            for axis, faces in enumerate(self.faces_along_axis)
        ]
        return Points(*np.meshgrid(*xps, indexing="ij"))
