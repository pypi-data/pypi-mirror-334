from __future__ import annotations

import operator
import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from music_pykg.prof1d import Prof1d
from rich import box
from rich.table import Table
from rich.text import Text

from .term import err_txt, info_txt
from .validation import ValidationResult

if typing.TYPE_CHECKING:
    from typing import Callable, Mapping

    from numpy.typing import ArrayLike, NDArray
    from pandas import DataFrame

    from .dumps import Dump, FileDump


class SelfCheck(ABC):
    @abstractmethod
    def check_run(self, run_dir: Path) -> ValidationResult:
        raise NotImplementedError

    def __and__(self, other: SelfCheck) -> SelfCheck:
        return CombinedSelfCheck(self, other, operator.and_)

    def __or__(self, other: SelfCheck) -> SelfCheck:
        return CombinedSelfCheck(self, other, operator.or_)


@dataclass(frozen=True)
class CombinedSelfCheck(SelfCheck):
    check1: SelfCheck
    check2: SelfCheck
    binary_op: Callable[[ValidationResult, ValidationResult], ValidationResult]

    def check_run(self, run_dir: Path) -> ValidationResult:
        return self.binary_op(
            self.check1.check_run(run_dir), self.check2.check_run(run_dir)
        )


def _mapping_norm_msg(mapping: Mapping[str, ArrayLike] | DataFrame) -> Table:
    def norm_1(x: ArrayLike) -> np.number:
        return np.mean(np.abs(x))

    def norm_2(x: ArrayLike) -> np.number:
        return np.sqrt(np.mean(np.abs(x) ** 2))

    def norm_inf(x: ArrayLike) -> np.number:
        return np.max(np.abs(x))

    table = Table(box=box.SIMPLE)
    table.add_column("key", no_wrap=True)
    table.add_column("L1")
    table.add_column("L2")
    table.add_column("Linf")
    for k, v in mapping.items():
        table.add_row(
            f"{k!r}",
            f"{norm_1(v):.4e}",
            f"{norm_2(v):.4e}",
            f"{norm_inf(v):.4e}",
        )
    return table


@dataclass(frozen=True)
class CheckAgainstRefDump(SelfCheck):
    dump1: Dump
    dump2: Dump
    comparison_method: ComparisonMethod

    def check_run(self, run_dir: Path) -> ValidationResult:
        hdr1, data1 = self.dump1.with_path(run_dir).header_and_data()
        hdr2, data2 = self.dump2.with_path(run_dir).header_and_data()
        if data1.keys() != data2.keys():
            return ValidationResult(
                False,
                err_txt(
                    "Dumps hold different fields:",
                    "dump1: " + str(sorted(data1.keys())),
                    "dump2: " + str(sorted(data2.keys())),
                ),
            )
        fields_identical = all(
            self.comparison_method.array_comparison(fld1, data2[name])
            for name, fld1 in data1.items()
        )
        if not fields_identical:
            _, diff = (self.dump1 - self.dump2).with_path(run_dir).header_and_data()
            return ValidationResult(False, _mapping_norm_msg(diff))
        coords_identical = (
            np.all(hdr1.face_loc_1 == hdr2.face_loc_1)
            and np.all(hdr1.face_loc_2 == hdr2.face_loc_2)
            and np.all(hdr1.face_loc_3 == hdr2.face_loc_3)
        )
        if not coords_identical:
            diff = {
                "face_loc_1": hdr1.face_loc_1 - hdr2.face_loc_1,
                "face_loc_2": hdr1.face_loc_2 - hdr2.face_loc_2,
                "face_loc_3": np.asarray(
                    (hdr1.face_loc_3 or 0) - (hdr2.face_loc_3 or 0)
                ),
            }
            return ValidationResult(False, _mapping_norm_msg(diff))
        return ValidationResult(True, Text("dumps are identical (fields and coord)"))


class ComparisonMethod(ABC):
    @abstractmethod
    def array_comparison(self, arr1: NDArray, arr2: NDArray) -> bool: ...


