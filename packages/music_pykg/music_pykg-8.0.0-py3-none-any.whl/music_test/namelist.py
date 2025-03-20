from __future__ import annotations

import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

import f90nml
from music_pykg.namelist import MusicNamelist

if typing.TYPE_CHECKING:
    from os import PathLike
    from pathlib import Path
    from typing import Any, Mapping

    from .utils import RelativePath


class NmlFile(ABC):
    @abstractmethod
    def path_in(self, directory: Path) -> Path: ...

    @abstractmethod
    def read_in(self, directory: Path) -> MusicNamelist: ...

    @abstractmethod
    def ensure_present_in(self, directory: Path) -> None: ...


@dataclass(frozen=True)
class MusicNmlFile(NmlFile):
    filepath: str | PathLike | RelativePath

    def path_in(self, directory: Path) -> Path:
        return directory / self.filepath

    def read_in(self, directory: Path) -> MusicNamelist:
        return MusicNamelist(self.path_in(directory))

    def ensure_present_in(self, directory: Path) -> None:
        if not self.path_in(directory).is_file():
            raise RuntimeError(f"Namelist {self!r} not found in {directory}")


@dataclass(frozen=True)
class MusicNamelistFromTemplate(NmlFile):
    template: str | PathLike | RelativePath
    changes: Mapping[str, Mapping[str, Any]] = field(hash=False)
    filename: str

    def path_in(self, directory: Path) -> Path:
        return directory / self.filename

    def read_in(self, directory: Path) -> MusicNamelist:
        nml = MusicNamelist(directory / self.template)
        for section, opts in self.changes.items():
            for option, value in opts.items():
                nml.nml[section][option] = value
        return nml

    def ensure_present_in(self, directory: Path) -> None:
        nml = self.read_in(directory)
        out_path = self.path_in(directory)
        assert nml.path != out_path
        f90nml.write(nml.nml, out_path, force=True)
