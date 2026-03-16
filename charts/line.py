"""
折线图模块。
支持多序列、数据点标记、可选置信区间带。
"""
from __future__ import annotations

import logging

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from core.theme import JournalTheme, THEMES

logger = logging.getLogger(__name__)

MARKER_STYLES = ["o", "s", "^", "D", "v", "P", "X"]


def _apply_theme(ax: plt.Axes, theme: JournalTheme) -> None:
    ax.spines["top"].set_visible(theme.spine_top)
    ax.spines["right"].set_visible(theme.spine_right)
    ax.tick_params(labelsize=theme.font_size_tick)


def _add_confidence_band(
    ax: plt.Axes,
    x: np.ndarray,
    y: np.ndarray,
    color: str,
) -> None:
    """使用移动标准差近似展示波动区间（示意用，实际项目中应使用真实 CI 数据）。"""
    window = max(3, len(y) // 5)
    se = pd.Series(y).rolling(window, center=True, min_periods=1).std().fillna(0).values
    ax.fill_between(x, y - 1.96 * se, y + 1.96 * se, alpha=0.15, color=color)


def plot_line(
    data: pd.DataFrame,
    x_col: str,
    y_cols: list[str],
    add_markers: bool = True,
    add_ci: bool = False,
    theme: JournalTheme = THEMES["通用学术"],
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
) -> plt.Figure:
    """
    绘制折线图（时间序列）。

    Args:
        data:        输入 DataFrame
        x_col:       X 轴列名（时间/分类）
        y_cols:      Y 轴列名列表（多序列）
        add_markers: 是否在数据点添加标记
        add_ci:      是否添加置信区间带（近似）
        theme:       期刊主题
        title:       图标题
        xlabel:      X 轴标签
        ylabel:      Y 轴标签

    Returns:
        matplotlib Figure
    """
    if x_col not in data.columns:
        raise ValueError(f"数据中缺少列 '{x_col}'")

    missing = [c for c in y_cols if c not in data.columns]
    if missing:
        raise ValueError(f"数据中缺少列：{missing}")

    fig, ax = plt.subplots(figsize=(theme.fig_width, theme.fig_height))

    x_vals = data[x_col].values
    try:
        x_numeric = pd.to_numeric(pd.Series(x_vals), errors="coerce").values
        use_numeric = not np.isnan(x_numeric).all()
    except Exception:
        use_numeric = False

    for i, y_col in enumerate(y_cols):
        y_vals = data[y_col].values.astype(float)
        color = theme.colors[i % len(theme.colors)]
        marker = MARKER_STYLES[i % len(MARKER_STYLES)] if add_markers else None

        plot_x = x_numeric if use_numeric else np.arange(len(x_vals))
        ax.plot(
            plot_x, y_vals,
            color=color,
            marker=marker,
            markersize=5,
            linewidth=1.8,
            label=y_col,
        )

        if add_ci:
            _add_confidence_band(ax, plot_x, y_vals, color)

    if not use_numeric:
        ax.set_xticks(np.arange(len(x_vals)))
        ax.set_xticklabels(
            [str(v) for v in x_vals],
            rotation=15, ha="right",
            fontsize=theme.font_size_tick,
        )

    ax.set_xlabel(xlabel or x_col, fontsize=theme.font_size_label)
    ax.set_ylabel(ylabel, fontsize=theme.font_size_label)
    if title:
        ax.set_title(title, fontsize=theme.font_size_title, fontweight="bold", pad=10)

    if len(y_cols) > 1:
        ax.legend(fontsize=theme.font_size_legend, framealpha=0.8)

    _apply_theme(ax, theme)
    ax.grid(linestyle=":", alpha=0.4)
    fig.tight_layout()
    return fig
