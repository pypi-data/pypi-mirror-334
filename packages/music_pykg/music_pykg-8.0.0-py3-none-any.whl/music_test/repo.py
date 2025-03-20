"""Test repository classes"""

from __future__ import annotations

import collections
import fnmatch
import importlib.util as imp
import re
import sys
from abc import ABC, abstractmethod
from contextlib import contextmanager
from dataclasses import dataclass
from functools import lru_cache
from itertools import chain
from pathlib import Path
from typing import Iterable, Iterator, Sequence

from .cmake_builder import CmakeBuilder, Target
from .test import ConcreteTest, Test


class RepoException(Exception):
    """Base exception for repository errors"""


class TestConfigError(RepoException):
    """Error with test configuration"""


class TestRepositoryBase(ABC):
    """Base class for repositories of tests"""

    @property
    @abstractmethod
    def path(self) -> Path:
        """The path of the repository."""

    @abstractmethod
    def tests(self) -> Sequence[ConcreteTest]:
        """Returns the list of tests for this repository"""
        raise NotImplementedError

    @abstractmethod
    def all_tags(self, test: ConcreteTest) -> Sequence[str]:
        """Return set of tags for a given test."""
        raise NotImplementedError

    def targets(self) -> frozenset[Target]:
        """Return collection of targets for the tests of this repository"""
        return frozenset().union(*(test.build_targets() for test in self.tests()))

    def print_tests(self) -> None:
        """Print out a list of this repository's tests to stdout"""
        for test in self.tests():
            print(test.rel_run_path)
            print("   Desc:", test.description)
            print("   Tags:", ", ".join(self.all_tags(test)))
            print()


def _is_valid_test_name(name: object) -> bool:
    if not isinstance(name, str):
        return False

    if name.startswith("."):
        return False

    # allow (non-leading) dots in test name
    return name.replace(".", "_").isidentifier()


@contextmanager
def _without_pycache() -> Iterator[None]:
    previous_value = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        yield
    finally:
        sys.dont_write_bytecode = previous_value


def _all_tests_in(root: Path) -> Iterable[ConcreteTest]:
    for config_fname in root.glob("**/test_config.py"):
        with _without_pycache():
            spec = imp.spec_from_file_location("test_config", config_fname)
            if spec is None or spec.loader is None:
                raise TestConfigError(f"Could not import '{config_fname}")
            mod = imp.module_from_spec(spec)
            sys.modules["test_config"] = mod
            spec.loader.exec_module(mod)

        # two exclusive ways of defining tests
        has_test = hasattr(mod, "test")  # a unique Test
        has_tests = hasattr(mod, "tests")  # a str > Test mapping
        if has_test is has_tests:
            raise TestConfigError(
                f"{config_fname}: exactly one of 'test' and 'tests' should be defined"
            )

        if has_tests:
            for name in mod.tests.keys():
                if not _is_valid_test_name(name):
                    raise TestConfigError(f"{config_fname}: invalid test name {name!r}")

        tests = {".": mod.test} if has_test else mod.tests
        for subdir, test in tests.items():
            parent_dir = config_fname.parent
            name = (parent_dir / str(subdir)).relative_to(root)
            if not isinstance(test, Test):
                raise TestConfigError(
                    "{config_fname}: test '{name}' is not an instance of Test"
                )
            yield from test.with_paths(rel_run_path=name, config_dir=parent_dir)


@dataclass(frozen=True)
class TestRepository(TestRepositoryBase):
    """A repository of tests in the new format, relying on `test_config.py` files
    for test discovery and configuration.

    Tests are defined a subdirectories of `root_dir` that contain a `test_config.py` file.
    A test specification file named `<root_dir>/some/test/test_config.py`
    will define the test named `some/test`.

    Each test specification file must be a valid Python script,
    and is expected to define a variable `test` of the class `Test`,
    which encapsulates all the required information for this test.
    """

    root_dir: Path
    builder: CmakeBuilder

    @property
    def path(self) -> Path:
        """Path to the directory of this repository"""
        return Path(self.root_dir)

    @lru_cache(maxsize=None)
    def all_tags(self, test: ConcreteTest) -> Sequence[str]:
        tags = set(
            chain.from_iterable(
                self.builder.target_tags(tgt) for tgt in test.build_targets()
            )
        )
        tags.update(test.run.auto_tags(test.config_dir), test.tags)

        is_word = re.compile(r"\w+")

        if not all(is_word.fullmatch(tag) for tag in tags):
            raise TestConfigError(f"All tags must be alphanumeric, found {tags}")

        return sorted(tags)

    def tests(self) -> Sequence[ConcreteTest]:
        tests = list(_all_tests_in(self.path))

        # Check that tests have unique relative paths (also their names)
        name_count = collections.Counter(test.rel_run_path for test in tests)
        duplicate_names = [name for (name, count) in name_count.items() if count > 1]
        if duplicate_names:
            raise TestConfigError(
                f"repository {self.path}: tests with duplicate names: {duplicate_names}"
            )
        return tests


@dataclass(frozen=True)
class TestsMatchingPatterns(TestRepositoryBase):
    """
    Select tests from a parent test repository whenever their
    names match any of the provided `fnmatch` (glob-style) patterns.
    """

    repo: TestRepositoryBase
    patterns: Sequence[str]

    @property
    def path(self) -> Path:
        return self.repo.path

    def all_tags(self, test: ConcreteTest) -> Sequence[str]:
        return self.repo.all_tags(test)

    def tests(self) -> Sequence[ConcreteTest]:
        return [
            test
            for test in self.repo.tests()
            if any(
                fnmatch.fnmatch(str(test.rel_run_path), pattern)
                for pattern in self.patterns
            )
        ]


def _tag_matches(tag: str, tag_set: set[str]) -> bool:
    if tag.startswith("~"):
        return tag[1:] not in tag_set
    return tag in tag_set


@dataclass(frozen=True)
class TestsWithAnyTag(TestRepositoryBase):
    """Selects tests matching any of the tags"""

    repo: TestRepositoryBase
    tags: Sequence[str]

    @property
    def path(self) -> Path:
        return self.repo.path

    def all_tags(self, test: ConcreteTest) -> Sequence[str]:
        return self.repo.all_tags(test)

    def tests(self) -> Sequence[ConcreteTest]:
        return [
            test
            for test in self.repo.tests()
            if any(_tag_matches(tag, set(self.all_tags(test))) for tag in self.tags)
        ]


@dataclass(frozen=True)
class TestsWithAllTags(TestRepositoryBase):
    """Selects tests matching all of the tags"""

    repo: TestRepositoryBase
    tags: Sequence[str]

    @property
    def path(self) -> Path:
        return self.repo.path

    def all_tags(self, test: ConcreteTest) -> Sequence[str]:
        return self.repo.all_tags(test)

    def tests(self) -> Sequence[ConcreteTest]:
        # Return tests whose tags are a superset of tag selection
        return [
            test
            for test in self.repo.tests()
            if all(_tag_matches(tag, set(self.all_tags(test))) for tag in self.tags)
        ]
