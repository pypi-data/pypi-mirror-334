from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

from loam.base import ConfigBase, Section, entry
from loam.cli import CLIManager, Subcmd
from loam.collections import TupleEntry
from loam.tools import command_flag, path_entry

from . import check_nml, cpu_decomp, pace_plot


@dataclass
class IcStellar(Section):
    """Stellar initial condition."""

    config: Path = path_entry(
        path="ic.toml",
        cli_short="c",
        doc="stellar IC configuration file (generated if doesn't exist)",
    )


@dataclass
class CheckNml(Section):
    """Namelist validation and generation."""

    file: Path = path_entry(
        path="params.nml",
        cli_short="f",
        doc="nml file (generated if doesn't exist)",
    )
    template: str = entry(
        val="main",
        cli_short="t",
        doc=f"which template to validate against/generate, one of {check_nml._MODEL.files()}",
    )
    advanced: bool = command_flag(
        shortname="A",
        doc="also output advanced namelists/options in generated file",
    )


@dataclass
class CpuDecomp(Section):
    """Possible core decompositions of a given grid on commonly used clusters."""

    params: Path = path_entry(
        "params.nml",
        doc="MUSIC namelist to get grid from IC, has no effect if `--ncells` is specified",
        cli_short="P",
    )
    ncells: Tuple[int, ...] = TupleEntry(int).entry(
        (),
        doc="total number of cells along each dimensions (e.g. 512,342,564), supercede `--params`",
        cli_short="c",
    )
    nghosts: int = entry(val=3, doc="number of ghost cells")
    nodes: int = entry(val=5, cli_short="n", doc="max number of nodes")
    platform: str = entry(
        val="",
        cli_short="p",
        doc=f"cluster, leave empty to check all, one of {set(cpu_decomp.CORES_PER_NODE.keys())}",
    )


@dataclass
class Pace(Section):
    """Pace from run log."""

    log_file: Path = path_entry(
        "",
        doc="path of MUSIC run log",
        cli_short="l",
    )
    output: Path = path_entry(
        "pace.pdf",
        doc="path of produced plot",
        cli_short="o",
    )
    axes: Tuple[str, ...] = TupleEntry(str).entry(
        default="wtime",
        doc=f"comma-separated list of axes to plot metrics against, choose from {set(pace_plot.AXES_COLS.keys())}",
        cli_short="a",
    )
    no_show: bool = command_flag(doc="do not show plot interactively", shortname="S")


@dataclass
class CliConfig(ConfigBase):
    ic_stellar: IcStellar
    nml: CheckNml
    cpu: CpuDecomp
    pace: Pace


def main() -> None:
    cli_conf = CliConfig.default_()
    climan = CLIManager(
        config_=cli_conf,
        ics=Subcmd(
            "Generate initial condition for stellar setup.",
            "ic_stellar",
        ),
        nml=Subcmd("Validate/generate namelist file."),
        cpu=Subcmd("CPU decomposition on commonly used clusters."),
        pace=Subcmd("Plot pace from MUSIC run log."),
    )
    args = climan.parse_args()
    match args.loam_sub_name:
        case "ics":
            from . import ic_stellar

            ic_stellar.main(cli_conf)
        case "nml":
            check_nml.main(cli_conf)
        case "cpu":
            cpu_decomp.main(cli_conf)
        case "pace":
            pace_plot.main(cli_conf)
        case _:
            print("See musicsim -h for usage")
