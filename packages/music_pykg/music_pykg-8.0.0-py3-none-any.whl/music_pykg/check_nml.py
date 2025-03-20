from __future__ import annotations

import importlib.resources as imlr
import json
import sys
import typing
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path

import f90nml
import rich
from rich.prompt import Confirm
from rich.text import Text

if typing.TYPE_CHECKING:
    from typing import Any

    from .cli import CliConfig


def warn(path: Path, msg: str) -> None:
    rich.print(Text(f"WARNING: {path}: {msg}", style="yellow"))


def err(path: Path, msg: str) -> None:
    rich.print(Text(f"ERROR: {path}: {msg}", style="red"))


@dataclass(frozen=True)
class NmlModel:
    spec: str

    @cached_property
    def _data(self) -> dict[str, Any]:
        return json.loads(self.spec)

    def files(self) -> set[str]:
        return set(self._data["files"])

    def options_in(self, config_file: str) -> dict[str, set[str]]:
        out = {}
        for nml_id in self._data["files"][config_file]["namelists"]:
            nml_spec = self._data["namelists"][nml_id]
            nml_name = nml_spec.get("name", nml_id)
            out[nml_name] = set(nml_spec["parameters"].keys())
        return out

    def options_for_nml(
        self,
        config_file: str,
        exclude_advanced: bool,
    ) -> dict[str, dict[str, str]]:
        out: dict[str, dict[str, str]] = {}
        for nml_id in self._data["files"][config_file]["namelists"]:
            nml_spec = self._data["namelists"][nml_id]
            nml_name = nml_spec.get("name", nml_id)
            if exclude_advanced and nml_spec.get("advanced", False):
                continue
            out[nml_name] = {}
            for option, spec in nml_spec["parameters"].items():
                if exclude_advanced and spec.get("advanced", False):
                    continue
                default = spec.get("default_nml", spec["default"])
                if default:
                    out[nml_name][option] = default
        return out


_MODEL = NmlModel(
    spec=imlr.read_text(__package__, "parameters.json"),
)


def check_validity(nml_path: Path, filename: str, nml_model: NmlModel) -> None:
    nml_ref = nml_model.options_in(filename)
    nml = f90nml.read(nml_path)

    non_existent_nml = []
    non_existent_option = []

    for nml_name, nml_content in nml.items():
        if nml_name not in nml_ref:
            non_existent_nml.append(nml_name)
            continue
        for option in nml_content:
            if option not in nml_ref[nml_name]:
                non_existent_option.append((nml_name, option))

    missing_nml = [nml_name for nml_name in nml_ref if nml_name not in nml]
    if non_existent_nml:
        warn(nml_path, "unknown namelists found")
        for nml_name in non_existent_nml:
            print("  -", nml_name)
        print()
    if missing_nml:
        warn(nml_path, "some namelists that could be required were not found")
        for nml_name in missing_nml:
            print("  -", nml_name)
        print()
    if non_existent_option:
        err(nml_path, "invalid options found")
        for nml_name, option in non_existent_option:
            candidate_nml = set(
                name for name, opts in nml_ref.items() if option in opts
            )
            msg = (
                "perhaps you meant "
                + ", or ".join(f"{name}.{option}" for name in candidate_nml)
                if candidate_nml
                else "nor in any other namelist"
            )
            print(f"  - {nml_name}.{option} does not exist", msg, sep=", ")
        sys.exit(1)


def generate(
    nml_path: Path,
    filename: str,
    nml_model: NmlModel,
    keep_advanced: bool,
) -> None:
    with nml_path.open("w") as nmlf:
        for nml_name, content in nml_model.options_for_nml(
            filename,
            exclude_advanced=not keep_advanced,
        ).items():
            print(f"&{nml_name}", file=nmlf)
            for opt, dflt in content.items():
                print(f"  {opt} = {dflt}", file=nmlf)
            print("/\n", file=nmlf)


def main(conf: CliConfig) -> None:
    nml_file = conf.nml.file

    if nml_file.exists():
        check_validity(nml_file, conf.nml.template, _MODEL)
    else:
        gen = Confirm.ask(
            Text(f"{nml_file} doesn't exist, generate from template?"),
            default=False,
        )
        if gen:
            generate(
                nml_file,
                conf.nml.template,
                _MODEL,
                keep_advanced=conf.nml.advanced,
            )
