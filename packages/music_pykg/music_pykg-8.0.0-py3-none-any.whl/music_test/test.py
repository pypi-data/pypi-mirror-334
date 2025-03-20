from __future__ import annotations

import typing
from dataclasses import dataclass, field

from .runs import CmdRun, NoOpCmd

if typing.TYPE_CHECKING:
    from pathlib import Path
    from typing import Callable, Iterable, Mapping

    from .cmake_builder import Target
    from .comparison_checks import ComparisonCheck
    from .runs import Run
    from .self_checks import SelfCheck


@dataclass(frozen=True)
class Test:
    """A test to run"""

    preparation: Callable[[Path], None] | None
    run: Run | None
    self_check: SelfCheck | None
    comparison_check: ComparisonCheck | None
    description: str
    tags: tuple[str, ...]
    depends_on: Mapping[str, Test] = field(default_factory=dict)

    def with_paths(
        self, rel_run_path: Path, config_dir: Path
    ) -> Iterable[ConcreteTest]:
        dep_paths = []
        for dep_name, dep_test in self.depends_on.items():
            if not dep_name.isidentifier():
                raise ValueError(f"dependent test has invalid ID: {dep_name}")
            dep_rel_path = rel_run_path / dep_name
            dep_paths.append(dep_rel_path)
            yield from dep_test.with_paths(
                rel_run_path=dep_rel_path, config_dir=config_dir
            )

        yield ConcreteTest(
            preparation=self.preparation,
            run=self.run if self.run is not None else CmdRun(NoOpCmd()),
            self_check=self.self_check,
            comparison_check=self.comparison_check,
            description=self.description,
            tags=self.tags,
            depends_on=tuple(dep_paths),
            rel_run_path=rel_run_path,
            config_dir=config_dir,
        )


@dataclass(frozen=True)
class ConcreteTest:
    preparation: Callable[[Path], None] | None
    run: Run
    self_check: SelfCheck | None
    comparison_check: ComparisonCheck | None
    description: str
    tags: tuple[str, ...]
    depends_on: tuple[Path, ...]
    rel_run_path: Path
    config_dir: Path

    def build_targets(self) -> frozenset[Target]:
        return frozenset(self.run.build_targets())

    def setup_dir_for_run(self, dst_path: Path) -> None:
        """Setup given path for this test's run"""
        if self.preparation is not None:
            self.preparation(dst_path)
        self.run.setup_run_dir(dst_path)
