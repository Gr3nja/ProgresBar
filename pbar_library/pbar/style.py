from __future__ import annotations
from dataclasses import dataclass


# ── ANSI カラーコード ───────────────────────────────────────

COLORS: dict[str, str] = {
    "red":          "\033[31m",
    "green":        "\033[32m",
    "yellow":       "\033[33m",
    "blue":         "\033[34m",
    "magenta":      "\033[35m",
    "cyan":         "\033[36m",
    "white":        "\033[37m",
    "bright_green": "\033[92m",
    "bright_cyan":  "\033[96m",
    "reset":        "\033[0m",
}


def colorize(text: str, color: str | None) -> str:
    """テキストにANSIカラーコードを付ける。"""
    if not color:
        return text
    return f"{COLORS.get(color, '')}{text}{COLORS['reset']}"


# ── スピナーフレーム ────────────────────────────────────────

SPINNER_STYLES: dict[str, list[str]] = {
    "classic": ["|", "/", "-", "\\"],
    "dots":    ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],
    "circle":  ["◐", "◓", "◑", "◒"],
    "bounce":  ["⠁", "⠂", "⠄", "⠂"],
    "arrow":   ["←", "↖", "↑", "↗", "→", "↘", "↓", "↙"],
    "braille": ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"],
}


# ── BarStyle ────────────────────────────────────────────────

@dataclass
class BarStyle:

    fill:      str = "█"
    empty:     str = "░"
    left_cap:  str = "|"
    right_cap: str = "|"
    length:    int = 40

    @classmethod
    def classic(cls) -> "BarStyle":
        return cls(fill="█", empty="░", length=40)

    @classmethod
    def smooth(cls) -> "BarStyle":
        return cls(fill="▓", empty="─", length=40)

    @classmethod
    def ascii(cls) -> "BarStyle":
        return cls(fill="#", empty="-", left_cap="[", right_cap="]", length=40)

    @classmethod
    def minimal(cls) -> "BarStyle":
        return cls(fill="=", empty=" ", left_cap="[", right_cap="]", length=30)

    @classmethod
    def arrow(cls) -> "BarStyle":
        return cls(fill="=", empty=" ", left_cap="[", right_cap="]", length=40)

    @classmethod
    def dots(cls) -> "BarStyle":
        return cls(fill="●", empty="○", length=30)

    @classmethod
    def blocks(cls) -> "BarStyle":
        return cls(fill="■", empty="□", length=30)