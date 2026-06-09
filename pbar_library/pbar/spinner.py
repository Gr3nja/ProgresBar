
from __future__ import annotations

import sys
import time
import threading

from .style import SPINNER_STYLES, colorize


class Spinner:

    def __init__(
        self,
        message: str = "処理中",
        *,
        style: str = "classic",
        interval: float = 0.1,
        color: str | None = None,
        done_message: str = "✓ 完了",
        file=None,
    ) -> None:
        self.message = message
        self._frames = SPINNER_STYLES.get(style, SPINNER_STYLES["classic"])
        self._interval = interval
        self._color = color
        self._done_message = done_message
        self._file = file or sys.stdout
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def _spin(self) -> None:
        idx = 0
        while not self._stop_event.is_set():
            frame = colorize(self._frames[idx % len(self._frames)], self._color)
            self._file.write(f"\r{frame} {self.message}")
            self._file.flush()
            idx += 1
            time.sleep(self._interval)

    def start(self) -> "Spinner":
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._spin, daemon=True)
        self._thread.start()
        return self

    def stop(self, success: bool = True) -> None:
        self._stop_event.set()
        if self._thread:
            self._thread.join()
        icon = colorize(self._done_message if success else "✗ 失敗", self._color)
        self._file.write(f"\r{icon}          \n")
        self._file.flush()

    def __enter__(self) -> "Spinner":
        return self.start()

    def __exit__(self, exc_type, *_) -> None:
        self.stop(success=exc_type is None)