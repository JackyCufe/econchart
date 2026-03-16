"""
箱线图模块。
支持多组数据对比，符合期刊出版规范。
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


def plot_boxplot(
    data: pd.DataFrame,
    y_cols: list[str],
    group_col: Optional[str] = None,
    show_outliers: bool = True,
    theme: JournalTheme = THEMES["通用学术"],
    title: str = "",
    ylabel: str = "",
) -> plt.Figure:
    """
    绘制箱线图。

    Args:
        data:          输入 DataFrame
        y_cols:        要绘制的数值列名列表
        group_col:     分组列名（可选，若提供则按组绘制）
        show_outliers: 是否显示离群点
        theme:         期刊主题
        title:         图标题
        ylabel:        Y 轴标签

    Returns:
        matplotlib Figure
    """
    missing = [c for c in y_cols if c not in data.columns]
    if missing:
        raise ValueError(f"数据中缺少列：{missing}")

    fig, ax = plt.subplots(figsize=(theme.fig_width, theme.fig_height))

    flier_props = dict(
        marker="o",
        markersize=3,
        linestyle="none",
        alpha=0.5,
    )

    if group_col and group_col in data.columns and len(y_cols) == 1:
        y_col = y_cols[0]
        groups = sorted(data[group_col].unique())
        plot_data = [data.loc[data[group_col] == g, y_col].dropna().values for g in groups]
        labels = [str(g) for g in groups]
    else:
        plot_data = [data[c].dropna().values for c in y_cols]
        labels = y_cols

    bp = ax.boxplot(
        plot_data,
        tick_labels=labels,
        patch_artist=True,
        showfliers=show_outliers,
        flierprops=flier_props,
        medianprops=dict(color="black", linewidth=1.5),
        whiskerprops=dict(linewidth=1.2),
        capprops=dict(linewidth=1.2),
    )

    for i, patch in enumerate(bp["boxes"]):
        color = theme.colors[i % len(theme.colors)]
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

        if show_outliers and i < len(bp["fliers"]):
            bp["fliers"][i].set_markerfacecolor(color)
            bp["fliers"][i].set_markeredgecolor(color)

    ax.set_xticklabels(labels, fontsize=theme.font_size_tick, rotation=15, ha="right")
    ax.set_ylabel(ylabel or (y_cols[0] if len(y_cols) == 1 else ""), fontsize=theme.font_size_label)
    if title:
        ax.set_title(title, fontsize=theme.font_size_title, fontweight="bold", pad=10)

    _apply_theme(ax, theme)
    ax.grid(axis="y", linestyle=":", alpha=0.4)
    fig.tight_layout()
    return fig
