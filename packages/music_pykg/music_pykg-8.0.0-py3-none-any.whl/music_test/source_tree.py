from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

from .utils import check_call_tee


class Repository(ABC):
    """A repository that can report its current HEAD and the diff to it."""

    @abstractmethod
    def report_head_into(self, filename: Path) -> None:
        """Print the current HEAD commit in the given file."""

    @abstractmethod
    def report_diff_into(self, filename: Path) -> None:
        """Print the diff to the current HEAD."""


@dataclass(frozen=True)
class GitRepository(Repository):
    """A git repository at the specified path. Requires the `git` command to be executable."""

    path: Path

    def report_head_into(self, head_fname: Path) -> None:
        with open(head_fname, "w") as head_file:
            check_call_tee(
                ["git", "log", "-1"],
                head_file,
                also_to_stdout=False,
                cwd=str(self.path),
            )

    def report_diff_into(self, diff_fname: Path) -> None:
        with open(diff_fname, "w") as diff_file:
            check_call_tee(
                ["git", "diff", "HEAD"],
                diff_file,
                also_to_stdout=False,
                cwd=str(self.path),
            )


class NoOpRepository(Repository):
    """A VCS repository that does nothing.
    This is useful for some runtime environments that cannot execute `git` or other VCS commands locally.
    """

    def report_head_into(self, head_fname: Path) -> None:
        pass

    def report_diff_into(self, diff_fname: Path) -> None:
        pass


@dataclass(frozen=True)
class MusicSourceTree:
    path: Path
    vcs_repo: Repository

    def store_vcs_info(self, vcs_head_fname: Path, vcs_diff_fname: Path) -> None:
        self.vcs_repo.report_head_into(vcs_head_fname)
        self.vcs_repo.report_diff_into(vcs_diff_fname)
