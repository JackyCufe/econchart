"""
分布直方图模块。
支持单变量分布展示，可叠加 KDE 曲线。
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


def _add_kde(ax: plt.Axes, data: np.ndarray, color: str) -> None:
    """叠加 KDE 曲线（使用 scipy，不可用时跳过）。"""
    try:
        from scipy.stats import gaussian_kde
    except ImportError:
        logger.warning("scipy not installed; skipping KDE curve.")
        return

    kde = gaussian_kde(data)
    x_range = np.linspace(data.min(), data.max(), 300)
    # 缩放 KDE 到与直方图同量纲（密度模式）
    ax.plot(x_range, kde(x_range), color=color, linewidth=2.0, label="KDE")


def plot_histogram(
    data: pd.DataFrame,
    col: str,
    bins: int = 20,
    add_kde: bool = True,
    density: bool = False,
    color_idx: int = 0,
    theme: JournalTheme = THEMES["通用学术"],
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
) -> plt.Figure:
    """
    绘制分布直方图。

    Args:
        data:      输入 DataFrame
        col:       要绘制的数值列名
        bins:      分组数量
        add_kde:   是否叠加 KDE 曲线
        density:   True 时 Y 轴显示密度，False 时显示频数
        color_idx: 使用主题颜色列表的第 N 个颜色
        theme:     期刊主题
        title:     图标题
        xlabel:    X 轴标签
        ylabel:    Y 轴标签

    Returns:
        matplotlib Figure
    """
    if col not in data.columns:
        raise ValueError(f"数据中缺少列 '{col}'")

    values = data[col].dropna().values.astype(float)
    if len(values) == 0:
        raise ValueError(f"列 '{col}' 中没有有效数据")

    fig, ax = plt.subplots(figsize=(theme.fig_width, theme.fig_height))

    color = theme.colors[color_idx % len(theme.colors)] if theme.colors else "#2C3E50"
    use_density = density or add_kde

    ax.hist(
        values,
        bins=bins,
        density=use_density,
        color=color,
        alpha=0.75,
        edgecolor="white",
        linewidth=0.5,
        label=col,
    )

    if add_kde:
        _add_kde(ax, values, color)
        ax.legend(fontsize=theme.font_size_legend, framealpha=0.8)

    ax.set_xlabel(xlabel or col, fontsize=theme.font_size_label)
    ax.set_ylabel(
        ylabel or ("密度" if use_density else "频数"),
        fontsize=theme.font_size_label,
    )
    if title:
        ax.set_title(title, fontsize=theme.font_size_title, fontweight="bold", pad=10)

    # 添加描述统计注释
    mean_val = values.mean()
    std_val = values.std()
    ax.axvline(mean_val, color="red", linestyle="--", linewidth=1.2, alpha=0.7)
    ax.text(
        0.98, 0.95,
        f"均值={mean_val:.3f}\nStd={std_val:.3f}\nN={len(values)}",
        transform=ax.transAxes,
        fontsize=theme.font_size_legend - 1,
        ha="right", va="top",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.7),
    )

    _apply_theme(ax, theme)
    ax.grid(axis="y", linestyle=":", alpha=0.4)
    fig.tight_layout()
    return fig
