"""
柱状图模块。
支持分组柱状图、堆叠柱状图、水平柱状图及误差棒。
"""
from __future__ import annotations

import logging
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from core.theme import JournalTheme, THEMES

logger = logging.getLogger(__name__)


def _apply_theme(ax: plt.Axes, theme: JournalTheme) -> None:
    ax.spines["top"].set_visible(theme.spine_top)
    ax.spines["right"].set_visible(theme.spine_right)
    ax.tick_params(labelsize=theme.font_size_tick)


def plot_bar(
    data: pd.DataFrame,
    x_col: str,
    y_cols: list[str],
    stacked: bool = False,
    horizontal: bool = False,
    error_col: Optional[str] = None,
    theme: JournalTheme = THEMES["通用学术"],
    title: str = "",
) -> plt.Figure:
    """
    绘制柱状图（分组 / 堆叠 / 水平）。

    Args:
        data:       输入 DataFrame
        x_col:      X 轴（分类）列名
        y_cols:     Y 轴列名列表，多个时绘制分组/堆叠柱状图
        stacked:    True 时堆叠，False 时分组
        horizontal: True 时水平绘制
        error_col:  误差棒列名（仅单 y_col 时有效）
        theme:      期刊主题
        title:      图标题

    Returns:
        matplotlib Figure
    """
    if x_col not in data.columns:
        raise ValueError(f"数据中缺少列 '{x_col}'")

    missing = [c for c in y_cols if c not in data.columns]
    if missing:
        raise ValueError(f"数据中缺少列：{missing}")

    fig, ax = plt.subplots(figsize=(theme.fig_width, theme.fig_height))

    x_labels = data[x_col].astype(str).values
    x_idx = np.arange(len(x_labels))
    n_groups = len(y_cols)
    bar_width = 0.7 / max(n_groups, 1) if not stacked else 0.6

    bottom = np.zeros(len(x_labels))

    for i, y_col in enumerate(y_cols):
        y_vals = data[y_col].values.astype(float)
        color = theme.colors[i % len(theme.colors)]

        if stacked:
            offset = x_idx
        else:
            offset = x_idx + (i - n_groups / 2 + 0.5) * bar_width

        yerr = data[error_col].values if (error_col and error_col in data.columns and i == 0) else None

        if horizontal:
            ax.barh(
                offset, y_vals, height=bar_width,
                left=bottom if stacked else 0,
                color=color, label=y_col, alpha=0.85,
                xerr=yerr, error_kw={"elinewidth": 1.2, "capsize": 3},
            )
        else:
            ax.bar(
                offset, y_vals, width=bar_width,
                bottom=bottom if stacked else 0,
                color=color, label=y_col, alpha=0.85,
                yerr=yerr, error_kw={"elinewidth": 1.2, "capsize": 3},
            )

        if stacked:
            bottom += y_vals

    if horizontal:
        ax.set_yticks(x_idx)
        ax.set_yticklabels(x_labels, fontsize=theme.font_size_tick)
    else:
        ax.set_xticks(x_idx)
        ax.set_xticklabels(x_labels, fontsize=theme.font_size_tick, rotation=15, ha="right")

    if n_groups > 1 or stacked:
        ax.legend(fontsize=theme.font_size_legend, framealpha=0.8)

    if title:
        ax.set_title(title, fontsize=theme.font_size_title, fontweight="bold", pad=10)

    _apply_theme(ax, theme)
    ax.grid(axis="x" if horizontal else "y", linestyle=":", alpha=0.4)
    fig.tight_layout()
    return fig
