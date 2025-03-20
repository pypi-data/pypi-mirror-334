#!/usr/bin/env python3

from __future__ import annotations

import typing
from collections import defaultdict
from dataclasses import dataclass
from functools import cached_property, reduce
from itertools import product
from operator import mul

import f90nml
from rich import box
from rich.console import Console
from rich.style import Style
from rich.table import Table
from rich.text import Text

from .format2 import MusicNewFormatDumpFile

if typing.TYPE_CHECKING:
    from typing import Iterable, Sequence

    from .cli import CliConfig

CORES_PER_NODE = {
    "isca": 16,
    "dial2": 36,
    "dial3": 128,
    "csd3_cclake": 56,
    "csd3_icelake": 76,
}


def prod(nums: Iterable[int]) -> int:
    return reduce(mul, nums, 1)


@dataclass(frozen=True)
class PrimeFactors:
    _factors: defaultdict[int, int]

    @staticmethod
    def of(val: int) -> PrimeFactors:
        if val <= 0:
            raise ValueError(f"PrimeFactors deals with positive numbers, {val} given.")
        factors: defaultdict[int, int] = defaultdict(int)
        while val % 2 == 0:
            val //= 2
            factors[2] += 1
        prime = 3
        while val > 1:
            while val % prime == 0:
                val //= prime
                factors[prime] += 1
            prime += 2
        return PrimeFactors(factors)

    def __floordiv__(self, other: PrimeFactors) -> PrimeFactors:
        factors = defaultdict(int, self._factors)
        for prime, exponent in other._factors.items():
            factors[prime] -= exponent
            if factors[prime] < 0:
                raise ValueError(f"{other} does not divide {self}")
        return PrimeFactors(factors)

    def __mul__(self, other: PrimeFactors) -> PrimeFactors:
        factors = defaultdict(int, self._factors)
        for prime, exponent in other._factors.items():
            factors[prime] += exponent
        return PrimeFactors(factors)

    def common_divisors(self, other: PrimeFactors) -> Iterable[PrimeFactors]:
        """Yield all divisors of `self` that are also divisors of `other`.

        For instance, PrimeFactors.of(30).common_divisors(PrimeFactors.of(24))
        yields 1, 2, 3, 6 (as PrimeFactors instances).
        """
        factor_ranges: dict[int, range] = {}
        for prime, exponent in other._factors.items():
            factor_ranges[prime] = range(0, 1 + min(exponent, self._factors[prime]))
        # Cannot use nested generators here because of Python's broken name-capture
        # mechanism (`p` in the inner tuple would be bound to the last value of `p`
        # in the outer loop).
        factor_lists = [[(p, e) for e in fr] for p, fr in factor_ranges.items()]
        for pfs in product(*factor_lists):
            yield PrimeFactors(defaultdict(int, pfs))

    def subfactors_not_dividing(self, other: PrimeFactors) -> PrimeFactors:
        """Return subfactors of `self` that don't divide `other`."""
        factors = {
            prime: exp
            for prime, exponent in self._factors.items()
            if (exp := exponent - other._factors[prime]) > 0
        }
        return PrimeFactors(defaultdict(int, factors))

    def value(self) -> int:
        return prod(prime**exp for prime, exp in self._factors.items())


