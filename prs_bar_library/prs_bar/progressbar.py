
from __future__ import annotations

import sys
import time

from .style import BarStyle, COLORS, colorize


class ProgressBar:

    def __init__(
        self,
        total: int,
        *,
        prefix: str = "Progress",
        suffix: str = "Complete",
        style: BarStyle | None = None,
        color: str | None = None,
        show_elapsed: bool = False,
        show_eta: bool = False,
        file=None,
    ) -> None:
        self.total = total
        self.prefix = prefix
        self.suffix = suffix
        self.style = style or BarStyle.classic()
        self.color = color
        self.show_elapsed = show_elapsed
        self.show_eta = show_eta
        self._file = file or sys.stdout
        self._current = 0
        self._start_time = time.time()
        self._closed = False
        self._render(0)

    def _build_bar(self, current: int) -> str:
        s = self.style
        percent = current / self.total if self.total else 0
        filled = int(s.length * percent)

        # arrowスタイルは先端に '>' を付ける
        if s.fill == "=" and s.empty == " ":
            arrow = ">" if filled < s.length else ""
            bar_inner = s.fill * max(filled - 1, 0) + arrow + s.empty * (s.length - filled)
        else:
            bar_inner = s.fill * filled + s.empty * (s.length - filled)

        return colorize(f"{s.left_cap}{bar_inner}{s.right_cap}", self.color)

    def _time_info(self, current: int) -> str:
        elapsed = time.time() - self._start_time
        parts = []
        if self.show_elapsed:
            parts.append(f"経過:{elapsed:.1f}s")
        if self.show_eta and current > 0 and current < self.total:
            eta = elapsed / current * (self.total - current)
            parts.append(f"残り:{eta:.1f}s")
        return " " + " ".join(parts) if parts else ""

    def _render(self, current: int) -> None:
        percent_str = f"{current / self.total * 100 if self.total else 0:5.1f}%"
        bar = self._build_bar(current)
        time_info = self._time_info(current)
        line = f"\r{self.prefix}: {bar} {percent_str} [{current}/{self.total}] {self.suffix}{time_info}"
        self._file.write(line)
        self._file.flush()

    def update(self, current: int | None = None, *, step: int = 1) -> None:

        if self._closed:
            return
        if current is not None:
            self._current = current
        else:
            self._current += step
        self._current = min(self._current, self.total)
        self._render(self._current)

    def close(self) -> None:
        """バーを完了状態にして改行する。"""
        if not self._closed:
            self._render(self.total)
            self._file.write("\n")
            self._file.flush()
            self._closed = True

    def __enter__(self) -> "ProgressBar":
        return self

    def __exit__(self, *_) -> None:
        self.close()