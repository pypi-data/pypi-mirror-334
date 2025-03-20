from __future__ import annotations

from dataclasses import dataclass

from rich.console import Group, RenderableType
from rich.padding import Padding


def _combine_msgs(*messages: RenderableType | None) -> RenderableType | None:
    non_empty = list(msg for msg in messages if msg is not None)
    if len(non_empty) == 1:
        return non_empty[0]
    elif non_empty:
        return Group(*non_empty)
    else:
        return None


@dataclass(frozen=True)
class ValidationResult:
    is_success: bool
    message: RenderableType | None = None

    def __and__(self, other: ValidationResult) -> ValidationResult:
        assert isinstance(other, ValidationResult)
        return ValidationResult(
            self.is_success and other.is_success,
            message=_combine_msgs(self.message, other.message),
        )

    def __or__(self, other: ValidationResult) -> ValidationResult:
        assert isinstance(other, ValidationResult)
        return ValidationResult(
            self.is_success or other.is_success,
            message=_combine_msgs(self.message, other.message),
        )

    def with_header_msg(self, header_msg: RenderableType) -> ValidationResult:
        if self.message is None:
            msg = None
        else:
            msg = Group(header_msg, Padding.indent(self.message, 2))
        return ValidationResult(self.is_success, msg)