def _decomp(
    ncores: PrimeFactors, ncells_tot: int, ncells: list[int]
) -> list[list[int]]:
    if len(ncells) == 1:
        nc = ncores.value()
        assert ncells[0] % nc == 0
        return [[nc]]
    ncells = list(ncells)
    ncell = ncells.pop()
    ncells_tot //= ncell
    must_be_in_current = ncores.subfactors_not_dividing(PrimeFactors.of(ncells_tot))
    current_ncells_rem = PrimeFactors.of(ncell) // must_be_in_current
    ncores //= must_be_in_current
    out: list[list[int]] = []
    for divisor in ncores.common_divisors(current_ncells_rem):
        ncore = must_be_in_current * divisor
        ncore_val = ncore.value()
        for lst in _decomp(ncores // divisor, ncells_tot, ncells):
            lst.append(ncore_val)
            out.append(lst)
    return out


def decomposition(ncores: int, ncells: Sequence[int]) -> list[list[int]]:
    ncells_tot = prod(ncells)
    if ncells_tot % ncores != 0:
        return []
    # flip ncells (and flip back resulting core decomposition) to favour
    # splitting along the last dimension rather than the first
    return list(
        map(
            lambda cores: cores[::-1],
            _decomp(
                PrimeFactors.of(ncores),
                ncells_tot,
                list(ncells[::-1]),
            ),
        )
    )


@dataclass(frozen=True)
class DecompItemText:
    ncores: str
    nloc: str
    overhead: str

    def __rich__(self) -> Text:
        return Text.assemble(
            Text(self.ncores, Style(bold=True)),
            Text(f" [{self.nloc}]", Style(color="magenta")),
            Text(f" ({self.overhead})", Style(dim=True)),
        )


@dataclass(frozen=True)
class DecompItem:
    ncores: Sequence[int]
    ncells: Sequence[int]
    nghosts: int

    @cached_property
    def nloc(self) -> Sequence[int]:
        return tuple(ncell // ncore for ncell, ncore in zip(self.ncells, self.ncores))

    @cached_property
    def overhead(self) -> float:
        nbulk = prod(self.nloc)
        nwith_gc = prod(map(lambda nc: nc + 2 * self.nghosts, self.nloc))
        return nwith_gc / nbulk - 1

    def __rich__(self) -> DecompItemText:
        return DecompItemText(
            ncores=" ".join(map(str, self.ncores)),
            nloc=" ".join(map(str, self.nloc)),
            overhead=f"{self.overhead:.2}",
        )


def main(conf: CliConfig) -> None:
    console = Console(markup=False, highlight=False)

    if conf.cpu.ncells:
        ncells = conf.cpu.ncells
        shape_provenance = Text("Using shape specified via `--ncells`:")
    else:
        nml = f90nml.read(conf.cpu.params)
        ic = MusicNewFormatDumpFile(conf.cpu.params.parent / nml["io"]["input"])
        hdr = ic.read_header()
        nfaces = [hdr.face_loc_1.size, hdr.face_loc_2.size]
        if hdr.face_loc_3 is not None:
            nfaces.append(hdr.face_loc_3.size)
        ncells = tuple(map(lambda nf: nf - 1, nfaces))
        shape_provenance = Text(f"Using shape from {ic.file_name}:")

    console.print(shape_provenance, Text(f"{ncells}", style="blue"), end="\n\n")

    console.print("item format:", DecompItemText("ncores", "ncells_loc", "overhead"))
    for plf, ncore_per_nodes in CORES_PER_NODE.items():
        if conf.cpu.platform and plf != conf.cpu.platform:
            continue
        console.print()
        plf_label = f"{plf} ({ncore_per_nodes} cores/node)"
        table = Table(title=plf_label, box=box.SIMPLE)
        table.add_column("nodes")
        table.add_column("cores")
        table.add_column("best")
        table.add_column("2nd best")
        table.add_column("3rd best")
        for nnodes in range(1, conf.cpu.nodes):
            info = [
                DecompItem(
                    ncores=ncores,
                    ncells=ncells,
                    nghosts=conf.cpu.nghosts,
                )
                for ncores in decomposition(ncore_per_nodes * nnodes, ncells)
            ]
            info.sort(key=lambda elt: elt.overhead)
            if info:
                table.add_row(str(nnodes), str(nnodes * ncore_per_nodes), *info[:3])
        if table.row_count > 0:
            console.print(table)
        else:
            console.print(
                Text(f"{plf_label}:", style="table.title"),
                Text("no decomposition", style="dim"),
            )
