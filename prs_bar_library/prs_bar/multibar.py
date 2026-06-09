
from __future__ import annotations

import sys
from dataclasses import dataclass, field

from .style import BarStyle, COLORS, colorize


class MultiBar:

    def __init__(self, file=None) -> None:
        self._file = file or sys.stdout
        self._bars: list[_MultiBarItem] = []

    def add(
        self,
        total: int,
        *,
        prefix: str = "Progress",
        suffix: str = "Complete",
        style: BarStyle | None = None,
        color: str | None = None,
    ) -> "_MultiBarItem":
        item = _MultiBarItem(
            total=total,
            prefix=prefix,
            suffix=suffix,
            style=style or BarStyle.classic(),
            color=color,
            index=len(self._bars),
            parent=self,
        )
        self._bars.append(item)
        self._file.write("\n")  # 各バー用の行を確保
        self._file.flush()
        return item

    def _render_all(self) -> None:
        n = len(self._bars)
        self._file.write(f"\033[{n}A")  # カーソルをn行上へ
        for item in self._bars:
            bar = item._build_bar()
            pct = f"{item._current / item.total * 100:5.1f}%"
            color_code = COLORS.get(item.color or "", "")
            reset = COLORS["reset"] if item.color else ""
            line = (
                f"\r{color_code}{item.prefix}: {bar} {pct}"
                f" [{item._current}/{item.total}] {item.suffix}{reset}\n"
            )
            self._file.write(line)
        self._file.flush()

    def __enter__(self) -> "MultiBar":
        return self

    def __exit__(self, *_) -> None:
        pass


@dataclass
class _MultiBarItem:
    total:  int
    prefix: str
    suffix: str
    style:  BarStyle
    color:  str | None
    index:  int
    parent: "MultiBar"
    _current: int = field(default=0, init=False)

    def _build_bar(self) -> str:
        s = self.style
        percent = self._current / self.total if self.total else 0
        filled = int(s.length * percent)
        bar_inner = s.fill * filled + s.empty * (s.length - filled)
        return f"{s.left_cap}{bar_inner}{s.right_cap}"

    def update(self, current: int | None = None, *, step: int = 1) -> None:
        if current is not None:
            self._current = min(current, self.total)
        else:
            self._current = min(self._current + step, self.total)
        self.parent._render_all()