"""
系数图（森林图风格）模块。
用于可视化回归系数及置信区间，符合中国经管期刊规范。
"""
from __future__ import annotations

import logging
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from core.theme import JournalTheme, THEMES

logger = logging.getLogger(__name__)

REQUIRED_COLS = {"variable", "coef"}
CI_MULTIPLIERS = {
    "se": 1.96,     # 95% 置信区间（±1.96 SE）
    "95ci": None,   # 直接使用 ci_lower / ci_upper
    "90ci": 1.645,  # 90% 置信区间
}


def _validate_data(data: pd.DataFrame, ci_type: str) -> pd.DataFrame:
    """校验数据格式，返回清洗后的副本。快速失败。"""
    missing = REQUIRED_COLS - set(data.columns)
    if missing:
        raise ValueError(f"数据缺少必要列：{missing}。必须包含：variable, coef")

    if ci_type == "95ci" or ci_type == "90ci":
        if "se" not in data.columns and (
            "ci_lower" not in data.columns or "ci_upper" not in data.columns
        ):
            raise ValueError(
                f"ci_type='{ci_type}' 需要 'se' 列 或 'ci_lower'+'ci_upper' 列"
            )

    df = data.copy()
    df["coef"] = pd.to_numeric(df["coef"], errors="raise")
    return df


def _compute_ci(df: pd.DataFrame, ci_type: str) -> tuple[np.ndarray, np.ndarray]:
    """计算置信区间下限和上限，返回 (xerr_low, xerr_high) 相对于 coef 的误差。"""
    if "ci_lower" in df.columns and "ci_upper" in df.columns and ci_type == "95ci":
        low = df["coef"].values - df["ci_lower"].values
        high = df["ci_upper"].values - df["coef"].values
        return low, high

    if "se" not in df.columns:
        raise ValueError("计算 CI 需要 'se' 列")

    se = df["se"].values
    multiplier = CI_MULTIPLIERS.get(ci_type, 1.96)
    half = multiplier * se
    return half, half


def _apply_theme(ax: plt.Axes, theme: JournalTheme) -> None:
    """将期刊主题样式应用到坐标轴。"""
    ax.spines["top"].set_visible(theme.spine_top)
    ax.spines["right"].set_visible(theme.spine_right)
    ax.tick_params(labelsize=theme.font_size_tick)


def plot_coefficients(
    data: pd.DataFrame,
    ci_type: str = "se",
    theme: JournalTheme = THEMES["通用学术"],
    title: str = "",
    xlabel: str = "系数估计值",
    zero_line: bool = True,
    sort_by: str = "none",
    exclude_vars: Optional[list[str]] = None,
) -> plt.Figure:
    """
    绘制回归系数图（森林图风格）。

    Args:
        data:         必须含列：variable, coef，以及 se 或 ci_lower/ci_upper
        ci_type:      "se"（±1.96SE）| "95ci"（直接CI列）| "90ci"（±1.645SE）
        theme:        期刊主题
        title:        图标题
        xlabel:       X 轴标签
        zero_line:    是否绘制 x=0 参考线
        sort_by:      "none" | "coef_asc" | "coef_desc"
        exclude_vars: 排除的变量名列表（如常数项 "_cons"）

    Returns:
        matplotlib Figure
    """
    df = _validate_data(data, ci_type)

    if exclude_vars:
        df = df[~df["variable"].isin(exclude_vars)]

    if sort_by == "coef_asc":
        df = df.sort_values("coef", ascending=True)
    elif sort_by == "coef_desc":
        df = df.sort_values("coef", ascending=False)

    df = df.reset_index(drop=True)
    y_pos = np.arange(len(df))

    fig, ax = plt.subplots(
        figsize=(theme.fig_width, max(theme.fig_height, len(df) * 0.45 + 1))
    )

    xerr_low, xerr_high = _compute_ci(df, ci_type)

    color = theme.colors[0] if theme.colors else "#2C3E50"
    ax.errorbar(
        x=df["coef"].values,
        y=y_pos,
        xerr=[xerr_low, xerr_high],
        fmt="o",
        color=color,
        ecolor=color,
        elinewidth=1.5,
        capsize=4,
        capthick=1.5,
        markersize=7,
        label="系数估计值",
    )

    if zero_line:
        ax.axvline(x=0, color="black", linewidth=1.0, linestyle="--", alpha=0.6)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(df["variable"].values, fontsize=theme.font_size_tick)
    ax.set_xlabel(xlabel, fontsize=theme.font_size_label)
    if title:
        ax.set_title(title, fontsize=theme.font_size_title, fontweight="bold", pad=10)

    ci_label = {"se": "95% CI (±1.96SE)", "95ci": "95% CI", "90ci": "90% CI"}.get(
        ci_type, "CI"
    )
    ax.set_title(
        ax.get_title(),
        fontsize=theme.font_size_title,
    )

    _apply_theme(ax, theme)
    ax.grid(axis="x", linestyle=":", alpha=0.4)

    fig.text(
        0.98, 0.98, ci_label,
        ha="right", va="top",
        fontsize=theme.font_size_legend - 1,
        color="gray",
        transform=ax.transAxes,
    )

    fig.tight_layout()
    return fig
