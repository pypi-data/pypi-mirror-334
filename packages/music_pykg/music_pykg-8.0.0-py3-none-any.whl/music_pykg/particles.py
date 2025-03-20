from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property
from os import PathLike

import h5py
import numpy as np
import pandas as pd


@dataclass(frozen=True)
class ParticleData:
    fname: str | PathLike
    group: str = "tracers"
    position_vector: int = 0

    def _fd(self) -> h5py.File:
        return h5py.File(self.fname, "r")

    @cached_property
    def time(self) -> float:
        with self._fd() as fd:
            return fd[self.group].attrs["time"]  # type: ignore

    @cached_property
    def npart(self) -> int:
        with self._fd() as fd:
            return fd[self.group].attrs["npart"]  # type: ignore

    @cached_property
    def ndim(self) -> int:
        with self._fd() as fd:
            return fd[self.group + "/pos"].shape[1]  # type: ignore

    def dataframe(self) -> pd.DataFrame:
        with self._fd() as fd:
            g = fd[self.group]
            pos = np.asarray(g["pos"][()])  # type: ignore
            _, ndim, _ = pos.shape
            gid = g["gid"][()]  # type: ignore
            fields = [
                {"gid": gid},
                *[
                    {f"x{ax + 1}": pos[self.position_vector, ax, :]}
                    for ax in range(ndim)
                ],
                *[{f"attr:{a}": g["attrs"][a][()]} for a in g["attrs"]],  # type: ignore
            ]

            df = pd.concat(
                [pd.DataFrame(d) for d in fields],
                axis="columns",
            ).set_index("gid")
            assert df is not None
            return df
