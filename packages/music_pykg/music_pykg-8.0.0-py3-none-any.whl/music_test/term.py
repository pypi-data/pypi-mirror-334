from __future__ import annotations

import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import cached_property
from typing import Sequence, TextIO

from rich.console import Console, RenderableType
from rich.padding import Padding
from rich.text import Text
from rich.theme import Theme


class TermBase(ABC):
    @abstractmethod
    def print(self, obj: RenderableType, indent: int = 0) -> None: ...


class BlackHole(TermBase):
    def print(self, obj: RenderableType, indent: int = 0) -> None:
        pass


@dataclass(frozen=True)
class Term(TermBase):
    stream: TextIO = sys.stdout
    indent_size: int = 2

    @cached_property
    def console(self) -> Console:
        theme = Theme(dict(success="green", warning="yellow", error="red"))
        return Console(file=self.stream, soft_wrap=True, theme=theme)

    def print(self, obj: RenderableType, indent: int = 0) -> None:
        self.console.print(Padding.indent(obj, indent * self.indent_size))


@dataclass(frozen=True)
class TeeTerm(TermBase):
    terms: Sequence[TermBase]

    def print(self, obj: RenderableType, indent: int = 0) -> None:
        for term in self.terms:
            term.print(obj, indent)


def info_txt(*strings: str) -> Text:
    return Text(text="\n".join(strings))


def success_txt(*strings: str) -> Text:
    return Text(text="\n".join(strings), style="success")


def warn_txt(*strings: str) -> Text:
    return Text(text="\n".join(strings), style="warning")


def err_txt(*strings: str) -> Text:
    return Text(text="\n".join(strings), style="error")
