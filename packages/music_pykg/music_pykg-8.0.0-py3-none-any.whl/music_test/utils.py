"""Misc utility functions for the MUSIC test system"""

from __future__ import annotations

import subprocess
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from time import perf_counter
from typing import Any, Sequence, TextIO

import f90nml


def round(m: int, base: int) -> int:
    """Round `m` to next multiple of `p`"""
    return m + ((base - m) % base)


def check_call_tee_multi(
    command: Sequence[str], fd_seq: Sequence[TextIO], **kwargs: Any
) -> None:
    """
    Run command, redirecting stdout and stderr to all file descriptors in a sequence.
    Raises CalledProcessError if return code is nonzero, like subprocess.check_call.
    """
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1,
        **kwargs,
    )
    # TYPE SAFETY: proc created so that stdout is a TextIO
    for line in iter(proc.stdout.readline, ""):  # type: ignore
        # Write line to each file descriptor provided
        for fdesc in fd_seq:
            fdesc.write(line)
    proc.wait()
    proc.stdout.close()  # type: ignore
    if proc.returncode != 0:
        raise subprocess.CalledProcessError(proc.returncode, command)


def check_call_tee(
    command: Sequence[str], fdesc: TextIO, also_to_stdout: bool = False, **kwargs: Any
) -> None:
    """Run command, redirecting stdout and stderr to given file descriptor,
    and optionally to sys.stdout as well.
    """
    if also_to_stdout:
        check_call_tee_multi(command, [fdesc, sys.stdout], **kwargs)
    else:
        check_call_tee_multi(command, [fdesc], **kwargs)


class Timer:
    """A simple timer based on time.perf_counter()"""

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.t0 = perf_counter()

    def time(self) -> float:
        return perf_counter() - self.t0

    def time_str(self) -> str:
        return f"{self.time():.2f} s"


class RelativePath(ABC):
    """A relative path that needs to know about its root for resolution.

    Instances support concatenation to a Path object, using this Path as the
    root for resolution.
    """

    @abstractmethod
    def resolve_in(self, root_dir: Path) -> Path:
        """Evaluate the relative path for a given root.

        Implementations should return the resolved relative path with the
        `root_dir` prepended so that `some_path / relative_path_resolver`
        has the expected value.
        """

    def __rtruediv__(self, root_dir: Path) -> Path:
        # This method is implemented so that a RelativePath can be
        # appended to a Path via the division operator like any other
        # path segment (such as a regular str or a PathLike).
        return self.resolve_in(root_dir)


@dataclass(frozen=True)
class LastFileNameInGlob(RelativePath):
    pattern: str

    def resolve_in(self, root_dir: Path) -> Path:
        try:
            return max(root_dir.glob(self.pattern))
        except ValueError:
            raise RuntimeError(
                f"Could not find a path matching {self.pattern} in {root_dir}"
            )


@dataclass(frozen=True)
class FilenameInNml(RelativePath):
    namelist: str
    section: str
    option: str

    def resolve_in(self, root_dir: Path) -> Path:
        nml = f90nml.read(root_dir / self.namelist)
        return root_dir / nml[self.section][self.option]
