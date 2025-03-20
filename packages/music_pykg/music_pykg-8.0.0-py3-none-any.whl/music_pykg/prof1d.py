"""Utility to read profile1d dat files."""

from __future__ import annotations

import typing
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from types import MappingProxyType

import pandas as pd

if typing.TYPE_CHECKING:
    from typing import Mapping


@dataclass(frozen=True)
class Prof1d:
    """Prof1d parser.

    This parses 1D profiles data. Files are expected to be in the following
    format (with arbitrary number of parameters and columns):

    ```txt
    param_label1 param_label2
    param_value1 param_value2
    column1 column2 column3
    val1_1  val1_2  val1_3
    val2_1  val2_2  val2_3
    val3_1  val3_2  val3_3
    val4_1  val4_2  val4_3
    val5_1  val5_2  val5_3
    ```

    A mapping between parameter labels and values is accessible via the `params`
    property. Profiles are accessible via the `profs` property.

    If there are no parameters, set `params_present` to `False`.
    """

    path: Path
    params_present: bool = True

    @staticmethod
    def with_path_hint(path_hint: Path) -> Prof1d:
        """Find a profile file from the given hint.

        Args:
            path_hint: either the path to the profile file, or the path to the
                folder containing the profile file.  In the latter case, the
                parser tries to find a file and fails if none is found or there
                is ambiguity.
        """
        if path_hint.is_file():
            return Prof1d(path_hint)
        candidates = [
            path
            for p1d in ("profile1d.dat", "profile1d_scalars.dat")
            if (path := path_hint / p1d).is_file()
        ]
        if not candidates:
            raise RuntimeError("No profile1d file found in {self._path_hint}")
        if len(candidates) > 1:
            raise RuntimeError(f"More than one profile1d files found: {candidates}")
        return Prof1d(candidates[0])

    @cached_property
    def params(self) -> Mapping[str, float]:
        if self.params_present:
            with self.path.open() as p1d:
                names = p1d.readline().split()
                values = map(float, p1d.readline().split())
            params = dict(zip(names, values))
            return MappingProxyType(params)
        return {}

    @cached_property
    def profs(self) -> pd.DataFrame:
        skip = 2 if self.params_present else 0
        return pd.read_csv(self.path, skiprows=skip, sep=r"\s+")
