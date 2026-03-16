"""
热力图模块。
支持相关矩阵可视化及任意数值矩阵展示。
"""
from __future__ import annotations

import logging

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd

from core.theme import JournalTheme, THEMES

logger = logging.getLogger(__name__)


def _apply_theme(ax: plt.Axes, theme: JournalTheme) -> None:
    ax.spines["top"].set_visible(theme.spine_top)
    ax.spines["right"].set_visible(theme.spine_right)
    ax.tick_params(labelsize=theme.font_size_tick)


def _select_colormap(theme: JournalTheme) -> str:
    """根据主题主色选择合适的 colormap。"""
    primary = theme.colors[0].lower() if theme.colors else "#2c3e50"
    # 学术风格使用冷暖对比 colormap
    return "RdYlBu_r"


def plot_heatmap(
    data: pd.DataFrame,
    annotate: bool = True,
    fmt: str = ".2f",
    theme: JournalTheme = THEMES["通用学术"],
    title: str = "",
    vmin: float | None = None,
    vmax: float | None = None,
) -> plt.Figure:
    """
    绘制热力图（相关矩阵或任意数值矩阵）。

    Args:
        data:     输入 DataFrame（数值矩阵）
        annotate: 是否在格子内显示数值
        fmt:      数值格式字符串
        theme:    期刊主题
        title:    图标题
        vmin:     色阶最小值（默认自动）
        vmax:     色阶最大值（默认自动）

    Returns:
        matplotlib Figure
    """
    numeric_data = data.select_dtypes(include="number")
    if numeric_data.empty:
        raise ValueError("数据中没有数值列，无法绘制热力图")

    matrix = numeric_data.values.astype(float)
    row_labels = list(numeric_data.index.astype(str))
    col_labels = list(numeric_data.columns.astype(str))

    n_rows, n_cols = matrix.shape
    cell_size = 0.7
    fig_w = max(theme.fig_width, n_cols * cell_size + 1.5)
    fig_h = max(theme.fig_height, n_rows * cell_size + 1.5)
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))

    cmap = _select_colormap(theme)
    auto_vmin = vmin if vmin is not None else np.nanmin(matrix)
    auto_vmax = vmax if vmax is not None else np.nanmax(matrix)

    im = ax.imshow(
        matrix,
        cmap=cmap,
        aspect="auto",
        vmin=auto_vmin,
        vmax=auto_vmax,
    )

    ax.set_xticks(np.arange(n_cols))
    ax.set_yticks(np.arange(n_rows))
    ax.set_xticklabels(col_labels, fontsize=theme.font_size_tick, rotation=45, ha="right")
    ax.set_yticklabels(row_labels, fontsize=theme.font_size_tick)

    if annotate:
        threshold = (auto_vmin + auto_vmax) / 2
        for r in range(n_rows):
            for c in range(n_cols):
                val = matrix[r, c]
                text_color = "white" if val < threshold else "black"
                if np.isnan(val):
                    txt = "N/A"
                else:
                    txt = format(val, fmt)
                ax.text(
                    c, r, txt,
                    ha="center", va="center",
                    color=text_color,
                    fontsize=theme.font_size_tick - 1,
                )

    fig.colorbar(im, ax=ax, fraction=0.04, pad=0.03)

    if title:
        ax.set_title(title, fontsize=theme.font_size_title, fontweight="bold", pad=10)

    _apply_theme(ax, theme)
    fig.tight_layout()
    return fig
