from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType


@dataclass(frozen=True)
class PhysConsts:
    label: str
    gravitational: float
    speed_of_light: float
    stefan_boltzmann: float
    radiation_density: float
    molar_gas: float


_revisions = (
    PhysConsts(
        label="legacy",
        gravitational=6.6732e-8,
        speed_of_light=(c := 2.997925e10),
        radiation_density=(arad := 7.56471e-15),
        stefan_boltzmann=arad * c / 4,  # type: ignore
        molar_gas=8.314462618e7,
    ),
    PhysConsts(
        label="CODATA2022",
        gravitational=6.67430e-8,
        speed_of_light=(c := 2.99792458e10),
        stefan_boltzmann=(sigmab := 5.670374419e-5),
        radiation_density=4 * sigmab / c,
        molar_gas=8.314462618e7,
    ),
)


REVISIONS = MappingProxyType({pc.label: pc for pc in _revisions})
