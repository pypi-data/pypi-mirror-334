#!/usr/bin/env python3

from __future__ import annotations

import itertools
import re
import typing
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from rich import progress

if typing.TYPE_CHECKING:
    from typing import Iterator

    from .cli import CliConfig

AXES_COLS = {
    "wtime": "wtime_hours",
    "time": "time_to",
    "step": "step",
}


@dataclass(frozen=True)
class PerformanceLog:
    log_fname: Path

    @cached_property
    def ncpu(self) -> int:
        re_decomp = re.compile(
            r"^PARALLEL: requested parallel decomposition: \[(\d+), (\d+), (\d+)\] processors$"
        )
        with self.log_fname.open("r") as f:
            for ln in itertools.islice(f, 1000):  # only look in first 1000 lines
                if (m := re_decomp.match(ln)) is not None:
                    return int(m.group(1)) * int(m.group(2)) * int(m.group(3))
        raise ValueError("Could not determine ncpu")

    def _entries(self) -> Iterator[dict]:
        # In order of appearance in time step
        re_step = re.compile(
            r"^TIME_LOOP: begin step: step=(\d+), time_from=(.*), model_from=(\d+)$"
        )
        re_pace = re.compile(
            r"^PERF: sim pace \[sim_time_units/CPU_hour\]: current=(.*), 10min_avg=(.*), 3hour_avg=(.*), sim_time_units/wall_day=(.*)$"
        )
        re_dump = re.compile(r"^IO: dump:.*$")
        re_speedup = re.compile(r"^SOLVER_SPEEDUP.*$")
        re_hbeat = re.compile(r"^PERF: heartbeat: wtime_since_beg_run=(.*)")

        with progress.open(self.log_fname, mode="r", description="reading log...") as f:
            # Store (current, last) for step, time_from, model_from. This is
            # because by the time we see a new (step, time_from, model_from)
            # tuple, we have data pertaining to the step *before* that, so we
            # need memory of the previous step.
            step: tuple[int, int] = (-1, -1)
            time_from: tuple[float, float] = (0.0, 0.0)
            model_from: tuple[int, int] = (0, 0)
            # --
            pace: float = 0.0
            pace_10m: float = 0.0
            pace_3h: float = 0.0
            dumps_done: int = 0
            speedups_done: int = 0
            heartbeat: float = 0.0

            for ln in f:
                if (m := re_step.match(ln)) is not None:
                    step = (int(m.group(1)), step[0])
                    time_from = (float(m.group(2)), time_from[0])
                    model_from = (int(m.group(3)), model_from[0])

                    if step[1] >= 0:
                        yield {
                            "step": step[1],
                            "time_from": time_from[1],
                            "time_to": time_from[0],
                            "model_from": model_from[1],
                            # --
                            "pace": pace,
                            "pace_10m_avg": pace_10m,
                            "pace_3h_avg": pace_3h,
                            "dumps_done": dumps_done,
                            "speedups_done": speedups_done,
                            "heartbeat": heartbeat,
                        }
                    continue
                if (m := re_dump.match(ln)) is not None:
                    dumps_done += 1
                    continue
                if (m := re_speedup.match(ln)) is not None:
                    speedups_done += 1
                    continue
                if (m := re_hbeat.match(ln)) is not None:
                    heartbeat = float(m.group(1))
                    continue
                if (m := re_pace.match(ln)) is not None:
                    pace = float(m.group(1))
                    pace_10m = float(m.group(2))
                    pace_3h = float(m.group(3))
                    continue

    @cached_property
    def dataframe(self) -> pd.DataFrame:
        df = pd.DataFrame(list(self._entries()))

        df["dt"] = df["time_to"] - df["time_from"]
        df["step_cpu_hours"] = df["dt"] / df["pace"]

        if np.any(df["heartbeat"] > 0.0):
            # We have the heartbeat column
            df["wtime_hours"] = df["heartbeat"] / 3600.0
        else:
            # Reconstruct the wall time from pace
            df["wtime_hours"] = np.cumsum(df["step_cpu_hours"]) / self.ncpu

        return df

    @cached_property
    def averaged_pace(self) -> float:
        df = self.dataframe
        return df["dt"].sum() / df["step_cpu_hours"].sum()


def main(conf: CliConfig) -> None:
    if not conf.pace.log_file.is_file():
        print("specify log file with `--log-file`")
        return

    log = PerformanceLog(log_fname=conf.pace.log_file)

    nrows, ncols = 3, len(conf.pace.axes)
    fig, axes = plt.subplots(
        nrows=nrows,
        ncols=ncols,
        sharex="col",
        sharey="row",
        squeeze=False,
        figsize=(10 * ncols, 3 * nrows),
    )

    for icol, index_col in enumerate(AXES_COLS[a] for a in conf.pace.axes):
        axs = iter(axes[:, icol].flatten())
        df = log.dataframe.set_index(index_col)

        # Pace plot
        ax = next(axs)
        ax.set_title(conf.pace.log_file)

        df["pace"].plot(ax=ax)
        df["pace_10m_avg"].plot(ax=ax)
        df["pace_3h_avg"].plot(ax=ax)
        ax.axhline(log.averaged_pace, color="k", ls="--", label="whole run average")
        ax.legend()
        ax.set_ylabel("pace [sim_time_units/CPU_hour]")

        # dt plot
        ax = next(axs)
        df["dt"].plot(ax=ax)
        ax.set_ylabel("dt")

        # Cost of time step plot
        ax = next(axs)
        df["step_cpu_hours"].plot(ax=ax)
        ax.set_ylabel("CPU hours for step")

    fig.tight_layout()
    fig.savefig(conf.pace.output)

    if not conf.pace.no_show:
        plt.show()
