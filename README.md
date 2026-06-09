# prs_bar

シンプルで使いやすいCLIプログレスバーライブラリ。

---

## インストール

```bash
pip install prs_bar
```

---

## クイックスタート

```python
import time
from prs_bar import ProgressBar

with ProgressBar(100, prefix="処理中") as bar:
    for i in range(100):
        time.sleep(0.05)
        bar.update(i + 1)
```

---

## 機能一覧

| クラス / 関数 | 用途 |
|---|---|
| `ProgressBar` | 基本のプログレスバー |
| `track()` | イテラブルを自動ラップ |
| `Spinner` | 不定期処理向けスピナー |
| `MultiBar` | 複数バーの同時表示 |
| `BarStyle` | バーの見た目のカスタマイズ |

---

## ProgressBar

### 基本の使い方

```python
import time
from prs_bar import ProgressBar

# with文（推奨）
with ProgressBar(100, prefix="処理中", suffix="完了") as bar:
    for i in range(100):
        time.sleep(0.05)
        bar.update(i + 1)
```

### update() の2通りの使い方

```python
# 絶対値で指定
bar.update(50)       # 50/100 にセット

# ステップ数で指定（省略するとstep=1）
bar.update(step=1)   # 現在値 +1
bar.update(step=5)   # 現在値 +5
```

### 引数一覧

| 引数 | 型 | デフォルト | 説明 |
|---|---|---|---|
| `total` | int | 必須 | 合計値 |
| `prefix` | str | `"Progress"` | バー左側のラベル |
| `suffix` | str | `"Complete"` | バー右側のラベル |
| `style` | BarStyle | `BarStyle.classic()` | バーのスタイル |
| `color` | str | `None` | バーの色 |
| `show_elapsed` | bool | `False` | 経過時間を表示 |
| `show_eta` | bool | `False` | 残り時間を表示 |

### 経過時間・残り時間の表示

```python
with ProgressBar(100, prefix="ダウンロード", show_elapsed=True, show_eta=True) as bar:
    for i in range(100):
        time.sleep(0.05)
        bar.update(i + 1)
# → ダウンロード: |████░░░░| 40.0% [40/100] Complete 経過:2.0s 残り:3.0s
```

---

## track()

イテラブル（リストなど）をそのままループに渡すだけで自動的にプログレスバーが表示される。

```python
import time
from prs_bar import track

items = list(range(100))

for item in track(items, prefix="処理中", color="green"):
    time.sleep(0.05)
```

### 引数一覧

| 引数 | 型 | デフォルト | 説明 |
|---|---|---|---|
| `iterable` | Iterable | 必須 | ループ対象 |
| `total` | int | `None` | 合計値（省略時は自動取得） |
| `prefix` | str | `"Progress"` | バー左側のラベル |
| `suffix` | str | `"Complete"` | バー右側のラベル |
| `style` | BarStyle | `BarStyle.classic()` | バーのスタイル |
| `color` | str | `None` | バーの色 |
| `show_elapsed` | bool | `False` | 経過時間を表示 |
| `show_eta` | bool | `False` | 残り時間を表示 |

---

## Spinner

処理の完了タイミングが読めない場合に使うアニメーションスピナー。
`with` ブロックを抜けると自動で止まる。例外が発生した場合は「✗ 失敗」と表示される。

```python
import time
from prs_bar import Spinner

with Spinner("データを取得中", style="dots", color="cyan"):
    time.sleep(3)
# → ✓ 完了
```

### 引数一覧

| 引数 | 型 | デフォルト | 説明 |
|---|---|---|---|
| `message` | str | `"処理中"` | スピナー右側のメッセージ |
| `style` | str | `"classic"` | スピナーのスタイル名 |
| `interval` | float | `0.1` | フレームの切り替え速度（秒） |
| `color` | str | `None` | スピナーの色 |
| `done_message` | str | `"✓ 完了"` | 完了時に表示するメッセージ |

### スピナースタイル一覧

