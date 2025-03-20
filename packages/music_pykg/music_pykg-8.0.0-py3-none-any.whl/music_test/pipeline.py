from __future__ import annotations

import filecmp
import shutil
import traceback
import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass
from types import MappingProxyType

from rich import box
from rich.console import RenderableType
from rich.style import Style
from rich.table import Table
from rich.text import Text

from .term import TermBase, err_txt
from .test import ConcreteTest
from .utils import Timer

if typing.TYPE_CHECKING:
    from pathlib import Path
    from typing import Mapping, Sequence

    from .cli import CommandHooks
    from .cmake_builder import BuildOutcome
    from .dirs import TestsOutputDirectory


@dataclass(frozen=True, eq=True)
class Outcome:
    label: str
    symbol: str
    termcolor: str | None
    stops_pipeline: bool
    changed: bool
    is_failure: bool

    @property
    def char(self) -> Text:
        return Text(self.symbol, style=Style(color=self.termcolor))


PASS = Outcome(
    label="Passed",
    symbol="✔",
    termcolor="green",
    stops_pipeline=False,
    changed=True,
    is_failure=False,
)

REUSE = Outcome(
    label="Reused",
    symbol="♻",
    termcolor="blue",
    stops_pipeline=False,
    changed=False,
    is_failure=False,
)

FAIL = Outcome(
    label="Failed",
    symbol="✗",
    termcolor="red",
    stops_pipeline=True,
    changed=True,
    is_failure=True,
)

SKIP = Outcome(
    label="Skipped",
    symbol="⮞",
    termcolor="yellow",
    stops_pipeline=True,
    changed=False,
    is_failure=False,
)

NA = Outcome(
    label="N/A",
    symbol="-",
    termcolor=None,
    stops_pipeline=False,
    changed=False,
    is_failure=False,
)

ALL_OUTCOMES = [PASS, REUSE, FAIL, SKIP, NA]


class TestsTally:
    def __init__(self, tests: Sequence[ConcreteTest], stages: Sequence[str]):
        self.tests = tests
        self.stages = stages

        self._outcomes: dict[Path, dict[str, Outcome]] = {
            t.rel_run_path: {} for t in tests
        }  # outcome[test.rel_run_path][stage]

    def register(self, test: ConcreteTest, stage: str, outcome: Outcome) -> None:
        assert stage in self.stages
        assert stage not in self._outcomes[test.rel_run_path]
        self._outcomes[test.rel_run_path][stage] = outcome

    def _finalize_matrix(self) -> None:
        for test in self.tests:
            for i, stage in enumerate(self.stages):
                if stage not in self._outcomes[test.rel_run_path]:
                    assert i > 0
                    prev_outcome = self._outcomes[test.rel_run_path][self.stages[i - 1]]
                    assert prev_outcome.stops_pipeline
                    self._outcomes[test.rel_run_path][stage] = SKIP

    def outcomes(self) -> Mapping[Path, Mapping[str, Outcome]]:
        return MappingProxyType(self._outcomes)

    def print_report_to(self, term: TermBase, print_key: bool = True) -> None:
        self._finalize_matrix()

        grid = Table(title="Tally", box=box.SIMPLE)
        grid.add_column(Text("Test name"), no_wrap=True)
        for stage in self.stages:
            grid.add_column(Text(stage), justify="center", no_wrap=True)
        for test in self.tests:
            cols = [Text(str(test.rel_run_path))]
            for stage in self.stages:
                cols.append(self._outcomes[test.rel_run_path][stage].char)
            grid.add_row(*cols)
        term.print(grid)

        if print_key:
            term.print("\nKey:")
            for outcome in ALL_OUTCOMES:
                term.print(
                    Text.assemble(outcome.char, Text(f" : {outcome.label}")),
                    indent=1,
                )

    def count_failures(self) -> int:
        """Count number of tests that have at least one failure in their pipeline"""
        self._finalize_matrix()
        return sum(
            any(
                self._outcomes[test.rel_run_path][stage].is_failure
                for stage in self.stages
            )
            for test in self.tests
        )

    @property
    def num_tests(self) -> int:
        return len(self.tests)


@dataclass(frozen=True)
class StageResult:
    outcome: Outcome
    message: RenderableType | None = None
    timing: float | None = None

    @property
    def stops_pipeline(self) -> bool:
        return self.outcome.stops_pipeline

    @property
    def is_failure(self) -> bool:
        return self.outcome.is_failure

    @property
    def changed(self) -> bool:
        return self.outcome.changed

    def log_to(self, term: TermBase, header: str, indent: int = 0) -> None:
        timer_str = f" [{self.timing:.2f} s]" if self.timing is not None else ""
        term.print(
            Text(
                f"{self.outcome.label}{timer_str}: {header}",
                style=Style(color=self.outcome.termcolor),
            ),
            indent,
        )
        if self.message is not None:
            term.print(self.message, indent + 1)


