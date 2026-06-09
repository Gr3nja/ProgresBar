"""
prs_bar ライブラリのデモスクリプト
"""
import sys
import time

sys.path.insert(0, ".")

from prs_bar import ProgressBar, BarStyle, Spinner, MultiBar, track

TOTAL = 40
SLEEP = 0.03


def demo_basic():
    print("━━ デモ1: 基本的な使い方 (ProgressBar) ━━")
    with ProgressBar(TOTAL, prefix="基本", suffix="完了") as bar:
        for i in range(TOTAL):
            time.sleep(SLEEP)
            bar.update(i + 1)


def demo_styles():
    print("\n━━ デモ2: スタイルプリセット ━━")
    styles = [
        ("classic",  BarStyle.classic(),  None),
        ("smooth",   BarStyle.smooth(),   "cyan"),
        ("ascii",    BarStyle.ascii(),    "yellow"),
        ("minimal",  BarStyle.minimal(),  "green"),
        ("arrow",    BarStyle.arrow(),    "magenta"),
        ("dots",     BarStyle.dots(),     "blue"),
        ("blocks",   BarStyle.blocks(),   "red"),
    ]
    for name, style, color in styles:
        with ProgressBar(TOTAL, prefix=f"{name:8}", suffix="", style=style, color=color) as bar:
            for i in range(TOTAL):
                time.sleep(SLEEP // 2)
                bar.update(i + 1)


def demo_time_info():
    print("\n━━ デモ3: 経過時間・ETA表示 ━━")
    with ProgressBar(
        TOTAL,
        prefix="ダウンロード",
        suffix="",
        style=BarStyle.smooth(),
        color="bright_cyan",
        show_elapsed=True,
        show_eta=True,
    ) as bar:
        for i in range(TOTAL):
            time.sleep(SLEEP)
            bar.update(i + 1)


def demo_track():
    print("\n━━ デモ4: track() ━━")
    data = list(range(TOTAL))
    result = []
    for item in track(data, prefix="処理中", color="bright_green", show_eta=True):
        time.sleep(SLEEP)
        result.append(item * 2)
    print(f"  処理件数: {len(result)}")


def demo_spinner():
    print("\n━━ デモ5: Spinner ━━")
    for sty in ["classic", "dots", "circle", "braille"]:
        with Spinner(f"スタイル [{sty}] で処理中", style=sty, color="cyan", interval=0.08):
            time.sleep(1.2)


def demo_step():
    print("\n━━ デモ6: step指定での更新 ━━")
    bar = ProgressBar(TOTAL, prefix="step更新", color="yellow", style=BarStyle.arrow())
    for _ in range(TOTAL):
        time.sleep(SLEEP)
        bar.update(step=1)
    bar.close()


def demo_multibar():
    print("\n━━ デモ7: MultiBar（複数バーの同時表示）━━")
    configs = [
        ("タスクA", "green"),
        ("タスクB", "cyan"),
        ("タスクC", "yellow"),
    ]
    with MultiBar() as mb:
        bars = [mb.add(TOTAL, prefix=name, color=color) for name, color in configs]
        steps = [1, 2, 3]
        while any(b._current < b.total for b in bars):
            for bar, step in zip(bars, steps):
                bar.update(step=step)
            time.sleep(SLEEP * 2)


if __name__ == "__main__":
    demo_basic()
    demo_styles()
    demo_time_info()
    demo_track()
    demo_spinner()
    demo_step()
    demo_multibar()
    print("\n✅ 全デモ完了！")