| スタイル名 | フレーム例 |
|---|---|
| `classic` | `| / - \` |
| `dots` | `⠋ ⠙ ⠹ ⠸ ⠼ ⠴ ⠦ ⠧ ⠇ ⠏` |
| `circle` | `◐ ◓ ◑ ◒` |
| `bounce` | `⠁ ⠂ ⠄ ⠂` |
| `arrow` | `← ↖ ↑ ↗ → ↘ ↓ ↙` |
| `braille` | `⣾ ⣽ ⣻ ⢿ ⡿ ⣟ ⣯ ⣷` |

---

## MultiBar

複数のプログレスバーを同時に表示する。

```python
import time
from prs_bar import MultiBar

with MultiBar() as mb:
    bar_a = mb.add(100, prefix="ダウンロード", color="cyan")
    bar_b = mb.add(100, prefix="変換中",       color="green")
    bar_c = mb.add(100, prefix="アップロード", color="yellow")

    for i in range(100):
        bar_a.update(step=1)
        bar_b.update(step=1)
        bar_c.update(step=1)
        time.sleep(0.05)
```

### mb.add() の引数一覧

| 引数 | 型 | デフォルト | 説明 |
|---|---|---|---|
| `total` | int | 必須 | 合計値 |
| `prefix` | str | `"Progress"` | バー左側のラベル |
| `suffix` | str | `"Complete"` | バー右側のラベル |
| `style` | BarStyle | `BarStyle.classic()` | バーのスタイル |
| `color` | str | `None` | バーの色 |

---

## BarStyle

バーの見た目を変えるスタイルクラス。プリセットを使うか、自分でカスタムできる。

### プリセット一覧

| 名前 | 表示例 |
|---|---|
| `BarStyle.classic()` | `|████░░░░|` |
| `BarStyle.smooth()` | `|▓▓▓▓────|` |
| `BarStyle.ascii()` | `[####----]` |
| `BarStyle.minimal()` | `[====    ]` |
| `BarStyle.arrow()` | `[===>    ]` |
| `BarStyle.dots()` | `|●●●○○○|` |
| `BarStyle.blocks()` | `|■■■□□□|` |

```python
from prs_bar import ProgressBar, BarStyle

with ProgressBar(100, style=BarStyle.arrow(), color="green") as bar:
    ...
```

### カスタムスタイル

```python
from prs_bar import BarStyle

my_style = BarStyle(
    fill="▶",
    empty="─",
    left_cap="(",
    right_cap=")",
    length=30,
)
```

| 引数 | 型 | デフォルト | 説明 |
|---|---|---|---|
| `fill` | str | `"█"` | 塗りつぶし文字 |
| `empty` | str | `"░"` | 未完了文字 |
| `left_cap` | str | `"|"` | バー左端の文字 |
| `right_cap` | str | `"|"` | バー右端の文字 |
| `length` | int | `40` | バーの長さ（文字数） |

---

## カラー一覧

`color` 引数に以下の文字列を渡す。

| 名前 | 色 |
|---|---|
| `"red"` | 赤 |
| `"green"` | 緑 |
| `"yellow"` | 黄 |
| `"blue"` | 青 |
| `"magenta"` | マゼンタ |
| `"cyan"` | シアン |
| `"white"` | 白 |
| `"bright_green"` | 明るい緑 |
| `"bright_cyan"` | 明るいシアン |

---

## ファイル構成

```
prs_bar_library/
├── setup.py
├── pyproject.toml
└── prs_bar/
    ├── __init__.py       # 全クラスをまとめてエクスポート
    ├── style.py          # BarStyle・カラー・スピナーフレーム定義
    ├── progressbar.py    # ProgressBar クラス
    ├── track.py          # track() 関数
    ├── spinner.py        # Spinner クラス
    └── multibar.py       # MultiBar クラス
```

---

## import まとめ

```python
from prs_bar import ProgressBar   # 基本バー
from prs_bar import track          # イテラブル自動ラップ
from prs_bar import Spinner        # スピナー
from prs_bar import MultiBar       # 複数バー同時表示
from prs_bar import BarStyle       # スタイル指定
```