from __future__ import annotations

import typing
from dataclasses import dataclass
from pathlib import Path

from music_pykg.gravity import GravityFile
from rich.text import Text

from .comparison_checks import ComparisonCheck, _DictComparison

if typing.TYPE_CHECKING:
    from .validation import ValidationResult


@dataclass(frozen=True)
class CompareGravityProfile(ComparisonCheck):
    gravity_file: str
    atol: float = 1e-13
    rtol: float = 1e-13

    def compare_run_to_ref(
        self, music_dir: Path, run_dir: Path, ref_dir: Path
    ) -> ValidationResult:
        grav_run = GravityFile(run_dir / self.gravity_file)
        grav_ref = GravityFile(ref_dir / self.gravity_file)

        result = _DictComparison(self.atol, self.rtol).approx_equal(
            {"grav": grav_run.data}, {"grav": grav_ref.data}
        )
        return result.with_header_msg(
            Text(f"CompareGravityProfiles: run='{grav_run.path}' ref='{grav_ref.path}'")
        )
