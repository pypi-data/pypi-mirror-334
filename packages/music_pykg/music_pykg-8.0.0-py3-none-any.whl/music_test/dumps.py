from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from os import PathLike
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping

import h5py
import numpy as np
from music_pykg.format2 import Header, MusicNewFormatDumpFile
from music_pykg.grid import Grid
from music_pykg.known_variables import KnownMusicVariables
from numpy.typing import NDArray

from .ic_gen import CachedStateAtNodes, Problem
from .utils import RelativePath


class Dump(ABC):
    """Base class for dump definition without knowing its concrete location."""

    @abstractmethod
    def with_path(self, path: Path) -> ConcreteDump:
        """Return a concrete dump relative to the provided location."""

    def __sub__(self, other: Dump) -> Dump:
        """Represent the difference between two dumps."""
        return DiffDump(self, other)


class ConcreteDump(ABC):
    """Dump knowing its concrete location."""

    @abstractmethod
    def header_and_data(self) -> tuple[Header, dict[str, NDArray]]:
        """Return a tuple (header, data) of two dictionaries,
        which map entry names to numerical values for the dump
        (typically of type `int`, `float` or `numpy.ndarray`).
        """


class FileDump(Dump, ABC):
    """A dump which corresponds to an actual file on disk"""

    filename: str | PathLike | RelativePath

    @abstractmethod
    def with_path(self, path: Path) -> ConcreteFileDump: ...


class ConcreteFileDump(ConcreteDump, ABC):
    fdump: FileDump
    path: Path

    @property
    def full_filename(self) -> Path:
        return self.path / self.fdump.filename


@dataclass(frozen=True)
class MusicDump2(FileDump):
    """New-style MUSIC dump (output_method=2)"""

    filename: str | PathLike | RelativePath

    def with_path(self, path: Path) -> ConcreteDump2:
        return ConcreteDump2(fdump=self, path=path)


@dataclass(frozen=True)
class ConcreteDump2(ConcreteFileDump):
    fdump: MusicDump2
    path: Path

    def header_and_data(self) -> tuple[Header, dict[str, NDArray]]:
        music_vars = KnownMusicVariables()
        hdr, data = MusicNewFormatDumpFile(self.full_filename).read()
        data = {music_vars.legacy(name).name: vals for name, vals in data.items()}
        return hdr, data


@dataclass(frozen=True)
class MusicDumpH5(FileDump):
    """MUSIC dump in HDF5 format."""

    filename: str | PathLike | RelativePath

    def with_path(self, path: Path) -> ConcreteDumpH5:
        return ConcreteDumpH5(fdump=self, path=path)


@dataclass(frozen=True)
class ConcreteDumpH5(ConcreteFileDump):
    fdump: MusicDumpH5
    path: Path

    def namelist(self) -> Mapping[str, Mapping[str, Any]]:
        nml = {}
        with h5py.File(self.full_filename) as h5f:
            for sec_name, sec in h5f["parameters_nml"].items():
                nml[sec_name] = MappingProxyType(
                    {opt: val[()].squeeze for opt, val in sec.items()}
                )
        return MappingProxyType(nml)

    def header_and_data(self) -> tuple[Header, dict[str, NDArray]]:
        data = {}
        with h5py.File(self.full_filename) as h5f:
            for name, values in h5f["fields"].items():
                data[name] = values[()].squeeze().T

            ndim = data[name].ndim
            nfaces = h5f["geometry/ncells"][()] + 1
            xsmin = h5f["geometry/xmin"][()]
            xsmax = h5f["geometry/xmax"][()]

            cartesian = "cartesian" in h5f["geometry/type"].asstr()

            header = Header(
                xmcore=h5f["parameters_header/xmcore"][()].item(),
                model=h5f["parameters_header/model"][()].item(),
                dtn=h5f["parameters_header/dtn"][()].item(),
                time=h5f["parameters_header/time"][()].item(),
                spherical=not cartesian,
                face_loc_1=np.linspace(xsmin[0], xsmax[0], nfaces[0]),
                face_loc_2=np.linspace(xsmin[1], xsmax[1], nfaces[1]),
                face_loc_3=(
                    None if ndim == 2 else np.linspace(xsmin[2], xsmax[2], nfaces[2])
                ),
            )
        return header, data


@dataclass(frozen=True)
class DiffDump(Dump):
    """A dump formed by selecting the header of either `dump_left` or `dump_right`,
    and taking the differences of the data arrays.
    """

    dump_left: Dump
    dump_right: Dump
    which_header: str = "left"  # select header from dump_left or dump_right

    def with_path(self, path: Path) -> ConcreteDiffDump:
        return ConcreteDiffDump(
            self.dump_left.with_path(path),
            self.dump_right.with_path(path),
            which_header=self.which_header,
        )


@dataclass(frozen=True)
class ConcreteDiffDump(ConcreteDump):
    dump_left: ConcreteDump
    dump_right: ConcreteDump
    which_header: str = "left"  # select header from dump_left or dump_right

    def header_and_data(self) -> tuple[Header, dict[str, NDArray]]:
        header_left, data_left = self.dump_left.header_and_data()
        header_right, data_right = self.dump_right.header_and_data()
        if self.which_header == "left":
            header = header_left
        elif self.which_header == "right":
            header = header_right
        else:
            raise ValueError(
                f"DiffDumpData: expected which_header to be "
                f"either 'left' or 'right', got '{self.which_header}'"
            )

        if not set(data_left.keys()) == set(data_right.keys()):
            raise ValueError(
                "DiffDumpData: non-identical data keys, got "
                f"keys_left={list(data_left.keys())}, "
                f"keys_right={list(data_right.keys())}"
            )

        return header, {k: data_left[k] - data_right[k] for k in data_left}


@dataclass(frozen=True)
class AnalyticalSolution(Dump):
    problem: Problem
    ref_dump: Dump

    def with_path(self, path: Path) -> ConcreteAnalyticalSolution:
        return ConcreteAnalyticalSolution(self.problem, self.ref_dump.with_path(path))


@dataclass(frozen=True)
class ConcreteAnalyticalSolution(ConcreteDump):
    problem: Problem
    ref_dump: ConcreteDump

    def header_and_data(self) -> tuple[Header, dict[str, NDArray]]:
        header, data = self.ref_dump.header_and_data()

        music_vars = KnownMusicVariables()
        unknown_vars = set(name for name in data.keys() if name not in music_vars)
        if unknown_vars:
            raise ValueError(
                f"{self.ref_dump} has variables {sorted(unknown_vars)}"
                " whose mesh centering cannot be inferred"
            )

        cached_state = CachedStateAtNodes(
            problem=self.problem,
            time=header.time,
            grid=Grid.from_header(header),
        )

        def sol(var: str) -> NDArray:
            fields = cached_state.at(music_vars[var].nodes).as_data_dict()
            if var not in fields:
                raise ValueError(
                    f"field '{var}' is present in '{self.ref_dump}' but not in analytical solution"
                )
            return fields[var].squeeze()

        return header, {k: sol(k) for k in data}
