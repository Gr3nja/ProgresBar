
from __future__ import annotations

from typing import Iterable, Iterator, TypeVar

from .style import BarStyle
from .progressbar import ProgressBar

T = TypeVar("T")


def track(
    iterable: Iterable[T],
    *,
    total: int | None = None,
    prefix: str = "Progress",
    suffix: str = "Complete",
    style: BarStyle | None = None,
    color: str | None = None,
    show_elapsed: bool = False,
    show_eta: bool = False,
) -> Iterator[T]:

    items = list(iterable)
    n = total if total is not None else len(items)
    bar = ProgressBar(
        n,
        prefix=prefix,
        suffix=suffix,
        style=style,
        color=color,
        show_elapsed=show_elapsed,
        show_eta=show_eta,
    )
    try:
        for i, item in enumerate(items, 1):
            yield item
            bar.update(i)
    finally:
        bar.close()