@dataclass(frozen=True)
class WithPrecision(ComparisonMethod):
    rtol: float = 1e-15
    atol: float = 1e-15

    def array_comparison(self, arr1: NDArray, arr2: NDArray) -> bool:
        return np.allclose(arr1, arr2, rtol=self.rtol, atol=self.atol)


@dataclass(frozen=True)
class BitIdentical(ComparisonMethod):
    def array_comparison(self, arr1: NDArray, arr2: NDArray) -> bool:
        return np.array_equal(arr1, arr2)


@dataclass(frozen=True)
class ReportNorms(SelfCheck):
    """Report norms of input dump object to log messages, always returning a successful status.

    NOTE: the norms are computed pointwise naively, i.e. they are seen as norms on data arrays,
    not as proper integral norms e.g. on the sphere.
    """

    dump: Dump
    label: str = ""

    def check_run(self, run_dir: Path) -> ValidationResult:
        _, data = self.dump.with_path(run_dir).header_and_data()
        message = _mapping_norm_msg(data)

        return ValidationResult(True, message).with_header_msg(
            Text("ReportNorms" + (f"[{self.label}]" if self.label else "") + ":")
        )


@dataclass(frozen=True)
class ReportProf1dDiff(SelfCheck):
    """Report difference between two prof1d."""

    prof1d_left: str
    prof1d_right: str
    label: str = ""

    def check_run(self, run_dir: Path) -> ValidationResult:
        p1dl = Prof1d(run_dir / self.prof1d_left)
        p1dr = Prof1d(run_dir / self.prof1d_right)

        params = {k: p1dl.params[k] - rval for k, rval in p1dr.params.items()}
        message = _mapping_norm_msg(params)
        result = ValidationResult(True, message).with_header_msg(
            Text(
                "ReportProf1dDiff-params"
                + (f"[{self.label}]" if self.label else "")
                + ":"
            )
        )

        profs = p1dl.profs - p1dr.profs
        message = _mapping_norm_msg(profs)
        result &= ValidationResult(True, message).with_header_msg(
            Text(
                "ReportProf1dDiff-profs"
                + (f"[{self.label}]" if self.label else "")
                + ":"
            )
        )
        return result


@dataclass(frozen=True)
class CheckTimeOfDump(SelfCheck):
    dump: FileDump
    time: float

    def check_run(self, run_dir: Path) -> ValidationResult:
        dump = self.dump.with_path(run_dir)
        header, _ = dump.header_and_data()
        t = header.time
        if not np.isclose(t, self.time):
            return ValidationResult(
                False,
                message=Text(
                    f"dump '{dump.full_filename}': expected time={self.time} but found {t}",
                    style="error",
                ),
            )
        return ValidationResult(
            True,
            Text(f"dump '{dump.full_filename}': expected time={self.time}, found {t}"),
        )


@dataclass(frozen=True)
class SpatialConvergenceCheck(SelfCheck):
    """Analysis of convergence order with grid spacing amongst several runs."""

    error: Dump
    field: str
    expected_order: float
    subdirs: tuple[str, ...]
    order_tol: float = 0.05

    def check_run(self, run_dir: Path) -> ValidationResult:
        err_rms = []
        resols = []
        for subdir in self.subdirs:
            header, data = self.error.with_path(run_dir / subdir).header_and_data()
            resols.append(header.nfaces[0] - 1)
            err_rms.append(np.sqrt(np.mean(data[self.field] ** 2)))
        msgs = []
        success = True
        resol_ref = resols[0]
        for resol, err in zip(resols[1:], err_rms[1:]):
            order = np.log(err / err_rms[0]) / np.log(resol_ref / resol)
            success = success and abs(order - self.expected_order) <= self.order_tol
            msgs.append(
                f"comparing {resol:03d} to {resol_ref:03d} ({self.field}): "
                f"order={order} (expected {self.expected_order}±{self.order_tol})"
            )
        return ValidationResult(
            is_success=success,
            message=info_txt(*msgs),
        )