@dataclass(frozen=True)
class PipelineByTest:
    stages: Sequence[PipelineStage]

    def process(self, tests: Sequence[ConcreteTest], term: TermBase) -> TestsTally:
        tally = TestsTally(tests, [stage.describe() for stage in self.stages])
        # Loop over tests
        for test in tests:
            term.print(Text(f"Test={test.rel_run_path}"), indent=1)

            # Loop over stages for this test
            force_downstream_update = False
            for stage in self.stages:
                try:
                    result = stage.execute(
                        test, force_downstream_update, tally.outcomes()
                    )
                except Exception:
                    result = StageResult(
                        FAIL,
                        err_txt(
                            "Unexpected error! The following exception was raised:",
                            *traceback.format_exc().splitlines(),
                        ),
                    )
                force_downstream_update = result.changed
                tally.register(test, stage.describe(), result.outcome)
                result.log_to(
                    term, f"{stage.describe()}({test.rel_run_path})", indent=2
                )
                if result.stops_pipeline:
                    break  # Break from pipeline stage loop

        return tally


class PipelineStage(ABC):
    @abstractmethod
    def describe(self) -> str:
        """Short description of the stage."""

    @abstractmethod
    def execute(
        self,
        test: ConcreteTest,
        force_exec: bool,
        outcomes: Mapping[Path, Mapping[str, Outcome]],
    ) -> StageResult:
        raise NotImplementedError


def _same_file_contents(path1: Path, path2: Path) -> bool:
    return path1.is_file() and path2.is_file() and filecmp.cmp(path1, path2)


@dataclass(frozen=True)
class PrepStage(PipelineStage):
    tests_out_dir: TestsOutputDirectory
    build_outcome: BuildOutcome
    reuse_if_ready: bool

    def describe(self) -> str:
        return "Preparation"

    def _files_out_of_date(self, test: ConcreteTest) -> Sequence[tuple[Path, Path]]:
        # files from the test configuration directory
        required_files = [file for file in test.config_dir.iterdir() if file.is_file()]
        # build targets
        required_files.extend(
            self.build_outcome.target_path(tgt) for tgt in test.build_targets()
        )

        run_path = self.tests_out_dir.run_path(test)
        return [
            (file, out_file)
            for file in required_files
            if not _same_file_contents(file, out_file := run_path / file.name)
        ]

    def execute(
        self,
        test: ConcreteTest,
        force_exec: bool,
        outcomes: Mapping[Path, Mapping[str, Outcome]],
    ) -> StageResult:
        if not test.build_targets() <= self.build_outcome.built_targets:
            return StageResult(FAIL)

        run_path = self.tests_out_dir.run_path(test)
        run_path.mkdir(parents=True, exist_ok=True)

        files_to_copy = self._files_out_of_date(test)
        if self.reuse_if_ready and not files_to_copy:
            return StageResult(REUSE)

        for file1, file2 in files_to_copy:
            shutil.copy(file1, file2)

        # additional setup defined by the test itself
        test.setup_dir_for_run(run_path)

        return StageResult(PASS)


@dataclass(frozen=True)
class RunStage(PipelineStage):
    tests_out_dir: TestsOutputDirectory
    reuse_if_ready: bool
    verbose: bool
    hooks: CommandHooks

    def describe(self) -> str:
        return "Run"

    def execute(
        self,
        test: ConcreteTest,
        force_exec: bool,
        outcomes: Mapping[Path, Mapping[str, Outcome]],
    ) -> StageResult:
        run_dir = self.tests_out_dir.test_run_directory(test)
        attempt_reuse = (not force_exec) and self.reuse_if_ready
        dep_oc = [
            outcomes.get(relpath, {}).get(self.describe(), NA)
            for relpath in test.depends_on
        ]

        if not all(oc in (PASS, REUSE) for oc in dep_oc):
            return StageResult(SKIP)

        if attempt_reuse and run_dir.is_ready() and all(oc == REUSE for oc in dep_oc):
            return StageResult(REUSE)

        return run_dir.run(hooks=self.hooks, verbose=self.verbose)


@dataclass(frozen=True)
class SelfCheckStage(PipelineStage):
    tests_out_dir: TestsOutputDirectory

    def describe(self) -> str:
        return "Self-check"

    def execute(
        self,
        test: ConcreteTest,
        force_exec: bool,
        outcomes: Mapping[Path, Mapping[str, Outcome]],
    ) -> StageResult:
        if test.self_check is None:
            return StageResult(NA)

        timer = Timer()
        run_path = self.tests_out_dir.run_path(test)
        result = test.self_check.check_run(run_path)
        if result.is_success:
            return StageResult(PASS, message=result.message, timing=timer.time())

        return StageResult(FAIL, message=result.message, timing=timer.time())


@dataclass(frozen=True)
class CompareStage(PipelineStage):
    music_dir: Path
    tests_out_dir: TestsOutputDirectory
    ref_dir: TestsOutputDirectory

    def describe(self) -> str:
        return "Comparison"

    def execute(
        self,
        test: ConcreteTest,
        force_exec: bool,
        outcomes: Mapping[Path, Mapping[str, Outcome]],
    ) -> StageResult:
        if test.comparison_check is None:  # Test prescribes no comparison
            return StageResult(NA)

        ref_run_dir = self.ref_dir.test_run_directory(test)
        if not ref_run_dir.is_ready():  # No matching run in ref output dir
            return StageResult(
                SKIP,
                message=Text(
                    f"reference run directory '{ref_run_dir.path}' not found",
                    style="warning",
                ),
            )

        timer = Timer()
        run_path = self.tests_out_dir.run_path(test)
        result = test.comparison_check.compare_run_to_ref(
            self.music_dir, run_path, ref_run_dir.path
        )
        if result.is_success:
            return StageResult(PASS, message=result.message, timing=timer.time())

        return StageResult(FAIL, message=result.message, timing=timer.time())
