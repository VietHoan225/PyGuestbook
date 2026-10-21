"""Vẽ biểu đồ cột số lời nhắn theo người gửi bằng matplotlib."""

import matplotlib

matplotlib.use("Agg")  # vẽ ra file, không cần màn hình

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# Màu theo giao diện sáng / tối của trang
THEMES = {
    "light": {
        "surface": "#fcfcfb",
        "bar": "#2a78d6",
        "text": "#0b0b0b",
        "muted": "#52514e",
        "grid": "#e4e3df",
    },
    "dark": {
        "surface": "#1a1a19",
        "bar": "#3987e5",
        "text": "#f0efec",
        "muted": "#c3c2b7",
        "grid": "#383835",
    },
}

MAX_LABEL_LEN = 12


def _short(name):
    return name if len(name) <= MAX_LABEL_LEN else name[: MAX_LABEL_LEN - 1] + "…"


def draw_sender_chart(rows, path, theme="light"):
    """rows: list dict {name, total}, đã sắp xếp giảm dần."""
    colors = THEMES[theme]
    names = [_short(r["name"]) for r in rows]
    totals = [r["total"] for r in rows]

    width = min(max(6.0, 0.75 * len(rows) + 2), 14.0)
    fig, ax = plt.subplots(figsize=(width, 4.2), dpi=144)
    fig.patch.set_facecolor(colors["surface"])
    ax.set_facecolor(colors["surface"])

    bars = ax.bar(names, totals, width=0.55, color=colors["bar"], zorder=3)
    ax.bar_label(bars, padding=4, color=colors["text"], fontsize=10)

    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_ylim(0, max(totals) * 1.18)
    ax.grid(axis="y", color=colors["grid"], linewidth=0.8, zorder=0)
    ax.set_ylabel("Số lời nhắn", color=colors["muted"], fontsize=10)

    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(colors["grid"])
    ax.tick_params(colors=colors["muted"], labelsize=10, length=0, pad=6)

    if len(rows) > 6:
        plt.setp(ax.get_xticklabels(), rotation=30, ha="right")

    fig.tight_layout()
    fig.savefig(path, facecolor=colors["surface"])
    plt.close(fig)
