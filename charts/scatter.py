"""
散点图模块。
支持分组着色、气泡大小、回归线及置信区间带。
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


def _add_regression_line(
    ax: plt.Axes,
    x: np.ndarray,
    y: np.ndarray,
    color: str,
    add_confidence: bool,
) -> None:
    """添加线性回归线及可选置信区间带。"""
    try:
        from scipy import stats
    except ImportError:
        logger.warning("scipy not installed; skipping regression line.")
        return

    mask = np.isfinite(x) & np.isfinite(y)
    xf, yf = x[mask], y[mask]
    if len(xf) < 3:
        return

    slope, intercept, r_value, p_value, std_err = stats.linregress(xf, yf)
    x_line = np.linspace(xf.min(), xf.max(), 200)
    y_line = slope * x_line + intercept

    ax.plot(x_line, y_line, color=color, linewidth=1.5, zorder=3)

    if add_confidence:
        n = len(xf)
        x_mean = xf.mean()
        se = std_err * np.sqrt(
            1 / n + (x_line - x_mean) ** 2 / ((xf - x_mean) ** 2).sum()
        )
        t_crit = 1.96
        ax.fill_between(
            x_line,
            y_line - t_crit * se,
            y_line + t_crit * se,
            color=color,
            alpha=0.15,
            zorder=2,
        )

    r2_text = f"R²={r_value**2:.3f}"
    ax.text(
        0.05, 0.95, r2_text,
        transform=ax.transAxes,
        fontsize=8,
        va="top",
        color=color,
    )


def plot_scatter(
    data: pd.DataFrame,
    x_col: str,
    y_col: str,
    color_col: Optional[str] = None,
    size_col: Optional[str] = None,
    add_regression: bool = True,
    add_confidence: bool = True,
    theme: JournalTheme = THEMES["通用学术"],
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
) -> plt.Figure:
    """
    绘制散点图，支持分组着色、气泡大小、回归线及置信区间带。

    Args:
        data:           输入 DataFrame
        x_col:          X 轴列名
        y_col:          Y 轴列名
        color_col:      分组着色列名（可选）
        size_col:       气泡大小列名（可选）
        add_regression: 是否添加回归线
        add_confidence: 是否添加置信区间带
        theme:          期刊主题
        title:          图标题
        xlabel:         X 轴标签
        ylabel:         Y 轴标签

    Returns:
        matplotlib Figure
    """
    if x_col not in data.columns or y_col not in data.columns:
        raise ValueError(f"数据中缺少列 '{x_col}' 或 '{y_col}'")

    fig, ax = plt.subplots(figsize=(theme.fig_width, theme.fig_height))

    sizes = None
    if size_col and size_col in data.columns:
        raw = data[size_col].values.astype(float)
        sizes = 20 + 200 * (raw - raw.min()) / (raw.max() - raw.min() + 1e-9)

    if color_col and color_col in data.columns:
        groups = data[color_col].unique()
        for i, grp in enumerate(groups):
            mask = data[color_col] == grp
            sub = data[mask]
            c = theme.colors[i % len(theme.colors)]
            sz = sizes[mask] if sizes is not None else 50
            ax.scatter(sub[x_col], sub[y_col], c=c, s=sz, label=str(grp),
                       alpha=0.75, edgecolors="white", linewidths=0.5, zorder=4)
            if add_regression:
                _add_regression_line(
                    ax,
                    sub[x_col].values.astype(float),
                    sub[y_col].values.astype(float),
                    c, add_confidence,
                )
        ax.legend(fontsize=theme.font_size_legend, framealpha=0.8)
    else:
        c = theme.colors[0] if theme.colors else "#2C3E50"
        ax.scatter(data[x_col], data[y_col], c=c, s=sizes if sizes is not None else 50,
                   alpha=0.75, edgecolors="white", linewidths=0.5, zorder=4)
        if add_regression:
            _add_regression_line(
                ax,
                data[x_col].values.astype(float),
                data[y_col].values.astype(float),
                c, add_confidence,
            )

    ax.set_xlabel(xlabel or x_col, fontsize=theme.font_size_label)
    ax.set_ylabel(ylabel or y_col, fontsize=theme.font_size_label)
    if title:
        ax.set_title(title, fontsize=theme.font_size_title, fontweight="bold", pad=10)

    _apply_theme(ax, theme)
    ax.grid(linestyle=":", alpha=0.4)
    fig.tight_layout()
    return fig
