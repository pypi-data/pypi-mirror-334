from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property
from types import MappingProxyType
from typing import Mapping, Sequence

from .grid import NODES_CENTER, NODES_FACE_1, NODES_FACE_2, NODES_FACE_3, Nodes


@dataclass(frozen=True)
class Variable:
    name: str
    legacy_name: str
    nodes: Nodes


@dataclass(frozen=True)
class KnownMusicVariables:
    named_scalars: Sequence[str] = ()

    @cached_property
    def _vars(self) -> Sequence[Variable]:
        return [
            Variable(name="density", legacy_name="rho", nodes=NODES_CENTER),
            Variable(name="e_int_spec", legacy_name="e", nodes=NODES_CENTER),
            # --
            Variable(name="vel_1", legacy_name="v_r", nodes=NODES_FACE_1),
            Variable(name="vel_2", legacy_name="v_t", nodes=NODES_FACE_2),
            Variable(name="vel_3", legacy_name="v_p", nodes=NODES_FACE_3),
            # --
            Variable(name="magfield_1", legacy_name="b_r", nodes=NODES_FACE_1),
            Variable(name="magfield_2", legacy_name="b_t", nodes=NODES_FACE_2),
            Variable(name="magfield_3", legacy_name="b_p", nodes=NODES_FACE_3),
            # --
            *[
                Variable(
                    name=name,
                    legacy_name=f"Scalar{i}",
                    nodes=NODES_CENTER,
                )
                for i, name in enumerate(self.named_scalars, 1)
            ],
        ]

    @cached_property
    def _legacy_names_dict(self) -> Mapping[str, Variable]:
        return MappingProxyType({v.legacy_name: v for v in self._vars})

    @cached_property
    def _names_dict(self) -> Mapping[str, Variable]:
        return MappingProxyType({v.name: v for v in self._vars})

    def legacy(self, name: str) -> Variable:
        """Get a variable by its legacy name."""
        if name in self._legacy_names_dict:
            return self._legacy_names_dict[name]
        if not self.named_scalars and name.startswith("Scalar"):
            try:
                iscalar = int(name[6:])
                return Variable(
                    name=f"scalar_{iscalar}",
                    legacy_name=name,
                    nodes=NODES_CENTER,
                )
            except ValueError:
                pass
        raise KeyError(
            f"Variable with legacy name '{name}' unknown to KnownMusicVariables"
        )

    def __getitem__(self, name: str) -> Variable:
        """Get a variable by its name."""
        if name in self._names_dict:
            return self._names_dict[name]
        if not self.named_scalars and name.startswith("scalar_"):
            try:
                iscalar = int(name[7:])
                return Variable(
                    name=name,
                    legacy_name=f"Scalar{iscalar}",
                    nodes=NODES_CENTER,
                )
            except ValueError:
                pass
        raise KeyError(f"Variable with name '{name}' unknown to KnownMusicVariables")

    def __contains__(self, name: str) -> bool:
        """Check whether a variable is known."""
        try:
            self[name]
        except KeyError:
            return False
        return True
