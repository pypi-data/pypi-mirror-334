from __future__ import annotations

import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass

from music_pykg.namelist import MusicNamelist

from .cmake_builder import Target

if typing.TYPE_CHECKING:
    from os import PathLike
    from pathlib import Path
    from typing import Iterable, Sequence, TypeAlias

    from .cli import CommandHooks
    from .namelist import NmlFile
    from .utils import RelativePath

    FinalPathSegment: TypeAlias = str | PathLike | RelativePath


class Command(ABC):
    @abstractmethod
    def required_targets(self) -> Iterable[Target]:
        """Targets required for this command."""

    @abstractmethod
    def build(self, hooks: CommandHooks) -> Sequence[str]:
        """The command itself."""


class NoOpCmd(Command):
    def required_targets(self) -> Iterable[Target]:
        return ()

    def build(self, hooks: CommandHooks) -> Sequence[str]:
        return ("true",)


@dataclass(frozen=True)
class BareCmd(Command):
    exe: Target
    args: Sequence[str] = ()

    def required_targets(self) -> Iterable[Target]:
        yield self.exe

    def build(self, hooks: CommandHooks) -> Sequence[str]:
        return f"./{self.exe.name}", *self.args


@dataclass(frozen=True)
class MpiCmd(Command):
    nprocs: int
    cmd: Command

    def required_targets(self) -> Iterable[Target]:
        return self.cmd.required_targets()

    def build(self, hooks: CommandHooks) -> Sequence[str]:
        mpi_exec = map(lambda s: s.format(ntasks=self.nprocs), hooks.mpi_exec)
        return *mpi_exec, *self.cmd.build(hooks)


class Run(ABC):
    @property
    def log_filename(self) -> str:
        return "run.log"

    @abstractmethod
    def command(self, run_path: Path, hooks: CommandHooks) -> Command:
        """Command to run."""

    @abstractmethod
    def build_targets(self) -> Iterable[Target]:
        """Required build targets for the run."""

    def setup_run_dir(self, run_dir: Path) -> None:
        """Prepare the run directory.

        This hook is called right before executing the run, and after files
        from the test directory have been copied over to the run directory.
        This is useful to create files dynamically right before the run.
        """

    def auto_tags(self, path: Path) -> Sequence[str]:
        """Return a sequence of automatic tags determined from the run properties."""
        return ()


@dataclass(frozen=True)
class CmdRun(Run):
    cmd: Command

    def build_targets(self) -> Iterable[Target]:
        return self.cmd.required_targets()

    def command(self, run_path: Path, hooks: CommandHooks) -> Command:
        return self.cmd


@dataclass(frozen=True)
class CmakeTargetRun(Run):
    target_name: str
    args: tuple[str, ...]
    nprocs: int

    @property
    def target(self) -> Target:
        return Target(name=self.target_name)

    def build_targets(self) -> Iterable[Target]:
        yield self.target

    def command(self, run_path: Path, hooks: CommandHooks) -> Command:
        return MpiCmd(
            nprocs=self.nprocs,
            cmd=BareCmd(
                exe=self.target,
                args=self.args,
            ),
        )


@dataclass(frozen=True)
class MusicRun(Run):
    """A (serial or parallel) run of MUSIC.

    The number of cores to run on is obtained from the namelist.
    """

    namelist: NmlFile

    def nml_in(self, path: Path) -> MusicNamelist:
        return self.namelist.read_in(path)

    @property
    def target(self) -> Target:
        return Target(name="music")

    def build_targets(self) -> Iterable[Target]:
        yield self.target

    def command(self, run_path: Path, hooks: CommandHooks) -> Command:
        nml_file = str(self.namelist.path_in(run_path).relative_to(run_path))
        args = [nml_file]
        if not hooks.with_music_self_tests:
            args.append("--skip-self-tests")
        return MpiCmd(
            nprocs=self.nml_in(run_path).num_procs,
            cmd=BareCmd(exe=self.target, args=args),
        )

    def setup_run_dir(self, dst_path: Path) -> None:
        self.namelist.ensure_present_in(dst_path)
        # Create directory for output files; important otherwise MUSIC crashes weirdly
        output = self.nml_in(dst_path).get("io", "dataoutput", "")
        if "/" in output:
            output_dir = output.rsplit("/", 1)[0]
            (dst_path / output_dir).mkdir(exist_ok=True, parents=True)

    def auto_tags(self, path: Path) -> Sequence[str]:
        namelist = self.nml_in(path)

        ndim = namelist.get("dims", "ndim", 2)
        nmom = namelist.get("dims", "nmom", 2)
        if ndim == 2 and nmom == 2:
            dim_tag = "2D"
        elif ndim == 3 and nmom == 3:
            dim_tag = "3D"
        else:
            dim_tag = "2_5D"

        tags = [
            "serial" if namelist.num_procs == 1 else "parallel",
            namelist.eos + "_eos",
            dim_tag,
        ]

        tags.extend(
            tag
            for predicate, tag in (
                (namelist.nscalars > 0, "scalars"),
                (namelist.nactive_scalars > 0, "activescalars"),
                (namelist.has_rotation, "rot"),
                (namelist.mhd_enabled, "mhd"),
                (namelist.precond == "si", "pbp"),
            )
            if predicate
        )

        tags.append("gravity_" + namelist.gravity_type)
        tags.append("solver_" + namelist.solver)

        return tags
