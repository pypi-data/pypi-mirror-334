from __future__ import annotations

import subprocess
import typing
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path

from rich.text import Text

from .term import BlackHole, TermBase, err_txt

if typing.TYPE_CHECKING:
    from typing import Iterable, Sequence

    from .dirs import TestsOutputDirectory


@dataclass(frozen=True)
class Target:
    name: str


@dataclass(frozen=True)
class BuildOutcome:
    """Result from calling CmakeBuilder.build_targets."""

    built_targets: frozenset[Target]
    all_successful: bool
    build_path: Path

    def target_path(self, target: Target) -> Path:
        return self.build_path / target.name


@dataclass(frozen=True)
class CmakeBuilder:
    """Build binaries for tests using CMake.

    music_dir: the root of the music repository.
    """

    music_dir: Path
    outdir: TestsOutputDirectory
    external_build: Path | None

    @cached_property
    def build_path(self) -> Path:
        if self.external_build is not None:
            cache = self.external_build / "CMakeCache.txt"
            if not cache.is_file():
                raise RuntimeError(
                    f"Cannot reuse {self.external_build}: not a CMake build directory"
                )
            return self.external_build
        return self.outdir.default_build_path

    def target_tags(self, target: Target) -> Sequence[str]:
        """Tags related to build options."""
        return (target.name,)

    def _configure(self, *, output_to: TermBase, indent: int) -> bool:
        config_log = self.outdir.logs_directory / "config_cmake.log"
        with config_log.open("w") as clog:
            config_process = subprocess.run(
                [
                    "cmake",
                    "-S",
                    self.music_dir,
                    "-B",
                    self.build_path,
                ],
                stdout=clog,
                stderr=clog,
            )
        if config_process.returncode == 0:
            return True
        else:
            output_to.print(
                err_txt(
                    "Configuration failed",
                    f"See log in {config_log}",
                ),
                indent,
            )
            return False

    def build_targets(
        self,
        targets: Iterable[Target],
        *,
        output_to: TermBase | None = None,
        indent: int = 0,
    ) -> BuildOutcome:
        """Build test targets."""
        output_to = output_to if output_to is not None else BlackHole()

        build_dir = self.build_path
        build_dir.mkdir(exist_ok=True)

        output_to.print(Text(f"Configuring build directory {build_dir}"), indent)
        config_success = self._configure(output_to=output_to, indent=indent + 1)
        if not config_success:
            return BuildOutcome(frozenset(), False, build_dir)

        targets = set(targets)
        ntargets = len(targets)
        build_success = True
        built_targets: list[Target] = []

        for itgt, tgt in enumerate(targets, 1):
            output_to.print(
                Text(f"Building target {itgt}/{ntargets} ({tgt.name})"),
                indent + 1,
            )
            build_log = self.outdir.logs_directory / f"build_{tgt.name}.log"
            with build_log.open("w") as blog:
                bld_process = subprocess.run(
                    [
                        "cmake",
                        "--build",
                        build_dir,
                        "--target",
                        tgt.name,
                        "--parallel",
                    ],
                    stdout=blog,
                    stderr=blog,
                )
            if bld_process.returncode == 0:
                built_targets.append(tgt)
            else:
                build_success = False
                output_to.print(
                    err_txt(
                        f"Build of target `{tgt.name}` failed",
                        f"See log in {build_log}",
                    ),
                    indent + 1,
                )
        return BuildOutcome(frozenset(built_targets), build_success, build_dir)
